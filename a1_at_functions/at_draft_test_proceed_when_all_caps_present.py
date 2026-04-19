# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_proceed_when_all_caps_present.py:7
# Component id: at.source.a1_at_functions.test_proceed_when_all_caps_present
from __future__ import annotations

__version__ = "0.1.0"

def test_proceed_when_all_caps_present(self, tmp_path):
    from ass_ade.map_terrain import active_terrain_gate
    # Use capabilities we know exist in the base inventory
    result = active_terrain_gate(
        ["ass_ade_agent"],
        working_dir=str(tmp_path),
        write_stubs=False,
    )
    assert result.verdict == "PROCEED"
    assert "ass_ade_agent" in result.capabilities_present
