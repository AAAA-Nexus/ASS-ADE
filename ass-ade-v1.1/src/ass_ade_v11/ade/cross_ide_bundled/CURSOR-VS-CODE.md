# Cursor, VS Code (Copilot + Codex), and `.ade/`

| Surface | What `.ade` gives you | How automation attaches |
|--------|------------------------|----------------------------|
| **Cursor** | Swarm **hooks** under `.cursor/hooks/` (signal bus, scribe, ADE gate) | Cursor `hooks.json` — runs Python on `sessionStart` / `postToolUse` (see [Cursor Hooks](https://cursor.com/docs/hooks)) |
| **VS Code + GitHub Copilot** | Agent mode, **MCP**, same repo + `.ade` docs | **No** `hooks.json` from Cursor. Use [Copilot customization / MCP](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) and [Copilot hooks](https://code.visualstudio.com/docs/copilot/customization/hooks) (VS Code’s own system). |
| **VS Code + OpenAI Codex** (extension) | Same repo; use **model picker** and optional **MCP** | Auth via the Codex / ChatGPT flow. Tooling: terminal + `ass-ade-unified` like Copilot. |

**Single repo, many IDEs:** Clone once. Materialize with `ass-ade-unified ade materialize` (from an `ass-ade` install) so every machine gets **`.ade/`** with the same operator layout.

**Invariants (MAP = TERRAIN):**

- **Release gates** = `ass-ade-unified book` / `assimilate` / CI — not a specific editor.
- **Swarm scribe** (`SCRIBE-*.md`) and **signal** files (`.ato-plans/assclaw-v1/signals/`) are on disk: any IDE can `python .ade/persistent/run_swarm_services.py status` in the **integrated terminal**; only Cursor’s hooks **inject** unread signals into the agent loop automatically.

**VS Code** users: add MCP from `cross-ide/vscode-mcp.example.json`, enable **Agent** mode, and (optionally) follow `CODEX-BUILD-CYCLE.md` for a disciplined loop with Codex and/or Copilot.
