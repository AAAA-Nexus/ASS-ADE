# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_detect_ci.py:5
# Component id: at.source.ass_ade.detect_ci
__version__ = "0.1.0"

def detect_ci(root: Path) -> list[str]:
    found: list[str] = []

    workflows_dir = root / ".github" / "workflows"
    if workflows_dir.exists():
        try:
            if any(p.suffix in {".yml", ".yaml"} for p in workflows_dir.iterdir()):
                found.append("github-actions")
        except Exception:
            pass

    if (root / ".gitlab-ci.yml").exists():
        found.append("gitlab-ci")

    if (root / "Jenkinsfile").exists():
        found.append("jenkins")

    if (root / ".circleci" / "config.yml").exists():
        found.append("circleci")

    return found
