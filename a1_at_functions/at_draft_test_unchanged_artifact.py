# Extracted from C:/!ass-ade/tests/test_version_tracker.py:125
# Component id: at.source.ass_ade.test_unchanged_artifact
from __future__ import annotations

__version__ = "0.1.0"

def test_unchanged_artifact(self):
    body = "def foo(): pass"
    prev = {
        "at.foo": {
            "version": "0.2.1",
            "body_hash": content_hash(body),
            "body": body,
        }
    }
    version, change_type = assign_version("at.foo", body, "python", prev)
    assert version == "0.2.1"
    assert change_type == "none"
