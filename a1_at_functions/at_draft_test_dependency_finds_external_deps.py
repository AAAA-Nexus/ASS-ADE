# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:181
# Component id: at.source.ass_ade.test_dependency_finds_external_deps
__version__ = "0.1.0"

def test_dependency_finds_external_deps(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _dependency_agent(tmp_path, files)

    assert result["python_files"] > 0
    assert isinstance(result["unique_external_deps"], int)
    assert isinstance(result["circular_deps"], list)
    assert isinstance(result["max_import_depth"], int)
