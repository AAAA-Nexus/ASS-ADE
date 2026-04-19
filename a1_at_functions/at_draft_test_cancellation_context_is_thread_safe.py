# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cancellation_context_is_thread_safe.py:7
# Component id: at.source.a1_at_functions.test_cancellation_context_is_thread_safe
from __future__ import annotations

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
