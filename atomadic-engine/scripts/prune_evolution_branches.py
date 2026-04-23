#!/usr/bin/env python3
"""Prune stale ``auto-evolve/*`` remote branches using the GitHub ``gh`` CLI.

Rules (conservative defaults for scheduled cleanup):

1. **Never** delete if an **open** PR exists with this branch as ``head``.
2. **Delete** if at least one **merged** PR exists with this head (leftover remote
   after merge when auto-delete is off).
3. **Delete** if there is **no open PR** and the branch tip is older than
   ``--stale-days`` (abandoned / push-failed / superseded).

Requires ``gh`` authenticated for the target repo (``GH_TOKEN`` / ``GITHUB_TOKEN``).

Examples::

    python scripts/prune_evolution_branches.py --dry-run
    python scripts/prune_evolution_branches.py --repo AAAA-Nexus/ASS-ADE --max-delete 40
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timezone
from shutil import which


def _repo_default() -> str:
    return os.environ.get("GITHUB_REPOSITORY", "").strip()


def _run_gh_json(argv: list[str]) -> object:
    proc = subprocess.run(
        ["gh", *argv],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"gh failed ({proc.returncode}): {' '.join(argv)}\n{proc.stderr.strip()}"
        )
    return json.loads(proc.stdout or "null")


def _run_gh(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *argv], capture_output=True, text=True, check=False)


def _iter_remote_branches(repo: str) -> list[str]:
    names: list[str] = []
    page = 1
    while True:
        chunk = _run_gh_json(
            [
                "api",
                f"repos/{repo}/branches",
                "-F",
                f"per_page=100",
                "-F",
                f"page={page}",
            ]
        )
        if not isinstance(chunk, list) or not chunk:
            break
        for row in chunk:
            if isinstance(row, dict) and row.get("name"):
                names.append(str(row["name"]))
        if len(chunk) < 100:
            break
        page += 1
    return names


def _branch_tip_iso(repo: str, branch: str) -> str | None:
    enc = urllib.parse.quote(branch, safe="")
    try:
        data = _run_gh_json(["api", f"repos/{repo}/commits/{enc}"])
    except RuntimeError:
        return None
    if not isinstance(data, dict):
        return None
    commit = data.get("commit")
    if not isinstance(commit, dict):
        return None
    committer = commit.get("committer")
    if isinstance(committer, dict) and committer.get("date"):
        return str(committer["date"])
    return None


def _parse_github_ts(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _pr_count(repo: str, branch: str, state: str) -> int:
    proc = _run_gh(
        [
            "pr",
            "list",
            "--repo",
            repo,
            "--head",
            branch,
            "--state",
            state,
            "--json",
            "number",
        ]
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gh pr list failed: {proc.stderr.strip()}")
    data = json.loads(proc.stdout or "[]")
    return len(data) if isinstance(data, list) else 0


def _delete_remote_branch(repo: str, branch: str) -> bool:
    enc = urllib.parse.quote(branch, safe="")
    proc = _run_gh(["api", "-X", "DELETE", f"repos/{repo}/git/refs/heads/{enc}"])
    if proc.returncode == 0:
        return True
    err = (proc.stderr or "").lower()
    if proc.returncode == 404 or "not found" in err:
        return True
    print(f"::warning::delete failed for {branch}: {proc.stderr.strip()}", file=sys.stderr)
    return False


@dataclass(frozen=True)
class BranchDecision:
    branch: str
    action: str  # keep | delete_merged | delete_stale
    detail: str


def decide(repo: str, branch: str, stale_days: int, now: datetime) -> BranchDecision:
    open_n = _pr_count(repo, branch, "open")
    if open_n > 0:
        return BranchDecision(branch, "keep", f"{open_n} open PR(s)")

    merged_n = _pr_count(repo, branch, "merged")
    if merged_n > 0:
        return BranchDecision(branch, "delete_merged", f"{merged_n} merged PR(s)")

    tip = _branch_tip_iso(repo, branch)
    if tip is None:
        return BranchDecision(branch, "keep", "could not resolve tip commit")

    age_days = (now - _parse_github_ts(tip)).total_seconds() / 86400.0
    if age_days > stale_days:
        return BranchDecision(
            branch,
            "delete_stale",
            f"no open PR; tip {age_days:.1f}d old (> {stale_days}d)",
        )
    return BranchDecision(branch, "keep", f"no open PR; tip only {age_days:.1f}d old")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        default=_repo_default(),
        help="owner/name (default: GITHUB_REPOSITORY in Actions)",
    )
    parser.add_argument(
        "--prefix",
        default="auto-evolve/",
        help="only consider remote branches whose name starts with this",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=21,
        help="delete unprotected heads with no open PR when tip is older than this",
    )
    parser.add_argument(
        "--max-delete",
        type=int,
        default=50,
        help="cap deletions per invocation (safety)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print planned deletions without calling DELETE",
    )
    args = parser.parse_args()
    if not args.repo:
        print("error: pass --repo or set GITHUB_REPOSITORY", file=sys.stderr)
        return 2

    if not which("gh"):
        print("error: gh CLI not found on PATH", file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc)
    candidates = [
        b for b in _iter_remote_branches(args.repo) if b.startswith(args.prefix)
    ]
    decisions: list[BranchDecision] = []
    for b in sorted(candidates):
        decisions.append(decide(args.repo, b, args.stale_days, now))

    to_delete = [d for d in decisions if d.action.startswith("delete")]
    deleted = 0
    for d in to_delete:
        print(f"{d.action}: {d.branch} — {d.detail}")
        if args.dry_run:
            continue
        if deleted >= args.max_delete:
            print(f"cap reached (--max-delete {args.max_delete}); stopping")
            break
        if _delete_remote_branch(args.repo, d.branch):
            deleted += 1

    kept = sum(1 for d in decisions if d.action == "keep")
    print(f"summary: candidates={len(candidates)} delete_planned={len(to_delete)} deleted={deleted} kept={kept}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
