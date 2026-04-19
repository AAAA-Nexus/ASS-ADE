# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygates.py:19
# Component id: at.source.ass_ade.test_scan_prompt_exception
__version__ = "0.1.0"

    def test_scan_prompt_exception(self):
        client = MagicMock()
        client.prompt_inject_scan.side_effect = Exception("network error")
        gates = QualityGates(client)
        assert gates.scan_prompt("test") is None
