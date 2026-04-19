# Extracted from C:/!ass-ade/tests/test_map_terrain.py:144
# Component id: at.source.ass_ade.test_map_terrain_discovers_repo_asset_conventions
from __future__ import annotations

__version__ = "0.1.0"

def test_map_terrain_discovers_repo_asset_conventions(tmp_path: Path) -> None:
    skills = tmp_path / "skills"
    skills.mkdir()
    (skills / "design.skill.md").write_text("# Design\n", encoding="utf-8")

    prompts = tmp_path / "prompts"
    prompts.mkdir()
    (prompts / "blueprint-architect.md").write_text(
        "# Blueprint Architect\n", encoding="utf-8"
    )
    (prompts / "router_pack.prompt.md").write_text("# Router Pack\n", encoding="utf-8")

    instructions = tmp_path / "instructions"
    instructions.mkdir()
    (instructions / "router_rules.instructions.md").write_text(
        "# Router Rules\n", encoding="utf-8"
    )

    harnesses = tmp_path / "harnesses"
    harnesses.mkdir()
    (harnesses / "smoke_runner.py").write_text(
        "def run_harness():\n    return {}\n", encoding="utf-8"
    )

    result = map_terrain(
        task_description="Load generated repo assets.",
        required_capabilities={
            "skills": ["design"],
            "prompts": ["blueprint_architect", "router_pack"],
            "instructions": ["router_rules"],
            "harnesses": ["smoke_runner"],
        },
        working_dir=tmp_path,
    )

    assert result.verdict == "PROCEED"
    assert result.inventory_check["skills"]["design"] == "exists"
    assert result.inventory_check["prompts"]["blueprint_architect"] == "exists"
    assert result.inventory_check["instructions"]["router_rules"] == "exists"
