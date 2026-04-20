"""Documentation presence for ass-ade-atomadic-final-form plan (T6/T8)."""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def test_nexus_trust_surfaces_doc() -> None:
    p = _REPO / "docs" / "NEXUS_AND_TRUST_SURFACES.md"
    t = p.read_text(encoding="utf-8")
    assert "trust_gate" in t
    assert "DEFER" in t
    assert "src/ass_ade/nexus/client.py" in t


def test_forge_narrow_slice_doc() -> None:
    p = _REPO / "docs" / "FORGE_NARROW_SLICE.md"
    t = p.read_text(encoding="utf-8")
    assert "tier-map.json" in t
    assert "growthNotes" in t


def test_final_form_audit_log_exists() -> None:
    p = _REPO / ".ass-ade" / "final-form-audit.log"
    assert p.is_file()
    assert "final-form-narrow-slice" in p.read_text(encoding="utf-8")


def test_terrain_index_lists_final_form_pointers() -> None:
    raw = (_REPO / ".ass-ade" / "terrain-index.v0.json").read_text(encoding="utf-8")
    assert "nexusTrustSurfacesDoc" in raw
    assert "forgeNarrowSliceDoc" in raw
    assert "finalFormAuditLog" in raw
