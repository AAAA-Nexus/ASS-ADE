# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_prompt_hash.py:7
# Component id: at.source.a1_at_functions.prompt_hash
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
