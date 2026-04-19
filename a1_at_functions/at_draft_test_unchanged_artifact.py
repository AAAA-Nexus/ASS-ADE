# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_unchanged_artifact.py:7
# Component id: at.source.a1_at_functions.test_unchanged_artifact
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
