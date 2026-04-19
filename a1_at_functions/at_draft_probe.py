# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_probe.py:7
# Component id: at.source.a1_at_functions.probe
from __future__ import annotations

__version__ = "0.1.0"

def probe(group: str, name: str, fn: Callable[[], Any]) -> None:
    """Call fn(), record PASS / FAIL, print one line."""
    t0 = time.perf_counter()
    try:
        fn()
        ms = (time.perf_counter() - t0) * 1000
        print(f"  {PASS} {name:55s} {DIM}{ms:7.0f} ms{RESET}")
        results.append((group, name, "PASS", ms))
    except Exception as exc:
        ms = (time.perf_counter() - t0) * 1000
        short = str(exc)[:80].replace("\n", " ")
        print(f"  {FAIL} {name:55s} {DIM}{short}{RESET}")
        results.append((group, name, "FAIL", ms))
