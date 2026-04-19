# Extracted from C:/!ass-ade/tests/test_gates.py:168
# Component id: at.source.ass_ade.scan_with_extra
from __future__ import annotations

__version__ = "0.1.0"

def scan_with_extra(text: str):
    result = original_scan(text)
    gates._gate_log.append(GateResult(gate="scan_extra", passed=True, confidence=1.0))
    return result
