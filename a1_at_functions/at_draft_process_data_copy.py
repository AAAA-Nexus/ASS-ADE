# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_process_data_copy.py:7
# Component id: at.source.a1_at_functions.process_data_copy
from __future__ import annotations

__version__ = "0.1.0"

def process_data_copy(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
