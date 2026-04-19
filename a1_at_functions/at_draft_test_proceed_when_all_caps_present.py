# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testactiveterraingate.py:6
# Component id: at.source.ass_ade.test_proceed_when_all_caps_present
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
