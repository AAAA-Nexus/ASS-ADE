# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_test_mcp_invoke_schema_validate_fails.py:12
# Component id: qk.source.a0_qk_constants.fakeclient
from __future__ import annotations

__version__ = "0.1.0"

class FakeClient:
    def __init__(self, base_url: str, timeout: float = 20.0, transport=None, api_key: str | None = None):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def get_mcp_manifest(self):
        return manifest
