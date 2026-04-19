# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_record_evolution_event_writes_ledger_and_markdown.py:7
# Component id: at.source.a1_at_functions.test_record_evolution_event_writes_ledger_and_markdown
from __future__ import annotations

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
