# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_parse_command_specs.py:7
# Component id: at.source.a1_at_functions.parse_command_specs
from __future__ import annotations

__version__ = "0.1.0"

def parse_command_specs(items: Iterable[str]) -> list[EvolutionCommand]:
    commands: list[EvolutionCommand] = []
    for item in items:
        text = item.strip()
        if not text:
            continue
        status = "recorded"
        notes = ""
        command = text
        if "::" in text:
            prefix, command = text.split("::", 1)
            for part in prefix.split(","):
                if "=" not in part:
                    continue
                key, value = part.split("=", 1)
                if key.strip() == "status":
                    status = value.strip() or status
                elif key.strip() == "notes":
                    notes = value.strip()
        commands.append(EvolutionCommand(command=command.strip(), status=status, notes=notes))
    return commands
