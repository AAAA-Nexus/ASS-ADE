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
    }) + "\n");
}
