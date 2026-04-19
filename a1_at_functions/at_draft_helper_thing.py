# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_helper_thing.py:7
# Component id: at.source.a1_at_functions.helper_thing
from __future__ import annotations

__version__ = "0.1.0"

def helper_thing(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                return x + y + z
            else:
                return x + y
        else:
            return x
    else:
        return 0
