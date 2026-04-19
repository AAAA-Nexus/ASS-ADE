# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:390
# Component id: at.source.ass_ade.test_cli_recon_json_flag
from __future__ import annotations

__version__ = "0.1.0"

def test_cli_recon_json_flag(tmp_path: Path) -> None:
    import json
    _seed_full_repo(tmp_path)
    result = runner.invoke(app, ["recon", str(tmp_path), "--json"])
    assert result.exit_code == 0
    # JSON output should be parseable
    # The output may be Rich-rendered; extract the JSON block
    lines = result.output.strip().splitlines()
    # Find the first line that looks like JSON
    json_start = next((i for i, l in enumerate(lines) if l.strip().startswith("{")), None)
    assert json_start is not None, "No JSON block found in output"
    json_text = "\n".join(lines[json_start:])
    # Remove any trailing non-JSON lines
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        # Try to find the closing brace
        depth = 0
        end = 0
        for i, ch in enumerate(json_text):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        data = json.loads(json_text[:end])
    assert "scout" in data
    assert "test" in data
