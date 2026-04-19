# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1159
# Component id: mo.source.ass_ade.data_convert
__version__ = "0.1.0"

    def data_convert(self, content: str, target_format: str, **kwargs: Any) -> dict:
        """/v1/data/convert — Convert text content to a target format. $0.020/request"""
        return self._post_raw("/v1/data/convert", {"content": content, "target_format": target_format, **kwargs})
