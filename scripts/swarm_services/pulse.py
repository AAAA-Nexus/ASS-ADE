from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from .config import SwarmServiceConfig
from .plan_tasks import build_node_map, load_tasks_json, node_status, ready_nodes
from .state import DaemonState, TaskStateFile

ISO = "%Y-%m-%dT%H:%M:%SZ"


def _now() -> str:
    return datetime.now(timezone.utc).strftime(ISO)


def plan_dir(cfg: SwarmServiceConfig) -> Path:
    return cfg.repo_root / ".ato-plans" / cfg.plan_rel_dir


def tasks_path(cfg: SwarmServiceConfig) -> Path:
    return plan_dir(cfg) / "tasks.json"


def evolution_log_path(cfg: SwarmServiceConfig) -> Path:
    p = plan_dir(cfg) / "evolution.log"
    return p


def automation_dir(cfg: SwarmServiceConfig) -> Path:
    d = cfg.repo_root / ".ato-plans" / "assclaw-v1" / "swarm_services"
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_automation_pulse(
    cfg: SwarmServiceConfig,
    st: DaemonState,
    summary: str,
) -> Path:
    path = automation_dir(cfg) / "AUTOMATION-PULSE.md"
    line = f"- **{_now()}** — tick {st.tick_count} — {summary}\n"
    if path.is_file():
        text = path.read_text(encoding="utf-8")
    else:
        text = (
            "# Swarm services — automation pulse (append-only)\n\n"
            "Written by `scripts/run_swarm_services.py`. **Do not hand-edit** the "
            "log lines; use `swarm task mark` to update task state.\n\n## Events\n\n"
        )
    path.write_text(text + line, encoding="utf-8", newline="\n")
    return path


def append_evolution_tick(cfg: SwarmServiceConfig, line: str) -> None:
    p = evolution_log_path(cfg)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(f"{_now()}  [swarm-services]  {line}\n")


def run_regenerate_ass_ade_docs(cfg: SwarmServiceConfig) -> tuple[bool, str]:
    script = cfg.repo_root / "scripts" / "regenerate_ass_ade_docs.py"
    if not script.is_file():
        return False, "regenerate_ass_ade_docs.py missing"
    r = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(cfg.repo_root),
        capture_output=True,
        text=True,
        timeout=600,
    )
    msg = (r.stdout or r.stderr or "").strip()[:2000]
    return r.returncode == 0, msg or f"exit {r.returncode}"


def run_ade_harness_verify(cfg: SwarmServiceConfig) -> tuple[bool, str]:
    script = cfg.repo_root / "ADE" / "harness" / "verify_ade_harness.py"
    if not script.is_file():
        return False, "verify_ade_harness.py missing"
    r = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(cfg.repo_root),
        capture_output=True,
        text=True,
        timeout=300,
    )
    msg = (r.stdout or r.stderr or "").strip()[:2000]
    return r.returncode == 0, msg or f"exit {r.returncode}"


def broadcast_p3(
    cfg: SwarmServiceConfig, subject: str, body: str, issued_by: str = "swarm-services"
) -> tuple[bool, str]:
    sig = cfg.repo_root / ".cursor" / "hooks" / "swarm_signal.py"
    if not sig.is_file():
        return False, "swarm_signal.py not found"
    env = os.environ.copy()
    env["SWARM_AGENT"] = "orchestrator"
    r = subprocess.run(
        [
            sys.executable,
            str(sig),
            "broadcast",
            "--priority",
            "P3-fyi",
            "--subject",
            subject,
            "--body",
            body,
            "--routes",
            cfg.routes,
            "--issued-by",
            issued_by,
        ],
        cwd=str(cfg.repo_root),
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    out = (r.stdout or r.stderr or "").strip()
    return r.returncode == 0, out or f"exit {r.returncode}"


def one_tick(
    cfg: SwarmServiceConfig, st: DaemonState, daily_reset: bool = True
) -> tuple[DaemonState, str]:
    """Run one automation cycle. Returns (new_state, summary for pulse)."""
    tpath = tasks_path(cfg)
    pd = plan_dir(cfg)
    if not tpath.is_file():
        st.tick_count += 1
        st.last_tick_utc = _now()
        return st, f"no tasks.json at {tpath.relative_to(cfg.repo_root)}"

    tasks_doc = load_tasks_json(tpath)
    nodes = build_node_map(tasks_doc)
    tfile = TaskStateFile.load(pd)
    if not tfile.plan_slug and tasks_doc.get("planSlug"):
        tfile.plan_slug = str(tasks_doc["planSlug"])
    state_map = tfile.nodes

    ready = ready_nodes(nodes, state_map)
    pending = [n for n in nodes if node_status(n, nodes, state_map) != "done"]
    done_ct = len(nodes) - len(pending)
    all_nodes_done = bool(nodes) and not pending

    parts: list[str] = []
    if ready:
        parts.append(f"ready: {', '.join(ready)}")
    if done_ct:
        parts.append(f"done {done_ct}/{len(nodes)}")
    if not ready and pending:
        parts.append(f"blocked: {', '.join(sorted(pending)[:6])}{'…' if len(pending) > 6 else ''}")

    st.tick_count += 1
    st.last_tick_utc = _now()

    # doc regen
    if cfg.run_doc_regen:
        last = st.last_doc_regen_utc
        need = True
        if last:
            try:
                t0 = datetime.fromisoformat(last.replace("Z", "+00:00"))
                t1 = datetime.now(timezone.utc)
                if (t1 - t0).total_seconds() < cfg.doc_regen_interval_sec:
                    need = False
            except ValueError:
                pass
        if need:
            ok, msg = run_regenerate_ass_ade_docs(cfg)
            st.last_doc_regen_utc = _now()
            m1 = (msg or "").splitlines()[0].strip()[:100] if msg else ""
            parts.append(f"docs: {'ok' if ok else 'fail'}" + (f" ({m1})" if m1 else ""))

    if cfg.run_ade_harness_check:
        ok, msg = run_ade_harness_verify(cfg)
        parts.append(f"harness: {'ok' if ok else 'fail'}")

    # nudge: first ready node, if cooldown allows
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if daily_reset and st.nudge_counts_utc_date != today:
        st.nudge_counts_utc_date = today
        st.nudge_count_today = 0

    nudge_note = ""
    if (
        cfg.broadcast_on_ready
        and ready
        and st.nudge_count_today < cfg.max_signals_per_day
    ):
        nid = ready[0]
        last_n = st.nudged_nodes.get(nid, "")
        cool = float(cfg.nudge_cooldown_sec)
        if last_n:
            try:
                t0 = datetime.fromisoformat(last_n.replace("Z", "+00:00"))
                elapsed = (datetime.now(timezone.utc) - t0).total_seconds()
            except ValueError:
                elapsed = cool + 1.0
        else:
            elapsed = cool + 1.0

        if elapsed >= cool:
            title = (nodes.get(nid) or {}).get("title") or nid
            body = (
                f"Dependency gate clear for **{nid}** — {title}.\n\n"
                f"Assign a lane, set `SWARM_AGENT`, run the listed `@agent` in "
                f"`swarm-execution.md`. Mark done: "
                f"`python scripts/run_swarm_services.py task mark {nid} done`"
            )
            ok, br = broadcast_p3(
                cfg,
                subject=f"Ready to execute: {nid}",
                body=body,
            )
            if ok:
                st.nudge_count_today += 1
                st.nudged_nodes[nid] = _now()
                nudge_note = f"broadcast P3 for {nid}"
            else:
                nudge_note = f"nudge fail: {br[:120]}"

    if nudge_note:
        parts.append(nudge_note)

    if all_nodes_done:
        parts.append("**PLAN COMPLETE** — all task nodes marked done; review ship checklist + CI before tagging.")

    summary = "; ".join(parts) if parts else "idle"
    return st, summary
