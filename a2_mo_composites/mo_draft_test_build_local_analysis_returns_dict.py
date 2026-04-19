# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_docs_engine.py:147
# Component id: mo.source.ass_ade.test_build_local_analysis_returns_dict
__version__ = "0.1.0"

def test_build_local_analysis_returns_dict(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("def main(): pass\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )

    analysis = build_local_analysis(tmp_path)

    assert isinstance(analysis, dict)
    for key in ("root", "languages", "metadata", "symbols", "test_framework", "ci", "summary"):
        assert key in analysis, f"missing key: {key}"
