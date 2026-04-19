# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_map_terrain_auto_invent_persists_tool_plan.py:7
# Component id: at.source.a1_at_functions.test_map_terrain_auto_invent_persists_tool_plan
from __future__ import annotations

__version__ = "0.1.0"

def test_map_terrain_auto_invent_persists_tool_plan(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Run Semgrep before merge.",
        required_capabilities={"tools": ["nexus_semgrep_scan"]},
        auto_invent_if_missing=True,
        working_dir=tmp_path,
    )

    assert result.verdict == "HALT_AND_INVENT"
    assert result.development_plan is not None
    assert result.development_plan.auto_invent_triggered is True
    assert len(result.development_plan.created_assets) == 1
    path = Path(result.development_plan.created_assets[0])
    assert path.exists()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["capability"]["name"] == "nexus_semgrep_scan"
