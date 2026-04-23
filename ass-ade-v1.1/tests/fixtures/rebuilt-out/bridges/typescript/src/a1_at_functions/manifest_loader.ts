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
