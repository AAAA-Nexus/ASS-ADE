# Extracted from C:/!ass-ade/src/ass_ade/prompt_toolkit.py:110
# Component id: at.source.ass_ade.prompt_hash
from __future__ import annotations

__version__ = "0.1.0"

def prompt_hash(
    *,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
) -> PromptHashResult:
    artifact = load_prompt_artifact(
        working_dir=working_dir,
        prompt_text=prompt_text,
        prompt_path=prompt_path,
    )
    encoded = artifact.text.encode()
    return PromptHashResult(
        source=artifact.source,
        sha256=hashlib.sha256(encoded).hexdigest(),
        bytes=len(encoded),
        lines=len(artifact.text.splitlines()),
    )
