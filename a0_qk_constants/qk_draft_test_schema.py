# Extracted from C:/!ass-ade/tests/test_engine.py:45
# Component id: qk.source.ass_ade.test_schema
from __future__ import annotations

__version__ = "0.1.0"

def test_schema(self):
    s = ToolSchema(name="read_file", description="Read a file", parameters={"type": "object"})
    assert s.name == "read_file"
