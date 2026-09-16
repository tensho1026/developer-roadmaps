import Foundation

public enum RoadmapPersistence {
    public static func savePreviewName(_ name: String) {
        UserDefaults.standard.set(name, forKey: "previewName")
    }

    public static func previewName() -> String? {
        UserDefaults.standard.string(forKey: "previewName")
    }
}
