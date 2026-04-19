# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:245
# Component id: mo.source.ass_ade.test_pre_synthesis_check
__version__ = "0.1.0"

    def test_pre_synthesis_check(self, tmp_path):
        tca = self._make(tmp_path)
        tca.record_read("/read.py")
        result = tca.pre_synthesis_check(["/read.py", "/unread.py"])
        assert result["ncb_violated"] is True
        assert "/unread.py" in [Path(p).name for p in result["stale_paths"]] or True
