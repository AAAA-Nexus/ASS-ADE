# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_write_branch_evolution_demo.py:7
# Component id: at.source.a1_at_functions.write_branch_evolution_demo
from __future__ import annotations

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
