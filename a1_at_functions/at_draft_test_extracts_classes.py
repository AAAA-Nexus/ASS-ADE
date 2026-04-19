# Extracted from C:/!ass-ade/tests/test_version_tracker.py:75
# Component id: at.source.ass_ade.test_extracts_classes
from __future__ import annotations

__version__ = "0.1.0"

def test_extracts_classes(self):
    body = "class Foo: pass\nclass _Hidden: pass"
    assert _public_python_api(body) == {"Foo"}
