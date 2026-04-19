# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testcancellationcontext.py:29
# Component id: at.source.ass_ade.check_many_times
__version__ = "0.1.0"

        def check_many_times():
            for _ in range(100):
                results.append(ctx.check())
                time.sleep(0.001)
