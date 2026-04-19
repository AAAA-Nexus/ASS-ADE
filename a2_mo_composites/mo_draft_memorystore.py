# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_memorystore.py:7
# Component id: mo.source.a2_mo_composites.memorystore
from __future__ import annotations

__version__ = "0.1.0"

class MemoryStore:
    """Local-only memory for the Atomadic interpreter.

    Two layers:
    - Community intelligence: learned from code quality via the LoRA flywheel (remote).
    - Personal context: learned from this user's interactions (local, never sent remotely).
    """

    user_profile: dict[str, Any] = field(default_factory=dict)
    project_contexts: dict[str, Any] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=dict)
    _history_path: Path = field(init=False, repr=False)

    def __post_init__(self) -> None:
        _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        self._history_path = _MEMORY_DIR / "conversation_history.jsonl"

    # ── Persistence ────────────────────────────────────────────────────────────

    @classmethod
    def load(cls) -> "MemoryStore":
        _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        store = cls()
        for attr, filename in [
            ("user_profile", "user_profile.json"),
            ("project_contexts", "project_contexts.json"),
            ("preferences", "preferences.json"),
        ]:
            p = _MEMORY_DIR / filename
            if p.exists():
                try:
                    setattr(store, attr, json.loads(p.read_text(encoding="utf-8")))
                except (json.JSONDecodeError, OSError):
                    pass
        return store

    def save(self) -> None:
        _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        for attr, filename in [
            ("user_profile", "user_profile.json"),
            ("project_contexts", "project_contexts.json"),
            ("preferences", "preferences.json"),
        ]:
            p = _MEMORY_DIR / filename
            try:
                p.write_text(
                    json.dumps(getattr(self, attr), indent=2, default=str),
                    encoding="utf-8",
                )
            except OSError:
                pass

    @classmethod
    def clear(cls) -> None:
        for filename in [
            "user_profile.json", "project_contexts.json",
            "preferences.json", "conversation_history.jsonl",
        ]:
            p = _MEMORY_DIR / filename
            if p.exists():
                try:
                    p.unlink()
                except OSError:
                    pass

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_profile": self.user_profile,
            "project_contexts": self.project_contexts,
            "preferences": self.preferences,
        }

    # ── History ────────────────────────────────────────────────────────────────

    def append_history(self, turn: "Turn") -> None:
        try:
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "user": turn.user,
                "intent": turn.intent,
                "tone": turn.tone,
                "path": turn.path,
                "ok": "[error" not in (turn.output or "").lower(),
            }
            lines: list[str] = []
            if self._history_path.exists():
                lines = self._history_path.read_text(encoding="utf-8").splitlines()
            lines.append(json.dumps(entry))
            lines = lines[-_HISTORY_MAX:]
            self._history_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        except OSError:
            pass

    def recent_history(self, n: int = 5) -> list[dict]:
        if not self._history_path.exists():
            return []
        lines = self._history_path.read_text(encoding="utf-8").splitlines()
        results = []
        for line in reversed(lines[-n * 2:]):
            try:
                results.append(json.loads(line))
                if len(results) >= n:
                    break
            except json.JSONDecodeError:
                continue
        return list(reversed(results))

    # ── Profile learning ───────────────────────────────────────────────────────

    def update_from_turn(self, turn: "Turn") -> None:
        profile = self.user_profile
        # Tone frequency tracking
        tones = profile.setdefault("tone_counts", {})
        tones[turn.tone] = tones.get(turn.tone, 0) + 1
        # Dominant tone
        profile["dominant_tone"] = max(tones, key=lambda k: tones[k])
        # Command frequency
        cmds = profile.setdefault("command_counts", {})
        cmds[turn.intent] = cmds.get(turn.intent, 0) + 1
        profile["favorite_command"] = max(cmds, key=lambda k: cmds[k])
        # Session count
        profile["session_interactions"] = profile.get("session_interactions", 0) + 1

        # Project context
        path_key = str(Path(turn.path).resolve())
        ctx = self.project_contexts.setdefault(path_key, {})
        ctx.setdefault("first_seen", datetime.now(timezone.utc).isoformat())
        ctx["last_seen"] = datetime.now(timezone.utc).isoformat()
        intent_log = ctx.setdefault("commands_run", [])
        intent_log.append({"intent": turn.intent, "ts": datetime.now(timezone.utc).isoformat()})
        ctx["commands_run"] = intent_log[-50:]  # keep last 50 per project

    # ── Greeting ───────────────────────────────────────────────────────────────

    def greeting(self, working_dir: Path) -> str | None:
        if not self.user_profile:
            return None
        parts: list[str] = []
        tone = self.user_profile.get("dominant_tone", "formal")
        path_key = str(working_dir.resolve())
        ctx = self.project_contexts.get(path_key, {})
        recent = self.recent_history(3)

        if tone == TONE_CASUAL:
            parts.append("Hey, welcome back!")
        else:
            parts.append("Welcome back.")

        if ctx:
            last_cmds = [e.get("intent") for e in ctx.get("commands_run", [])[-3:]]
            if last_cmds:
                last = last_cmds[-1]
                if tone == TONE_CASUAL:
                    parts.append(f"Last time here we ran `{last}` on this project.")
                else:
                    parts.append(f"Last operation on this project: `{last}`.")

        fav = self.user_profile.get("favorite_command")
        if fav and fav != "chat":
            if tone == TONE_CASUAL:
                parts.append(f"Quick tip: `{fav}` is your most-used command.")
            else:
                parts.append(f"Most-used command: `{fav}`.")

        return " ".join(parts) if parts else None

    # ── Summary ────────────────────────────────────────────────────────────────

    def summarize(self) -> str:
        if not self.user_profile and not self.project_contexts:
            return "No memory yet. Start chatting to build it up."
        lines = ["**Atomadic memory**\n"]
        if self.user_profile:
            lines.append("**You:**")
            tone = self.user_profile.get("dominant_tone", "unknown")
            lines.append(f"  - Tone: {tone}")
            fav = self.user_profile.get("favorite_command")
            if fav:
                lines.append(f"  - Favorite command: `{fav}`")
            count = self.user_profile.get("session_interactions", 0)
            lines.append(f"  - Total interactions: {count}")
        if self.project_contexts:
            lines.append("\n**Projects:**")
            for path, ctx in list(self.project_contexts.items())[-5:]:
                name = Path(path).name
                last = ctx.get("last_seen", "")[:10]
                n_cmds = len(ctx.get("commands_run", []))
                lines.append(f"  - `{name}` — last seen {last}, {n_cmds} commands run")
        return "\n".join(lines)
