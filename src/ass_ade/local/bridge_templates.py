"""Tier a1 — pure template strings for multi-language bridge scaffolding."""

from __future__ import annotations

SCHEMA_VERSION = "ASSADE-MULTILANG-BRIDGE-1"

# ---------------------------------------------------------------------------
# TypeScript bridge templates
# ---------------------------------------------------------------------------

TS_BRIDGE_CONTRACT = """\
export type BridgeManifest = {
  schema: string;
  bridge_ready: boolean;
  bridge_languages: string[];
  python_bridge_command: string[];
  supported_languages: string[];
};

export const DEFAULT_MANIFEST_REL = ".ass-ade/bridges/bridge_manifest.json";
"""

TS_MANIFEST_LOADER = """\
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";

import { DEFAULT_MANIFEST_REL, type BridgeManifest } from "../a0_qk_constants/bridge_contract.js";

function asStringArray(value: unknown): string[] {
  return Array.isArray(value) ? value.map((item) => String(item)) : [];
}

export function findRepoRoot(start: string = process.cwd(), manifestRel: string = DEFAULT_MANIFEST_REL): string {
  let current = start;
  for (;;) {
    const candidate = join(current, manifestRel);
    try {
      readFileSync(candidate, "utf-8");
      return current;
    } catch (error) {
      void error;
    }
    const parent = dirname(current);
    if (parent === current) {
      throw new Error(`Could not find ${manifestRel} from ${start}`);
    }
    current = parent;
  }
}

export function loadBridgeManifest(root: string = process.cwd(), manifestRel: string = DEFAULT_MANIFEST_REL): BridgeManifest {
  const repoRoot = findRepoRoot(root, manifestRel);
  const payload = JSON.parse(readFileSync(join(repoRoot, manifestRel), "utf-8")) as Record<string, unknown>;
  return {
    schema: String(payload.schema ?? ""),
    bridge_ready: Boolean(payload.bridge_ready),
    bridge_languages: asStringArray(payload.bridge_languages),
    python_bridge_command: asStringArray(payload.python_bridge_command),
    supported_languages: asStringArray(payload.supported_languages),
  };
}
"""

TS_PYTHON_BRIDGE_CLIENT = """\
import { spawnSync, type SpawnSyncReturns } from "node:child_process";

import type { BridgeManifest } from "../a0_qk_constants/bridge_contract.js";
import { findRepoRoot, loadBridgeManifest } from "../a1_at_functions/manifest_loader.js";

export class PythonBridgeClient {
  constructor(private readonly root: string = process.cwd()) {}

  manifest(): BridgeManifest {
    return loadBridgeManifest(this.root);
  }

  run(args: string[]): SpawnSyncReturns<string> {
    const manifest = this.manifest();
    if (manifest.python_bridge_command.length === 0) {
      throw new Error("Bridge command is not configured for this rebuild.");
    }
    const [cmd, ...baseArgs] = manifest.python_bridge_command;
    return spawnSync(cmd, [...baseArgs, ...args], {
      cwd: findRepoRoot(this.root),
      encoding: "utf-8",
    });
  }
}
"""

TS_BRIDGE_FEATURE = """\
import type { BridgeManifest } from "../a0_qk_constants/bridge_contract.js";
import { PythonBridgeClient } from "../a2_mo_composites/python_bridge_client.js";

export function describeBridge(root: string = process.cwd()): BridgeManifest {
  return new PythonBridgeClient(root).manifest();
}
"""

TS_BRIDGE_MAIN = """\
import type { SpawnSyncReturns } from "node:child_process";

import type { BridgeManifest } from "../a0_qk_constants/bridge_contract.js";
import { PythonBridgeClient } from "../a2_mo_composites/python_bridge_client.js";
import { describeBridge } from "../a3_og_features/bridge_feature.js";

export function loadBridgeSummary(root: string = process.cwd()): BridgeManifest {
  return describeBridge(root);
}

export function runAssAde(args: string[], root: string = process.cwd()): SpawnSyncReturns<string> {
  return new PythonBridgeClient(root).run(args);
}
"""

TS_INDEX = """\
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { loadBridgeSummary } from "./a4_sy_orchestration/bridge_main.js";

export { findRepoRoot, loadBridgeManifest } from "./a1_at_functions/manifest_loader.js";
export { runAssAde, loadBridgeSummary } from "./a4_sy_orchestration/bridge_main.js";

export function configuredBridgeCommand(root: string = process.cwd()): string[] {
    return [...loadBridgeSummary(root).python_bridge_command];
}

const here = dirname(fileURLToPath(import.meta.url));
if (process.argv[1] && process.argv[1] === fileURLToPath(import.meta.url)) {
    const manifest = loadBridgeSummary(here);
    process.stdout.write(JSON.stringify({
    schema: manifest.schema,
    bridgeReady: manifest.bridge_ready,
    bridgeLanguages: manifest.bridge_languages,
    }) + "\\n");
}
"""

TS_NODE_SHIMS = """\
declare module "node:fs" {
    export function readFileSync(path: string, encoding: string): string;
}

declare module "node:path" {
    export function dirname(path: string): string;
    export function join(...parts: string[]): string;
}

declare module "node:url" {
    export function fileURLToPath(url: unknown): string;
}

declare module "node:child_process" {
    export interface SpawnSyncReturns<T> {
        status: number | null;
        stdout: T;
        stderr: T;
        error?: Error;
    }

    export function spawnSync(
        command: string,
        args?: string[],
        options?: { cwd?: string; encoding?: string },
    ): SpawnSyncReturns<string>;
}

declare const process: {
    argv: string[];
    cwd(): string;
    stdout: { write(chunk: string): void };
};
"""

TS_TSCONFIG = """\
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "outDir": "dist"
  },
  "include": ["src/**/*"]
}
"""

def ts_package_json(project_name: str) -> str:
    slug = project_name.lower().replace(" ", "-").replace("_", "-")
    return f"""\
{{
  "name": "ass-ade-bridge-{slug}",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {{
    "build": "tsc -p tsconfig.json",
    "smoke": "node smoke.mjs"
  }},
  "devDependencies": {{
    "@types/node": "^20.16.0",
    "typescript": "^5.6.0"
  }}
}}
"""

TS_SMOKE_MJS = """\
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MANIFEST_REL = ".ass-ade/bridges/bridge_manifest.json";

function findRepoRoot(start = process.cwd()) {
  let current = start;
  for (;;) {
    const candidate = join(current, MANIFEST_REL);
    try {
      JSON.parse(readFileSync(candidate, "utf-8"));
      return current;
    } catch (error) {
      void error;
    }
    const parent = dirname(current);
    if (parent === current) {
      throw new Error(`Could not find ${MANIFEST_REL} from ${start}`);
    }
    current = parent;
  }
}

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = findRepoRoot(here);
const manifest = JSON.parse(readFileSync(join(repoRoot, MANIFEST_REL), "utf-8"));
process.stdout.write(JSON.stringify({
  schema: manifest.schema,
  bridgeReady: Boolean(manifest.bridge_ready),
  bridgeLanguages: manifest.bridge_languages,
  command: manifest.python_bridge_command,
}) + "\\n");
"""

# ---------------------------------------------------------------------------
# Shared sample / readme templates
# ---------------------------------------------------------------------------

BRIDGE_REQUEST_SAMPLE = """\
{
  "command": "recon",
  "args": [
    "."
  ],
  "cwd": ".",
  "expect_json": false
}
"""

BRIDGE_RESPONSE_SAMPLE = """\
{
  "schema": "ASSADE-MULTILANG-BRIDGE-1",
  "exit_code": 0,
  "stdout": "",
  "stderr": ""
}
"""

BRIDGES_README = """\
# ASS-ADE Multi-Language Bridges

This directory contains bridge scaffolding that lets non-Python code call
the ASS-ADE Python core via subprocess spawn.

## Usage (TypeScript)

```typescript
import { runAssAde } from "./typescript/src/index.js";

const result = runAssAde(["recon", "."]);
console.log(result.stdout);
```

## Bridge contract

The bridge reads `.ass-ade/bridges/bridge_manifest.json` at the repo root.
Set `python_bridge_command` to the command that runs ass-ade (e.g.
`["python", "-m", "ass_ade"]`) and set `bridge_ready` to `true`.

## Rebuild

Run `ass-ade bridge init [PATH]` to regenerate this scaffolding.
"""

def bridge_report_md(
    project_name: str,
    python_cmd: list[str],
    bridge_ready: bool,
    languages: list[str],
) -> str:
    cmd_str = " ".join(python_cmd) if python_cmd else "not configured"
    ready_str = "YES" if bridge_ready else "NO"
    lang_list = ", ".join(f"`{l}`" for l in ["python", "rust", "typescript", "kotlin", "swift", "atomadic"])
    target_list = ", ".join(f"`{l}`" for l in languages)
    rows = "\n".join(f"| `{l}` | `bridges/{l}` |" for l in languages)
    return f"""\
# Multi-language Bridges

Generated bridge scaffolding for `{project_name}`.

- Bridge mode: `spawn-cli`
- Bridge ready: {ready_str}
- Vendored ASS-ADE: NO
- Python bridge command: `{cmd_str}`
- Supported languages: {lang_list}
- Prepared bridge targets: {target_list}

## Wiring contract

- Manifest: `.ass-ade/bridges/bridge_manifest.json`
- Samples: `bridges/samples/bridge_request.sample.json`, `bridges/samples/bridge_response.sample.json`
- Generated tests: `tests/test_generated_multilang_bridges.py`

## Prepared bridge roots

| Language | Root |
|----------|------|
{rows}

## Notes

- These files are bridge-ready wiring artifacts with a minimal a0-a4 monadic scaffold for each bridge language.
- They read the rebuild bridge manifest and expose a stable process-spawn contract around the shipped Python surface.
- They do not synthesize domain-specific non-Python atom bodies yet.
- Use them as starting points for real TypeScript, Rust, Kotlin, and Swift adapters in downstream repos.
"""
