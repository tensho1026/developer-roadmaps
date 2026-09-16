// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "IosPlayground",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    products: [
        .library(name: "IosPlayground", targets: ["IosPlayground"])
    ],
    dependencies: [
        .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.10.0")
    ],
    targets: [
        .target(
            name: "IosPlayground",
            dependencies: ["Alamofire"]
        ),
        .testTarget(
            name: "IosPlaygroundTests",
            dependencies: ["IosPlayground"]
        )
    ]
)
