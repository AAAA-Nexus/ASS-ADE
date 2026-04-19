# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_build_handler.py:5
# Component id: at.source.ass_ade.build_handler
__version__ = "0.1.0"

def build_handler(manifest: dict) -> type[_Handler]:
    """Return a handler class with the given manifest bound."""
    class BoundHandler(_Handler):
        pass
    BoundHandler.manifest = manifest
    return BoundHandler
