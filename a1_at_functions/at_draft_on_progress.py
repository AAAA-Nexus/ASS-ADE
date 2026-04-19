# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1313
# Component id: at.source.ass_ade.on_progress
from __future__ import annotations

__version__ = "0.1.0"

def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
    color = "green" if status == StepStatus.PASSED else "red"
    if status == StepStatus.RUNNING:
        color = "yellow"
    console.print(f"[{current}/{total}] {name}: [{color}]{status.value}[/{color}]")
