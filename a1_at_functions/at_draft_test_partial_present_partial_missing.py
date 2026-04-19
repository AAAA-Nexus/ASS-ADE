# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testactiveterraingate.py:37
# Component id: at.source.ass_ade.test_partial_present_partial_missing
__version__ = "0.1.0"

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
