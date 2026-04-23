import java.nio.file.Paths

fun bridgeSummary(): BridgeManifestSummary = describeBridge(Paths.get("").toAbsolutePath())

fun runBridge(): String = PythonBridgeClient(Paths.get("").toAbsolutePath()).manifestPayload()
