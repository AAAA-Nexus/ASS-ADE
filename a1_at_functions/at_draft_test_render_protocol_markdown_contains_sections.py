# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_render_protocol_markdown_contains_sections.py:7
# Component id: at.source.a1_at_functions.test_render_protocol_markdown_contains_sections
from __future__ import annotations

__version__ = "0.1.0"

def test_render_protocol_markdown_contains_sections(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    report = run_protocol("Improve public shell", tmp_path, AssAdeConfig(profile="local"))
    markdown = render_protocol_markdown(report)

    assert "# ASS-ADE Public Enhancement Cycle" in markdown
    assert "## Assessment" in markdown
    assert "## Audit" in markdown
    assert "## Recommendations" in markdown
