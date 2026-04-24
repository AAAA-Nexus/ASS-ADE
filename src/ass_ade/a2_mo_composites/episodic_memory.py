"""Tier a2 — episodic memory for multi-session continuity."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_MEMORY_DIR = Path.home() / ".ass-ade" / "memory"
_EPISODES_PATH = _MEMORY_DIR / "episodes.jsonl"
_ANCHORS_PATH = _MEMORY_DIR / "anchors.json"
_MAX_EPISODES = 200
_TOP_K = 3


@dataclass
class EpisodicStore:
    """Persistent episodic memory — what Atomadic has done and what the user has explicitly anchored.

    Two storage types:
    - **Episodes**: auto-recorded session summaries (project, intents run, outcomes).
    - **Anchors**: explicit user-stated facts ("@remember prod: always requires PR review").

    Episodes are scored by keyword overlap to find relevant context for the working memory.
    """

    _episodes: list[dict] = field(default_factory=list, init=False, repr=False)
    _anchors: dict[str, str] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        self._load()

    @classmethod
    def load(cls) -> "EpisodicStore":
        return cls()

    def _load(self) -> None:
        if _EPISODES_PATH.exists():
            try:
                for line in _EPISODES_PATH.read_text(encoding="utf-8").splitlines():
                    try:
                        self._episodes.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
                self._episodes = self._episodes[-_MAX_EPISODES:]
            except OSError:
                pass

        if _ANCHORS_PATH.exists():
            try:
                self._anchors = json.loads(_ANCHORS_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass

    # ── Episode recording ──────────────────────────────────────────────────────

    def record_episode(self, project: str, turns: list[Any]) -> None:
        """Summarise and persist a batch of turns as one episode.

        ``turns`` should be ``Turn`` dataclass instances; only duck-typed
        attributes ``intent`` and ``output`` are accessed.
        """
        if not turns:
            return

        intents = [getattr(t, "intent", "?") for t in turns]
        outcomes = [
            "ok" if not str(getattr(t, "output", "")).lower().startswith("[error") else "error"
            for t in turns
        ]
        unique = list(dict.fromkeys(intents))
        note = f"Ran {', '.join(unique[:5])}"
        err_count = outcomes.count("error")
        if err_count:
            note += f" ({err_count} error{'s' if err_count > 1 else ''})"

        episode = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "project": project,
            "intents": intents[:20],
            "outcomes": outcomes[:20],
            "note": note,
            "tags": unique[:8],
        }

        try:
            existing: list[str] = []
            if _EPISODES_PATH.exists():
                existing = _EPISODES_PATH.read_text(encoding="utf-8").splitlines()
            existing.append(json.dumps(episode))
            existing = existing[-_MAX_EPISODES:]
            _EPISODES_PATH.write_text("\n".join(existing) + "\n", encoding="utf-8")
            self._episodes.append(episode)
            if len(self._episodes) > _MAX_EPISODES:
                self._episodes = self._episodes[-_MAX_EPISODES:]
        except OSError:
            pass

    # ── Anchors ────────────────────────────────────────────────────────────────

    def add_anchor(self, key: str, value: str) -> None:
        """Store an explicit user-stated fact."""
        self._anchors[key.strip()] = value.strip()
        self._save_anchors()

    def remove_anchor(self, key: str) -> bool:
        """Delete an anchor. Returns True if it existed."""
        if key in self._anchors:
            del self._anchors[key]
            self._save_anchors()
            return True
        return False

    def get_anchors(self) -> dict[str, str]:
        return dict(self._anchors)

    def _save_anchors(self) -> None:
        try:
            _ANCHORS_PATH.write_text(
                json.dumps(self._anchors, indent=2), encoding="utf-8"
            )
        except OSError:
            pass

    # ── Retrieval ──────────────────────────────────────────────────────────────

    def find_relevant(self, context: str, k: int = _TOP_K) -> list[dict]:
        """Return top-k episodes most relevant to ``context`` via keyword overlap."""
        if not self._episodes:
            return []

        query_tokens = set(re.sub(r"[^\w\s]", "", context.lower()).split())
        if not query_tokens:
            return self._episodes[-k:]

        scored: list[tuple[float, dict]] = []
        for ep in self._episodes:
            ep_text = " ".join([
                ep.get("project", ""),
                ep.get("note", ""),
                " ".join(ep.get("tags", [])),
            ]).lower()
            ep_tokens = set(re.sub(r"[^\w\s]", "", ep_text).split())
            overlap = len(query_tokens & ep_tokens)
            if overlap > 0:
                scored.append((overlap / len(query_tokens), ep))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in scored[:k]]

    def working_memory(self, context: str) -> str:
        """Build a compact working memory string to include in LLM system prompts."""
        parts: list[str] = []

        if self._anchors:
            parts.append("User knowledge anchors:")
            for k, v in list(self._anchors.items())[:10]:
                parts.append(f"  [{k}] {v}")

        relevant = self.find_relevant(context)
        if relevant:
            parts.append("Relevant past sessions:")
            for ep in relevant:
                date = ep.get("ts", "")[:10]
                proj = ep.get("project", "?")
                note = ep.get("note", "")
                parts.append(f"  [{date}] {proj}: {note}")

        return "\n".join(parts)

    # ── Introspection ──────────────────────────────────────────────────────────

    def summarize(self) -> str:
        lines = ["**Episodic Memory**\n"]

        if self._anchors:
            lines.append("**Knowledge anchors:**")
            for k, v in self._anchors.items():
                lines.append(f"  `{k}` → {v}")
            lines.append("")

        if self._episodes:
            lines.append(f"**{len(self._episodes)} session(s) recorded**")
            lines.append("*(most recent first)*\n")
            for ep in reversed(self._episodes[-8:]):
                date = ep.get("ts", "")[:10]
                proj = ep.get("project", "?")
                note = ep.get("note", "")
                lines.append(f"  [{date}] `{proj}`: {note}")
        else:
            lines.append("No episodes recorded yet.")
            lines.append("Atomadic records a session summary after meaningful work.")
        return "\n".join(lines)

    def clear(self) -> None:
        self._episodes.clear()
        self._anchors.clear()
        for p in (_EPISODES_PATH, _ANCHORS_PATH):
            if p.exists():
                try:
                    p.unlink()
                except OSError:
                    pass
