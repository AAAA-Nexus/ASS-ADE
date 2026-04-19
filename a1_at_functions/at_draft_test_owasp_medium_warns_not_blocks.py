# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_owasp_medium_warns_not_blocks.py:7
# Component id: at.source.a1_at_functions.test_owasp_medium_warns_not_blocks
from __future__ import annotations

__version__ = "0.1.0"

def test_owasp_medium_warns_not_blocks(self):
    from ass_ade.agent.cie import CIEPipeline
    cie = CIEPipeline({"cie": {"enable_lint": False, "hard_block_owasp": True}})
    code = "import hashlib\nhashlib.md5(b'data')\n"
    result = cie.run(code, "python")
    # A02_weak_hash is medium — owasp_clean stays True, but warning present
    assert result.owasp_clean is True
    assert any("OWASP_medium" in w for w in result.warnings)
