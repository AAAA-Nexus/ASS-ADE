# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_certifier.py:32
# Component id: at.source.ass_ade.test_hash_file_different_content
__version__ = "0.1.0"

def test_hash_file_different_content(tmp_path: Path) -> None:
    f1 = tmp_path / "a.py"
    f2 = tmp_path / "b.py"
    f1.write_bytes(b"x = 1")
    f2.write_bytes(b"x = 2")

    assert hash_file(f1) != hash_file(f2)
