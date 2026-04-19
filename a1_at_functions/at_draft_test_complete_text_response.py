# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testnexusprovider.py:6
# Component id: at.source.ass_ade.test_complete_text_response
__version__ = "0.1.0"

    def test_complete_text_response(self):
        mock_client = MagicMock()
        mock_client.inference.return_value = MagicMock(
            result="Hello from Nexus!",
            text=None,
            model="llama-3.1-8b",
        )

        provider = NexusProvider(mock_client)
        req = CompletionRequest(messages=[Message(role="user", content="hi")])
        resp = provider.complete(req)

        assert resp.message.content == "Hello from Nexus!"
        assert resp.model == "llama-3.1-8b"
        assert resp.finish_reason == "stop"
