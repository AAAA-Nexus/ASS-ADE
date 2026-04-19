# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testcancellationcontext.py:7
# Component id: mo.source.a2_mo_composites.testcancellationcontext
from __future__ import annotations

__version__ = "0.1.0"

class TestCancellationContext:
    """Test basic cancellation context behavior."""

    def test_cancellation_context_defaults_to_not_cancelled(self) -> None:
        ctx = CancellationContext()
        assert ctx.check() is False
        assert ctx.is_cancelled is False

    def test_cancellation_context_can_be_marked_cancelled(self) -> None:
        ctx = CancellationContext()
        ctx.cancel()
        assert ctx.check() is True
        assert ctx.is_cancelled is True

    def test_null_cancellation_context_never_cancels(self) -> None:
        ctx = NullCancellationContext()
        ctx.cancel()
        assert ctx.check() is False
        assert ctx.is_cancelled is False

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
