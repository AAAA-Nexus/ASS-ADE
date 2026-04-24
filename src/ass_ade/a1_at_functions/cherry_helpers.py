"""Tier a1 — pure helpers for cherry-pick candidate ranking, menu formatting, and selection parsing."""

from __future__ import annotations

import re

from ass_ade.a0_qk_constants.cherry_types import CherryItemDict

_ACTION_PRIORITY: dict[str, int] = {"assimilate": 0, "enhance": 1, "rebuild": 2}
_VALID_ACTIONS = frozenset({"assimilate", "rebuild", "enhance"})


def action_priority(action: str) -> int:
    """Lower number = higher priority in the cherry-pick menu."""
    return _ACTION_PRIORITY.get(action, 99)


def rank_candidates(targets: list[dict[str, object]]) -> list[CherryItemDict]:
    """Convert raw TargetDecision dicts from a scout report into ranked CherryItemDicts.

    Ranking: action priority ASC, confidence DESC, has_nearby_test DESC, qualname ASC.
    Only actions in {assimilate, rebuild, enhance} are included (skip is excluded).
    """
    items: list[CherryItemDict] = []
    for raw in targets:
        action = str(raw.get("action", ""))
        if action not in _VALID_ACTIONS:
            continue
        symbol = raw.get("symbol")
        if not isinstance(symbol, dict):
            continue
        items.append(
            CherryItemDict(
                index=0,
                action=action,
                kind=str(symbol.get("kind", "function")),
                qualname=str(symbol.get("qualname", "")),
                module=str(symbol.get("module", "")),
                rel_path=str(symbol.get("rel_path", "")),
                source_root=str(symbol.get("root", "")),
                lineno=int(symbol.get("lineno", 0)),
                end_lineno=int(symbol.get("end_lineno", 0)),
                confidence=float(raw.get("confidence", 0.0)),
                reasons=list(raw.get("reasons", [])),
                recommended_path=str(raw.get("recommended_path", "")),
                docstring_present=bool(symbol.get("docstring_present", False)),
                has_nearby_test=bool(symbol.get("has_nearby_test", False)),
            )
        )

    items.sort(
        key=lambda i: (
            action_priority(i["action"]),
            -i["confidence"],
            0 if i["has_nearby_test"] else 1,
            i["qualname"],
        )
    )
    for idx, item in enumerate(items):
        item["index"] = idx + 1

    return items


def filter_by_actions(items: list[CherryItemDict], actions: set[str]) -> list[CherryItemDict]:
    """Keep only items whose action is in the given set."""
    if not actions:
        return items
    return [i for i in items if i["action"] in actions]


def parse_selection(raw: str, max_idx: int) -> list[int]:
    """Parse a user selection string into a sorted unique list of 1-based indices.

    Accepted formats:
      "all"       → [1 .. max_idx]
      "1,3,5"     → [1, 3, 5]
      "1-5"       → [1, 2, 3, 4, 5]
      "1,3-5,7"   → [1, 3, 4, 5, 7]
    Returns empty list if nothing is valid.
    """
    raw = raw.strip().lower()
    if raw in ("all", "a", "*"):
        return list(range(1, max_idx + 1))

    indices: set[int] = set()
    for part in re.split(r"[,\s]+", raw):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            bounds = part.split("-", 1)
            try:
                lo, hi = int(bounds[0]), int(bounds[1])
                for n in range(lo, hi + 1):
                    if 1 <= n <= max_idx:
                        indices.add(n)
            except ValueError:
                continue
        else:
            try:
                n = int(part)
                if 1 <= n <= max_idx:
                    indices.add(n)
            except ValueError:
                continue

    return sorted(indices)


def format_menu_header() -> str:
    return (
        f"{'#':>4}  {'ACT':<12}  {'KIND':<8}  {'CONF':>5}  {'TST':<3}  "
        f"{'QUALNAME':<40}  PATH"
    )


def format_menu_row(item: CherryItemDict) -> str:
    tst = "yes" if item["has_nearby_test"] else " no"
    conf = f"{item['confidence']:.0%}"
    qualname = item["qualname"][:38]
    path = f"{item['rel_path']}:{item['lineno']}"[:50]
    return (
        f"{item['index']:>4}  {item['action']:<12}  {item['kind']:<8}  "
        f"{conf:>5}  {tst:<3}  {qualname:<40}  {path}"
    )
