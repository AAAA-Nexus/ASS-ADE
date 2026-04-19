# Extracted from C:/!ass-ade/benchmarks/messy_demo/utils.py:18
# Component id: at.source.ass_ade.helper_thing
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
