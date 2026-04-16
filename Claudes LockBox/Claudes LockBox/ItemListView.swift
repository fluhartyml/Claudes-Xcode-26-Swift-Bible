//
//  ItemListView.swift
//  Claudes LockBox
//
//  Created by Michael Fluharty on 4/16/26.
//

import SwiftUI
import SwiftData

struct ItemListView: View {
    let folder: Folder
    @Binding var selectedItem: VaultItem?
    @Binding var searchText: String
    @Environment(\.modelContext) private var modelContext
    @State private var showAddItem = false
    @State private var showScanner = false
    @State private var scannedPages: [Data] = []

    var filteredItems: [VaultItem] {
        let items = folder.items.sorted { $0.dateModified > $1.dateModified }
        if searchText.isEmpty {
            return items
        }
        return items.filter {
            $0.title.localizedCaseInsensitiveContains(searchText) ||
            $0.notes.localizedCaseInsensitiveContains(searchText)
        }
    }

    /// Cards folder opens scanner first, others open the form directly
    var isCardFolder: Bool {
        folder.name == "Cards"
    }

    var body: some View {
        List(selection: $selectedItem) {
            ForEach(filteredItems) { item in
                itemRow(item)
                    .tag(item)
            }
            .onDelete(perform: deleteItems)
        }
        .navigationTitle(folder.name)
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button {
                    if isCardFolder {
                        showScanner = true
                    } else {
                        showAddItem = true
                    }
                } label: {
                    Label("Add Item", systemImage: "plus")
                }
            }
        }
        .sheet(isPresented: $showAddItem) {
            AddItemView(folder: folder, initialImages: $scannedPages)
                .onDisappear {
                    scannedPages = []
                }
        }
        #if os(iOS)
        .sheet(isPresented: $showScanner, onDismiss: {
            // Open the form after the scanner sheet fully closes
            if !scannedPages.isEmpty {
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                    showAddItem = true
                }
            }
        }) {
            DocumentScannerView { pages in
                scannedPages = pages
            }
        }
        #endif
        .dropDestination(for: String.self) { droppedStrings, _ in
            for text in droppedStrings {
                let newItem = VaultItem(title: text, folder: folder)
                modelContext.insert(newItem)
            }
            return true
        }
    }

    @ViewBuilder
    private func itemRow(_ item: VaultItem) -> some View {
        HStack(spacing: 12) {
            // Show first image thumbnail if available
            #if canImport(UIKit)
            if let firstImage = item.imageData.first,
               let uiImage = UIImage(data: firstImage) {
                Image(uiImage: uiImage)
                    .resizable()
                    .scaledToFill()
                    .frame(width: 50, height: 50)
                    .clipShape(RoundedRectangle(cornerRadius: 6))
            }
            #endif

            VStack(alignment: .leading, spacing: 4) {
                Text(item.title)
                    .font(.system(size: 18, weight: .semibold))

                HStack(spacing: 8) {
                    if !item.imageData.isEmpty {
                        Label("\(item.imageData.count)", systemImage: "doc.fill")
                            .font(.system(size: 14))
                            .foregroundStyle(.secondary)
                    }
                    Text(item.dateModified, format: .dateTime.month(.abbreviated).day().year())
                        .font(.system(size: 14))
                        .foregroundStyle(.secondary)
                }
            }
        }
        .draggable(item.title) {
            Label(item.title, systemImage: "doc.fill")
                .padding(8)
                .background(.regularMaterial)
                .clipShape(RoundedRectangle(cornerRadius: 8))
        }
    }

    private func deleteItems(at offsets: IndexSet) {
        let items = filteredItems
        for index in offsets {
            modelContext.delete(items[index])
        }
    }
}
