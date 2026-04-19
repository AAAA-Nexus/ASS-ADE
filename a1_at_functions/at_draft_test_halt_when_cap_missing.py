# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_halt_when_cap_missing.py:7
# Component id: at.source.a1_at_functions.test_halt_when_cap_missing
from __future__ import annotations

__version__ = "0.1.0"

def test_halt_when_cap_missing(self, tmp_path):
    from ass_ade.map_terrain import active_terrain_gate
    result = active_terrain_gate(
        ["nonexistent_capability_xyz_abc"],
        working_dir=str(tmp_path),
        write_stubs=False,
    )
    assert result.verdict == "HALT_AND_INVENT"
    assert "nonexistent_capability_xyz_abc" in result.capabilities_missing
