# Extracted from C:/!ass-ade/src/ass_ade/mcp/mock_server.py:87
# Component id: sy.source.ass_ade.build_handler
from __future__ import annotations

__version__ = "0.1.0"

def build_handler(manifest: dict) -> type[_Handler]:
    """Return a handler class with the given manifest bound."""
    class BoundHandler(_Handler):
        pass
    BoundHandler.manifest = manifest
    return BoundHandler
