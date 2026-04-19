# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_generate_status_report.py:7
# Component id: at.source.a1_at_functions.generate_status_report
from __future__ import annotations

__version__ = "0.1.0"

def generate_status_report(self) -> str:
    """Generate a human-readable status report."""
    stats = self.manager.get_statistics()
    return (
        f"Task Report:\n"
        f"  Total tasks: {stats['total']}\n"
        f"  Completion: {stats['completion_rate']:.1f}%\n"
        f"  By status: {stats['by_status']}"
    )
