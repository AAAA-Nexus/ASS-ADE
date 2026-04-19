# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:40
# Component id: mo.source.ass_ade.openapidocument
__version__ = "0.1.0"

class OpenApiDocument(NexusModel):
    openapi: str | None = None
    info: OpenApiInfo
