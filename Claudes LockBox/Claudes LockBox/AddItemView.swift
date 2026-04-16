//
//  AddItemView.swift
//  Claudes LockBox
//
//  Created by Michael Fluharty on 4/16/26.
//

import SwiftUI
import SwiftData

struct AddItemView: View {
    let folder: Folder
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss
    @State private var title = ""
    @State private var pin = ""
    @State private var notes = ""

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    TextField("Title", text: $title)
                        .font(.system(size: 18))
                } header: {
                    Text("Name")
                        .font(.system(size: 16))
                }

                Section {
                    TextField("PIN, code, or password", text: $pin)
                        .font(.system(size: 20, design: .monospaced))
                        .keyboardType(.default)
                } header: {
                    Text("PIN / Code")
                        .font(.system(size: 16))
                }

                Section {
                    TextEditor(text: $notes)
                        .font(.system(size: 18))
                        .frame(minHeight: 80)
                } header: {
                    Text("Notes")
                        .font(.system(size: 16))
                }
            }
            .navigationTitle("New Item")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                        .font(.system(size: 18))
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        let newItem = VaultItem(
                            title: title.isEmpty ? "Untitled" : title,
                            notes: notes,
                            pin: pin,
                            folder: folder
                        )
                        modelContext.insert(newItem)
                        dismiss()
                    }
                    .font(.system(size: 18, weight: .semibold))
                }
            }
        }
    }
}
