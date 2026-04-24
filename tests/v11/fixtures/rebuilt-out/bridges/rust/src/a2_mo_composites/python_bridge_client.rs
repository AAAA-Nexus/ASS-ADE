use std::path::PathBuf;

use crate::a0_qk_constants::bridge_contract::BridgeManifestSummary;
use crate::a1_at_functions::manifest_loader::{find_repo_root, load_manifest, load_manifest_payload};

pub struct PythonBridgeClient {
    repo_root: PathBuf,
}

impl PythonBridgeClient {
    pub fn new(start: PathBuf) -> Result<Self, String> {
        Ok(Self {
            repo_root: find_repo_root(start)?,
        })
    }

    pub fn manifest(&self) -> Result<BridgeManifestSummary, String> {
        load_manifest(self.repo_root.clone())
    }

    pub fn manifest_payload(&self) -> Result<String, String> {
        load_manifest_payload(self.repo_root.clone())
    }
}
