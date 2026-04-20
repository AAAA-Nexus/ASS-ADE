# User Guide

This guide is for someone using ASS-ADE as a public
open-source tool, not as an internal Atomadic engineer.

## What ASS-ADE Does

ASS-ADE is a Python-first developer shell with three modes:

- local: useful with no remote dependency
- hybrid: local shell plus public AAAA-Nexus contract calls
- premium: paid remote services through public contracts

The repo is intentionally strongest as a local tool first. Remote features are opt-in.

## Install

Create a virtual environment and install the package:

```bash
python -m venv .venv
. .venv/Scripts/activate
python -m pip install -e .[dev]
```

Check that the CLI is available:

```bash
ass-ade --help
```

## First Run

Create a config file:

```bash
ass-ade init
```

Inspect the current environment:

```bash
ass-ade doctor
```

By default, ASS-ADE stays in local mode and does not call AAAA-Nexus.

## Core Local Workflows

### Inspect a repo

```bash
ass-ade repo summary .
```

### Draft a plan

```bash
ass-ade plan "Document the public shell"
```

### Run the public-safe protocol cycle

```bash
ass-ade protocol run "Improve the public shell"
ass-ade cycle "Improve the public shell"
```

### Start the agent shell

```bash
ass-ade agent chat
ass-ade agent run "Summarize this repository"
```

### Run the local MCP server

```bash
ass-ade mcp serve
```

### Run the mock MCP server for local integration work

```bash
ass-ade mcp mock-server --port 8787
```

## A2A Workflows

Validate or compare public agent cards:

```bash
ass-ade a2a validate https://example.com
ass-ade a2a discover https://example.com
ass-ade a2a negotiate https://example.com
ass-ade a2a local-card
```

## MCP Workflows

When you are in a remote-enabled profile, you can inspect
or invoke public MCP manifests:

```bash
ass-ade mcp tools --allow-remote
ass-ade mcp inspect 1 --allow-remote
ass-ade mcp invoke 1 --dry-run --allow-remote
```

Use `--dry-run` first when you are exploring a new remote manifest.

## Configuration

The default config path is `.ass-ade/config.json` in the current workspace.

Key fields:

- `profile`: `local`, `hybrid`, or `premium`
- `nexus_base_url`: public AAAA-Nexus base URL
- `request_timeout_s`: request timeout
- `agent_id`: default local agent identity
- `agent_model`: default model selection hint

Environment overrides:

- `AAAA_NEXUS_API_KEY`
- `AAAA_NEXUS_BASE_URL`
- `ASS_ADE_PROVIDER_URL`
- `ASS_ADE_PROVIDER_KEY`
- `ASS_ADE_MODEL`
- `OPENAI_API_KEY`
- `OLLAMA_HOST`

## Current Limits

These are known product limits, not hidden behavior:

- agent conversation memory is per run, not durable across sessions
- coordination primitives exist, but there is not yet
  a first-class coordinator
- premium billing UX is still thin compared to the underlying contract surface
- editor-native packaging is not shipped yet

## Public-Safe Boundary

ASS-ADE consumes public contracts. It does not contain:

- private instruction bodies
- unpublished verification corpora
- backend orchestration internals
- hidden pricing or routing logic

If a workflow needs those things, this repo should call
a remote contract or degrade gracefully.

## Troubleshooting

### Remote command says it is disabled

You are probably in `local` profile. Either switch the
profile to `hybrid` or `premium`, or pass `--allow-remote`
when the command supports it.

### Agent command works but forgets prior work later

That is expected today. Durable agent memory is a known gap.

### MCP or workflow command needs an API key

Set `AAAA_NEXUS_API_KEY` in your environment or `.env`
file at the workspace root.

### Wallet address does not render

The x402 wallet status command can show the wallet
address when `eth-account` is installed. If it is not
installed, the command still works but only shows
configuration status.
