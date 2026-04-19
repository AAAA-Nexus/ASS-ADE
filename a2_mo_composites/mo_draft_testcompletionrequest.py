# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testcompletionrequest.py:5
# Component id: mo.source.ass_ade.testcompletionrequest
__version__ = "0.1.0"

class TestCompletionRequest:
    def test_defaults(self):
        r = CompletionRequest(messages=[Message(role="user", content="hi")])
        assert r.temperature == 0.0
        assert r.max_tokens == 4096
        assert r.tools == []
        assert r.model is None
