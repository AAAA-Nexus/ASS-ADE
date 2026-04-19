# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1312
# Component id: at.source.ass_ade.on_progress
__version__ = "0.1.0"

    def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
        color = "green" if status == StepStatus.PASSED else "red"
        if status == StepStatus.RUNNING:
            color = "yellow"
        console.print(f"[{current}/{total}] {name}: [{color}]{status.value}[/{color}]")
