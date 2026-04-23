use std::path::PathBuf;

use crate::a0_qk_constants::bridge_contract::BridgeManifestSummary;
use crate::a2_mo_composites::python_bridge_client::PythonBridgeClient;

pub fn describe_bridge(start: PathBuf) -> Result<BridgeManifestSummary, String> {
    PythonBridgeClient::new(start)?.manifest()
}
