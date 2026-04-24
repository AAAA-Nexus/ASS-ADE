#!/usr/bin/env python3
"""Persistent swarm automation — heartbeat, terrain regen, task-graph nudges.

  python scripts/run_swarm_services.py run        # loop until Ctrl+C
  python scripts/run_swarm_services.py once       # single tick
  python scripts/run_swarm_services.py status     # plan + task state
  python scripts/run_swarm_services.py task mark T3 done --note "…"

Env: ``SWARM_PLAN_DIR`` (default active/ass-ade-ship-…), ``SWARM_TICK_SEC``,
``SWARM_REGEN_DOCS`` (0/1), ``SWARM_BROADCAST_READY`` (0/1), ``SWARM_NUDGE_COOLDOWN_SEC``,
``ATOMADIC_WORKSPACE`` or ``--repo``."""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Package lives next to this script
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from swarm_services.config import SwarmServiceConfig  # noqa: E402
from swarm_services.loop import run_forever  # noqa: E402
from swarm_services.plan_tasks import (  # noqa: E402
    build_node_map,
    node_sort_key,
    depends_satisfied,
    load_tasks_json,
    node_status,
    ready_nodes,
)
from swarm_services.pulse import (  # noqa: E402
    evolution_log_path,
    one_tick,
    plan_dir,
    tasks_path,
    write_automation_pulse,
)
from swarm_services.repo import discover_repo_root  # noqa: E402
from swarm_services.state import DaemonState, TaskStateFile  # noqa: E402


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cmd_status(cfg: SwarmServiceConfig) -> int:
    tpath = tasks_path(cfg)
    pd = plan_dir(cfg)
    if not tpath.is_file():
        print(f"Missing {tpath}", file=sys.stderr)
        return 1
    doc = load_tasks_json(tpath)
    nodes = build_node_map(doc)
    tf = TaskStateFile.load(pd)
    state = tf.nodes
    print(f"plan: {pd}\n  tasks: {tpath.name}\n  slug: {doc.get('planSlug')}\n")
    ready = ready_nodes(nodes, state)
    for nid in sorted(nodes.keys(), key=node_sort_key):
        st = node_status(nid, nodes, state)
        dep_ok = depends_satisfied(nid, nodes, state)
        title = (nodes[nid].get("title") or "")[:72]
        if st == "done":
            tag = "DONE"
        elif st == "blocked":
            tag = "BLOCKED"
        elif st == "in_progress":
            tag = "ACTIVE"
        elif dep_ok:
            tag = "READY"
        else:
            tag = "WAITING"
        print(f"  {nid:4}  {tag:8}  {title}")
    print(f"\nReady to start (actionable pending): {', '.join(ready) or '(none)'}")
    blocked = [
        nid
        for nid in sorted(nodes.keys(), key=node_sort_key)
        if node_status(nid, nodes, state) == "blocked"
    ]
    if blocked:
        print(f"Blocked (human / gate): {', '.join(blocked)}")
    evo = evolution_log_path(cfg)
    if evo.is_file():
        print(f"\nEvolution log: {evo}")
    dstate = automation_dir_path(cfg) / "daemon_state.json"
    if dstate.is_file():
        print(f"Daemon state: {dstate}")
    return 0


def automation_dir_path(cfg: SwarmServiceConfig) -> Path:
    d = cfg.repo_root / ".ato-plans" / "assclaw-v1" / "swarm_services"
    d.mkdir(parents=True, exist_ok=True)
    return d


def cmd_once(cfg: SwarmServiceConfig) -> int:
    dpath = automation_dir_path(cfg) / "daemon_state.json"
    st = DaemonState.load(dpath)
    st, summary = one_tick(cfg, st)
    write_automation_pulse(cfg, st, summary)
    st.save(dpath)
    print(summary)
    return 0


def cmd_task_mark(cfg: SwarmServiceConfig, node_id: str, status: str, note: str) -> int:
    pd = plan_dir(cfg)
    tpath = tasks_path(cfg)
    if not tpath.is_file():
        print(f"Missing {tpath}", file=sys.stderr)
        return 1
    doc = load_tasks_json(tpath)
    nodes = build_node_map(doc)
    if node_id not in nodes:
        print(f"Unknown node {node_id!r}; valid: {', '.join(sorted(nodes))}", file=sys.stderr)
        return 1
    if status not in ("done", "pending", "blocked", "in_progress"):
        print("status must be one of: done, pending, blocked, in_progress", file=sys.stderr)
        return 1
    tf = TaskStateFile.load(pd)
    if doc.get("planSlug"):
        tf.plan_slug = str(doc["planSlug"])
    tf.nodes[node_id] = {
        "status": status,
        "updated": _now(),
        "note": note,
    }
    tf.save(pd)
    rel = TaskStateFile.path_for_plan(pd).relative_to(cfg.repo_root)
    print(f"OK -> {rel} set {node_id}={status}")
    line = f"task {node_id} -> {status}" + (f" ({note})" if note else "")
    el = evolution_log_path(cfg)
    el.parent.mkdir(parents=True, exist_ok=True)
    with el.open("a", encoding="utf-8", newline="\n") as f:
        f.write(f"{_now()}  [swarm-services]  {line}\n")
    print(f"Appended: {el.relative_to(cfg.repo_root)}")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="run_swarm_services")
    p.add_argument("--repo", type=Path, default=None, help="Repo root (default: discover)")

    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run", help="Run heartbeat loop until interrupted")
    sub.add_parser("once", help="Run a single tick")
    sub.add_parser("status", help="Show task graph + state")

    t = sub.add_parser("task", help="Update swarm_task_state.json")
    tsub = t.add_subparsers(dest="taskcmd", required=True)
    m = tsub.add_parser("mark", help="Mark a task node")
    m.add_argument("id", help="e.g. T3")
    m.add_argument("status", help="done | pending | blocked | in_progress")
    m.add_argument("--note", default="", help="Free-text note")

    args = p.parse_args(argv)
    try:
        root = discover_repo_root(args.repo)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1
    os.environ.setdefault("ATOMADIC_WORKSPACE", str(root))
    cfg = SwarmServiceConfig.from_env(root)

    if args.cmd == "run":
        return run_forever(cfg)
    if args.cmd == "once":
        return cmd_once(cfg)
    if args.cmd == "status":
        return cmd_status(cfg)
    if args.cmd == "task" and args.taskcmd == "mark":
        return cmd_task_mark(cfg, args.id, args.status, args.note)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
