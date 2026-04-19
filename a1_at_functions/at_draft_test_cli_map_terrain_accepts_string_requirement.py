# Extracted from C:/!ass-ade/tests/test_map_terrain.py:272
# Component id: at.source.ass_ade.test_cli_map_terrain_accepts_string_requirement
from __future__ import annotations

__version__ = "0.1.0"

def test_cli_map_terrain_accepts_string_requirement(tmp_path: Path) -> None:
    req = tmp_path / "requirements.json"
    req.write_text(json.dumps({"tools": "read_file"}), encoding="utf-8")
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
