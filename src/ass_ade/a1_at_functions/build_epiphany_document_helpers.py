"""Tier a1 — assimilated function 'build_epiphany_document'

Assimilated from: rebuild/epiphany_cycle.py:138-167
"""

from __future__ import annotations


# --- assimilated symbol ---
def build_epiphany_document(
    goal: str,
    *,
    track: str,
    plan_steps: list[str],
    recon_verdict: str | None,
    recon_files: list[str],
    observations: list[str],
) -> dict[str, object]:
    """Assemble the machine-readable cycle document (no filesystem access)."""
    epiphanies = observations_to_epiphanies(observations)
    hypotheses = hypotheses_from_epiphanies(epiphanies)
    experiments = experiments_from_track(track, plan_steps)
    files = [str(p) for p in recon_files[:24]]

    return {
        "schema_version": SCHEMA_VERSION,
        "goal": goal.strip(),
        "track": track,
        "epiphany_phase_steps": list(EPIPHANY_PHASE_STEPS),
        "epiphanies": epiphanies,
        "hypotheses": hypotheses,
        "experiments": experiments,
        "promotion_checks": promotion_checks(),
        "plan_steps": list(plan_steps),
        "recon": {
            "verdict": recon_verdict,
            "relevant_files": files,
        },
    }

