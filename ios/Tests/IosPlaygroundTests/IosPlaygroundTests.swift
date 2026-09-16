import XCTest
@testable import IosPlayground

final class IosPlaygroundTests: XCTestCase {
    func testSampleURL() {
        XCTAssertEqual(RoadmapNetworking.sampleURL().host, "jsonplaceholder.typicode.com")
    }
}
