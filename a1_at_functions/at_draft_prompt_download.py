# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_prompt_download.py:7
# Component id: at.source.a1_at_functions.prompt_download
from __future__ import annotations

__version__ = "0.1.0"

def prompt_download(self) -> dict:
    """/v1/prompts/download — curated agent-ready prompt library. Free"""
    return self._get_raw("/v1/prompts/download")
