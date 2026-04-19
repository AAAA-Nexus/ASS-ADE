# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:234
# Component id: sy.source.ass_ade.puppeteer
__version__ = "0.1.0"

    def puppeteer(self):
        if self._puppeteer is None:
            from ass_ade.agent.puppeteer import Puppeteer
            self._puppeteer = Puppeteer(self._config, self._nexus)
        return self._puppeteer
