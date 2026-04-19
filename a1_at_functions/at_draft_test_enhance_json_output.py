# Extracted from C:/!ass-ade/tests/test_enhance_cli.py:71
# Component id: at.source.ass_ade.test_enhance_json_output
from __future__ import annotations

__version__ = "0.1.0"

def test_enhance_json_output(tmp_path: Path) -> None:
    (tmp_path / "sample.py").write_text("def f():\n    pass  # TODO: implement\n", encoding="utf-8")

    result = runner.invoke(app, ["enhance", str(tmp_path), "--json", "--local-only"])

    assert result.exit_code == 0
    start = result.output.find("{")
    assert start != -1, f"No JSON in output:\n{result.output}"
    payload = json.loads(result.output[start:], strict=False)
    assert "total_findings" in payload
