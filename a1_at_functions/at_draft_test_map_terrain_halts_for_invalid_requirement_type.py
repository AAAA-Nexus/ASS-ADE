# Extracted from C:/!ass-ade/tests/test_map_terrain.py:214
# Component id: at.source.ass_ade.test_map_terrain_halts_for_invalid_requirement_type
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
    assert (
        result.inventory_check["requirements"]["unknown_type"]
        == "unsupported capability type"
    )
