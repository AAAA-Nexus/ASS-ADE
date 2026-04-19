# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_compute_codebase_digest_deterministic.py:5
# Component id: at.source.ass_ade.test_compute_codebase_digest_deterministic
__version__ = "0.1.0"

def test_compute_codebase_digest_deterministic(tmp_path: Path) -> None:
    (tmp_path / "stable.py").write_text("stable = True\n", encoding="utf-8")

    r1 = compute_codebase_digest(tmp_path)
    r2 = compute_codebase_digest(tmp_path)

    assert r1["root_digest"] == r2["root_digest"]
