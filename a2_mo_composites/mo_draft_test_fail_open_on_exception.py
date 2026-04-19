# Extracted from C:/!ass-ade/tests/test_phase_engines.py:394
# Component id: mo.source.ass_ade.test_fail_open_on_exception
from __future__ import annotations

__version__ = "0.1.0"

def test_fail_open_on_exception(self):
    from ass_ade.agent.cie import CIEPipeline
    cie = CIEPipeline({})
    # Should not raise even with weird input
    result = cie.run(None, "python")  # type: ignore
    assert result is not None
