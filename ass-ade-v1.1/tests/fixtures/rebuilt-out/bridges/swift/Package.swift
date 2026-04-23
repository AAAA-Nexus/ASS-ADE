// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "AssAdeBridge",
    products: [
        .executable(name: "ass-ade-bridge", targets: ["AssAdeBridge"]),
    ],
    targets: [
        .executableTarget(name: "AssAdeBridge"),
    ]
)
