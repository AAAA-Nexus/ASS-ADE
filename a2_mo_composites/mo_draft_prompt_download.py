# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:485
# Component id: mo.source.a2_mo_composites.prompt_download
from __future__ import annotations

__version__ = "0.1.0"

def prompt_download(self) -> dict:
    """/v1/prompts/download — curated agent-ready prompt library. Free"""
    return self._get_raw("/v1/prompts/download")
