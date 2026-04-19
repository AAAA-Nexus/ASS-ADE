# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_write_branch_evolution_demo.py:5
# Component id: at.source.ass_ade.write_branch_evolution_demo
__version__ = "0.1.0"

def write_branch_evolution_demo(
    *,
    root: Path,
    branches: Iterable[str],
    iterations: int,
    output: Path | None = None,
) -> Path:
    root = root.resolve()
    target = output if output is not None else root / DEFAULT_DEMO_PATH
    if not target.is_absolute():
        target = root / target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"{render_branch_evolution_demo(root=root, branches=branches, iterations=iterations)}\n",
        encoding="utf-8",
    )
    return target
