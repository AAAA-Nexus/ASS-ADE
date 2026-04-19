# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testmcpcancellation.py:31
# Component id: sy.source.ass_ade.test_cancellation_notification_marks_context_cancelled
__version__ = "0.1.0"

    def test_cancellation_notification_marks_context_cancelled(self, server: MCPServer) -> None:
        """Verify that notifications/cancelled marks the context as cancelled."""
        _initialize_server(server)

        req_id = 456
        # Create a cancellation context by starting a request
        # (in practice, the server._handle_tools_call creates it)
        ctx = server._cancellation_contexts[req_id] = CancellationContext()

        # Send a cancellation notification
        cancel_notif = {
            "method": "notifications/cancelled",
            "params": {"requestId": req_id},
        }
        server._handle(cancel_notif)

        # The context should now be marked as cancelled
        assert ctx.check() is True
