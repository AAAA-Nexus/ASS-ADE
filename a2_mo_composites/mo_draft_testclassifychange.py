# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testclassifychange.py:7
# Component id: mo.source.a2_mo_composites.testclassifychange
from __future__ import annotations

__version__ = "0.1.0"

class TestClassifyChange:
    def test_identical(self):
        body = "def foo(): pass"
        assert classify_change(body, body) == "none"

    def test_patch_internal_change(self):
        old = "def foo():\n    return 1"
        new = "def foo():\n    return 2"
        assert classify_change(old, new) == "patch"

    def test_minor_new_function(self):
        old = "def foo(): pass"
        new = "def foo(): pass\ndef bar(): pass"
        assert classify_change(old, new) == "minor"

    def test_major_removed_function(self):
        old = "def foo(): pass\ndef bar(): pass"
        new = "def foo(): pass"
        assert classify_change(old, new) == "major"

    def test_non_python_falls_back_to_patch(self):
        assert classify_change("old code", "new code", language="rust") == "patch"

    def test_empty_old_body(self):
        new = "def foo(): pass"
        result = classify_change("", new)
        assert result in {"minor", "patch"}
