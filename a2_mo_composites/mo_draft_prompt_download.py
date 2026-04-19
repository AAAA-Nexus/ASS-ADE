# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:680
# Component id: mo.source.ass_ade.prompt_download
__version__ = "0.1.0"

    def prompt_download(self) -> dict:
        """/v1/prompts/download — curated agent-ready prompt library. Free"""
        return self._get_raw("/v1/prompts/download")
