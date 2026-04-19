# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_compute_codebase_digest_ignores_pyc.py:5
# Component id: at.source.ass_ade.test_compute_codebase_digest_ignores_pyc
__version__ = "0.1.0"

def test_compute_codebase_digest_ignores_pyc(tmp_path: Path) -> None:
    (tmp_path / "module.pyc").write_bytes(b"\x00\x01\x02")

    result = compute_codebase_digest(tmp_path)

    assert result["file_count"] == 0
    assert "module.pyc" not in result.get("files", {})
