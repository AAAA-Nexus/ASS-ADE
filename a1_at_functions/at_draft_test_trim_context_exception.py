# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_gates.py:113
# Component id: at.source.ass_ade.test_trim_context_exception
__version__ = "0.1.0"

    def test_trim_context_exception(self):
        client = MagicMock()
        client.memory_trim.side_effect = Exception("fail")
        gates = QualityGates(client)
        assert gates.trim_context("text", 100) is None
