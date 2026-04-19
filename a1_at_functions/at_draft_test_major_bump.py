# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_major_bump.py:7
# Component id: at.source.a1_at_functions.test_major_bump
from __future__ import annotations

__version__ = "0.1.0"

def test_major_bump(self):
    old_body = "def foo(): pass\ndef bar(): pass"
    new_body = "def foo(): pass"
    prev = {
        "at.foo": {
            "version": "0.1.3",
            "body_hash": content_hash(old_body),
            "body": old_body,
        }
    }
    version, change_type = assign_version("at.foo", new_body, "python", prev)
    assert version == "1.0.0"
    assert change_type == "major"
