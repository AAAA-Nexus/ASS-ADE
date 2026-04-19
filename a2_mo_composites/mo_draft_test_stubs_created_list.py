# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:295
# Component id: mo.source.ass_ade.test_stubs_created_list
__version__ = "0.1.0"

    def test_stubs_created_list(self, tmp_path):
        from ass_ade.map_terrain import active_terrain_gate
        result = active_terrain_gate(
            ["missing_engine_alpha"],
            working_dir=str(tmp_path),
            write_stubs=False,  # don't write to disk in tests
        )
        assert len(result.stubs_created) == 1
        assert result.stubs_created[0].capability_name == "missing_engine_alpha"
