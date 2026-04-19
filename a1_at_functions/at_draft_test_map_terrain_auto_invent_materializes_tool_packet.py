# Extracted from C:/!ass-ade/tests/test_map_terrain.py:61
# Component id: at.source.ass_ade.test_map_terrain_auto_invent_materializes_tool_packet
from __future__ import annotations

__version__ = "0.1.0"

def test_map_terrain_auto_invent_materializes_tool_packet(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Run Semgrep before merge.",
        required_capabilities={"tools": ["nexus_semgrep_scan"]},
        auto_invent_if_missing=True,
        working_dir=tmp_path,
    )

    assert result.verdict == "HALT_AND_INVENT"
    assert result.development_plan is not None
    assert result.development_plan.auto_invent_triggered is True
    tool_path = (
        tmp_path / "src" / "ass_ade" / "tools" / "generated" / "nexus_semgrep_scan.py"
    )
    packet_root = (
        tmp_path
        / ".ass-ade"
        / "capability-development"
        / "generated"
        / "tools-nexus_semgrep_scan"
    )
    manifest_path = packet_root / "manifest.json"
    assert tool_path.exists()
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["capability"]["name"] == "nexus_semgrep_scan"
    follow_up = map_terrain(
        task_description="Run Semgrep before merge.",
        required_capabilities={"tools": ["nexus_semgrep_scan"]},
        working_dir=tmp_path,
    )
    assert follow_up.verdict == "PROCEED"
