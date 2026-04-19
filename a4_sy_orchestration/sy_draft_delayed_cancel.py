# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testmcpcancellation.py:119
# Component id: sy.source.ass_ade.delayed_cancel
__version__ = "0.1.0"

        def delayed_cancel():
            time.sleep(0.05)
            ctx.cancel()
