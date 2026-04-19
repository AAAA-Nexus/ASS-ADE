# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_prompthashtool.py:7
# Component id: mo.source.a2_mo_composites.prompthashtool
from __future__ import annotations

__version__ = "0.1.0"

class PromptHashTool(_PromptToolBase):
    @property
    def name(self) -> str:
        return "prompt_hash"

    @property
    def description(self) -> str:
        return "Return SHA-256 metadata for an explicit prompt file or prompt text."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt_path": {"type": "string", "description": "Repo-relative prompt file."},
                "prompt_text": {"type": "string", "description": "Inline prompt text."},
            },
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        return self._json(prompt_hash(working_dir=self._cwd, **kwargs))
