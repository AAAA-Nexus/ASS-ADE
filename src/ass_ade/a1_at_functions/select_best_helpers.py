"""Tier a1 — assimilated function 'select_best'

Assimilated from: scoring.py:416-448
"""

from __future__ import annotations


# --- assimilated symbol ---
def select_best(
    candidates: list[Atom],
    blueprint: BlueprintItem,
    *,
    weights: ScoringWeights | None = None,
    metadata: dict[str, AtomMetadata] | None = None,
    session=None,
    now: datetime | None = None,
    constants: ScoringConstants | None = None,
    spec_path: Path | None = None,
) -> tuple[Atom, AtomScore, list[AtomScore]]:
    """Return ``(winner_atom, winner_score, ranked_list)``."""
    ranked = score(
        candidates,
        blueprint,
        weights=weights,
        metadata=metadata,
        session=session,
        now=now,
        constants=constants,
        spec_path=spec_path,
    )
    if not ranked:
        raise NoCandidatesError("no scored candidates")
    winner_ref = ranked[0].atom_ref
    winner_atom = next(
        (a for a in candidates if AtomRef.from_atom(a) == winner_ref), None
    )
    if winner_atom is None:
        raise NoCandidatesError(
            "winner AtomRef not present in candidate list — ranking invariant violated"
        )
    return winner_atom, ranked[0], ranked

