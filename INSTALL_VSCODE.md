# ASS-ADE — VS Code Integration Guide

## Prerequisites

- Python 3.12+
- VS Code with the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  and [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) extensions

## 1. Install ASS-ADE

```bash
# From PyPI (when published)
pip install ass-ade

# Or from source (development)
git clone https://github.com/atomadic-tech/ass-ade
cd ass-ade
python -m pip install -e ".[dev]"
```

## 2. Open the repo in VS Code

```bash
code .
```

VS Code will prompt you to install recommended extensions — accept.
The workspace ships with `.vscode/extensions.json` recommending:

- `ms-python.python` — Python language support
- `ms-python.vscode-pylance` — type checking and IntelliSense
- `charliermarsh.ruff` — fast Python linter / formatter
- `ms-python.debugpy` — debugger
- `tamasfe.even-better-toml` — pyproject.toml support
- `anthropic.claude-code` — Claude Code IDE extension (for MCP integration)

## 3. Select the virtual environment

Press `Ctrl+Shift+P` → **Python: Select Interpreter** → choose `.venv`.

If you used `pip install -e ".[dev]"`, the venv is wherever pip placed it.
The workspace `settings.json` defaults to `.venv/Scripts/python.exe`.

## 4. Run tasks from VS Code

Press `Ctrl+Shift+B` (or `Terminal > Run Task`) to run any built-in task:

| Task label | What it does |
|------------|--------------|
| `ass-ade: doctor` | Environment diagnostics |
| `ass-ade: recon` | Parallel codebase reconnaissance |
| `ass-ade: eco-scan` | Monadic compliance scan |
| `ass-ade: lint` | Ruff lint check |
| `ass-ade: certify` | Generate a SHA-256 certificate |
| `ass-ade: rebuild` | Rebuild into 5-tier structure |
| `ass-ade: run tests` | Full pytest suite (default test task) |
| `ass-ade: agent chat` | Interactive agentic shell |
| `ass-ade: mcp serve` | Start the MCP server (background) |

Run the **default test task** with `Ctrl+Shift+T` (or F5 after selecting it).

## 5. Integrate with Claude Code (MCP)

If you have the [Claude Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)
VS Code extension:

1. Copy `mcp.json.example` to `.mcp.json` in your project root.
2. Edit the `env` block to point at your install:

```json
{
  "mcpServers": {
    "ass-ade": {
      "command": "python",
      "args": ["-m", "ass_ade", "mcp", "serve"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/ass-ade/src",
        "ASS_ADE_CONFIG": "/absolute/path/to/ass-ade/.ass-ade/config.json"
      }
    }
  }
}
```

3. Reload VS Code. Claude Code will discover the MCP server and expose all
   ASS-ADE tools — `recon`, `rebuild`, `eco_scan`, `lint`, `certify`,
   `design`, `doctor`, and the full IDE/workflow tool set.

Copy `CLAUDE.md.example` to `CLAUDE.md` in your project root so Claude knows
what each tool does.

## 6. Terminal usage

All ASS-ADE commands are available from the integrated terminal:

```bash
ass-ade doctor
ass-ade recon . --out RECON_REPORT.md
ass-ade eco-scan . --out ECO_SCAN_REPORT.md
ass-ade lint .
ass-ade certify .
ass-ade design "add streaming response support" --path . --local-only
ass-ade rebuild . --yes
```

The workspace `terminal.integrated.env` block automatically sets `PYTHONPATH`
and `ASS_ADE_CONFIG` so the CLI finds your config without extra setup.

## 7. Debugging

Six launch configurations are included in `.vscode/launch.json`:

- **ass-ade: doctor** — run diagnostics with the debugger attached
- **ass-ade: agent chat** — debug the interactive agent shell
- **ass-ade: mcp serve (debug)** — step through MCP server request handling
- **ass-ade: workflow phase0-recon** — debug the recon workflow
- **pytest: all tests** — run the full test suite under the debugger
- **pytest: engine integration** — run engine-specific tests

Press `F5` with one selected to start.
