# Example 1: Local Quickstart

Get started with ASS-ADE in local mode — no remote API keys or online calls required.

## What You'll Do

1. Initialize a configuration file
2. Run the doctor command to inspect your environment
3. Set up a free LLM provider
4. Start an interactive agent chat
5. Generate a repo summary
6. Create an onboarding package

## Prerequisites

- Python 3.12+
- ASS-ADE installed: `pip install ass-ade`
- A free LLM provider API key (Groq, DeepSeek, or Cerebras)

## Step 1: Initialize Configuration

Create a local config file:

```bash
ass-ade init
```

This creates `~/.ass-ade/config.json` with default settings in local mode. Open it and verify the profile is set to `local`:

```json
{
  "profile": "local",
  "nexus_base_url": "https://atomadic.tech",
  "agent_id": "your-agent-id-here"
}
```

## Step 2: Run the Doctor

Inspect your environment:

```bash
ass-ade doctor
```

Expected output:

```
Python version:     3.12.1 ✓
ASS-ADE version:    1.0.0
Config path:        /home/user/.ass-ade/config.json
Profile:            local
Config valid:       ✓
Providers available:
  - groq             (no API key)
  - deepseek         (no API key)
  - cerebras         (no API key)
  - openai           (no API key)
  - ollama           (not running)
MCP server:         ready
Agent loop:         ready
```

## Step 3: Set Up a Free Provider

Choose a free LLM provider and obtain an API key:

**Option A: Groq (Recommended)**

1. Sign up at https://console.groq.com/keys
2. Create an API key
3. Set the environment variable:

```bash
export GROQ_API_KEY="your-key-here"
```

**Option B: DeepSeek**

1. Sign up at https://platform.deepseek.com/api_keys
2. Create an API key
3. Set the environment variable:

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

**Option C: Cerebras**

1. Sign up at https://www.cerebras.net/
2. Create an API key
3. Set the environment variable:

```bash
export CEREBRAS_API_KEY="your-key-here"
```

Verify the provider is available:

```bash
ass-ade doctor
```

Look for your provider in the output with a checkmark:

```
Providers available:
  - groq             (✓ API key found)
```

## Step 4: Interactive Agent Chat

Start a conversation with the agent:

```bash
ass-ade agent chat
```

Expected output (you get an interactive prompt):

```
Starting agent chat in local mode.
Provider: groq (model: mixtral-8x7b-32768)
Type 'exit' or 'quit' to end the conversation.
Type 'help' for available commands.

You: Explain what ASS-ADE does in 2 sentences
Assistant: ASS-ADE is a developer shell that transforms codebases
into tier-partitioned modular structures. It works locally first
but can optionally use remote contracts for trust, security, and
advanced workflows.

You: What is the rebuild engine?
Assistant: The rebuild engine reads any codebase and reorganizes it
into five composition tiers: qk_codex (constants), at_kernel (pure
functions), mo_engines (stateful compositions), og_swarm (feature
modules), and sy_manifold (top-level orchestration). This makes
large codebases easier to reason about.

You: exit
```

Try asking the agent questions about ASS-ADE, software architecture, or your own code.

## Step 5: Generate a Repo Summary

Get a structured summary of any repository:

```bash
ass-ade repo summary .
```

If you're in the ASS-ADE repo, expected output:

```json
{
  "path": ".",
  "stats": {
    "total_files": 128,
    "total_lines": 45230,
    "languages": {
      "python": 42510,
      "markdown": 2400,
      "json": 320
    }
  },
  "structure": {
    "src/ass_ade/": {
      "cli.py": 1420,
      "agent/": {
        "loop.py": 890,
        "gates.py": 560
      },
      "mcp/": {
        "server.py": 770,
        "utils.py": 340
      }
    },
    "docs/": {
      "user-guide.md": 450,
      "architecture.md": 680
    },
    "tests/": {
      "test_cli.py": 1230,
      "test_agent.py": 950
    }
  },
  "entry_points": [
    "src/ass_ade/cli.py::main",
    "src/ass_ade/agent/loop.py::run_agent_loop"
  ]
}
```

## Step 6: Create an Onboarding Package

Generate a comprehensive onboarding package for your repo:

```bash
ass-ade eco-scan .
```

Expected output:

```
Scanning repository structure...
Analyzing dependencies...
Extracting key concepts...
Identifying common tasks...

Onboarding package generated:
  - .atomadic/onboarding/2026-04-18T14-32-45Z/ONBOARDING.md (human-readable overview)
  - .atomadic/onboarding/2026-04-18T14-32-45Z/ONBOARDING.json (machine-readable payload)
  - .atomadic/onboarding/2026-04-18T14-32-45Z/QUICK_START.md (commands only)
```

Open the generated files to see:

- **ONBOARDING.md**: A human-friendly guide with architecture overview, key files, important concepts, and common tasks
- **ONBOARDING.json**: Structured data about the project for tool integration
- **QUICK_START.md**: Just the essential commands to get started

Example ONBOARDING.md content:

```markdown
# ASS-ADE Onboarding

## Project Overview

ASS-ADE is a developer shell that transforms codebases into
tier-partitioned structures using the rebuild engine.

## Architecture

- **src/ass_ade/cli.py**: Main CLI entry point with 50+ commands
- **src/ass_ade/agent/**: Agent loop, routing, and gating logic
- **src/ass_ade/mcp/**: MCP server and tool integration
- **src/ass_ade/nexus/**: Client for AAAA-Nexus remote contracts

## Key Concepts

- **Profile**: local, hybrid, or premium operating mode
- **Rebuild Engine**: Transforms code into 5-tier modular structure
- **Eco-scan**: Generates onboarding packages
- **Trust Gate**: Validates agent identity with remote contracts
- **Pipeline**: Composable workflows with multiple steps

## Common Tasks

### Generate a repo summary
\`\`\`bash
ass-ade repo summary .
\`\`\`

### Rebuild a codebase
\`\`\`bash
ass-ade rebuild /path/to/codebase
\`\`\`

### Run the agent loop
\`\`\`bash
ass-ade agent run "Summarize this project"
\`\`\`
```

## Verification

After completing all steps, verify everything works by running a full workflow:

```bash
# Generate a plan for your project
ass-ade plan "Document my repository"
```

Expected output:

```
Plan for: Document my repository

Tasks:
1. Read existing documentation files
2. Analyze code structure and entry points
3. Generate API documentation
4. Create a contributors guide
5. Set up automated docs building

Estimated complexity: medium
Estimated time: 3-4 hours
```

## Troubleshooting

### Agent chat hangs

Press Ctrl+C to interrupt. Check that your LLM provider has API quota remaining.

### Provider not detected

Make sure the API key environment variable is set:

```bash
echo $GROQ_API_KEY
```

If it's empty, set it again:

```bash
export GROQ_API_KEY="your-key-here"
```

### repo summary returns empty structure

This can happen if the directory is large or has many symlinks. Try:

```bash
ass-ade repo summary . --max-depth 2
```

### eco-scan is slow

On large repos (10k+ files), scanning can take a few minutes. This is normal. You can limit the scan:

```bash
ass-ade eco-scan . --max-files 1000
```

## Next Steps

Now that you're comfortable with local mode:

1. Read [../02-rebuild-a-codebase/README.md](../02-rebuild-a-codebase/README.md) to see the rebuild engine in action
2. Try hybrid mode by setting your profile to `hybrid` and obtaining an AAAA-Nexus API key
3. Explore the CLI reference: `ass-ade --help`
4. Integrate ASS-ADE into your CI/CD pipeline

## Resources

- [../docs/user-guide.md](../../docs/user-guide.md) — Full user guide
- [../README.md](../../README.md) — Feature overview
- `ass-ade --help` — CLI reference
- `ass-ade <command> --help` — Help for specific commands
