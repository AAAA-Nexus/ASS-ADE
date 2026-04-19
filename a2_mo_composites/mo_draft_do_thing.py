# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_datamanager.py:17
# Component id: mo.source.ass_ade.do_thing
__version__ = "0.1.0"

    def do_thing(self, x):
        self.data.append(x)
        self.count += 1
        self.total += x
        self.average = self.total / self.count
        if x > self.maximum: self.maximum = x
        if x < self.minimum: self.minimum = x
        return self.data
