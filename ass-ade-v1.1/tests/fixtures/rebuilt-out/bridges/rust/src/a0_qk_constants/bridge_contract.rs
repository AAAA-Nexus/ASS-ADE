#[derive(Debug, Clone)]
pub struct BridgeManifestSummary {
    pub schema: String,
    pub bridge_ready: bool,
    pub bridge_languages: Vec<String>,
    pub python_bridge_command: Vec<String>,
}

pub const DEFAULT_MANIFEST_REL: &str = ".ass-ade/bridges/bridge_manifest.json";
