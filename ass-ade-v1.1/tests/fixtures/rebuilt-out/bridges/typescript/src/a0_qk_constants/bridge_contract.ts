export type BridgeManifest = {
  schema: string;
  bridge_ready: boolean;
  bridge_languages: string[];
  python_bridge_command: string[];
  supported_languages: string[];
};

export const DEFAULT_MANIFEST_REL = ".ass-ade/bridges/bridge_manifest.json";
