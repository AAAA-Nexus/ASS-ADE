# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:184
# Component id: at.source.ass_ade.test_persist_creates_file
__version__ = "0.1.0"

    def test_persist_creates_file(self, tmp_path: Path) -> None:
        pipe = Pipeline("persist", persist_dir=str(tmp_path))
        pipe.add("s1", pass_step)
        pipe.run()

        files = list(tmp_path.glob("persist_*.json"))
        assert len(files) == 1

        data = json.loads(files[0].read_text())
        assert data["name"] == "persist"
        assert data["passed"] is True
        assert len(data["steps"]) == 1
