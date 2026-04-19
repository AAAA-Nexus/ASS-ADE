# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1132
# Component id: mo.source.ass_ade.text_keywords
__version__ = "0.1.0"

    def text_keywords(self, text: str, top_k: int = 10, **kwargs: Any) -> TextKeywords:
        """/v1/text/keywords — TF-IDF keyword extraction. $0.020/request"""
        return self._post_model("/v1/text/keywords", TextKeywords, {"text": text, "top_k": top_k, **kwargs})
