# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_gates.py:168
# Component id: at.source.ass_ade.scan_with_extra
__version__ = "0.1.0"

        def scan_with_extra(text: str):
            result = original_scan(text)
            gates._gate_log.append(GateResult(gate="scan_extra", passed=True, confidence=1.0))
            return result
