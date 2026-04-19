# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpersistence.py:19
# Component id: at.source.ass_ade.test_persist_records_failure
__version__ = "0.1.0"

    def test_persist_records_failure(self, tmp_path: Path) -> None:
        pipe = Pipeline("failp", persist_dir=str(tmp_path))
        pipe.add("s1", fail_step)
        pipe.run()

        files = list(tmp_path.glob("failp_*.json"))
        data = json.loads(files[0].read_text())
        assert data["passed"] is False
        assert data["steps"][0]["error"] == "something broke"
