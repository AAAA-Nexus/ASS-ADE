"""Phase 0 — recon gate before ingest."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from ass_ade.a1_at_functions.repo_stats import compute_repo_surface

ReconVerdict = Literal["READY_FOR_PHASE_1", "RECON_REQUIRED"]


def run_phase0_recon(source_root: Path, *, task_description: str = "rebuild") -> dict[str, Any]:
    """Return structured recon receipt; MAP = TERRAIN (filesystem reads only)."""
    source_root = source_root.resolve()
    if not source_root.is_dir():
        return {
            "verdict": "RECON_REQUIRED",
            "task_description": task_description,
            "codebase": {"root": str(source_root), "error": "not_a_directory"},
            "required_actions": ["Provide an existing source directory."],
        }

    surface = compute_repo_surface(source_root)
    ready = surface["python_files"] > 0
    verdict: ReconVerdict = "READY_FOR_PHASE_1" if ready else "RECON_REQUIRED"
    required: list[str] = []
    if not ready:
        required.append("Add at least one .py file under the source root (or adjust exclusions).")

    return {
        "verdict": verdict,
        "task_description": task_description,
        "codebase": surface,
        "research_targets": [],
        "provided_sources": [],
        "required_actions": required,
    }
