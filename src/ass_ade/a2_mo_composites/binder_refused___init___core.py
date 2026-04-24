"""Tier a2 — assimilated method 'BinderRefused.__init__'

Assimilated from: nexus.py:109-111
"""

from __future__ import annotations


# --- assimilated symbol ---
def __init__(self, code: str, message: str = ""):
    self.code = code
    super().__init__(message or code)

