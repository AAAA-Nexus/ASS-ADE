import Foundation

final class PythonBridgeClient {
    private let start: URL

    init(start: URL) {
        self.start = start
    }

    func manifest() throws -> BridgeManifestSummary {
        try loadBridgeManifest(start: start)
    }

    func manifestPayload() throws -> String {
        try loadManifestPayload(start: start)
    }
}
