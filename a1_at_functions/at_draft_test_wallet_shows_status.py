# Extracted from C:/!ass-ade/tests/test_x402_flow.py:397
# Component id: at.source.ass_ade.test_wallet_shows_status
from __future__ import annotations

__version__ = "0.1.0"

def test_wallet_shows_status(self, tmp_path: Path) -> None:
    result = runner.invoke(
        app, ["wallet", "--config", str(_hybrid_config(tmp_path))],
        env={"ATOMADIC_X402_TESTNET": "1", "ATOMADIC_WALLET_KEY": ""},
    )
    assert result.exit_code == 0
    assert "Testnet Mode" in result.stdout or "x402" in result.stdout
