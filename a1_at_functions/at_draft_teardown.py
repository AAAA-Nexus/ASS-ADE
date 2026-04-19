# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_teardown.py:7
# Component id: at.source.a1_at_functions.teardown
from __future__ import annotations

__version__ = "0.1.0"

def teardown(self) -> None:
    """Mark the session as ended (client-side only)."""
    self.session_id = None
    self.epoch = 0
    self._started = False
