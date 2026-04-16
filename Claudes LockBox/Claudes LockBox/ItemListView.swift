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

    var body: some View {
        List(selection: $selectedItem) {
            ForEach(filteredItems) { item in
                VStack(alignment: .leading, spacing: 4) {
                    Text(item.title)
                        .font(.system(size: 18, weight: .semibold))
                    Text(item.dateModified, format: .dateTime.month(.abbreviated).day().year())
                        .font(.system(size: 16))
                        .foregroundStyle(.secondary)
                }
                .tag(item)
                .draggable(item.title) {
                    // Drag preview
                    Label(item.title, systemImage: "doc.fill")
                        .padding(8)
                        .background(.regularMaterial)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                }
            }
            .onDelete(perform: deleteItems)
        }
        .navigationTitle(folder.name)
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button {
                    showAddItem = true
                } label: {
                    Label("Add Item", systemImage: "plus")
                }
            }
        }
        .sheet(isPresented: $showAddItem) {
            AddItemView(folder: folder)
        }
        .dropDestination(for: String.self) { droppedStrings, _ in
            // Accept text drops as new vault items
            for text in droppedStrings {
                let newItem = VaultItem(title: text, folder: folder)
                modelContext.insert(newItem)
            }
            return true
        }
    }

    private func deleteItems(at offsets: IndexSet) {
        let items = filteredItems
        for index in offsets {
            modelContext.delete(items[index])
        }
    }
}
