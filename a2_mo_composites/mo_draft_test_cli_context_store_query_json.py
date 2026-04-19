# Extracted from C:/!ass-ade/tests/test_recon_context.py:177
# Component id: mo.source.ass_ade.test_cli_context_store_query_json
from __future__ import annotations

__version__ = "0.1.0"

def test_cli_context_store_query_json(tmp_path: Path) -> None:
    stored = runner.invoke(
        app,
        [
            "context",
            "store",
            "trusted docs packet",
            "--namespace",
            "demo",
            "--path",
            str(tmp_path),
            "--json",
        ],
    )
    queried = runner.invoke(
        app,
        [
            "context",
            "query",
            "trusted docs",
            "--namespace",
            "demo",
            "--path",
            str(tmp_path),
            "--json",
        ],
    )

    assert stored.exit_code == 0
    assert queried.exit_code == 0
    assert '"matches"' in queried.stdout
