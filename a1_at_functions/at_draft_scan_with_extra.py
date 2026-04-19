# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_pipeline_collects_multiple_entries_appended_by_a_stage.py:12
# Component id: at.source.a1_at_functions.scan_with_extra
from __future__ import annotations

__version__ = "0.1.0"

def scan_with_extra(text: str):
    result = original_scan(text)
    gates._gate_log.append(GateResult(gate="scan_extra", passed=True, confidence=1.0))
    return result
