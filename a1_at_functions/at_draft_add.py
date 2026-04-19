# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/pipeline.py:131
# Component id: at.source.ass_ade.add
__version__ = "0.1.0"

    def add(self, name: str, fn: StepFunction) -> Pipeline:
        """Add a step to the pipeline. Returns self for chaining."""
        self._steps.append(_StepEntry(name=name, fn=fn))
        return self
