# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_test_map_terrain_discovers_repo_agent_registry.py:7
# Component id: og.source.a3_og_features.test_map_terrain_discovers_repo_agent_registry
from __future__ import annotations

__version__ = "0.1.0"

def test_map_terrain_discovers_repo_agent_registry(tmp_path: Path) -> None:
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "certifier.agent.md").write_text("# Certifier\n", encoding="utf-8")
    (agents / "blueprint-architect.agent.md").write_text("# Blueprint Architect\n", encoding="utf-8")

    result = map_terrain(
        task_description="Certify the package.",
        required_capabilities={"agents": ["certifier", "blueprint_architect"]},
        working_dir=tmp_path,
    )

    assert result.verdict == "PROCEED"
    assert result.inventory_check["agents"]["certifier"] == "exists"
    assert result.inventory_check["agents"]["blueprint_architect"] == "exists"
