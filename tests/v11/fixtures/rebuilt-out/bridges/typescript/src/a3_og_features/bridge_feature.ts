import type { BridgeManifest } from "../a0_qk_constants/bridge_contract.js";
import { PythonBridgeClient } from "../a2_mo_composites/python_bridge_client.js";

export function describeBridge(root: string = process.cwd()): BridgeManifest {
  return new PythonBridgeClient(root).manifest();
}
