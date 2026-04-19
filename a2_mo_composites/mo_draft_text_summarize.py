# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1128
# Component id: mo.source.ass_ade.text_summarize
__version__ = "0.1.0"

    def text_summarize(self, text: str, **kwargs: Any) -> TextSummary:
        """/v1/text/summarize — 1-3 sentence extractive summary. $0.040/request"""
        return self._post_model("/v1/text/summarize", TextSummary, {"text": text, **kwargs})
