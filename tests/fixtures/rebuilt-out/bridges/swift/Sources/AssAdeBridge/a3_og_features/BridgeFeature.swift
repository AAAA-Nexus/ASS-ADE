import Foundation

func describeBridge(start: URL = URL(fileURLWithPath: FileManager.default.currentDirectoryPath, isDirectory: true)) throws -> BridgeManifestSummary {
    try PythonBridgeClient(start: start).manifest()
}
