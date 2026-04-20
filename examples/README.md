# ASS-ADE Examples

This directory contains practical examples of ASS-ADE workflows in local, hybrid, and premium modes. Each example is a step-by-step guide with exact commands and expected output.

## Quick Overview

| Example | Mode | What It Shows |
|---------|------|---------------|
| [01-local-quickstart](#01-local-quickstart) | Local | Initialize config, run doctor, set up provider, chat with agent, repo summary, eco-scan |
| [02-rebuild-a-codebase](#02-rebuild-a-codebase) | Local | Rebuild engine, tier-partitioned structure, gap plan, certificate validation |
| [03-hybrid-workflows](#03-hybrid-workflows) | Hybrid | Trust gates, certify workflows, safe execution, pipeline composition |

## 01-local-quickstart

A complete introduction to ASS-ADE in local mode. No remote calls required.

**What you'll learn:**
- Initialize a config file
- Run the doctor command to inspect your environment
- Set up a free LLM provider (Groq, DeepSeek, or Cerebras)
- Start an interactive agent chat
- Generate a repo summary
- Create an onboarding package with eco-scan

**Time to complete:** 10-15 minutes

See [01-local-quickstart/README.md](01-local-quickstart/README.md)

## 02-rebuild-a-codebase

The rebuild engine transforms any codebase into a modular, tier-partitioned structure. This example walks through the entire rebuild workflow.

**What you'll learn:**
- What the rebuild engine does and why it's useful
- The five composition tiers: qk_codex, at_kernel, mo_engines, og_swarm, sy_manifold
- How to read a rebuild report
- How to interpret the gap plan
- How to validate an existing rebuild folder

**Time to complete:** 15-20 minutes

See [02-rebuild-a-codebase/README.md](02-rebuild-a-codebase/README.md)

## 03-hybrid-workflows

Hybrid workflows combine local processing with AAAA-Nexus remote contracts for trust, security, and certification.

**What you'll learn:**
- Configure hybrid mode
- Run trust-gate to verify agent identity
- Use the certify workflow to attest to output
- Safe-execute patterns for untrusted code
- Compose multi-step workflows using the pipeline engine
- Interpret JSON certificates and attestations

**Time to complete:** 20 minutes

See [03-hybrid-workflows/README.md](03-hybrid-workflows/README.md)

## Before You Start

Read these first for context:

- [../docs/user-guide.md](../docs/user-guide.md) — Core concepts and local workflows
- [../docs/remote-hybrid-guide.md](../docs/remote-hybrid-guide.md) — When to use hybrid mode, cost expectations
- [../README.md](../README.md) — Feature overview and CLI reference

## Configuration

All examples use the sample `ass-ade.config.json` in this directory. To use an example:

```bash
cd examples/01-local-quickstart
ass-ade --config ../ass-ade.config.json doctor
```

Or copy the config to your current working directory:

```bash
cp examples/ass-ade.config.json ~/.ass-ade/config.json
```

## Troubleshooting

### "command not found: ass-ade"

Make sure you've installed the package:

```bash
pip install ass-ade
```

Or use the development install from the repo root:

```bash
python -m pip install -e .
```

### "ModuleNotFoundError: No module named 'ass_ade'"

Use the development install:

```bash
cd /path/to/ass-ade
python -m pip install -e .
```

### "Profile is local but --allow-remote was not set"

Some commands require explicit opt-in to remote features. Use the `--allow-remote` flag or set your profile to `hybrid` in the config file.

### "Request timed out"

Check your network connection and the AAAA-Nexus service status:

```bash
ass-ade nexus health --allow-remote
```

## Next Steps

After completing the examples:

1. Try creating your own config file tailored to your environment
2. Explore the CLI reference: `ass-ade --help` and `ass-ade <command> --help`
3. Integrate ASS-ADE into your CI/CD pipeline
4. Set up the local MCP server and connect it to your IDE

See [../docs/](../docs/) for detailed architecture, protocol, and implementation guides.
