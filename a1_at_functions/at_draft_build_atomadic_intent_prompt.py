# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:370
# Component id: at.source.ass_ade.build_atomadic_intent_prompt
from __future__ import annotations

__version__ = "0.1.0"

def build_atomadic_intent_prompt(
    working_dir: str | Path = ".",
    *,
    memory_context: str | None = None,
) -> str:
    """Build the live LLM intent-classifier prompt with current capabilities.

    Loads agents/atomadic_interpreter.md dynamically so changes to the agent
    definition are picked up without code modifications. Also incorporates
    any ONBOARDING.md or RECON_REPORT.md found in working_dir.
    """
    wdir = Path(working_dir).resolve()
    repo_root = _find_repo_root(wdir)

    agent_definition = _load_agent_md(repo_root)
    context_files = _load_project_context_files(wdir)
    capability_section = render_capability_prompt_section(
        working_dir,
        max_cli=240,
        max_tools=30,
        max_mcp=40,
        max_agents=20,
    )

    identity_block = agent_definition if agent_definition else (
        "You are Atomadic, the intelligent front door of ASS-ADE (Autonomous Sovereign\n"
        "System: Atomadic Development Environment), a CLI for analyzing, rebuilding,\n"
        "documenting, certifying, and evolving codebases."
    )

    extra_sections: list[str] = []
    if memory_context:
        extra_sections.append(f"## User Context\n{memory_context}")
    if context_files:
        extra_sections.append(f"## Project Onboarding Context\n{context_files}")
    extra_block = "\n\n".join(extra_sections)

    return f"""\
{identity_block}

{extra_block + chr(10) + chr(10) if extra_block else ""}\
Classify the user's message and respond with ONLY a single valid JSON object.
Do not use markdown fences. Do not add prose outside the JSON object.

Core front-door intents:
- rebuild
- design
- docs
- lint
- certify
- enhance
- eco-scan
- recon
- doctor
- self-enhance
- help
- chat

If the message maps to a core front-door intent:
  {{"type":"command","intent":"<core intent>","path":"<input path or null>","output_path":"<output path or null, only for rebuild>","feature_desc":"<desc or null>"}}

If the message maps to another known ASS-ADE CLI command from the dynamic
inventory, dispatch it exactly through cli_args:
  {{"type":"command","intent":"cli","cli_args":["protocol","evolution-record"],"path":null,"output_path":null,"feature_desc":null}}

If the user asks what commands are available, what you can do, or says "help":
  {{"type":"command","intent":"help","path":null,"output_path":null,"feature_desc":null}}

If the message is general conversation:
  {{"type":"chat","response":"<short conversational reply>"}}

Prefer exact CLI command paths from the inventory. Do not invent command names.
For file paths, preserve user-provided [datetime] or {{datetime}} tokens exactly.

{capability_section}
"""
