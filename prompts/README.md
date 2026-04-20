# Prompt Packs

Prompt packs are premium system prompts designed to teach any LLM how to execute specialized tasks in the ass-ade ecosystem. Each pack is production-quality, verified, and comes with examples and checklists.

## What is a Prompt Pack?

A prompt pack is a structured markdown file with:

- YAML frontmatter (title, version, spec reference, pricing)
- A preamble explaining the pack's purpose and usage
- A complete, LLM-ready system prompt (copy-paste ready)
- Realistic examples demonstrating the prompt in action
- A verification checklist for quality assurance
- Usage instructions (how to integrate with ass-ade tools)
- Licensing and support information

## Current Packs

### Blueprint Architect ($58)

Teaches any LLM to write perfect AAAA-SPEC-004 blueprint files for the ass-ade ecosystem. Blueprints describe features and systems to build, feeding into `ass-ade rebuild` which materializes components.

Learn the 5-tier composition law, component decomposition, ID naming conventions, interface design, and common mistakes to avoid. Includes a realistic rate-limiting API middleware example.

**Usage:**

```bash
# 1. Copy the system prompt from blueprint-architect.md
# 2. Paste it into your LLM's system context
# 3. Use ass-ade design to create a blueprint
ass-ade design "Add rate limiting middleware"

# 4. Validate the output
ass-ade rebuild <blueprint.json> --validate

# 5. Certify the design
ass-ade certify <blueprint.json>
```

## Licensing

All prompt packs are licensed for single-team use. Updates are included for 12 months from purchase. Commercial redistribution is prohibited without prior written consent from Atomadic.

## Support

For questions about prompt packs or custom designs, contact the Atomadic team at contact@atomadic.tech.
