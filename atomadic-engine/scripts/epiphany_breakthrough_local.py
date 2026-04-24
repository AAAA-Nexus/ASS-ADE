#!/usr/bin/env python3
"""Local parity for MCP ``epiphany_breakthrough_cycle`` when Cursor cannot call stdio MCP.

Prints the same JSON document the tool places in ``content[0].text`` (schema
``ass-ade.epiphany-breakthrough-cycle.v1``). Exit code ``2`` means MCP-equivalent
``isError`` (recon ``RECON_REQUIRED`` and/or ``validation_errors``); ``0`` means success.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve()
_ASS_ADE_ROOT = _SCRIPT.parents[1]
_SRC = _ASS_ADE_ROOT / "src"
if _SRC.is_dir():
    sys.path.insert(0, str(_SRC))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "task_description",
        nargs="?",
        default="",
        help="Goal in one paragraph (or use --task-file)",
    )
    parser.add_argument(
        "--task-file",
        type=Path,
        help="File whose contents are task_description",
    )
    parser.add_argument(
        "--observation",
        "-o",
        action="append",
        default=[],
        metavar="TEXT",
        help="Grounding string; repeatable",
    )
    parser.add_argument(
        "--provided-source",
        "-s",
        action="append",
        default=[],
        metavar="URL_OR_PATH",
        help="Satisfies phase0 doc gate for technical tasks; repeatable",
    )
    parser.add_argument(
        "--no-phase0",
        action="store_true",
        help="Same as MCP run_phase0=false",
    )
    parser.add_argument(
        "--max-relevant-files",
        type=int,
        default=16,
        metavar="N",
    )
    parser.add_argument(
        "--working-dir",
        type=Path,
        default=None,
        help="ASS-ADE repo root for recon (default: parent of scripts/)",
    )
    args = parser.parse_args()

    if args.task_file is not None:
        task = args.task_file.read_text(encoding="utf-8").strip()
    else:
        task = str(args.task_description or "").strip()
    if not task:
        parser.error("task_description (positional) or --task-file is required")

    root = (args.working_dir or _ASS_ADE_ROOT).resolve()

    from ass_ade.engine.rebuild.epiphany_cycle import (
        build_epiphany_document,
        detect_track_and_steps,
        validate_epiphany_document,
    )
    from ass_ade.recon import phase0_recon

    recon_verdict: str | None = None
    recon_files: list[str] = []
    recon_failed = False
    if not args.no_phase0:
        pr = phase0_recon(
            task_description=task,
            working_dir=str(root),
            provided_sources=args.provided_source,
            max_relevant_files=args.max_relevant_files,
        )
        recon_verdict = pr.verdict
        recon_files = list(pr.codebase.relevant_files)
        recon_failed = pr.verdict == "RECON_REQUIRED"

    track, base = detect_track_and_steps(task)
    intro = f"Define success criteria for: {task}"
    plan_steps = [intro, *base]
    doc: dict[str, object] = build_epiphany_document(
        task,
        track=track,
        plan_steps=plan_steps,
        recon_verdict=recon_verdict,
        recon_files=recon_files,
        observations=list(args.observation),
    )
    val_errs = validate_epiphany_document(doc)
    if val_errs:
        doc["validation_errors"] = val_errs

    is_error = recon_failed or bool(val_errs)
    sys.stdout.write(json.dumps(doc, indent=2) + "\n")

    if is_error:
        sys.stderr.write(
            "epiphany_breakthrough_local: exit 2 == MCP isError "
            "(fix recon: add --provided-source for technical tasks, "
            "or use --no-phase0 if recon already satisfied this session).\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
