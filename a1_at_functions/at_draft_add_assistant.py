# Extracted from C:/!ass-ade/src/ass_ade/agent/conversation.py:41
# Component id: at.source.ass_ade.add_assistant
from __future__ import annotations

__version__ = "0.1.0"

def add_assistant(self, message: Message) -> None:
    self._messages.append(message)
