# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_cancellation.py:51
# Component id: sy.source.ass_ade.check_many_times
__version__ = "0.1.0"

        def check_many_times():
            for _ in range(100):
                results.append(ctx.check())
                time.sleep(0.001)
