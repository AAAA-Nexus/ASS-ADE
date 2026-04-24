use std::env;

use crate::a0_qk_constants::bridge_contract::BridgeManifestSummary;
use crate::a2_mo_composites::python_bridge_client::PythonBridgeClient;
use crate::a3_og_features::bridge_feature::describe_bridge;

pub fn load_bridge_summary() -> Result<BridgeManifestSummary, String> {
    describe_bridge(env::current_dir().map_err(|err| err.to_string())?)
}

pub fn run() -> Result<(), Box<dyn std::error::Error>> {
    let client = PythonBridgeClient::new(env::current_dir()?).map_err(std::io::Error::other)?;
    let payload = client.manifest_payload().map_err(std::io::Error::other)?;
    println!("{}", payload);
    Ok(())
}
