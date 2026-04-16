//
//  ImageViewerView.swift
//  Claudes LockBox
//
//  Created by Michael Fluharty on 4/16/26.
//

#if os(iOS)
import SwiftUI
import UIKit

struct ImageViewerView: View {
    let imageData: Data
    @Environment(\.dismiss) private var dismiss
    @State private var showShareSheet = false

    var body: some View {
        NavigationStack {
            if let uiImage = UIImage(data: imageData) {
                ScrollView([.horizontal, .vertical]) {
                    Image(uiImage: uiImage)
                        .resizable()
                        .scaledToFit()
                        .frame(maxWidth: .infinity)
                }
                .navigationTitle("Scan")
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Done") { dismiss() }
                            .font(.system(size: 18))
                    }
                    ToolbarItem(placement: .primaryAction) {
                        Button {
                            showShareSheet = true
                        } label: {
                            Image(systemName: "square.and.arrow.up")
                                .font(.system(size: 18))
                        }
                    }
                }
                .sheet(isPresented: $showShareSheet) {
                    let image = UIImage(data: imageData)!
                    ShareActivityView(items: [image])
                }
            }
        }
    }
}

struct ShareActivityView: UIViewControllerRepresentable {
    let items: [Any]

    func makeUIViewController(context: Context) -> UIActivityViewController {
        UIActivityViewController(activityItems: items, applicationActivities: nil)
    }

    func updateUIViewController(_ uiViewController: UIActivityViewController, context: Context) {}
}
#endif
