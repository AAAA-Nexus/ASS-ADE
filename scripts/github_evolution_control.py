#!/usr/bin/env python3
"""GitHub evolution control gate — mirror *local control* ideas for scheduled auto-evolve.

Reads ``.ass-ade/github-evolution-control.json`` and decides whether a lane should run,
primarily by counting open PRs whose ``head`` ref matches the configured branch prefix
and comparing to per-lane and global caps.

Writes GitHub Actions outputs when ``GITHUB_OUTPUT`` is set:

- ``proceed`` — ``true`` or ``false``
- ``reason`` — short machine-readable explanation

Exit code is always 0 when the gate evaluation completes (so skipped runs are green).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


SCHEMA = "ass-ade.github-evolution-control.v1"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_config(root: Path) -> dict:
    path = root / ".ass-ade" / "github-evolution-control.json"
    if not path.is_file():
        return {
            "schemaVersion": SCHEMA,
            "global": {"evolutionBranchPrefix": "auto-evolve/", "maxOpenEvolutionPrs": 99},
            "lanes": {},
        }
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        _write_outputs(False, "config_invalid")
        return {}
    if not isinstance(raw, dict):
        _write_outputs(False, "config_not_object")
        return {}
    return raw


def _write_outputs(proceed: bool, reason: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a", encoding="utf-8") as fh:
        fh.write(f"proceed={'true' if proceed else 'false'}\n")
        safe = reason.replace("\n", " ")[:500]
        fh.write(f"reason={safe}\n")


def _gh_pr_heads(repo: str) -> list[str] | None:
    token = (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or "").strip()
    if not token:
        return None
    cmd = [
        "gh",
        "pr",
        "list",
        "--repo",
        repo,
        "--state",
        "open",
        "--limit",
        "200",
        "--json",
        "headRefName",
    ]
    env = {**os.environ, "GH_TOKEN": token}
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=120, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"gh invocation failed: {exc}", file=sys.stderr)
        return None
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout or "gh failed", file=sys.stderr)
        return None
    try:
        rows = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        return None
    if not isinstance(rows, list):
        return None
    out: list[str] = []
    for row in rows:
        if isinstance(row, dict):
            h = row.get("headRefName")
            if isinstance(h, str) and h.strip():
                out.append(h.strip())
    return out


def _count_prefix(heads: list[str], prefix: str) -> int:
    p = prefix.replace("\\", "/")
    return sum(1 for h in heads if h.replace("\\", "/").startswith(p))


def cmd_gate(lane: str, root: Path) -> int:
    cfg = _load_config(root)
    if not cfg:
        return 0
    if cfg.get("schemaVersion") != SCHEMA:
        # Soft-accept unknown schema with same shape; still evaluate.
        pass

    lanes = cfg.get("lanes") if isinstance(cfg.get("lanes"), dict) else {}
    lane_cfg = lanes.get(lane) if isinstance(lanes.get(lane), dict) else {}
    enabled = bool(lane_cfg.get("enabled", True))
    if not enabled:
        _write_outputs(False, "lane_disabled")
        print("Lane disabled in github-evolution-control.json", file=sys.stderr)
        return 0

    global_cfg = cfg.get("global") if isinstance(cfg.get("global"), dict) else {}
    default_prefix = str(global_cfg.get("evolutionBranchPrefix", "auto-evolve/")).strip() or "auto-evolve/"
    branch_prefix = str(lane_cfg.get("branchPrefix") or default_prefix).strip() or default_prefix
    max_global = int(global_cfg.get("maxOpenEvolutionPrs", 99) or 99)
    max_lane_raw = lane_cfg.get("maxOpenPrsForLane")
    max_lane = int(max_lane_raw) if max_lane_raw is not None else max_global

    repo = (os.environ.get("GITHUB_REPOSITORY") or "").strip()
    if not repo:
        _write_outputs(True, "no_github_repository_env_skip_gh")
        return 0

    heads = _gh_pr_heads(repo)
    if heads is None:
        _write_outputs(False, "gh_pr_list_failed")
        return 0

    total_evo = _count_prefix(heads, default_prefix)
    lane_count = _count_prefix(heads, branch_prefix)

    if total_evo >= max_global:
        _write_outputs(False, f"global_cap open={total_evo} max={max_global}")
        return 0
    if lane_count >= max_lane:
        _write_outputs(False, f"lane_cap lane={lane} open={lane_count} max={max_lane}")
        return 0

    _write_outputs(True, f"ok open_evo={total_evo} open_lane={lane_count}")
    return 0


def main() -> int:
    root = _repo_root()
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gate", help="Evaluate whether an evolution lane should run")
    g.add_argument("--lane", required=True, help="Lane id (e.g. cycle, quality, security)")

    args = p.parse_args()
    if args.cmd == "gate":
        return cmd_gate(args.lane, root)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
