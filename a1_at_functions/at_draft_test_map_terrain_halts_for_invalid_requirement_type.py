# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_map_terrain_halts_for_invalid_requirement_type.py:7
# Component id: at.source.a1_at_functions.test_map_terrain_halts_for_invalid_requirement_type
from __future__ import annotations

__version__ = "0.1.0"

def test_map_terrain_halts_for_invalid_requirement_type(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Run a guarded action.",
        required_capabilities={"unknown_type": ["x"]},
        working_dir=tmp_path,
    )

    assert result.verdict == "HALT_AND_INVENT"
    assert result.development_plan is not None
    assert result.inventory_check["requirements"]["unknown_type"] == "unsupported capability type"
