from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_hook():
    hook_path = Path(__file__).resolve().parents[1] / "hooks" / "pre_prompt_governance.py"
    spec = importlib.util.spec_from_file_location("pre_prompt_governance", hook_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prompt_governance_hook_passes_clean_artifacts(tmp_path: Path) -> None:
    module = _load_hook()
    agents = tmp_path / "agents"
    skills = tmp_path / "skills"
    agents.mkdir()
    skills.mkdir()
    (agents / "prompt-governor.agent.md").write_text(
        "---\nname: Prompt Governor\n---\n\n# Prompt Governor\n\n## Constraints\n\n- Keep outputs public-safe.\n",
        encoding="utf-8",
    )
    (skills / "prompt-governance.skill.md").write_text(
        "# Prompt Governance Skill\n\n## Steps\n\n1. Hash the artifact.\n",
        encoding="utf-8",
    )

    result = module.run(str(tmp_path))

    assert result["ok"] is True
    assert result["ready"] is True
    assert result["artifact_count"] == 2


def test_prompt_governance_hook_blocks_secrets(tmp_path: Path) -> None:
    module = _load_hook()
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "bad.agent.md").write_text(
        "---\nname: Bad\n---\n\n# Bad\n\napi_key=abc123\n",
        encoding="utf-8",
    )

    result = module.run(str(tmp_path))

    assert result["ok"] is False
    assert result["critical_count"] == 1
    assert "credential" in result["findings"][0]["issues"][0]
