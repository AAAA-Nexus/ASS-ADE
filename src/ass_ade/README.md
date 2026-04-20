# ASS-ADE Package

Core library for ASS-ADE CLI and local/hybrid workflows.

## Submodules

| Submodule | Purpose | Key Files |
| --------- | ------- | --------- |
| a2a/ | A2A validation/discovery/negotiate/local-card. | __init__.py |
| agent/ | Agent loop/context/conversation/gates/routing. | loop.py, context.py |
| engine/ | LLM providers/router/tokens/types. | provider.py, router.py |
| local/ | Local planner/repo ops. | planner.py, repo.py |
| mcp/ | MCP server/client (14 tools). | server.py, mock_server.py |
| nexus/ | Resilient AAAA-Nexus client (~120 methods). | client.py, resilience.py |
| protocol/ | Cycle protocol. | cycle.py |
| tools/ | Builtin/history/plan/registry. | builtin.py, registry.py |
| cli.py | Typer CLI (95+ cmds/30 sub-apps). | |
| config.py | Config loading. | |
| pipeline.py | Pipelines. | |
| system.py | System utils. | |
| workflows.py | Hero workflows (trust-gate, certify, safe-execute). | |

## Usage

```bash
pip install -e .
ass-ade --help
```

Import: `from ass_ade.nexus import NexusClient`

See root [README.md](../../README.md).
