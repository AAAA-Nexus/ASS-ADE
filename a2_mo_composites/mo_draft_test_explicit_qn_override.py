# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwisdomengine.py:34
# Component id: mo.source.ass_ade.test_explicit_qn_override
__version__ = "0.1.0"

    def test_explicit_qN_override(self) -> None:
        w = WisdomEngine({})
        report = w.run_audit({"q1": True, "q2": False, "q3": True})
        # q1 and q3 explicitly True, q2 False
        assert report.passed >= 2
        found_q2_fail = any(f["id"] == 2 for f in report.failures)
        assert found_q2_fail
