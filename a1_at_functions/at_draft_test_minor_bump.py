# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:152
# Component id: at.source.ass_ade.test_minor_bump
__version__ = "0.1.0"

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
