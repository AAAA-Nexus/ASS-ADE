# Skill Definitions

This directory contains skill definition files for ASS-ADE. A skill is a structured
Markdown document that teaches an agent (or a human) how to use a specific
`ass-ade` command correctly.

## What a skill definition is

A skill definition covers:

- **When to use this skill** — the decision trigger
- **Step-by-step instructions** — ordered, actionable steps
- **Flags and options** — a reference table of common options
- **Output interpretation** — how to read the command's output
- **Error handling** — what to do when the command fails

Skills are consumed by agent system prompts via an include/reference mechanism, or
read directly by a human who wants to understand a command before running it.

## How to load a skill

Within an agent definition, reference a skill in the system prompt body:

```
{{include: skills/rebuild.skill.md}}
```

Or load at runtime when invoking the agent:

```
ass-ade agent run --agent code-rebuilder --skill skills/rebuild.skill.md
```

## Available skills

| File | Command | Purpose |
|------|---------|---------|
| `rebuild.skill.md` | `ass-ade rebuild` | Restructure a codebase into tier partitions |
| `design.skill.md` | `ass-ade design` | Generate a blueprint before rebuilding |
| `docs.skill.md` | `ass-ade docs` | Generate documentation from source |
| `enhance.skill.md` | `ass-ade enhance` | Find and apply ranked improvements |
| `lint.skill.md` | `ass-ade lint` | Run language-appropriate linters |
| `certify.skill.md` | `ass-ade certify` | Produce and verify tamper-evident certificates |
| `prompt-governance.skill.md` | `ass-ade prompt` | Validate prompt, agent, hook, tool, and skill artifact changes |

## Adding a new skill

1. Create `<command-name>.skill.md` in this directory.
2. Follow the section structure: When to use / Steps / Flags / Output / Errors.
3. Keep instructions concrete and command-level. Avoid abstract advice.
