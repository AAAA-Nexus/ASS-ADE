# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_status_structure.py:7
# Component id: at.source.a1_at_functions.test_status_structure
from __future__ import annotations

__version__ = "0.1.0"

def test_status_structure(self, tmp_path):
    fly = self._make(tmp_path)
    status = fly.status()
    assert hasattr(status, "adapter_version")
    assert hasattr(status, "contribution_count")
    assert hasattr(status, "ratchet_epoch")
    assert hasattr(status, "pending_count")
