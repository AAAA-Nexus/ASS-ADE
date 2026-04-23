import Foundation

private func extractString(payload: String, prefix: String) -> String {
    guard let range = payload.range(of: prefix) else {
        return ""
    }
    let rest = payload[range.upperBound...]
    guard let firstQuote = rest.firstIndex(of: """) else {
        return ""
    }
    let afterFirst = rest[rest.index(after: firstQuote)...]
    guard let secondQuote = afterFirst.firstIndex(of: """) else {
        return ""
    }
    return String(afterFirst[..<secondQuote])
}

private func extractBool(payload: String, prefix: String) -> Bool {
    guard let range = payload.range(of: prefix) else {
        return false
    }
    return payload[range.upperBound...].trimmingCharacters(in: .whitespacesAndNewlines).hasPrefix("true")
}

private func extractStringArray(payload: String, prefix: String) -> [String] {
    guard let range = payload.range(of: prefix) else {
        return []
    }
    let rest = payload[range.upperBound...]
    guard let closing = rest.firstIndex(of: "]") else {
        return []
    }
    let segment = rest[..<closing]
    return segment.split(separator: """).enumerated().compactMap { index, item in
        index.isMultiple(of: 2) ? nil : String(item)
    }
}

func findRepoRoot(start: URL, manifestRel: String = defaultManifestRel) throws -> URL {
    var current = start
    while true {
        let candidate = current.appendingPathComponent(manifestRel)
        if FileManager.default.fileExists(atPath: candidate.path) {
            return current
        }
        let parent = current.deletingLastPathComponent()
        if parent.path == current.path {
            throw NSError(domain: "AssAdeBridge", code: 1, userInfo: [NSLocalizedDescriptionKey: "Could not find \(manifestRel)"])
        }
        current = parent
    }
}

func loadManifestPayload(start: URL, manifestRel: String = defaultManifestRel) throws -> String {
    let repoRoot = try findRepoRoot(start: start, manifestRel: manifestRel)
    return try String(contentsOf: repoRoot.appendingPathComponent(manifestRel), encoding: .utf8)
}

func loadBridgeManifest(start: URL) throws -> BridgeManifestSummary {
    let payload = try loadManifestPayload(start: start)
    return BridgeManifestSummary(
        schema: extractString(payload: payload, prefix: ""schema": "),
        bridgeReady: extractBool(payload: payload, prefix: ""bridge_ready": "),
        bridgeLanguages: extractStringArray(payload: payload, prefix: ""bridge_languages": ["),
        pythonBridgeCommand: extractStringArray(payload: payload, prefix: ""python_bridge_command": [")
    )
}
