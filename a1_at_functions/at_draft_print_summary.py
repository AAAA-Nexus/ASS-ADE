# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_print_summary.py:7
# Component id: at.source.a1_at_functions.print_summary
from __future__ import annotations

__version__ = "0.1.0"

def print_summary() -> None:
    total = len(results)
    passed = sum(1 for _, _, s, _ in results if s == "PASS")
    failed = sum(1 for _, _, s, _ in results if s == "FAIL")

    print(f"{CYAN}{'=' * 70}{RESET}")
    print(f"{CYAN}  SUMMARY: {passed}/{total} passed  ({failed} failed){RESET}")
    print(f"{CYAN}{'=' * 70}{RESET}")

    if failed:
        print(f"\n{RED}  Failed endpoints:{RESET}")
        for grp, name, status, _ in results:
            if status == "FAIL":
                print(f"    {RED}  FAIL: {grp:15s} {name}{RESET}")

    # Per-group pass rate
    groups: dict[str, list[str]] = {}
    for grp, _, status, _ in results:
        groups.setdefault(grp, []).append(status)
    print(f"\n  {'Group':<20} {'Pass':>5} {'Fail':>5} {'Rate':>6}")
    print(f"  {'-'*20} {'-'*5} {'-'*5} {'-'*6}")
    for grp, statuses in sorted(groups.items()):
        p = statuses.count("PASS")
        f = statuses.count("FAIL")
        rate = f"{100*p//(p+f)}%" if p + f else "—"
        colour = GREEN if f == 0 else (YELLOW if p > 0 else RED)
        print(f"  {colour}{grp:<20} {p:>5} {f:>5} {rate:>6}{RESET}")
