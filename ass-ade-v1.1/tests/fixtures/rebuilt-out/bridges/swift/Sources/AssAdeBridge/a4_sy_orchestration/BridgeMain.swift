import Foundation

func bridgeSummary() throws -> BridgeManifestSummary {
    try describeBridge()
}

func runBridge() throws -> String {
    let start = URL(fileURLWithPath: FileManager.default.currentDirectoryPath, isDirectory: true)
    return try PythonBridgeClient(start: start).manifestPayload()
}
