# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_teststepstream.py:62
# Component id: at.source.ass_ade.test_blocked_event
__version__ = "0.1.0"

    def test_blocked_event(self, tmp_path):
        provider = _MockProvider([])
        mock_gates = MagicMock()
        mock_gates.scan_prompt.return_value = {"blocked": True}

        loop = AgentLoop(
            provider=provider,
            registry=ToolRegistry(),
            working_dir=str(tmp_path),
            quality_gates=mock_gates,
        )
        events = list(loop.step_stream("Bad input"))
        assert len(events) == 1
        assert events[0].kind == "blocked"
