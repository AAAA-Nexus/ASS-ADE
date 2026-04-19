# Extracted from C:/!ass-ade/tests/test_phase_engines.py:273
# Component id: mo.source.ass_ade.testactiveterraingate
from __future__ import annotations

__version__ = "0.1.0"

class TestActiveTerrainGate:
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

    def test_halt_when_cap_missing(self, tmp_path):
        from ass_ade.map_terrain import active_terrain_gate
        result = active_terrain_gate(
            ["nonexistent_capability_xyz_abc"],
            working_dir=str(tmp_path),
            write_stubs=False,
        )
        assert result.verdict == "HALT_AND_INVENT"
        assert "nonexistent_capability_xyz_abc" in result.capabilities_missing

    def test_stubs_created_list(self, tmp_path):
        from ass_ade.map_terrain import active_terrain_gate
        result = active_terrain_gate(
            ["missing_engine_alpha"],
            working_dir=str(tmp_path),
            write_stubs=False,  # don't write to disk in tests
        )
        assert len(result.stubs_created) == 1
        assert result.stubs_created[0].capability_name == "missing_engine_alpha"

    def test_partial_present_partial_missing(self, tmp_path):
        from ass_ade.map_terrain import active_terrain_gate
        result = active_terrain_gate(
            ["ass_ade_agent", "nonexistent_xyz_999"],
            working_dir=str(tmp_path),
            write_stubs=False,
        )
        assert result.verdict == "HALT_AND_INVENT"
        assert "ass_ade_agent" in result.capabilities_present
        assert "nonexistent_xyz_999" in result.capabilities_missing
