# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_load_prompt_artifact.py:5
# Component id: at.source.ass_ade.load_prompt_artifact
__version__ = "0.1.0"

def load_prompt_artifact(
    *,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
    source_label: str | None = None,
) -> PromptArtifact:
    if bool(prompt_text) == bool(prompt_path):
        raise ValueError("provide exactly one of prompt_text or prompt_path")

    if prompt_text is not None:
        return PromptArtifact(source=source_label or "inline", text=prompt_text)

    root = Path(working_dir).resolve()
    path = _resolve_under(root, prompt_path or "")
    return PromptArtifact(
        source=source_label or path.relative_to(root).as_posix(),
        text=path.read_text(encoding="utf-8", errors="replace"),
    )
