# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_taskreporter.py:12
# Component id: at.source.ass_ade.generate_status_report
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
