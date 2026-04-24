"""
Edge-case battery for Interpreter().process().

Run with:  python -m pytest tests/test_interpreter_edge_cases.py -v --no-header
"""
from __future__ import annotations
import textwrap
import pytest
from pathlib import Path
from unittest.mock import patch


# Disable LLM calls so tests are deterministic (falls back to keyword heuristic)
@pytest.fixture(autouse=True)
def no_llm(monkeypatch):
    monkeypatch.setattr("ass_ade.interpreter._call_llm", lambda *a, **kw: None)


@pytest.fixture()
def interp(tmp_path):
    from ass_ade.interpreter import Interpreter
    return Interpreter(working_dir=tmp_path)


# ─── helpers ──────────────────────────────────────────────────────────────────

def proc(interp, text):
    """Call process and return result, never raising."""
    return interp.process(text)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Empty string → empty string (documented sentinel)
# ══════════════════════════════════════════════════════════════════════════════
def test_empty_string(interp):
    result = proc(interp, "")
    assert result == "", f"Expected '' got {result!r}"


# ══════════════════════════════════════════════════════════════════════════════
# 2. Whitespace-only → empty (strip collapses it)
# ══════════════════════════════════════════════════════════════════════════════
def test_whitespace_only(interp):
    result = proc(interp, "   \t\n  ")
    assert result == "", f"Expected '' got {result!r}"


# ══════════════════════════════════════════════════════════════════════════════
# 3. Ambiguous "make it faster" → returns a non-empty string (doesn't crash)
# ══════════════════════════════════════════════════════════════════════════════
def test_ambiguous_make_it_faster(interp):
    result = proc(interp, "make it faster")
    assert isinstance(result, str) and len(result) > 0


# ══════════════════════════════════════════════════════════════════════════════
# 4. Casual greeting "yo what up" → non-empty (chat or fallback)
# ══════════════════════════════════════════════════════════════════════════════
def test_casual_greeting(interp):
    result = proc(interp, "yo what up")
    assert isinstance(result, str) and len(result) > 0


# ══════════════════════════════════════════════════════════════════════════════
# 5. "rebuild" with no path, no history → asks for clarification
# ══════════════════════════════════════════════════════════════════════════════
def test_rebuild_no_path_asks_clarification(interp):
    result = proc(interp, "rebuild")
    # Must ask for more info rather than run blindly
    assert isinstance(result, str) and len(result) > 0
    # State should be set for follow-up
    assert interp._pending_clarification == "path"


# ══════════════════════════════════════════════════════════════════════════════
# 6. Follow-up path after clarification request
#    Must give a path DIFFERENT from working_dir, otherwise the clarification
#    guard at line 791 re-fires (path==working_dir AND history still empty).
# ══════════════════════════════════════════════════════════════════════════════
def test_rebuild_clarification_resolved(interp, tmp_path):
    proc(interp, "rebuild")               # sets _pending_clarification
    assert interp._pending_clarification == "path"
    target = str(tmp_path / "subdir")     # distinct from working_dir
    result = proc(interp, target)         # provide path answer
    assert isinstance(result, str) and len(result) > 0
    assert interp._pending_clarification is None


# ══════════════════════════════════════════════════════════════════════════════
# 7. "what's my name?" → non-empty (memory or chat)
# ══════════════════════════════════════════════════════════════════════════════
def test_whats_my_name(interp):
    result = proc(interp, "what's my name?")
    assert isinstance(result, str) and len(result) > 0


# ══════════════════════════════════════════════════════════════════════════════
# 8. "design" bare keyword (no args) → non-empty
#    bare "design" misses the pre-LLM _design_triggers interceptor (which
#    requires "design a ", "design an ", etc.) but the keyword heuristic
#    classifier maps it to intent="design", so the approval gate IS set.
# ══════════════════════════════════════════════════════════════════════════════
def test_design_bare_keyword(interp):
    result = proc(interp, "design")
    assert isinstance(result, str) and len(result) > 0
    # keyword classifier routes bare "design" → design intent → gate set
    assert interp._pending_design_approval is True


# ══════════════════════════════════════════════════════════════════════════════
# 9. "design a login flow" → triggers design intent, sets approval gate
# ══════════════════════════════════════════════════════════════════════════════
def test_design_with_feature(interp):
    result = proc(interp, "design a login flow")
    assert isinstance(result, str) and len(result) > 0
    assert interp._pending_design_approval is True
    assert "login" in interp._pending_design_feature.lower()


# ══════════════════════════════════════════════════════════════════════════════
# 10. Design → approve ("yes") → approval consumed, add-feature dispatched
# ══════════════════════════════════════════════════════════════════════════════
def test_design_then_approve(interp):
    proc(interp, "design a login flow")
    assert interp._pending_design_approval is True
    result = proc(interp, "yes")
    assert isinstance(result, str) and len(result) > 0
    assert interp._pending_design_approval is False


# ══════════════════════════════════════════════════════════════════════════════
# 11. Design → reject ("no") → approval cleared, polite decline
# ══════════════════════════════════════════════════════════════════════════════
def test_design_then_reject(interp):
    proc(interp, "design a login flow")
    assert interp._pending_design_approval is True
    result = proc(interp, "no")
    assert isinstance(result, str) and len(result) > 0
    assert interp._pending_design_approval is False


# ══════════════════════════════════════════════════════════════════════════════
# 12. Invalid / nonexistent path → doesn't raise, returns string
# ══════════════════════════════════════════════════════════════════════════════
def test_invalid_path(interp):
    result = proc(interp, "lint /totally/nonexistent/path/xyz")
    assert isinstance(result, str)


# ══════════════════════════════════════════════════════════════════════════════
# 13. Numeric-only input "42" (not a startup suggestion) → non-empty
# ══════════════════════════════════════════════════════════════════════════════
def test_numeric_input(interp):
    result = proc(interp, "42")
    assert isinstance(result, str) and len(result) > 0


# ══════════════════════════════════════════════════════════════════════════════
# 14. Single digit "1" with no startup suggestions → falls through normally
# ══════════════════════════════════════════════════════════════════════════════
def test_digit_no_suggestions(interp):
    assert interp._startup_suggestions == []
    result = proc(interp, "1")
    assert isinstance(result, str) and len(result) > 0


# ══════════════════════════════════════════════════════════════════════════════
# 15. Single digit "2" WITH startup suggestions → consumes suggestion
# ══════════════════════════════════════════════════════════════════════════════
def test_digit_with_suggestions(interp):
    interp._startup_suggestions = ["Fix import errors", "Add tests"]
    result = proc(interp, "2")
    # suggestions consumed after use
    assert interp._startup_suggestions == []
    assert isinstance(result, str) and len(result) > 0


# ══════════════════════════════════════════════════════════════════════════════
# 16. Memory / identity save: "my name is Alice"
# ══════════════════════════════════════════════════════════════════════════════
def test_memory_save(interp):
    result = proc(interp, "my name is Alice")
    assert isinstance(result, str) and len(result) > 0


# ══════════════════════════════════════════════════════════════════════════════
# 17. Help query "what can you do?" → help intent
# ══════════════════════════════════════════════════════════════════════════════
def test_help_query(interp):
    result = proc(interp, "what can you do?")
    assert isinstance(result, str) and len(result) > 0


# ══════════════════════════════════════════════════════════════════════════════
# 18. Special chars / injection attempt → no crash, returns string
# ══════════════════════════════════════════════════════════════════════════════
def test_special_chars(interp):
    result = proc(interp, "'; DROP TABLE users; --")
    assert isinstance(result, str)


# ══════════════════════════════════════════════════════════════════════════════
# 19. Unicode / emoji input → no crash
# ══════════════════════════════════════════════════════════════════════════════
def test_unicode_emoji(interp):
    result = proc(interp, "lint 🚀 ./src ← pls")
    assert isinstance(result, str)


# ══════════════════════════════════════════════════════════════════════════════
# 20. Very long input (1 000 chars) → no crash
# ══════════════════════════════════════════════════════════════════════════════
def test_very_long_input(interp):
    long_input = "lint " + ("a" * 995)
    result = proc(interp, long_input)
    assert isinstance(result, str)
