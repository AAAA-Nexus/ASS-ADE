"""Tier a1 — assimilated function 'run_phase0_recon_multi'

Assimilated from: phase0_recon_multi.py:13-58
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from ass_ade.a1_at_functions.repo_stats import compute_repo_surface


# --- assimilated symbol ---
def run_phase0_recon_multi(
    source_roots: list[Path],
    *,
    task_description: str = "rebuild",
) -> dict[str, Any]:
    """Fail-closed: every root must be a directory with at least one ``.py`` file."""
    if not source_roots:
        return {
            "verdict": "RECON_REQUIRED",
            "task_description": task_description,
            "codebases": [],
            "required_actions": ["Provide at least one source directory."],
        }

    codebases: list[dict[str, Any]] = []
    required: list[str] = []

    for raw in source_roots:
        r = Path(raw).resolve()
        if not r.is_dir():
            codebases.append({"root": r.as_posix(), "error": "not_a_directory"})
            required.append(f"Not a directory: {r}")
            continue
        surface = compute_repo_surface(r)
        codebases.append({"root": r.as_posix(), "surface": surface})
        if surface["python_files"] <= 0:
            required.append(f"No Python files found under {r} (after exclusions).")

    verdict: ReconVerdict = (
        "READY_FOR_PHASE_1" if not required else "RECON_REQUIRED"
    )

    out: dict[str, Any] = {
        "verdict": verdict,
        "task_description": task_description,
        "codebases": codebases,
        "source_roots": [cb["root"] for cb in codebases],
        "research_targets": [],
        "provided_sources": [],
        "required_actions": required,
    }
    # Match single-root ``run_phase0_recon`` shape for callers that expect ``codebase``.
    if len(source_roots) == 1 and codebases:
        only = codebases[0]
        out["codebase"] = only.get("surface", only)
    return out

