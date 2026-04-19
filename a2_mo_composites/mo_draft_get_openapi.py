# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:277
# Component id: mo.source.ass_ade.get_openapi
__version__ = "0.1.0"

    def get_openapi(self) -> OpenApiDocument:
        """/openapi.json — free"""
        return self._get_model("/openapi.json", OpenApiDocument)
