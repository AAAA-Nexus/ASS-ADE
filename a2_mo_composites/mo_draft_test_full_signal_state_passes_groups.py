# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwisdomengine.py:13
# Component id: mo.source.ass_ade.test_full_signal_state_passes_groups
__version__ = "0.1.0"

    def test_full_signal_state_passes_groups(self) -> None:
        w = WisdomEngine({})
        cycle_state = {
            "recon_done": True,
            "complexity_scored": True,
            "tier": "hybrid",
            "memory_consulted": True,
            "lifr_queried": True,
            "trace_captured": True,
            "hallucination_checked": True,
            "certified": True,
            "map_terrain_done": True,
            "atlas_used": True,
            "tdmi_computed": True,
            "budget_ok": True,
            "tool_calls": ["read_file"],
        }
        report = w.run_audit(cycle_state)
        assert report.passed > 0
        assert report.score > 0.0
