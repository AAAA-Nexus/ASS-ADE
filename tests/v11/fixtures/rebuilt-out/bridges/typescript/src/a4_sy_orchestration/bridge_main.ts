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
