#!/usr/bin/env python3
"""CLI: governance-aligned evolution handoff (research pack + epiphany JSON + panel charter).

See ``ass_ade.local.uep_evolution_orchestrate`` for behavior.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve()
_ROOT = _SCRIPT.parents[1]
_SRC = _ROOT / "src"
if _SRC.is_dir():
    sys.path.insert(0, str(_SRC))


def main() -> int:
    from ass_ade.local.uep_evolution_orchestrate import EVOLUTION_HANDOFF_JSON, orchestrate

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--task", type=str, default="", help="Goal paragraph (unless --task-file)")
    p.add_argument("--task-file", type=Path, default=None, help="Read goal from this file")
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory under repo (default: .ass-ade/evolution-runs/<UTC stamp>)",
    )
    p.add_argument(
        "--repo",
        type=str,
        default="",
        help="owner/name for GitHub blob links (default: GITHUB_REPOSITORY env)",
    )
    p.add_argument(
        "--formal-codex-json",
        type=Path,
        default=None,
        metavar="PATH",
        help="Optional path to third-party formal specification JSON (overrides FORMAL_CODEX_JSON / search)",
    )
    args = p.parse_args()
    import os

    task = args.task.strip()
    if args.task_file is not None:
        task = args.task_file.read_text(encoding="utf-8").strip()
    if not task:
        p.error("provide --task or --task-file")

    repo = (args.repo or os.environ.get("GITHUB_REPOSITORY", "")).strip()
    if not repo:
        repo = "AAAA-Nexus/ASS-ADE"

    if args.out is None:
        from datetime import datetime, timezone

        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        out = _ROOT / ".ass-ade" / "evolution-runs" / stamp
    else:
        out = (_ROOT / args.out).resolve() if not args.out.is_absolute() else args.out

    formal = args.formal_codex_json.resolve() if args.formal_codex_json is not None else None
    res = orchestrate(root=_ROOT, task=task, out_dir=out, repo=repo, formal_codex_json=formal)
    print(f"Wrote: {res.research_json}", file=sys.stderr)
    print(f"Wrote: {res.epiphany_json}", file=sys.stderr)
    print(f"Wrote: {res.panel_md}", file=sys.stderr)
    print(f"Wrote: {res.audit_md}", file=sys.stderr)
    print(f"Wrote: {res.out_dir / EVOLUTION_HANDOFF_JSON}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
