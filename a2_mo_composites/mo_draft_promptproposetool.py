# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_promptproposetool.py:7
# Component id: mo.source.a2_mo_composites.promptproposetool
from __future__ import annotations

__version__ = "0.1.0"

class PromptProposeTool(_PromptToolBase):
    @property
    def name(self) -> str:
        return "prompt_propose"

    @property
    def description(self) -> str:
        return "Create a prompt self-improvement proposal for an explicit prompt artifact."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "objective": {"type": "string", "description": "Improvement objective."},
                "prompt_path": {"type": "string", "description": "Repo-relative prompt file."},
                "prompt_text": {"type": "string", "description": "Inline prompt text."},
            },
            "required": ["objective"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        return self._json(prompt_propose(working_dir=self._cwd, **kwargs))
