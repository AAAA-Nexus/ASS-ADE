# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_report_tracks_passes_failures.py:7
# Component id: at.source.a1_at_functions.test_report_tracks_passes_failures
from __future__ import annotations

__version__ = "0.1.0"

def test_report_tracks_passes_failures(self):
    from ass_ade.agent.cie import CIEPipeline
    cie = CIEPipeline({"cie": {"enable_lint": False}})
    cie.run("x = 1\n", "python")
    cie.run("def bad(:\n    pass\n", "python")
    rep = cie.report()
    assert rep["passes"] >= 1
    assert rep["failures"] >= 1
    assert 0.0 <= rep["pass_rate"] <= 1.0
