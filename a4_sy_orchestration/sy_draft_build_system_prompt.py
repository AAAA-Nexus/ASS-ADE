# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_build_system_prompt.py:7
# Component id: sy.source.a4_sy_orchestration.build_system_prompt
from __future__ import annotations

__version__ = "0.1.0"

def build_system_prompt(working_dir: str = ".") -> str:
    """Build the system prompt with project context."""
    cwd = Path(working_dir).resolve()
    project_info = _gather_project_info(cwd)
    capability_info = render_capability_prompt_section(cwd, max_cli=240, max_tools=40, max_mcp=50)
    return SYSTEM_PROMPT_TEMPLATE.format(
        cwd=cwd,
        project_info=project_info,
        capability_info=capability_info,
    )
