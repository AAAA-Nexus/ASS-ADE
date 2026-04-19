# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_cancellation.py:47
# Component id: sy.source.ass_ade.test_cancellation_context_is_thread_safe
__version__ = "0.1.0"

    def test_cancellation_context_is_thread_safe(self) -> None:
        ctx = CancellationContext()
        results = []

        def check_many_times():
            for _ in range(100):
                results.append(ctx.check())
                time.sleep(0.001)

        def cancel_once():
            time.sleep(0.01)
            ctx.cancel()

        threads = [threading.Thread(target=check_many_times) for _ in range(5)]
        threads.append(threading.Thread(target=cancel_once))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should have some False and some True values
        assert False in results
        assert True in results
