# Extracted from C:/!ass-ade/src/ass_ade/local/docs_engine.py:209
# Component id: mo.source.ass_ade.detect_ci
from __future__ import annotations

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
