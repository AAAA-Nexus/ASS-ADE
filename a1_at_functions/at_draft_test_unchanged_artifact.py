# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testassignversion.py:11
# Component id: at.source.ass_ade.test_unchanged_artifact
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
