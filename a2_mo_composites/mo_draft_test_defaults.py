# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine.py:51
# Component id: mo.source.ass_ade.test_defaults
__version__ = "0.1.0"

    def test_defaults(self):
        r = CompletionRequest(messages=[Message(role="user", content="hi")])
        assert r.temperature == 0.0
        assert r.max_tokens == 4096
        assert r.tools == []
        assert r.model is None
