# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testactiveterraingate.py:17
# Component id: at.source.ass_ade.test_halt_when_cap_missing
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
