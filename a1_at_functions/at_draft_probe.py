# Extracted from C:/!ass-ade/scripts/probe_endpoints.py:66
# Component id: at.source.ass_ade.probe
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
