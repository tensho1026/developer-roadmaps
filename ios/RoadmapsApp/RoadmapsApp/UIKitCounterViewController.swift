import SwiftUI
import UIKit

final class UIKitCounterViewController: UIViewController {
    private var count = 0
    private let label = UILabel()

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
        label.translatesAutoresizingMaskIntoConstraints = false
        label.font = .preferredFont(forTextStyle: .title1)
        let button = UIButton(type: .system)
        button.setTitle("Increment", for: .normal)
        button.addTarget(self, action: #selector(bump), for: .touchUpInside)
        button.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(label)
        view.addSubview(button)
        NSLayoutConstraint.activate([
            label.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            label.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            button.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            button.topAnchor.constraint(equalTo: label.bottomAnchor, constant: 16),
        ])
        render()
    }

    @objc private func bump() {
        count += 1
        render()
    }

    private func render() {
        label.text = "UIKit count: \(count)"
    }
}

struct UIKitCounterView: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> UIKitCounterViewController {
        UIKitCounterViewController()
    }

    func updateUIViewController(_ uiViewController: UIKitCounterViewController, context: Context) {}
}
