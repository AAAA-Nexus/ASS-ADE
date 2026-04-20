# Dev Stack

## Stack Decision

ASS-ADE remains Python-first. AAAA-Nexus storefront and edge systems remain Rust-first. Editor-native integrations should use TypeScript when needed.

That split still fits the codebase and the product boundary.

## Current Public Stack

### Core Language

- Python 3.12+

### Core Libraries

- `typer` for the CLI surface
- `rich` for terminal UX
- `pydantic` for config, request, and response models
- `httpx` for typed API clients and resilient transports
- `jsonschema` for schema validation in MCP paths

### Tooling

- `pytest` for the test suite
- `ruff` for linting and formatting
- `pyright` for static type checking

Verified status on 2026-04-16:

- 501 passing tests
- Python virtual environment in active use for the repo

## Why Python Still Fits Best

Python is the right public-shell language here because it supports:

- a large CLI surface with low ceremony
- typed contract clients without excessive boilerplate
- local file and shell automation
- agent loop and workflow experimentation
- fast integration work around MCP, A2A, and OpenAPI contracts

It also aligns with the existing local ecosystem around ASS-ADE.

## Why Rust Still Matters

Rust remains the right place for:

- storefront and edge handlers
- payment and security-sensitive infrastructure
- Cloudflare Worker deployment
- backend-side performance and systems concerns

The public repo should consume those surfaces, not absorb them.

## Why TypeScript Is Still Secondary But Important

TypeScript is not the center of the public shell today, but it is the likely choice for:

- a VS Code extension
- webview UI for workflow history and cost display
- editor-native MCP registration flows

## Why Go Is Still Not A Priority

Go would add maintenance surface without helping the current public-shell roadmap.

It may become relevant later for a narrow coordination daemon or service, but that is not justified by the current codebase.

## Current Architectural Libraries By Concern

### CLI and UX

- `typer`
- `rich`

### Typed Contracts and Validation

- `pydantic`
- `jsonschema`

### Networking and Resilience

- `httpx`
- custom `RetryTransport`
- custom `CircuitBreakerTransport`

### Agent and Workflow Runtime

- in-process Python orchestration
- token-budget accounting in `engine/tokens.py`
- workflow persistence through the local filesystem

## MCP Strategy

ASS-ADE is both an MCP consumer and an MCP server.

Current priorities:

1. consume remote MCP manifests and tools from public contracts
2. expose local ASS-ADE tools and workflows over MCP stdio
3. support local integration testing through the mock MCP server

The repo should not embed private internal MCP logic from non-public systems.

## A2A Strategy

ASS-ADE now supports public A2A validation, discovery, and negotiation flows, but still needs a stronger coordination layer on top of them.

That means the next work is not basic A2A support. It is durable agent memory and practical multi-agent orchestration.

## Recommended VS Code Tooling

- `ms-python.python`
- `ms-python.vscode-pylance`
- `charliermarsh.ruff`
- `rust-lang.rust-analyzer`
- `tamasfe.even-better-toml`
- `redhat.vscode-yaml`

Optional for storefront-side work:

- `cloudflare.cloudflare-workers-bindings-extension`

## Packaging Direction

Current release target:

- Python package with CLI entrypoint

Likely next packaging target:

- VS Code extension that sits on top of the existing MCP server and local CLI
