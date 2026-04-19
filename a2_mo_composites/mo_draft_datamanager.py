# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_datamanager.py:7
# Component id: mo.source.a2_mo_composites.datamanager
from __future__ import annotations

__version__ = "0.1.0"

class DataManager:
    def __init__(self):
        self.data = []
        self.cache = {}
        self.temp = None
        self.flag = False
        self.count = 0
        self.total = 0
        self.average = 0
        self.maximum = 0
        self.minimum = 0

    def do_thing(self, x):
        self.data.append(x)
        self.count += 1
        self.total += x
        self.average = self.total / self.count
        if x > self.maximum: self.maximum = x
        if x < self.minimum: self.minimum = x
        return self.data

    def do_thing_2(self, x):
        self.data.append(x)
        self.count += 1
        self.total += x
        self.average = self.total / self.count
        if x > self.maximum: self.maximum = x
        if x < self.minimum: self.minimum = x
        return self.data
