# Extracted from C:/!ass-ade/tests/test_workflows.py:182
# Component id: og.source.ass_ade.test_shield_failure_blocks_cert
from __future__ import annotations

__version__ = "0.1.0"

def test_shield_failure_blocks_cert(self) -> None:
    client = _mock_client()
    client.security_shield.return_value = ShieldResult(sanitized=False, blocked=True)
    result = safe_execute(client, "dangerous_tool", "rm -rf /")
    assert result.shield_passed is False
    # Certificate should not be generated when shield fails
    assert result.certificate_id is None
