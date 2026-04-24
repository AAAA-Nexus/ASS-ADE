import java.nio.file.Path
import java.nio.file.Paths

fun describeBridge(start: Path = Paths.get("").toAbsolutePath()): BridgeManifestSummary =
    PythonBridgeClient(start).manifest()
