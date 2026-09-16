import Foundation
#if canImport(Alamofire)
import Alamofire
#endif

public struct RemoteTodo: Decodable, Sendable {
    public let id: Int
    public let title: String
}

public enum RoadmapNetworking {
    public static func sampleURL() -> URL {
        URL(string: "https://jsonplaceholder.typicode.com/todos/1")!
    }

    public static func fetchTodo() async throws -> RemoteTodo {
        let (data, _) = try await URLSession.shared.data(from: sampleURL())
        return try JSONDecoder().decode(RemoteTodo.self, from: data)
    }
}
