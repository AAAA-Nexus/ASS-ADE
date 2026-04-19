# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:637
# Component id: at.source.ass_ade.test_ratchet_register_success
from __future__ import annotations

__version__ = "0.1.0"

def test_ratchet_register_success(self, tmp_path: Path, hybrid_config: Path) -> None:
    """Ratchet register should create a new security session."""
    mock_nx = MagicMock()
    mock_nx.ratchet_register.return_value = RatchetSession(
        session_id="sess-secure-abc",
        epoch=1,
        fips_203_compliant=True,
    )

    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["ratchet", "register", "agent-secure", "--config", str(hybrid_config)],
        )

    assert result.exit_code == 0
    assert "sess-secure-abc" in result.stdout or "session" in result.stdout.lower()
