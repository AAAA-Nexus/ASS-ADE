# Agent Definitions

This directory contains agent definition files for ASS-ADE. Each `.agent.md` file
describes a specialized agent that can be run via the `ass-ade agent` sub-commands or
loaded by any MCP-compatible host that supports the ASS-ADE stdio server.

## What an agent definition is

An agent definition is a Markdown file with YAML frontmatter that describes:

- **Identity** (`name`, `version`, `description`) — displayed in `ass-ade agent list`
- **Capabilities** — tags used for agent-discovery routing
- **Tools** — the built-in or Nexus tools the agent is allowed to call
- **System prompt body** — the instructions passed as the system message when the agent
  is invoked

Agent definitions are read-only at runtime. They cannot modify themselves or other
agent definitions.

## How to run an agent

```
# Interactive chat with a named agent
ass-ade agent chat --agent blueprint-architect

# One-shot task (non-interactive)
ass-ade agent run --agent linter --task "Lint the project at /path/to/repo"

# List all available agents
ass-ade agent list
```

The `--agent` flag accepts the `name` field from the frontmatter or the bare filename
without `.agent.md`.

## Available agents

| File | Name | Purpose |
|------|------|---------|
| `atomadic_interpreter.md` | Atomadic Interpreter | Conversational front door — receives any input, derives intent, dispatches commands |
| `blueprint-architect.agent.md` | Blueprint Architect | Generates AAAA-SPEC-004 blueprint JSON from natural language |
| `code-rebuilder.agent.md` | Code Rebuilder | Drives `ass-ade rebuild` workflows end-to-end |
| `doc-generator.agent.md` | Doc Generator | Runs `ass-ade docs` and interprets generated documentation |
| `enhancement-advisor.agent.md` | Enhancement Advisor | Uses `ass-ade enhance` to find and apply ranked improvements |
| `linter.agent.md` | Linter | Runs `ass-ade lint`, interprets findings, suggests fixes |
| `certifier.agent.md` | Certifier | Runs `ass-ade certify`, reads certificates, verifies signatures |
| `prompt-governor.agent.md` | Prompt Governor | Governs prompt, agent, hook, tool, and skill artifacts with validation and drift control |

## Adding a new agent

1. Create a file named `<role>.agent.md` in this directory.
2. Add YAML frontmatter with at minimum: `name`, `version`, `description`,
   `capabilities`, `tools`.
3. Write the system prompt in the Markdown body below the frontmatter.
4. Run `ass-ade agent list` to confirm it appears.

## IP boundary

Agent definitions are part of the public surface of this repository. Do not include
internal UEP pillar numbers, internal Codex symbol names, or internal Lean proof
identifiers in agent definitions. Public Nexus endpoint names (`nexus_*`) and the
monadic tier names (`qk`, `at`, `mo`, `og`, `sy`) are permitted.
