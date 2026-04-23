#!/usr/bin/env python3
"""Cursor hook + CLI for the ASS-ADE swarm signal bus.

This script is stdlib-only. It is the *bootstrap* companion to the shipped
`ass_ade.swarm` package: both sides agree on the same on-disk layout under
``<plan>/signals/``, so the hook works even before ``ass-ade`` is installed.

Subcommands
-----------
check                   Hook entry point. Reads the Cursor hook JSON on stdin
                        and prints a JSON response carrying any unread signals
                        for the current agent as ``additional_context``. Marks
                        delivered signals in ``signals/read/<agent>/``.

list                    Print every signal in the inbox, human-readable,
                        regardless of agent.

inbox                   Print only the signals that are unread for
                        ``$env:SWARM_AGENT``.

broadcast               Publish a new signal. Requires ``--priority``,
                        ``--subject``, and one of ``--body`` / ``--body-file``.

ack                     Write an acknowledgement for a specific signal so the
                        orchestrator knows an agent received and acted on it.

Environment
-----------
``SWARM_AGENT``         Identifier of the current Cursor tab / agent. Set this
                        once per tab (e.g. ``$env:SWARM_AGENT = "stream-A"``).
                        Default: ``"anonymous"``.
``SWARM_SIGNAL_ROOT``   Override signal root. Default:
                        ``.ato-plans/assclaw-v1/signals`` relative to repo root.
``SWARM_HOOK_SILENT``   If ``"1"``, ``check`` emits ``{}`` even when it finds
                        signals (emergency mute for debugging).
``SWARM_SCRIBE_SILENT`` If ``"1"``, hook does not append to lane scribe logs
                        (see ``swarm_scribe.py``).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable

# --- constants ----------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_ROOT = _REPO_ROOT / ".ato-plans" / "assclaw-v1" / "signals"

PRIORITIES = ("P0-halt", "P1-reroute", "P2-inform", "P3-fyi")
_FRONT_MATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
_ID_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z-(P[0-3]-[a-z0-9-]+)-[a-z0-9-]+$")


def _configure_stdio_utf8() -> None:
    """Use UTF-8 for stdout/stderr so inbox bodies (Unicode arrows, etc.)
    do not crash Windows consoles (cp1252) with UnicodeEncodeError.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError, io.UnsupportedOperation):
            pass


# --- helpers ------------------------------------------------------------------


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _now_rfc3339() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _slugify(text: str, limit: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (s[:limit] or "signal").rstrip("-")


def _signal_root() -> Path:
    override = os.environ.get("SWARM_SIGNAL_ROOT")
    root = Path(override) if override else _DEFAULT_ROOT
    (root / "inbox").mkdir(parents=True, exist_ok=True)
    (root / "read").mkdir(parents=True, exist_ok=True)
    (root / "acks").mkdir(parents=True, exist_ok=True)
    return root


def _agent_id() -> str:
    return os.environ.get("SWARM_AGENT", "anonymous").strip() or "anonymous"


def _atomic_write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(data)
        os.replace(tmp, path)
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        raise


def _append_log(root: Path, event: dict) -> None:
    log = root / "broadcast.log.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")


def _parse_front_matter(text: str) -> tuple[dict, str]:
    """Minimal YAML-ish front-matter parser (no deps).

    Supports ``key: value`` scalars and ``key:\\n  - item`` one-level lists.
    Good enough for the signal schema; we never ingest untrusted YAML here.
    """
    m = _FRONT_MATTER_RE.match(text)
    if not m:
        return {}, text
    head, body = m.group(1), text[m.end():]
    meta: dict = {}
    current_list_key: str | None = None
    for raw in head.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if current_list_key and line.lstrip().startswith("- "):
            meta.setdefault(current_list_key, []).append(line.lstrip()[2:].strip().strip('"\''))
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val == "":
            current_list_key = key
            meta[key] = []
        else:
            meta[key] = val.strip('"\'')
    return meta, body


def _render_front_matter(meta: dict) -> str:
    lines = ["---"]
    for key, val in meta.items():
        if isinstance(val, list):
            lines.append(f"{key}:")
            for item in val:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def _iter_inbox(root: Path) -> Iterable[Path]:
    inbox = root / "inbox"
    if not inbox.exists():
        return []
    return sorted(inbox.glob("*.md"))


def _routes_match(routes: list[str], agent: str) -> bool:
    if not routes or "*" in routes or "all" in routes:
        return True
    return agent in routes


def _read_signal(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta, body = _parse_front_matter(text)
    meta.setdefault("signal_id", path.stem)
    meta.setdefault("priority", "P2-inform")
    meta.setdefault("routes", [])
    if isinstance(meta["routes"], str):
        meta["routes"] = [r.strip() for r in meta["routes"].split(",") if r.strip()]
    meta["_body"] = body.strip()
    meta["_path"] = str(path)
    return meta


def _delivery_marker(root: Path, agent: str, signal_id: str) -> Path:
    return root / "read" / _slugify(agent, 64) / f"{signal_id}.delivered"


def _mark_delivered(root: Path, agent: str, signal_id: str) -> None:
    marker = _delivery_marker(root, agent, signal_id)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(_now_rfc3339() + "\n", encoding="utf-8")


def _is_delivered(root: Path, agent: str, signal_id: str) -> bool:
    return _delivery_marker(root, agent, signal_id).exists()


def _ade_harness_append() -> str:
    """Run ``ADE/harness/ade_hook_gate.py context``; return markdown to append.

    Disabled when ``ADE_HARNESS=0`` or the script is absent. Fail-open on errors.
    """
    script = _REPO_ROOT / "ADE" / "harness" / "ade_hook_gate.py"
    if not script.is_file():
        return ""
    if os.environ.get("ADE_HARNESS", "1").strip() == "0":
        return ""
    try:
        r = subprocess.run(
            [sys.executable, str(script), "context"],
            cwd=str(_REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=45,
        )
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "").strip()[:1200]
            return "\n\n### [ADE HARNESS — runner error]\n" + (err or "(no stderr)")
        out = (r.stdout or "").strip()
        return ("\n\n" + out) if out else ""
    except Exception as exc:  # pragma: no cover - defensive
        return f"\n\n### [ADE HARNESS — exception]\n{type(exc).__name__}: {exc}\n"


# --- commands -----------------------------------------------------------------


def cmd_check(_args) -> int:
    """Hook entry point. Reads Cursor hook JSON from stdin, replies on stdout.

    We never block, never return non-zero. Worst case we emit ``{}`` and the
    agent proceeds without a reroute — the next ``postToolUse`` fires within a
    few seconds and we get a second chance.

    Also forwards stdin to ``swarm_scribe.append_hook_event`` and runs
    ``append_messenger_pulse`` / ``refresh_master_index`` so each lane gets
    hook log + inbox messenger + coordination index updates.
    """
    raw = ""
    try:
        raw = sys.stdin.read()
    except Exception:
        pass

    try:
        from swarm_scribe import append_hook_event

        append_hook_event(raw)
    except Exception:
        pass

    if os.environ.get("SWARM_HOOK_SILENT") == "1":
        print("{}")
        return 0

    root = _signal_root()
    agent = _agent_id()

    unread: list[dict] = []
    for path in _iter_inbox(root):
        try:
            sig = _read_signal(path)
        except Exception as e:
            # A malformed file shouldn't break the hook; skip and log.
            _append_log(root, {"ts": _now_rfc3339(), "event": "parse_error",
                               "path": str(path), "error": str(e)})
            continue
        if not _routes_match(list(sig.get("routes", [])), agent):
            continue
        if _is_delivered(root, agent, sig["signal_id"]):
            continue
        unread.append(sig)

    try:
        from swarm_scribe import append_messenger_pulse, refresh_master_index

        append_messenger_pulse(agent, unread)
        refresh_master_index()
    except Exception:
        pass

    if not unread:
        ade = _ade_harness_append()
        if ade.strip():
            print(json.dumps({"additional_context": ade.strip()}))
        else:
            print("{}")
        return 0

    unread.sort(key=lambda s: (PRIORITIES.index(s["priority"])
                               if s["priority"] in PRIORITIES else 99,
                               s["signal_id"]))

    lines = [
        f"[SWARM SIGNAL BUS] {len(unread)} unread signal"
        f"{'s' if len(unread) != 1 else ''} for agent '{agent}'",
        "",
    ]
    for sig in unread:
        lines.append(f"---  {sig['signal_id']}  ({sig['priority']})  ---")
        for k in ("issued_by", "issued_at", "subject", "routes",
                  "ack_required", "expires_at"):
            if k in sig and sig[k] not in (None, "", []):
                lines.append(f"  {k}: {sig[k]}")
        if sig["_body"]:
            lines.append("")
            lines.append(sig["_body"])
        lines.append("")
        if str(sig.get("ack_required", "")).lower() in ("true", "yes", "1"):
            lines.append(
                f"  >> ACK REQUIRED: run  python .cursor/hooks/swarm_signal.py "
                f"ack --signal {sig['signal_id']} --note '<your note>'"
            )
            lines.append("")
        _mark_delivered(root, agent, sig["signal_id"])
        _append_log(root, {"ts": _now_rfc3339(), "event": "delivered",
                           "agent": agent, "signal_id": sig["signal_id"],
                           "priority": sig["priority"]})

    lines.append(
        "Orchestrator broadcasts live in "
        ".ato-plans/assclaw-v1/signals/inbox/ — "
        "respond per RULES.md (MAP = TERRAIN). "
        "If a P0-halt signal appears, stop current work and ack."
    )

    ade = _ade_harness_append()
    payload = {"additional_context": "\n".join(lines) + ade}
    print(json.dumps(payload))
    return 0


def cmd_list(_args) -> int:
    root = _signal_root()
    signals = [_read_signal(p) for p in _iter_inbox(root)]
    if not signals:
        print("(inbox empty)")
        return 0
    for sig in signals:
        print(f"{sig['signal_id']:50s}  {sig['priority']:11s}  "
              f"routes={','.join(sig.get('routes') or ['*']):20s}  "
              f"subject={sig.get('subject', '')}")
    return 0


def cmd_inbox(_args) -> int:
    root = _signal_root()
    agent = _agent_id()
    found = 0
    for path in _iter_inbox(root):
        sig = _read_signal(path)
        if not _routes_match(list(sig.get("routes", [])), agent):
            continue
        if _is_delivered(root, agent, sig["signal_id"]):
            continue
        found += 1
        print(f"--- {sig['signal_id']} ({sig['priority']}) ---")
        print(f"issued_by: {sig.get('issued_by', '?')}")
        print(f"subject:   {sig.get('subject', '?')}")
        print()
        print(sig["_body"])
        print()
    if not found:
        print(f"(no unread signals for agent '{agent}')")
    return 0


def cmd_broadcast(args) -> int:
    if args.priority not in PRIORITIES:
        print(f"error: --priority must be one of {PRIORITIES}", file=sys.stderr)
        return 2

    body: str
    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")
    elif args.body is not None:
        body = args.body
    elif not sys.stdin.isatty():
        body = sys.stdin.read()
    else:
        print("error: provide --body, --body-file, or pipe body on stdin",
              file=sys.stderr)
        return 2

    subject = args.subject.strip()
    issued_by = args.issued_by or _agent_id() or "orchestrator"
    routes = [r.strip() for r in (args.routes or "*").split(",") if r.strip()]
    ack_required = "true" if args.ack_required else "false"
    expires_at = args.expires_at or ""

    slug = _slugify(subject)
    signal_id = f"{_now_iso()}-{args.priority}-{slug}"
    digest = hashlib.sha256(
        (signal_id + subject + body + issued_by).encode("utf-8")
    ).hexdigest()[:12]

    meta = {
        "signal_id": signal_id,
        "priority": args.priority,
        "issued_by": issued_by,
        "issued_at": _now_rfc3339(),
        "subject": subject,
        "routes": routes,
        "ack_required": ack_required,
        "expires_at": expires_at,
        "digest": digest,
    }

    content = _render_front_matter(meta) + "\n" + body.strip() + "\n"
    root = _signal_root()
    target = root / "inbox" / f"{signal_id}.md"
    _atomic_write(target, content)
    _append_log(root, {"ts": _now_rfc3339(), "event": "broadcast",
                       "signal_id": signal_id, "priority": args.priority,
                       "issued_by": issued_by, "routes": routes,
                       "digest": digest})

    print(f"broadcast OK -> {target.relative_to(_REPO_ROOT)}")
    return 0


def cmd_ack(args) -> int:
    root = _signal_root()
    agent = _agent_id()
    acks_dir = root / "acks" / _slugify(agent, 64)
    acks_dir.mkdir(parents=True, exist_ok=True)
    ack_path = acks_dir / f"{args.signal}.ack.md"
    body = (args.note or "").strip()
    meta = {
        "signal_id": args.signal,
        "ack_by": agent,
        "ack_at": _now_rfc3339(),
    }
    _atomic_write(ack_path, _render_front_matter(meta) + "\n" + body + "\n")
    _append_log(root, {"ts": _now_rfc3339(), "event": "ack",
                       "agent": agent, "signal_id": args.signal,
                       "note": body})
    print(f"ack OK -> {ack_path.relative_to(_REPO_ROOT)}")
    return 0


# --- entrypoint ---------------------------------------------------------------


def main(argv: list[str]) -> int:
    _configure_stdio_utf8()
    parser = argparse.ArgumentParser(prog="swarm_signal")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("check", help="hook entry point (stdin JSON -> stdout JSON)")
    sub.add_parser("list", help="show all signals in the inbox")
    sub.add_parser("inbox", help="show unread signals for $SWARM_AGENT")

    b = sub.add_parser("broadcast", help="publish a new signal")
    b.add_argument("--priority", required=True,
                   help=f"one of: {', '.join(PRIORITIES)}")
    b.add_argument("--subject", required=True)
    b.add_argument("--body")
    b.add_argument("--body-file")
    b.add_argument("--routes", default="*",
                   help="comma-separated agent ids or '*' for all")
    b.add_argument("--issued-by")
    b.add_argument("--ack-required", action="store_true")
    b.add_argument("--expires-at", default="")

    a = sub.add_parser("ack", help="acknowledge a received signal")
    a.add_argument("--signal", required=True)
    a.add_argument("--note", default="")

    args = parser.parse_args(argv)
    cmd = args.cmd or "check"
    dispatch = {
        "check": cmd_check, "list": cmd_list, "inbox": cmd_inbox,
        "broadcast": cmd_broadcast, "ack": cmd_ack,
    }
    try:
        return dispatch[cmd](args)
    except Exception as e:
        sys.stderr.write(f"swarm_signal: {type(e).__name__}: {e}\n")
        if cmd == "check":
            print("{}")
            return 0
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
