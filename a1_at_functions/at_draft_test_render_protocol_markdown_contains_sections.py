# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_protocol.py:44
# Component id: at.source.ass_ade.test_render_protocol_markdown_contains_sections
__version__ = "0.1.0"

def test_render_protocol_markdown_contains_sections(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    report = run_protocol("Improve public shell", tmp_path, AssAdeConfig(profile="local"))
    markdown = render_protocol_markdown(report)

    assert "# ASS-ADE Public Enhancement Cycle" in markdown
    assert "## Assessment" in markdown
    assert "## Audit" in markdown
    assert "## Recommendations" in markdown
