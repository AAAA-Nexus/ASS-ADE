import Foundation

let defaultManifestRel = ".ass-ade/bridges/bridge_manifest.json"

struct BridgeManifestSummary {
    let schema: String
    let bridgeReady: Bool
    let bridgeLanguages: [String]
    let pythonBridgeCommand: [String]
}
