# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_prompt_section.py:7
# Component id: at.source.a1_at_functions.prompt_section
from __future__ import annotations

__version__ = "0.1.0"

def prompt_section(
    *,
    section: str,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
) -> PromptSectionResult:
    artifact = load_prompt_artifact(
        working_dir=working_dir,
        prompt_text=prompt_text,
        prompt_path=prompt_path,
    )
    found = _xml_section(artifact.text, section) or _markdown_section(artifact.text, section)
    if found is None:
        return PromptSectionResult(source=artifact.source, section=section, found=False)
    return PromptSectionResult(
        source=artifact.source,
        section=section,
        found=True,
        text=found,
        sha256=hashlib.sha256(found.encode()).hexdigest(),
    )
