# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/tools/prompt.py:103
# Component id: mo.source.ass_ade.promptdifftool
__version__ = "0.1.0"

class PromptDiffTool(_PromptToolBase):
    @property
    def name(self) -> str:
        return "prompt_diff"

    @property
    def description(self) -> str:
        return "Compare an explicit prompt artifact to a baseline and return a redacted diff."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "baseline_path": {"type": "string", "description": "Repo-relative baseline file."},
                "prompt_path": {"type": "string", "description": "Repo-relative current prompt file."},
                "prompt_text": {"type": "string", "description": "Inline current prompt text."},
                "redacted": {"type": "boolean", "description": "Redact secrets in diff."},
                "max_lines": {"type": "integer", "description": "Maximum diff lines to return."},
            },
            "required": ["baseline_path"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        return self._json(prompt_diff(working_dir=self._cwd, **kwargs))
