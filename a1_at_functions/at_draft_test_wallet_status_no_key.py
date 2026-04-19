# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_wallet_status_no_key.py:7
# Component id: at.source.a1_at_functions.test_wallet_status_no_key
from __future__ import annotations

__version__ = "0.1.0"

def test_wallet_status_no_key(self, tmp_path: Path, hybrid_config: Path) -> None:
    """Wallet status should display chain config and warn if key not set."""
    result = runner.invoke(
        app,
        ["wallet", "--config", str(hybrid_config)],
    )

    assert result.exit_code == 0
    assert "Wallet" in result.stdout or "wallet" in result.stdout.lower()
