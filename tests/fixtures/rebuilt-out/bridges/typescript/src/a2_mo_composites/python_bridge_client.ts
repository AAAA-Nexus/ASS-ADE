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
