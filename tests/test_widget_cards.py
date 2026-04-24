"""Tests for widget card schemas (a0_qk_constants.widget_cards)."""

from __future__ import annotations

from ass_ade.a0_qk_constants.widget_cards import (
    WIDGET_CARD_SCHEMAS,
    AnchorAddedCard,
    AssimilationTableCard,
    ScoutReportCard,
    SkillResultCard,
)


def test_schema_registry_has_all_expected_kinds() -> None:
    kinds = set(WIDGET_CARD_SCHEMAS.keys())
    assert {
        "scout_report",
        "assimilation_table",
        "skill_result",
        "anchor_added",
        "personality_snapshot",
    }.issubset(kinds)


def test_scout_report_card_is_typed_dict_accepting_partial() -> None:
    card: ScoutReportCard = {"repo": "/x", "counts": {"assimilate": 3}}
    assert card["repo"] == "/x"


def test_assimilation_table_card_shape() -> None:
    card: AssimilationTableCard = {
        "rows": [
            {"qualname": "pkg.fn", "action": "assimilate", "confidence": 0.9}
        ],
        "total_candidates": 1,
    }
    assert card["rows"][0]["action"] == "assimilate"


def test_skill_result_and_anchor_shapes() -> None:
    s: SkillResultCard = {"name": "scout", "output": "done"}
    a: AnchorAddedCard = {"key": "prod", "value": "always run tests"}
    assert s["name"] == "scout"
    assert a["key"] == "prod"
