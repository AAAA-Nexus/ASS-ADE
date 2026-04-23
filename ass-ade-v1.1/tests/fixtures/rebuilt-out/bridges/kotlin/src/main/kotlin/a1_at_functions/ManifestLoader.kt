import java.nio.file.Files
import java.nio.file.Path

private fun extractString(payload: String, prefix: String): String =
    payload.substringAfter(prefix, missingDelimiterValue = "").substringAfter('"', "").substringBefore('"', "")

private fun extractBoolean(payload: String, prefix: String): Boolean =
    payload.substringAfter(prefix, missingDelimiterValue = "").trimStart().startsWith("true")

private fun extractStringArray(payload: String, prefix: String): List<String> {
    val segment = payload.substringAfter(prefix, missingDelimiterValue = "")
        .substringBefore(']', missingDelimiterValue = "")
    if (segment.isEmpty()) {
        return emptyList()
    }
    return segment.split('"').drop(1).filterIndexed { index, _ -> index % 2 == 0 }
}

fun findRepoRoot(start: Path, manifestRel: String = DEFAULT_MANIFEST_REL): Path {
    var current = start
    while (true) {
        if (Files.isRegularFile(current.resolve(manifestRel))) {
            return current
        }
        val parent = current.parent ?: error("Could not find $manifestRel from $start")
        current = parent
    }
}

fun loadManifestPayload(start: Path, manifestRel: String = DEFAULT_MANIFEST_REL): String {
    val repoRoot = findRepoRoot(start, manifestRel)
    return Files.readString(repoRoot.resolve(manifestRel))
}

fun loadBridgeManifest(start: Path): BridgeManifestSummary {
    val payload = loadManifestPayload(start)
    return BridgeManifestSummary(
        schema = extractString(payload, ""schema": "),
        bridgeReady = extractBoolean(payload, ""bridge_ready": "),
        bridgeLanguages = extractStringArray(payload, ""bridge_languages": ["),
        pythonBridgeCommand = extractStringArray(payload, ""python_bridge_command": ["),
    )
}
