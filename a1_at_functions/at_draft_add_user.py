# Extracted from C:/!ass-ade/src/ass_ade/agent/conversation.py:38
# Component id: at.source.ass_ade.add_user
from __future__ import annotations

__version__ = "0.1.0"

def add_user(self, content: str) -> None:
    self._messages.append(Message(role="user", content=content))
