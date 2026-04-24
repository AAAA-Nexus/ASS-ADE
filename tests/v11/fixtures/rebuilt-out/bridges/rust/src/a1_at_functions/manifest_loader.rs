use std::fs;
use std::path::PathBuf;

use crate::a0_qk_constants::bridge_contract::{BridgeManifestSummary, DEFAULT_MANIFEST_REL};

fn extract_string(payload: &str, prefix: &str) -> String {
    payload
        .split(prefix)
        .nth(1)
        .and_then(|rest| rest.split('"').nth(1))
        .unwrap_or_default()
        .to_string()
}

fn extract_bool(payload: &str, prefix: &str) -> bool {
    payload
        .split(prefix)
        .nth(1)
        .map(|rest| rest.trim_start().starts_with("true"))
        .unwrap_or(false)
}

fn extract_string_array(payload: &str, prefix: &str) -> Vec<String> {
    let Some(rest) = payload.split(prefix).nth(1) else {
        return Vec::new();
    };
    let Some(segment) = rest.split(']').next() else {
        return Vec::new();
    };
    segment
        .split('"')
        .skip(1)
        .step_by(2)
        .map(str::to_string)
        .collect()
}

pub fn find_repo_root(start: PathBuf) -> Result<PathBuf, String> {
    let mut current = start;
    loop {
        let candidate = current.join(DEFAULT_MANIFEST_REL);
        if candidate.is_file() {
            return Ok(current);
        }
        let Some(parent) = current.parent() else {
            return Err(format!("could not find {}", DEFAULT_MANIFEST_REL));
        };
        current = parent.to_path_buf();
    }
}

pub fn load_manifest_payload(start: PathBuf) -> Result<String, String> {
    let repo_root = find_repo_root(start)?;
    let manifest_path = repo_root.join(".ass-ade/bridges/bridge_manifest.json");
    fs::read_to_string(manifest_path).map_err(|err| err.to_string())
}

pub fn load_manifest(start: PathBuf) -> Result<BridgeManifestSummary, String> {
    let payload = load_manifest_payload(start)?;
    Ok(BridgeManifestSummary {
        schema: extract_string(&payload, "\"schema\": "),
        bridge_ready: extract_bool(&payload, "\"bridge_ready\": "),
        bridge_languages: extract_string_array(&payload, "\"bridge_languages\": ["),
        python_bridge_command: extract_string_array(&payload, "\"python_bridge_command\": ["),
    })
}
