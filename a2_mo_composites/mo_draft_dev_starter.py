# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1018
# Component id: mo.source.a2_mo_composites.dev_starter
from __future__ import annotations

__version__ = "0.1.0"

def dev_starter(self, project_name: str, language: str = "python", **kwargs: Any) -> StarterKit:
    """/v1/dev/starter — scaffold agent project with x402 wiring (DEV-601). $0.040/call"""
    return self._post_model("/v1/dev/starter", StarterKit, {"project_name": project_name, "language": language, **kwargs})
