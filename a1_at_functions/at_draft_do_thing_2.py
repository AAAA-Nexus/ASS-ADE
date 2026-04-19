# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/benchmarks/messy_demo/helpers.py:32
# Component id: at.source.ass_ade.do_thing_2
__version__ = "0.1.0"

    def do_thing_2(self, x):
        self.data.append(x)
        self.count += 1
        self.total += x
        self.average = self.total / self.count
        if x > self.maximum: self.maximum = x
        if x < self.minimum: self.minimum = x
        return self.data
