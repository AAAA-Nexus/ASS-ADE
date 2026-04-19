# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_sync_atomadic_prompt_capabilities.py:7
# Component id: at.source.a1_at_functions.sync_atomadic_prompt_capabilities
from __future__ import annotations

__version__ = "0.1.0"

def sync_atomadic_prompt_capabilities(
    *,
    repo_root: str | Path = ".",
    prompt_path: str | Path = "agents/atomadic_interpreter.md",
) -> Path:
    """Refresh the generated capability block in the Atomadic prompt artifact."""
    root = Path(repo_root).resolve()
    target = Path(prompt_path)
    if not target.is_absolute():
        target = root / target
    target.parent.mkdir(parents=True, exist_ok=True)
    marker = "\n---\n\n## Current Capabilities"
    if target.exists():
        text = target.read_text(encoding="utf-8")
        if marker in text:
            text = text[: text.index(marker)].rstrip()
    else:
        text = "# Atomadic Nexus Interpreter\n"
    target.write_text(
        f"{text.rstrip()}\n\n{render_markdown_capability_section(root)}",
        encoding="utf-8",
    )
    return target
