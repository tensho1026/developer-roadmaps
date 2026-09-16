import SwiftUI

public struct CounterView: View {
    @State private var count = 0

    public init() {}

    public var body: some View {
        VStack(spacing: 16) {
            Text("iOS playground")
                .font(.title)
            Text("count: \(count)")
            Button("Increment") { count += 1 }
        }
        .padding()
    }
}
