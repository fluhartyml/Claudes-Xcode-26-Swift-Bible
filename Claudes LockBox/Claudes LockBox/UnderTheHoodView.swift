//
//  UnderTheHoodView.swift
//  Claudes LockBox
//
//  Created by Michael Fluharty on 4/16/26.
//

import SwiftUI

struct UnderTheHoodView: View {
    @State private var selectedFile: SourceFile?

    var body: some View {
        NavigationStack {
            List(SourceFile.allFiles) { file in
                Button {
                    selectedFile = file
                } label: {
                    HStack {
                        Image(systemName: "doc.text.fill")
                            .foregroundStyle(.blue)
                        VStack(alignment: .leading, spacing: 2) {
                            Text(file.name)
                                .font(.system(size: 18, weight: .semibold))
                                .foregroundStyle(.primary)
                            Text(file.description)
                                .font(.system(size: 14))
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("Under the Hood")
            .sheet(item: $selectedFile) { file in
                SourceCodeView(file: file)
            }
        }
    }
}

struct SourceCodeView: View {
    let file: SourceFile
    @Environment(\.dismiss) private var dismiss
    @State private var copied = false

    var body: some View {
        NavigationStack {
            ScrollView([.horizontal, .vertical]) {
                Text(file.source)
                    .font(.system(size: 14, design: .monospaced))
                    .padding()
            }
            .navigationTitle(file.name)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Done") { dismiss() }
                        .font(.system(size: 18))
                }
                ToolbarItem(placement: .primaryAction) {
                    Button {
                        #if os(iOS)
                        UIPasteboard.general.string = file.source
                        #elseif os(macOS)
                        NSPasteboard.general.clearContents()
                        NSPasteboard.general.setString(file.source, forType: .string)
                        #endif
                        copied = true
                        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                            copied = false
                        }
                    } label: {
                        Image(systemName: copied ? "checkmark" : "doc.on.doc")
                            .font(.system(size: 18))
                    }
                }
            }
        }
    }
}

struct SourceFile: Identifiable {
    let id = UUID()
    let name: String
    let description: String
    let source: String

    static let allFiles: [SourceFile] = [
        SourceFile(
            name: "Claudes_LockBoxApp.swift",
            description: "App entry point, ModelContainer setup",
            source: """
            import SwiftUI
            import SwiftData

            @main
            struct Claudes_LockBoxApp: App {
                var sharedModelContainer: ModelContainer = {
                    let schema = Schema([
                        Folder.self,
                        VaultItem.self,
                    ])
                    let modelConfiguration = ModelConfiguration(
                        schema: schema,
                        isStoredInMemoryOnly: false
                    )
                    do {
                        return try ModelContainer(for: schema, configurations: [modelConfiguration])
                    } catch {
                        fatalError("Could not create ModelContainer: \\(error)")
                    }
                }()

                var body: some Scene {
                    WindowGroup {
                        LockScreenView()
                    }
                    .modelContainer(sharedModelContainer)
                }
            }
            """
        ),
        SourceFile(
            name: "LockScreenView.swift",
            description: "Face ID / passcode authentication gate",
            source: """
            import SwiftUI
            import LocalAuthentication

            struct LockScreenView: View {
                @State private var isUnlocked = false
                @State private var authError: String?
                @Environment(\\.scenePhase) private var scenePhase

                var body: some View {
                    if isUnlocked {
                        ContentView()
                            .onChange(of: scenePhase) { _, newPhase in
                                if newPhase == .background {
                                    isUnlocked = false
                                }
                            }
                    } else {
                        // Lock screen with Face ID button
                        // Authenticates with biometrics or device passcode
                        // Auto-locks when app enters background
                    }
                }
            }
            """
        ),
        SourceFile(
            name: "Folder.swift",
            description: "SwiftData model for vault folders",
            source: """
            import Foundation
            import SwiftData

            @Model
            final class Folder {
                var name: String
                var iconName: String
                var dateCreated: Date
                var sortOrder: Int

                @Relationship(deleteRule: .cascade, inverse: \\VaultItem.folder)
                var items: [VaultItem] = []

                init(name: String, iconName: String = "folder.fill", sortOrder: Int = 0) {
                    self.name = name
                    self.iconName = iconName
                    self.dateCreated = Date()
                    self.sortOrder = sortOrder
                }
            }
            """
        ),
        SourceFile(
            name: "VaultItem.swift",
            description: "SwiftData model for vault entries",
            source: """
            import Foundation
            import SwiftData

            @Model
            final class VaultItem {
                var title: String
                var notes: String
                var pin: String
                var dateCreated: Date
                var dateModified: Date

                @Attribute(.externalStorage)
                var imageData: [Data] = []

                var folder: Folder?

                init(title: String, notes: String = "", pin: String = "",
                     folder: Folder? = nil) {
                    self.title = title
                    self.notes = notes
                    self.pin = pin
                    self.dateCreated = Date()
                    self.dateModified = Date()
                    self.folder = folder
                }
            }
            """
        ),
        SourceFile(
            name: "ContentView.swift",
            description: "Three-column NavigationSplitView layout",
            source: """
            import SwiftUI
            import SwiftData

            struct ContentView: View {
                @Environment(\\.modelContext) private var modelContext
                @Query(sort: \\Folder.sortOrder) private var folders: [Folder]
                @State private var selectedFolder: Folder?
                @State private var selectedItem: VaultItem?
                @State private var columnVisibility: NavigationSplitViewVisibility = .all

                var body: some View {
                    NavigationSplitView(columnVisibility: $columnVisibility) {
                        SidebarView(folders: folders, ...)
                    } content: {
                        ItemListView(folder: selectedFolder, ...)
                    } detail: {
                        ItemDetailView(item: selectedItem)
                    }
                    .searchable(text: $searchText, prompt: "Search vault")
                }
            }
            """
        ),
        SourceFile(
            name: "ItemDetailView.swift",
            description: "Vault item detail with PIN copy, photos, share",
            source: """
            import SwiftUI
            import PhotosUI

            struct ItemDetailView: View {
                @Bindable var item: VaultItem

                var body: some View {
                    ScrollView {
                        VStack(alignment: .leading, spacing: 20) {
                            TextField("Title", text: $item.title)
                            photosSection      // Thumbnails + Library/Camera/Scan
                            pinDisplaySection   // PIN with 30s auto-clear clipboard copy
                            pinEditorSection    // Editable PIN field
                            notesSection        // TextEditor for notes
                        }
                    }
                }

                // PIN copied to clipboard, auto-clears after 30 seconds
                private func copyPINToClipboard() {
                    UIPasteboard.general.string = item.pin
                    DispatchQueue.main.asyncAfter(deadline: .now() + 30) {
                        if UIPasteboard.general.string == item.pin {
                            UIPasteboard.general.string = ""
                        }
                    }
                }
            }
            """
        ),
        SourceFile(
            name: "DocumentScannerView.swift",
            description: "VisionKit document scanner bridge",
            source: """
            import SwiftUI
            import VisionKit

            struct DocumentScannerView: UIViewControllerRepresentable {
                var onScan: ([Data]) -> Void

                func makeUIViewController(context: Context) -> VNDocumentCameraViewController {
                    let scanner = VNDocumentCameraViewController()
                    scanner.delegate = context.coordinator
                    return scanner
                }

                // Coordinator handles didFinishWith scan:
                // Extracts each page as JPEG data
                // Calls onScan with array of page images
            }
            """
        ),
        SourceFile(
            name: "CameraCaptureView.swift",
            description: "Camera capture bridge for card photos",
            source: """
            import SwiftUI
            import UIKit

            struct CameraCaptureView: UIViewControllerRepresentable {
                var onCapture: (Data) -> Void

                func makeUIViewController(context: Context) -> UIImagePickerController {
                    let picker = UIImagePickerController()
                    picker.sourceType = .camera
                    picker.delegate = context.coordinator
                    return picker
                }

                // Coordinator handles didFinishPickingMediaWith:
                // Converts UIImage to JPEG data
                // Calls onCapture
            }
            """
        ),
        SourceFile(
            name: "ImageViewerView.swift",
            description: "Full-screen image viewer with pinch-to-zoom and share",
            source: """
            import SwiftUI

            struct ImageViewerView: View {
                let imageData: Data
                @State private var scale: CGFloat = 1.0
                @State private var offset: CGSize = .zero

                var body: some View {
                    NavigationStack {
                        Image(uiImage: UIImage(data: imageData)!)
                            .resizable()
                            .scaledToFit()
                            .scaleEffect(scale)
                            .offset(offset)
                            .gesture(MagnificationGesture()...)
                            .simultaneousGesture(DragGesture()...)
                            .onTapGesture(count: 2) { /* toggle zoom */ }
                    }
                    // Share button in toolbar opens UIActivityViewController
                }
            }
            """
        ),
        SourceFile(
            name: "ShareSheetView.swift",
            description: "UIActivityViewController bridge for sharing",
            source: """
            import SwiftUI
            import UIKit

            struct ShareSheetView: UIViewControllerRepresentable {
                let item: VaultItem

                func makeUIViewController(context: Context) -> UIActivityViewController {
                    var shareItems: [Any] = []
                    // Builds text summary: title + PIN + notes
                    // Attaches images
                    return UIActivityViewController(
                        activityItems: shareItems,
                        applicationActivities: nil
                    )
                }
            }
            """
        ),
    ]
}
