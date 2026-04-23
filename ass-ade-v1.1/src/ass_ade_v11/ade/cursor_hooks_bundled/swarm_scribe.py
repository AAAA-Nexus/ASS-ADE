#!/usr/bin/env python3
"""Automated lane scribe — documentation + messenger + coordination index.

Invents the missing layer Cursor does not ship:

1. **Hook log** — every ``sessionStart`` / ``postToolUse`` / ``subagentStart``
   appends to ``SCRIBE-<SWARM_AGENT>.md``.
2. **Messenger** — when unread inbox count or signal set changes, append a
   ``**messenger**`` line (subjects + priorities) and a line to
   ``COORDINATION-PULSE.md``.
3. **Master index** — refresh ``MASTER-SCRIBE-INDEX.md`` from log mtimes
   (~60s throttle).

Disable all: ``SWARM_SCRIBE_SILENT=1``.

Stdlib only; never raises to the hook caller.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIBE_DIR = _REPO_ROOT / ".ato-plans" / "assclaw-v1" / "stream-reports" / "scribe"
_SCRIBES_PLAN = _REPO_ROOT / ".ato-plans" / "assclaw-v1" / "scribes"
_COORD_PULSE = _SCRIBE_DIR / "COORDINATION-PULSE.md"
_MASTER_INDEX = _SCRIBES_PLAN / "MASTER-SCRIBE-INDEX.md"
_THROTTLE = Path(__file__).resolve().parent / ".scribe_throttle.json"
_MESSENGER_STATE = Path(__file__).resolve().parent / ".scribe_messenger_state.json"
_INDEX_REFRESH = Path(__file__).resolve().parent / ".scribe_index_refresh"
_DEDUP_SEC = 4.0
_INDEX_MIN_SEC = 60.0


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _slug_agent(agent: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._-]+", "-", (agent or "anonymous").strip()) or "anonymous"
    return s[:64]


def _scribe_path(agent: str) -> Path:
    return _SCRIBE_DIR / f"SCRIBE-{_slug_agent(agent)}.md"


def _walk_tool_hint(obj: object, depth: int = 0) -> str:
    if depth > 8:
        return ""
    if isinstance(obj, dict):
        for k, v in obj.items():
            lk = str(k).lower()
            if lk in ("name", "tool", "toolname", "command", "tool_name", "toolname"):
                if isinstance(v, str) and 0 < len(v) < 240:
                    return v.strip()
            if lk in ("tool_calls", "tools", "arguments") and depth < 4:
                r = _walk_tool_hint(v, depth + 1)
                if r:
                    return r
            r = _walk_tool_hint(v, depth + 1)
            if r:
                return r
    elif isinstance(obj, list):
        for x in obj[:32]:
            r = _walk_tool_hint(x, depth + 1)
            if r:
                return r
    return ""


def _guess_hook_kind(data: dict) -> str:
    for k in (
        "hook",
        "hookName",
        "hook_event_name",
        "event",
        "type",
        "hookEvent",
    ):
        v = data.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()[:80]
    return "hook"


def _parse_payload(raw: str) -> tuple[str, str]:
    """Return (hook_kind, detail)."""
    if not raw or not raw.strip():
        return "empty", ""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return "raw", raw.strip().replace("\n", " ")[:160]

    if not isinstance(data, dict):
        return "json", type(data).__name__

    kind = _guess_hook_kind(data)
    detail = _walk_tool_hint(data)
    if not detail:
        # Cursor may nest under "input" / "payload"
        for nest in ("input", "payload", "body", "context"):
            if nest in data:
                detail = _walk_tool_hint(data[nest])
                if detail:
                    break
    if not detail and "tool" in data and isinstance(data["tool"], str):
        detail = data["tool"][:120]
    return kind, (detail or "")[:200]


def _throttle_allows(agent: str, line_key: str) -> bool:
    try:
        if _THROTTLE.exists():
            state = json.loads(_THROTTLE.read_text(encoding="utf-8"))
        else:
            state = {}
    except Exception:
        state = {}
    if not isinstance(state, dict):
        state = {}
    h = hashlib.sha256(line_key.encode("utf-8")).hexdigest()[:20]
    now = _dt.datetime.now(_dt.timezone.utc).timestamp()
    key = _slug_agent(agent)
    bucket = state.setdefault(key, {})
    prev = bucket.get(h)
    if isinstance(prev, (int, float)) and (now - float(prev)) < _DEDUP_SEC:
        return False
    bucket[h] = now
    # prune old entries (keep last 50 keys per agent)
    if len(bucket) > 50:
        for k in list(bucket.keys())[:-40]:
            del bucket[k]
    try:
        _THROTTLE.parent.mkdir(parents=True, exist_ok=True)
        _THROTTLE.write_text(json.dumps(state, indent=0), encoding="utf-8")
    except Exception:
        pass
    return True


def _skip_throttle(kind: str) -> bool:
    k = (kind or "").lower()
    return any(x in k for x in ("session", "subagent", "start", "empty"))


def append_hook_event(raw_stdin: str) -> None:
    if os.environ.get("SWARM_SCRIBE_SILENT") == "1":
        return
    agent = os.environ.get("SWARM_AGENT", "anonymous").strip() or "anonymous"
    kind, detail = _parse_payload(raw_stdin)
    line_key = f"{kind}|{detail}"
    if not _skip_throttle(kind) and not _throttle_allows(agent, line_key):
        return

    path = _scribe_path(agent)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        return

    ts = _now_iso()
    detail_esc = detail.replace("|", "/") if detail else "-"
    line = f"- {ts} | `{kind}` | {detail_esc}\n"

    try:
        if not path.exists() or path.stat().st_size == 0:
            header = (
                f"# Scribe log (automated) — {_slug_agent(agent)}\n\n"
                f"*Hook-driven lines from `.cursor/hooks/swarm_scribe.py` "
                f"(every sessionStart / postToolUse / subagentStart).*\n\n"
                f"---\n\n"
            )
            path.write_text(header + line, encoding="utf-8", newline="\n")
        else:
            with path.open("a", encoding="utf-8", newline="\n") as f:
                f.write(line)
    except Exception:
        pass


def _load_json(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default


def _save_json(path: Path, data: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=0, sort_keys=True), encoding="utf-8")
    except Exception:
        pass


def append_messenger_pulse(agent: str, unread: list[dict]) -> None:
    """Log unread signal snapshot + subjects; messenger role for coordination.

    Called from ``swarm_signal.check`` after building the unread list (before
    deliver marks). Appends only when unread count changes vs last hook.
    """
    if os.environ.get("SWARM_SCRIBE_SILENT") == "1":
        return
    agent = (agent or "anonymous").strip() or "anonymous"
    n = len(unread)
    state = _load_json(_MESSENGER_STATE, {})
    if not isinstance(state, dict):
        state = {}
    prev = state.get(agent, {})
    prev_n = int(prev.get("unread_count", -1)) if isinstance(prev, dict) else -1
    if n == prev_n and n == 0:
        return

    if isinstance(prev, dict):
        prev_ids = prev.get("ids", "")
    else:
        prev_ids = ""
    ids_now = ",".join(s.get("signal_id", "") for s in unread[:12])
    if n == prev_n and ids_now == prev_ids:
        return

    state[agent] = {"unread_count": n, "ids": ids_now}
    _save_json(_MESSENGER_STATE, state)

    ts = _now_iso()
    parts: list[str] = []
    for s in unread[:8]:
        pr = s.get("priority", "")
        sub = (s.get("subject") or "")[:72]
        parts.append(f"{pr}:{sub}" if sub else str(pr))
    summary = " | ".join(parts) if parts else "(none)"
    line = f"- {ts} | **messenger** | unread={n} | {summary}\n"

    path = _scribe_path(agent)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.stat().st_size == 0:
            header = (
                f"# Scribe log (automated) — {_slug_agent(agent)}\n\n"
                f"*Hook lines + messenger pulses from `.cursor/hooks/swarm_scribe.py`.*\n\n"
                f"---\n\n"
            )
            path.write_text(header + line, encoding="utf-8", newline="\n")
        else:
            with path.open("a", encoding="utf-8", newline="\n") as f:
                f.write(line)
    except Exception:
        pass

    try:
        _COORD_PULSE.parent.mkdir(parents=True, exist_ok=True)
        gline = f"- {ts} | `{_slug_agent(agent)}` | unread={n} | {summary}\n"
        if not _COORD_PULSE.exists():
            _COORD_PULSE.write_text(
                "# Coordination pulse (automated)\n\n"
                "*Cross-lane messenger feed: unread inbox snapshot per hook when state changes.*\n\n"
                "---\n\n",
                encoding="utf-8",
                newline="\n",
            )
        with _COORD_PULSE.open("a", encoding="utf-8", newline="\n") as f:
            f.write(gline)
    except Exception:
        pass


def append_manual_digest(agent: str, body: str) -> None:
    """Append a human-authored session block to the lane scribe (UTF-8).

    Hook-driven lines stay in the same file; manual digests are prefixed with
    a level-3 heading so they are easy to grep. Intended for agents to record
    work summaries when the user asks the scribe to “document everything.”
    """
    if os.environ.get("SWARM_SCRIBE_SILENT") == "1":
        return
    agent = (agent or "anonymous").strip() or "anonymous"
    text = (body or "").strip()
    if not text:
        return
    path = _scribe_path(agent)
    ts = _now_iso()
    block = (
        f"\n### Manual digest — {ts}\n\n"
        f"{text.rstrip()}\n\n"
        f"---\n"
    )
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.stat().st_size == 0:
            header = (
                f"# Scribe log (automated + manual) — {_slug_agent(agent)}\n\n"
                f"*Hook lines from `swarm_scribe.append_hook_event`; messenger pulses; "
                f"manual digests from `append_manual_digest`.*\n\n"
                f"---\n"
            )
            path.write_text(header + block + "\n", encoding="utf-8", newline="\n")
        else:
            with path.open("a", encoding="utf-8", newline="\n") as f:
                f.write(block + "\n")
    except Exception:
        return
    try:
        refresh_master_index()
    except Exception:
        pass


def refresh_master_index() -> None:
    """Rewrite MASTER-SCRIBE-INDEX.md table from log file mtimes (throttled)."""
    if os.environ.get("SWARM_SCRIBE_SILENT") == "1":
        return
    now = _dt.datetime.now(_dt.timezone.utc).timestamp()
    try:
        if _INDEX_REFRESH.exists():
            last = float(_INDEX_REFRESH.read_text(encoding="utf-8").strip() or "0")
            if (now - last) < _INDEX_MIN_SEC:
                return
    except Exception:
        pass
    try:
        rows = []
        for p in sorted(_SCRIBE_DIR.glob("SCRIBE-*.md")):
            if p.name == "COORDINATION-PULSE.md":
                continue
            lane = p.stem.replace("SCRIBE-", "", 1)
            try:
                mtime = p.stat().st_mtime
                ut = _dt.datetime.fromtimestamp(mtime, tz=_dt.timezone.utc)
                ts = ut.strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                ts = "?"
            rel = f"`../stream-reports/scribe/{p.name}`"
            rows.append(f"| {lane} | {rel} | {ts} |")
        table = "\n".join(
            [
                "# Master scribe index (auto)",
                "",
                "**Regenerated from log mtimes by `swarm_scribe.refresh_master_index` (~60s throttle).**",
                "",
                "| Lane | Log file | Last mtime (UTC) |",
                "|------|----------|------------------|",
            ]
            + rows
            + [
                "",
                "Manual narrative index (if needed): see `COORDINATION-CHECKLIST.md`.",
                "",
            ]
        )
        _SCRIBES_PLAN.mkdir(parents=True, exist_ok=True)
        _MASTER_INDEX.write_text(table, encoding="utf-8", newline="\n")
        _INDEX_REFRESH.write_text(str(now), encoding="utf-8")
    except Exception:
        pass


def main(argv: list[str]) -> int:
    """CLI: ``digest`` (stdin → manual log) or default hook echo test."""
    if argv and argv[0] == "digest":
        agent = os.environ.get("SWARM_AGENT", "anonymous").strip() or "anonymous"
        raw = sys.stdin.read()
        append_manual_digest(agent, raw)
        return 0
    raw = sys.stdin.read()
    append_hook_event(raw)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
