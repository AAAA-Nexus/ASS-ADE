# Codex + Copilot build cycle (VS Code) on ASS-ADE

Use this on the **same repo** you materialized with `ass-ade ade materialize` (so **`.ade/`** and the CLI exist).

## 0) One-time in VS Code

1. **Extensions** (recommendations may be merged by `ade materialize` into `.vscode/extensions.json`): Python, Pylance, **GitHub Copilot**, and the **OpenAI Codex** extension (install from the Marketplace; names change — search “OpenAI Codex”).
2. **MCP (optional, recommended for Atomadic):** copy `cross-ide/vscode-mcp.example.json` into **`.vscode/mcp.json`**, add your servers (e.g. Playwright, AAAA-Nexus, Microsoft Learn). [Docs](https://code.visualstudio.com/docs/copilot/customization/mcp-servers).
3. **Agent mode & model:** open Chat (Copilot) → set mode to **Agent**; in the model picker, choose a **higher-reasoning** model (e.g. **Codex** / flagship) for multi-step work; use **Plan** (built-in) for a structured pass before big edits.
4. **Custom instructions (optional):** add a [Copilot instruction](https://docs.github.com/copilot) file, e.g. point at repo **AGENTS.md** and **ASS_ADE_SHIP_PLAN.md** (see `copilot-instructions.SAMPLE.md` in this folder for a template).

## 1) The cycle (each slice of work)

| Step | Do this | Outcome |
|------|---------|--------|
| **Recon** | In Chat, attach or `@`-reference `AGENTS.md`, `ASS_ADE_SHIP_PLAN.md` (or Phase N), and `.ade/README.md`. Ask: “Map current HAVE/GAP and next exit criterion.” | Shaped context before edits. |
| **Plan** | Use the **Plan** built-in (or a planning prompt) to break work into 3–7 steps. | A checklist you and the agent can follow. |
| **Implement (Codex or Copilot Agent)** | With **Agent** mode, ask for the first step only; require tool approval for shell/file ops until you trust the loop. | Diffs in editor; use multi-file awareness. |
| **Verify (terminal)** | **Integrated Terminal:** `ass-ade doctor` · `ass-ade ade doctor` · `python .ade/persistent/run_swarm_services.py once` (if materialized) · `pytest` / CI-equivalent. | Meets “terrain” not vibes. |
| **Mark plan** | Update ship docs or your `tasks` state (`swarm task mark …` on the monorepo host if using swarm automation). | Traceable progress. |
| **Rinse** | Next plan step. | Until exit criteria. |

## 2) When to use Cursor on the same tree

- Use **Cursor** for **swarm signal injection** (P0–P3) and hook-driven scribe lines between tool calls.
- Use **VS Code (Codex/Copilot)** for **heavier reasoning** sessions and **MCP** tools you have wired there.
- The **same git repo**; switch IDEs, don’t duplicate branches. Commit scribe and signals like any other artifact (per team policy).

## 3) Gotchas

- **Hooks are not portable:** VS Code will **not** run `~/.cursor/hooks.json` from Cursor; it uses the **VS Code** Copilot hooks and MCP. That’s why `.ade` documents both.
- **No fake MCP tool names** — use real tools from your config; see `agents/NEXUS_SWARM_MCP.md` on the monorepo.

---

*ADE layout v2+ — `CODEX-BUILD-CYCLE` ships under `.ade/cross-ide/` via `ass-ade ade materialize`.*
