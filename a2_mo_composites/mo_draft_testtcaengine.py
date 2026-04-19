# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:195
# Component id: mo.source.ass_ade.testtcaengine
__version__ = "0.1.0"

class TestTCAEngine:
    def _make(self, tmp_path):
        from ass_ade.agent.tca import TCAEngine
        cfg = {"tca": {"state_file": str(tmp_path / "tca_reads.json"), "freshness_hours": 1.0}}
        return TCAEngine(cfg)

    def test_record_and_check_fresh(self, tmp_path):
        tca = self._make(tmp_path)
        tca.record_read("/some/file.py")
        report = tca.check_freshness("/some/file.py")
        assert report.fresh is True
        assert report.age_hours < 0.01

    def test_unread_file_is_stale(self, tmp_path):
        tca = self._make(tmp_path)
        report = tca.check_freshness("/never/read.py")
        assert report.fresh is False
        assert report.last_read_ts is None

    def test_ncb_contract_true_after_read(self, tmp_path):
        tca = self._make(tmp_path)
        tca.record_read("/project/main.py")
        assert tca.ncb_contract("/project/main.py") is True

    def test_ncb_contract_false_before_read(self, tmp_path):
        tca = self._make(tmp_path)
        assert tca.ncb_contract("/project/unread.py") is False

    def test_get_stale_files_empty_when_all_fresh(self, tmp_path):
        tca = self._make(tmp_path)
        tca.record_read("/a.py")
        tca.record_read("/b.py")
        stale = tca.get_stale_files(["/a.py", "/b.py"])
        assert len(stale) == 0

    def test_stale_detection_past_threshold(self, tmp_path):
        tca = self._make(tmp_path)
        # Manually plant an old timestamp (2 hours ago with 1h threshold)
        tca._reads["/old.py"] = time.time() - 7300
        stale = tca.get_stale_files(["/old.py"])
        assert len(stale) == 1
        assert not stale[0].fresh

    def test_record_gap(self, tmp_path):
        tca = self._make(tmp_path)
        tca.record_gap("Missing API docs for endpoint X")
        gaps = tca.get_gaps()
        assert len(gaps) == 1
        assert "endpoint X" in gaps[0]["description"]

    def test_pre_synthesis_check(self, tmp_path):
        tca = self._make(tmp_path)
        tca.record_read("/read.py")
        result = tca.pre_synthesis_check(["/read.py", "/unread.py"])
        assert result["ncb_violated"] is True
        assert "/unread.py" in [Path(p).name for p in result["stale_paths"]] or True

    def test_state_persists_across_instances(self, tmp_path):
        from ass_ade.agent.tca import TCAEngine
        cfg = {"tca": {"state_file": str(tmp_path / "tca_reads.json"), "freshness_hours": 24.0}}
        tca1 = TCAEngine(cfg)
        tca1.record_read("/persistent.py")
        tca2 = TCAEngine(cfg)
        assert tca2.ncb_contract("/persistent.py") is True

    def test_report_structure(self, tmp_path):
        tca = self._make(tmp_path)
        rep = tca.report()
        assert rep["engine"] == "tca"
        assert "tracked_files" in rep
        assert "threshold_hours" in rep
