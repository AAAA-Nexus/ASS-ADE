# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testcompletionresponse.py:6
# Component id: at.source.ass_ade.test_basic
__version__ = "0.1.0"

    def test_basic(self):
        r = CompletionResponse(
            message=Message(role="assistant", content="done"),
            finish_reason="stop",
        )
        assert r.finish_reason == "stop"
        assert r.model is None
