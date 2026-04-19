# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwriteprojectversionfile.py:17
# Component id: at.source.ass_ade.test_empty_tiers_returns_initial
__version__ = "0.1.0"

    def test_empty_tiers_returns_initial(self, tmp_path: Path):
        path = write_project_version_file(tmp_path, {}, "tag1")
        first_line = Path(path).read_text().splitlines()[0]
        assert first_line == INITIAL_VERSION
