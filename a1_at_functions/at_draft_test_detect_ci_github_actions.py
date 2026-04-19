# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_detect_ci_github_actions.py:5
# Component id: at.source.ass_ade.test_detect_ci_github_actions
__version__ = "0.1.0"

def test_detect_ci_github_actions(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("on: push\n", encoding="utf-8")

    result = detect_ci(tmp_path)

    assert "github-actions" in result
