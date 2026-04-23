"""Unit tests for cross-root proposal deduplication (ordering edge cases)."""

from __future__ import annotations

from ass_ade_v11.a1_at_functions.gap_fill import (
    ProposedComponent,
    _dedup_key,
    _dedupe_proposals_cross_root,
)


def _prop(
    name: str,
    *,
    source_rank: int,
    path: str,
    cid: str,
) -> ProposedComponent:
    sym = {"name": name, "kind": "function", "path": path, "line": 1}
    dkey = _dedup_key("a1_at_functions", name, ["COR"])
    return ProposedComponent(
        id=cid,
        tier="a1_at_functions",
        kind="pure_function",
        name=name,
        source_symbol=sym,
        product_categories=["COR"],
        description="",
        dedup_key=dkey,
        source_rank=source_rank,
    )


def test_dedupe_lower_rank_wins_when_encountered_second() -> None:
    """Regression: merger must replace a higher-rank incumbent when a lower-rank prop arrives."""
    k = _dedup_key("a1_at_functions", "Dup", ["COR"])
    high_first = _prop("Dup", source_rank=1, path="b.py", cid="sec")
    low_second = _prop("Dup", source_rank=0, path="a.py", cid="pri")
    dedup, siblings = _dedupe_proposals_cross_root([high_first, low_second])
    assert dedup[k].id == "pri"
    assert len(siblings[k]) == 1


def test_dedupe_higher_rank_loses_drops_into_siblings() -> None:
    k = _dedup_key("a1_at_functions", "X", ["COR"])
    pri = _prop("X", source_rank=0, path="a.py", cid="p")
    sec = _prop("X", source_rank=1, path="b.py", cid="s")
    dedup, siblings = _dedupe_proposals_cross_root([pri, sec])
    assert dedup[k].id == "p"
    assert len(siblings[k]) == 1


def test_dedupe_same_rank_sort_key_tiebreak() -> None:
    k = _dedup_key("a1_at_functions", "Tie", ["COR"])
    first = _prop("Tie", source_rank=0, path="z.py", cid="zzz")
    second = _prop("Tie", source_rank=0, path="a.py", cid="aaa")
    dedup, siblings = _dedupe_proposals_cross_root([first, second])
    assert dedup[k].id == "aaa"
    assert len(siblings[k]) == 1
