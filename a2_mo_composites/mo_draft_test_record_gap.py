# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:238
# Component id: mo.source.ass_ade.test_record_gap
__version__ = "0.1.0"

    def test_record_gap(self, tmp_path):
        tca = self._make(tmp_path)
        tca.record_gap("Missing API docs for endpoint X")
        gaps = tca.get_gaps()
        assert len(gaps) == 1
        assert "endpoint X" in gaps[0]["description"]
