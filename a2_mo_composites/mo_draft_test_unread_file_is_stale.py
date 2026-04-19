# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testtcaengine.py:18
# Component id: mo.source.ass_ade.test_unread_file_is_stale
__version__ = "0.1.0"

    def test_unread_file_is_stale(self, tmp_path):
        tca = self._make(tmp_path)
        report = tca.check_freshness("/never/read.py")
        assert report.fresh is False
        assert report.last_read_ts is None
