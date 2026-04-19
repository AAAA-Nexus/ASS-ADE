# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_record_evolution_event_writes_ledger_and_markdown.py:5
# Component id: at.source.ass_ade.test_record_evolution_event_writes_ledger_and_markdown
__version__ = "0.1.0"

def test_record_evolution_event_writes_ledger_and_markdown(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )

    result = record_evolution_event(
        root=tmp_path,
        event_type="birth",
        summary="First public-safe birth record",
        commands=[],
        metrics={"tests_passed": 1150},
        reports=["RECON_REPORT.md"],
        timestamp_utc="2026-04-18T12:00:00Z",
    )

    assert Path(result.ledger_path).exists()
    assert Path(result.snapshot_path).exists()
    markdown = Path(result.markdown_path).read_text(encoding="utf-8")
    assert "First public-safe birth record" in markdown
    assert "`tests_passed`: 1150" in markdown
