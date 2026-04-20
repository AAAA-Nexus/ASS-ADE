"""Layout tests for expansion/evolution/promotion documentation (ato-plan eeep lane)."""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def test_triple_lane_handbook_exists_and_grounded() -> None:
    path = _REPO / "docs" / "atomadic-triple-lane-handbook.md"
    text = path.read_text(encoding="utf-8")
    assert path.is_file()
    assert "MAP = TERRAIN" in text
    assert ".ass-ade/terrain-index.v0.json" in text
    assert "Epistemic" in text


def test_release_checklist_exists() -> None:
    path = _REPO / "docs" / "RELEASE_CHECKLIST.md"
    assert path.is_file()
    body = path.read_text(encoding="utf-8")
    assert "check_evolution_context.py" in body
    assert "atomadic_dev_harness.py" in body


def test_readme_links_handbook_and_release() -> None:
    text = (_REPO / "README.md").read_text(encoding="utf-8")
    assert "docs/atomadic-triple-lane-handbook.md" in text
    assert "docs/RELEASE_CHECKLIST.md" in text


def test_terrain_index_lists_handbook_keys() -> None:
    raw = (_REPO / ".ass-ade" / "terrain-index.v0.json").read_text(encoding="utf-8")
    assert "tripleLaneHandbook" in raw
    assert "releaseChecklist" in raw
