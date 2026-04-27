# ATOMADIC_WORKSPACE path bindings

## Placeholder

In prompts, scripts, and examples, **`ATOMADIC_WORKSPACE`** means the directory that contains **both** `agents/` and the `ass-ade*` product folders.

Default checkout in Atomadic development: the folder named `!atomadic` on drive `C:` (i.e. the parent of `agents/`).

Resolve manually:

- `ATOMADIC_WORKSPACE/RULES.md`
- `ATOMADIC_WORKSPACE/agents/_PROTOCOL.md`
- `ATOMADIC_WORKSPACE/ass-ade/.ass-ade/genesis/events.schema.json` (canonical genesis schema today)
- `ATOMADIC_WORKSPACE/ass-ade/` — **default edit target** for `ass_ade` rebuild engine work (canonical: `src/ass_ade/` within ASS-ADE-SEED)

## Environment (optional)

Tools may define `ATOMADIC_WORKSPACE` explicitly when the repo is checked out elsewhere. If unset, humans/agents infer it as **the workspace root open in the IDE**.

## Second workspace (AAAA-Nexus / umbrella plans)

Use **`ATOMADIC_NEXUS_WORKSPACE`** in prose when a second checkout holds Nexus-driven `ato-plans` (replace with the actual path on your machine). It is **not** the same as `ATOMADIC_WORKSPACE`.

Examples (resolve locally — do not commit secrets):

- `ATOMADIC_NEXUS_WORKSPACE/.ato-plans/active/` — active umbrella plans when work is driven from the Nexus repo
- `ATOMADIC_WORKSPACE/.ato-plans/assclaw-v1/stream-reports/` — stream reports under the main Atomadic workspace

Legacy docs may mention `c:\!aaaa-nexus\` literally; treat that as an **example** of `ATOMADIC_NEXUS_WORKSPACE`.
