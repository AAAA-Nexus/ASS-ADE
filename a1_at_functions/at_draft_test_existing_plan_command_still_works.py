# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_existing_plan_command_still_works.py:7
# Component id: at.source.a1_at_functions.test_existing_plan_command_still_works
from __future__ import annotations

__version__ = "0.1.0"

def test_existing_plan_command_still_works() -> None:
    result = runner.invoke(app, ["plan", "Improve the system"])
    assert result.exit_code == 0
