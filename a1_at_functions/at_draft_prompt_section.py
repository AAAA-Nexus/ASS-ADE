# Extracted from C:/!ass-ade/src/ass_ade/prompt_toolkit.py:231
# Component id: at.source.ass_ade.prompt_section
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
