# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testconfigproviderfields.py:52
# Component id: at.source.ass_ade.test_env_hydration_does_not_override_process_env
__version__ = "0.1.0"

    def test_env_hydration_does_not_override_process_env(self, tmp_path, monkeypatch):
        from ass_ade.config import load_config
        monkeypatch.setenv("GROQ_API_KEY", "from-process")
        (tmp_path / ".env").write_text("GROQ_API_KEY=from-file\n")
        (tmp_path / ".ass-ade").mkdir()
        load_config(tmp_path / ".ass-ade" / "config.json")
        # Process env wins
        assert os.getenv("GROQ_API_KEY") == "from-process"
