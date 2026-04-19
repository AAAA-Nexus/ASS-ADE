# Extracted from C:/!ass-ade/tests/test_map_terrain.py:45
# Component id: at.source.ass_ade.test_map_terrain_halts_and_builds_invention_plan
from __future__ import annotations

__version__ = "0.1.0"

def test_map_terrain_halts_and_builds_invention_plan(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Scan Python code for OWASP findings.",
        required_capabilities={"agents": ["security_scanner"]},
        working_dir=tmp_path,
    )

    assert result.verdict == "HALT_AND_INVENT"
    assert result.missing_capabilities[0].name == "security_scanner"
    assert (
        result.missing_capabilities[0].recommended_creation_tool == "nexus_spawn_agent"
    )
    assert result.development_plan is not None
    assert result.development_plan.auto_invent_triggered is False
