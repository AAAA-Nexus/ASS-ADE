# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:219
# Component id: mo.source.ass_ade.test_ncb_contract_false_before_read
__version__ = "0.1.0"

    def test_ncb_contract_false_before_read(self, tmp_path):
        tca = self._make(tmp_path)
        assert tca.ncb_contract("/project/unread.py") is False
