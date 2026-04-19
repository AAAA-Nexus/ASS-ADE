# Extracted from C:/!ass-ade/benchmarks/messy_demo/utils.py:12
# Component id: at.source.ass_ade.process_data_copy
from __future__ import annotations

__version__ = "0.1.0"

def process_data_copy(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
