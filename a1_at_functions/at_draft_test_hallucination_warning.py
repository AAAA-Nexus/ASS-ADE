# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testagentloop.py:179
# Component id: at.source.ass_ade.test_hallucination_warning
__version__ = "0.1.0"

    def test_hallucination_warning(self, tmp_path):
        provider = _MockProvider([
            CompletionResponse(
                message=Message(role="assistant", content="I made this up."),
                finish_reason="stop",
            )
        ])
        registry = ToolRegistry()

        mock_gates = MagicMock(spec=QualityGates)
        mock_gates.scan_prompt.return_value = {"blocked": False}
        mock_gates.check_hallucination.return_value = {"verdict": "unsafe"}

        loop = AgentLoop(
            provider=provider,
            registry=registry,
            working_dir=str(tmp_path),
            quality_gates=mock_gates,
        )
        result = loop.step("Tell me something")
        assert "hallucination oracle" in result.lower()
