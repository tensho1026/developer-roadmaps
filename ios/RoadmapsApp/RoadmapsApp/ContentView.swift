import Combine
import CoreData
import SwiftUI

struct ContentView: View {
    @Environment(\.managedObjectContext) private var context
    @FetchRequest(sortDescriptors: [NSSortDescriptor(keyPath: \Note.createdAt, ascending: false)])
    private var notes: FetchedResults<Note>
    @StateObject private var ticker = CombineTicker()
    @State private var draft = ""

    var body: some View {
        NavigationStack {
            List {
                Section("SwiftUI + Combine") {
                    Text("ticks: \(ticker.ticks)")
                    NavigationLink("UIKit counter") {
                        UIKitCounterView()
                    }
                }
                Section("Core Data notes") {
                    TextField("memo", text: $draft)
                    Button("save") { addNote() }
                    ForEach(notes, id: \.objectID) { note in
                        Text(note.body ?? "")
                    }
                    .onDelete(perform: delete)
                }
            }
            .navigationTitle("iOS playground")
        }
    }

    private func addNote() {
        let note = Note(context: context)
        note.body = draft
        note.createdAt = Date()
        draft = ""
        try? context.save()
    }

    private func delete(at offsets: IndexSet) {
        offsets.map { notes[$0] }.forEach(context.delete)
        try? context.save()
    }
}

final class CombineTicker: ObservableObject {
    @Published var ticks = 0
    private var bag = Set<AnyCancellable>()

    init() {
        Timer.publish(every: 1, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] _ in self?.ticks += 1 }
            .store(in: &bag)
    }
}
