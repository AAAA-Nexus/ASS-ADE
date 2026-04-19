# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_promptvalidatetool.py:7
# Component id: at.source.a1_at_functions.promptvalidatetool
from __future__ import annotations

__version__ = "0.1.0"

class PromptValidateTool(_PromptToolBase):
    @property
    def name(self) -> str:
        return "prompt_validate"

    @property
    def description(self) -> str:
        return "Validate an explicit prompt artifact against a JSON hash manifest."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "manifest_path": {"type": "string", "description": "Repo-relative JSON manifest."},
                "prompt_path": {"type": "string", "description": "Repo-relative prompt file."},
                "prompt_text": {"type": "string", "description": "Inline prompt text."},
                "prompt_name": {"type": "string", "description": "Optional manifest prompt entry name."},
            },
            "required": ["manifest_path"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        return self._json(prompt_validate(working_dir=self._cwd, **kwargs))
