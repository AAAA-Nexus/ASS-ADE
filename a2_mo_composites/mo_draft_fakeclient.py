# Extracted from C:/!ass-ade/tests/test_mcp.py:168
# Component id: mo.source.ass_ade.fakeclient
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
