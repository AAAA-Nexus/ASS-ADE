#!/usr/bin/env python3
"""Evolution context gate: REFINE verdict must carry documented refinement progress.

Used from ASS-ADE CI (roadmap JSON in-repo) or locally against ``atomadic-suite-vision.json``.

Exit codes
----------
0 — Skip (no config file), not ``REFINE``, checks passed, or git step skipped.
1 — ``REFINE`` with empty ``refinementProgress``, or MCP-related git changes not cited in evidence.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _read_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return raw if isinstance(raw, dict) else None


def _research_radar(doc: dict) -> dict | None:
    rd = doc.get("researchRadar")
    return rd if isinstance(rd, dict) else None


def _progress_evidence_blob(rd: dict) -> str:
    parts: list[str] = []
    for row in rd.get("refinementProgress") or []:
        if not isinstance(row, dict):
            continue
        ev = row.get("evidence")
        if isinstance(ev, str) and ev.strip():
            parts.append(ev.strip())
    return " ".join(parts).replace("\\", "/").lower()


def _git_changed_paths(repo: Path, git_range: str) -> list[str] | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), "diff", "--name-only", git_range],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return [ln.strip().replace("\\", "/") for ln in proc.stdout.splitlines() if ln.strip()]


def _mcp_evolution_paths(paths: list[str]) -> list[str]:
    out: list[str] = []
    for p in paths:
        pl = p.lower()
        if pl == "mcp/server.json" or pl.endswith("/mcp/server.json"):
            out.append(p)
            continue
        if "src/ass_ade/mcp/" in pl.replace("\\", "/"):
            out.append(p)
    return out


def _evidence_covers_change(evidence_blob: str, changed: str) -> bool:
    norm = changed.replace("\\", "/").lower()
    if norm in evidence_blob:
        return True
    if "mcp/server.json" in norm and "mcp/server.json" in evidence_blob:
        return True
    if "src/ass_ade/mcp/" in norm or "/ass_ade/mcp/" in norm:
        return any(
            needle in evidence_blob
            for needle in ("ass_ade/mcp", "ass_ade.mcp", "test_mcp", "mcp/server.json")
        )
    return False


def check(
    *,
    doc: dict,
    git_range: str | None,
    repo: Path,
) -> tuple[bool, list[str]]:
    """Return (ok, messages)."""
    msgs: list[str] = []
    rd = _research_radar(doc)
    if not rd:
        return True, msgs
    if str(rd.get("verdict") or "").upper() != "REFINE":
        return True, msgs

    progress = rd.get("refinementProgress")
    if not isinstance(progress, list) or len(progress) == 0:
        msgs.append(
            "researchRadar.verdict is REFINE but refinementProgress is empty — "
            "append a dated progress row with evidence (paths, tests, or DEFER)."
        )
        return False, msgs

    blob = _progress_evidence_blob(rd)
    if not blob.strip():
        msgs.append(
            "researchRadar.verdict is REFINE but no refinementProgress[].evidence strings — "
            "fill evidence with pytest paths, script names, or doc paths."
        )
        return False, msgs

    if git_range:
        changed = _git_changed_paths(repo, git_range)
        if changed is None:
            msgs.append("git diff unavailable; skipping MCP path vs evidence check.")
            return True, msgs
        watched = _mcp_evolution_paths(changed)
        for p in watched:
            if not _evidence_covers_change(blob, p):
                msgs.append(
                    f"MCP evolution file touched ({p!r}) but path not found in "
                    "researchRadar.refinementProgress[].evidence — document the change."
                )
                return False, msgs

    return True, msgs


def _resolve_default_paths(cwd: Path) -> tuple[Path | None, Path | None]:
    vision = Path.home() / ".cursor" / "atomadic" / "atomadic-suite-vision.json"
    roadmap = cwd / ".ass-ade" / "ass-ade-suite-roadmap.json"
    v_ok = vision.is_file()
    r_ok = roadmap.is_file()
    return (vision if v_ok else None, roadmap if r_ok else None)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vision",
        type=Path,
        help="atomadic-suite-vision.json (default if present: ~/.cursor/atomadic/...)",
    )
    parser.add_argument(
        "--roadmap",
        type=Path,
        help="ass-ade-suite-roadmap.json (default if present: ./.ass-ade/... under cwd)",
    )
    parser.add_argument(
        "--git-range",
        metavar="REV_RANGE",
        help="e.g. origin/main...HEAD — require MCP touches cited in refinement evidence",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=None,
        help="Git repo root for --git-range (default: cwd)",
    )
    args = parser.parse_args()
    if args.vision is not None and args.roadmap is not None:
        parser.error("pass at most one of --vision and --roadmap")

    cwd = Path.cwd()
    dv, dr = _resolve_default_paths(cwd)
    if args.vision is not None:
        path: Path | None = args.vision
    elif args.roadmap is not None:
        path = args.roadmap
    else:
        path = dv or dr

    if path is None:
        print("check_evolution_context: no vision/roadmap file found; skip.", file=sys.stderr)
        return 0

    doc = _read_json(path)
    if doc is None:
        print(f"check_evolution_context: could not read JSON from {path}", file=sys.stderr)
        return 0

    repo = (args.repo or cwd).resolve()
    ok, msgs = check(doc=doc, git_range=args.git_range, repo=repo)
    for m in msgs:
        print(m, file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
