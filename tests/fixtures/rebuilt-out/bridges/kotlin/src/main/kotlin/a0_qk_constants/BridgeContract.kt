const val DEFAULT_MANIFEST_REL = ".ass-ade/bridges/bridge_manifest.json"

data class BridgeManifestSummary(
    val schema: String,
    val bridgeReady: Boolean,
    val bridgeLanguages: List<String>,
    val pythonBridgeCommand: List<String>,
)
