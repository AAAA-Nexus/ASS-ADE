# Extracted from C:/!ass-ade/tests/test_map_terrain.py:185
# Component id: at.source.ass_ade.test_map_terrain_auto_invent_supports_prompts_and_instructions
from __future__ import annotations

__version__ = "0.1.0"

def test_map_terrain_auto_invent_supports_prompts_and_instructions(
    tmp_path: Path,
) -> None:
    result = map_terrain(
        task_description="Create routing prompts and instructions.",
        required_capabilities={
            "prompts": ["router_pack"],
            "instructions": ["router_rules"],
        },
        auto_invent_if_missing=True,
        working_dir=tmp_path,
    )

    assert result.verdict == "HALT_AND_INVENT"
    assert result.development_plan is not None
    assert result.development_plan.auto_invent_triggered is True
    assert (tmp_path / "prompts" / "router_pack.prompt.md").exists()
    assert (tmp_path / "instructions" / "router_rules.instructions.md").exists()
    follow_up = map_terrain(
        task_description="Create routing prompts and instructions.",
        required_capabilities={
            "prompts": ["router_pack"],
            "instructions": ["router_rules"],
        },
        working_dir=tmp_path,
    )
    assert follow_up.verdict == "PROCEED"
