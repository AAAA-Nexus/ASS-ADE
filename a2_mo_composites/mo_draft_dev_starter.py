# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1213
# Component id: mo.source.ass_ade.dev_starter
from __future__ import annotations

__version__ = "0.1.0"

def dev_starter(self, project_name: str, language: str = "python", **kwargs: Any) -> StarterKit:
    """/v1/dev/starter — scaffold agent project with x402 wiring (DEV-601). $0.040/call"""
    return self._post_model("/v1/dev/starter", StarterKit, {"project_name": project_name, "language": language, **kwargs})
