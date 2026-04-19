# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_promptsectiontool.py:5
# Component id: mo.source.ass_ade.promptsectiontool
__version__ = "0.1.0"

class PromptSectionTool(_PromptToolBase):
    @property
    def name(self) -> str:
        return "prompt_section"

    @property
    def description(self) -> str:
        return "Extract a Markdown heading or XML tag section from an explicit prompt artifact."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "section": {"type": "string", "description": "Section title or XML tag name."},
                "prompt_path": {"type": "string", "description": "Repo-relative prompt file."},
                "prompt_text": {"type": "string", "description": "Inline prompt text."},
            },
            "required": ["section"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        return self._json(prompt_section(working_dir=self._cwd, **kwargs))
