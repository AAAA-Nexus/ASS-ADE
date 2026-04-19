# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cli_map_terrain_json.py:7
# Component id: at.source.a1_at_functions.test_cli_map_terrain_json
from __future__ import annotations

__version__ = "0.1.0"

def test_cli_map_terrain_json(tmp_path: Path) -> None:
    req = tmp_path / "requirements.json"
    req.write_text(json.dumps({"tools": ["read_file"]}), encoding="utf-8")
    result = runner.invoke(
        app,
        [
            "workflow",
            "map-terrain",
            "Read a file",
            "--requirements-file",
            str(req),
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert '"verdict": "PROCEED"' in result.stdout
