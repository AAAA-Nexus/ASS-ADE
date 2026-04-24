# Tests

Comprehensive test suite (501 tests passing, latest verified run).

## Coverage

- CLI: test_cli.py, test_new_commands.py
- Nexus: test_nexus_client.py, test_resilience.py
- Agent: test_agent.py, test_gates.py, test_routing.py
- MCP: test_mcp.py, test_mcp_server_streaming.py, test_mcp_extended.py
- Tools: test_tools_builtin.py
- Other: config, engine, errors, history, pipeline, plan, protocol, repo, session, tokens, validation, workflows, a2a.

## Run

```bash
pytest
pytest tests/test_cli.py -v
```

All passing per `docs/audit-report.md`.
