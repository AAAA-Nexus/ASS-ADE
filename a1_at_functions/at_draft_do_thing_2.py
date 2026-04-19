# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_do_thing_2.py:7
# Component id: at.source.a1_at_functions.do_thing_2
from __future__ import annotations

__version__ = "0.1.0"

def do_thing_2(self, x):
    self.data.append(x)
    self.count += 1
    self.total += x
    self.average = self.total / self.count
    if x > self.maximum: self.maximum = x
    if x < self.minimum: self.minimum = x
    return self.data
