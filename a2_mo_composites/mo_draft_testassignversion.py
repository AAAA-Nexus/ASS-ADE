# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:119
# Component id: mo.source.ass_ade.testassignversion
__version__ = "0.1.0"

class TestAssignVersion:
    def test_new_artifact(self):
        version, change_type = assign_version("at.foo", "", "python", {})
        assert version == INITIAL_VERSION
        assert change_type == "new"

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

    def test_patch_bump(self):
        old_body = "def foo():\n    return 1"
        new_body = "def foo():\n    return 2"
        prev = {
            "at.foo": {
                "version": "0.1.3",
                "body_hash": content_hash(old_body),
                "body": old_body,
            }
        }
        version, change_type = assign_version("at.foo", new_body, "python", prev)
        assert version == "0.1.4"
        assert change_type == "patch"

    def test_minor_bump(self):
        old_body = "def foo(): pass"
        new_body = "def foo(): pass\ndef bar(): pass"
        prev = {
            "at.foo": {
                "version": "0.1.3",
                "body_hash": content_hash(old_body),
                "body": old_body,
            }
        }
        version, change_type = assign_version("at.foo", new_body, "python", prev)
        assert version == "0.2.0"
        assert change_type == "minor"

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
