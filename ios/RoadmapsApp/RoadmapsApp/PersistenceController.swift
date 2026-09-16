import CoreData

@objc(Note)
final class Note: NSManagedObject {
    @NSManaged var body: String?
    @NSManaged var createdAt: Date?
}

struct PersistenceController {
    static let shared = PersistenceController()
    let container: NSPersistentContainer

    init(inMemory: Bool = false) {
        let entity = NSEntityDescription()
        entity.name = "Note"
        entity.managedObjectClassName = "Note"
        let body = NSAttributeDescription()
        body.name = "body"
        body.attributeType = .stringAttributeType
        let createdAt = NSAttributeDescription()
        createdAt.name = "createdAt"
        createdAt.attributeType = .dateAttributeType
        entity.properties = [body, createdAt]
        let model = NSManagedObjectModel()
        model.entities = [entity]

        container = NSPersistentContainer(name: "Roadmaps", managedObjectModel: model)
        if inMemory {
            container.persistentStoreDescriptions.first?.url = URL(fileURLWithPath: "/dev/null")
        }
        container.loadPersistentStores { _, error in
            if let error {
                fatalError("Core Data: \(error)")
            }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
    }
}
