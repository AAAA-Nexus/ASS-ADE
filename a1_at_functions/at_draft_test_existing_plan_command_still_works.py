# Extracted from C:/!ass-ade/tests/test_new_commands.py:428
# Component id: at.source.ass_ade.test_existing_plan_command_still_works
from __future__ import annotations

__version__ = "0.1.0"

def test_existing_plan_command_still_works() -> None:
    result = runner.invoke(app, ["plan", "Improve the system"])
    assert result.exit_code == 0
