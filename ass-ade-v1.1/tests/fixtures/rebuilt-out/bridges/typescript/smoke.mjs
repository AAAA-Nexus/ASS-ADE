import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";

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

const repoRoot = findRepoRoot();
const manifest = JSON.parse(readFileSync(join(repoRoot, MANIFEST_REL), "utf-8"));
process.stdout.write(JSON.stringify({
  schema: manifest.schema,
  bridgeReady: Boolean(manifest.bridge_ready),
  bridgeLanguages: manifest.bridge_languages,
  command: manifest.python_bridge_command,
}) + "\n");
