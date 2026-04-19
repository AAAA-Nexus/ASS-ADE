# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/prompt_toolkit.py:261
# Component id: at.source.ass_ade.prompt_diff
__version__ = "0.1.0"

def prompt_diff(
    *,
    baseline_path: str | Path,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
    redacted: bool = True,
    max_lines: int = 200,
) -> PromptDiffResult:
    root = Path(working_dir).resolve()
    current = load_prompt_artifact(
        working_dir=root,
        prompt_text=prompt_text,
        prompt_path=prompt_path,
    )
    baseline_file = _resolve_under(root, baseline_path)
    baseline = PromptArtifact(
        source=baseline_file.relative_to(root).as_posix(),
        text=baseline_file.read_text(encoding="utf-8", errors="replace"),
    )

    current_lines = current.text.splitlines()
    baseline_lines = baseline.text.splitlines()
    if redacted:
        current_lines = [_redact_line(line) for line in current_lines]
        baseline_lines = [_redact_line(line) for line in baseline_lines]

    diff_lines = list(difflib.unified_diff(
        baseline_lines,
        current_lines,
        fromfile=f"a/{baseline.source}",
        tofile=f"b/{current.source}",
        lineterm="",
    ))
    truncated = len(diff_lines) > max_lines
    if truncated:
        diff_lines = diff_lines[:max_lines] + ["... [diff truncated]"]

    return PromptDiffResult(
        source=current.source,
        baseline_source=baseline.source,
        current_sha256=hashlib.sha256(current.text.encode()).hexdigest(),
        baseline_sha256=hashlib.sha256(baseline.text.encode()).hexdigest(),
        diff="\n".join(diff_lines) or "(no changes)",
        redacted=redacted,
        truncated=truncated,
    )
