"""Tier a1 — assimilated function 'score'

Assimilated from: scoring.py:309-413
"""

from __future__ import annotations


# --- assimilated symbol ---
def score(
    candidates: list[Atom],
    blueprint: BlueprintItem,
    *,
    weights: ScoringWeights | None = None,
    metadata: dict[str, AtomMetadata] | None = None,
    session=None,
    now: datetime | None = None,
    constants: ScoringConstants | None = None,
    spec_path: Path | None = None,
) -> list[AtomScore]:
    """Score each candidate and return a descending-ranked list.

    Parameters
    ----------
    candidates:
        Atoms the binder already retrieved from the registry.
    blueprint:
        The :class:`BlueprintItem` driving the scoring call. Its
        ``scoring_preference`` picks an alternative weights profile
        unless ``weights`` is explicitly passed.
    weights:
        Optional per-call override. When ``None``, the scorer loads
        defaults from ``scoring-weights.yaml`` (or uses the blueprint's
        named preference profile).
    metadata:
        Map from ``canonical_name`` to :class:`AtomMetadata`. The
        registry populates this for real calls; tests can pass an
        explicit dict. Missing entries fall back to neutral defaults
        per the Scorer (12) contract.
    session:
        Sovereign session. When provided, ``m_trust`` and ``m_fit``
        are bounded via the oracle. When ``None`` the scorer runs in
        offline mode (local clamps, events tagged "offline").
    now:
        Reference time for recency. Defaults to ``datetime.now(UTC)``.
    constants:
        Optional override for public scoring constants. When ``None``
        :func:`load_constants` reads the YAML.
    spec_path:
        Optional override for the scoring YAML location.
    """
    if not candidates:
        raise NoCandidatesError("score() called with empty candidate list")
    if constants is None:
        constants = load_constants(spec_path)
    if weights is None:
        weights = _resolve_weights(blueprint, spec_path)
    weights.validate()
    now = now or datetime.now(UTC)
    metadata = metadata or {}
    offline = session is None

    max_usage = max((max(0, a.usage_count) for a in candidates), default=0)
    results: list[AtomScore] = []
    for atom in candidates:
        atom_meta = metadata.get(atom.canonical_name)
        fit_score, fit_tags = _m_fit_with_tags(
            atom, blueprint, session, offline=offline
        )
        m = {
            "trust": _m_trust(atom, session, offline=offline),
            "tests": _m_tests(atom, blueprint),
            "fit": fit_score,
            "usage": _m_usage(atom, max_usage=max_usage),
            "perf": _m_perf(atom, atom_meta),
            "provenance": _m_prov(atom, atom_meta),
            "recency": _m_recency(
                atom,
                atom_meta,
                half_life_days=constants.PUBLIC_RECENCY_HALF_LIFE_DAYS,
                now=now,
            ),
        }
        contributions = {k: m[k] * getattr(weights, k) for k in m}
        total = sum(contributions.values())
        breakdown = {**contributions, "total": total}
        results.append(
            AtomScore(
                atom_ref=AtomRef.from_atom(atom),
                score=total,
                breakdown=breakdown,
                weights=weights,
                tiebreak_path=[],
                tags=fit_tags,
            )
        )
    ranked = _rank_with_tiebreaks(results, candidates, constants)
    floor = float(constants.MIN_CANDIDATE_SCORE_FLOOR)
    if floor > 0.0 and ranked and ranked[0].score < floor:
        _emit_score_event(
            blueprint,
            ranked,
            weights,
            offline=offline,
            verdict="failure",
            rejection_kind="below_min_score_floor",
            min_score_floor=floor,
            best_score=float(ranked[0].score),
        )
        raise NoCandidatesError(
            f"best score {ranked[0].score} below MIN_CANDIDATE_SCORE_FLOOR ({floor})"
        )
    _emit_score_event(blueprint, ranked, weights, offline=offline)
    return ranked

