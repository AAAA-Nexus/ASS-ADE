# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_grepsearchtool.py:20
# Component id: at.source.ass_ade.parameters
__version__ = "0.1.0"

    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Regex pattern (case-insensitive)."},
                "include": {
                    "type": "string",
                    "description": "Glob to filter files (e.g., '**/*.py'). Default: all files.",
                },
            },
            "required": ["pattern"],
        }
