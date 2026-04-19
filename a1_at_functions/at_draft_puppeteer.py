# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_puppeteer.py:7
# Component id: at.source.a1_at_functions.puppeteer
from __future__ import annotations

__version__ = "0.1.0"

def puppeteer(self):
    if self._puppeteer is None:
        from ass_ade.agent.puppeteer import Puppeteer
        self._puppeteer = Puppeteer(self._config, self._nexus)
    return self._puppeteer
