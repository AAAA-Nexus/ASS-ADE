import java.nio.file.Path

class PythonBridgeClient(private val start: Path) {
    fun manifest(): BridgeManifestSummary = loadBridgeManifest(start)

    fun manifestPayload(): String = loadManifestPayload(start)
}
