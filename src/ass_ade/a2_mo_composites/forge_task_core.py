"""Tier a2 — assimilated class 'ForgeTask'

Assimilated from: rebuild/forge.py:225-237
"""

from __future__ import annotations


# --- assimilated symbol ---
class ForgeTask:
    """A single focused improvement task — one LLM call."""

    task_id: str
    file: str          # relative to target_root
    abs_path: str      # absolute path for file writes
    node: str          # function/class name
    node_type: str     # "function" | "class" | "module"
    start_line: int    # 1-indexed, inclusive
    end_line: int      # 1-indexed, inclusive
    code: str          # current source of the node
    issue: str         # "missing_docstring" | "todo_comment" | "debug_hardcoded" | "missing_404"
    instruction: str   # human-readable fix instruction for the LLM

