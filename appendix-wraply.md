# Appendix: Building Wraply — A Web Browser from Xcode to App Store

*Claude's Xcode 26 Swift Bible — Appendix Project*

---

This appendix walks you through building a complete web browser app called **Wraply** from an empty Xcode project to a published App Store listing. Every step is here. No jumping to other chapters, no assumptions about what you already know. Follow along in order and you'll have a working app on your phone by the end.

Wraply lets you browse the web, save bookmarks, and share pages. It also has a "kiosk mode" where you can lock it to a single website — useful if you want to wrap a company site into its own app icon on your home screen. That's where the name comes from: you're wrapping a website.

---

## 1. Creating the Project

1.1 Open Xcode. You'll see the Welcome screen with three options on the left and your recent projects on the right.

**[Fig. W.1 — Xcode 26.3 Welcome Screen]**

1.2 Click **Create New Project**. A template picker appears. Along the top you'll see platform tabs — Multiplatform, iOS, macOS, watchOS, tvOS, visionOS, DriverKit, Other. Pick **Multiplatform**. Under Application, pick **App**. Click **Next**.

**[Fig. W.2 — Template Picker: Multiplatform > App]**

1.3 Now you fill in the project details:

- **Product Name:** `Wraply`
- **Team:** Your Apple Developer account name (e.g., "Michael Fluharty")
- **Organization Identifier:** Pick something unique to you. We're using `com.ClaudeX26Bible`. Yours might be `com.yourname` or `com.yourcompany`. This never changes after submission, so pick it once and stick with it.
- **Bundle Identifier:** Xcode builds this automatically — it's your Organization Identifier + Product Name. You'll see `com.ClaudeX26Bible.Wraply` (or whatever yours is). This is how Apple tells your app apart from every other app in the world.
- **Testing System:** Swift Testing with XCTest UI Tests (the default is fine)
- **Storage:** SwiftData
- **Host in CloudKit:** Check this if you want bookmarks to sync across devices. Leave it unchecked if you don't care about sync yet — you can add it later.

**[Fig. W.3 — Project Options: Wraply filled in]**

1.4 Click **Next**. Xcode asks where to save the project. Pick a folder — we're using a folder called `Xcode26` inside the book's project directory, but any folder works. Make sure **"Create Git repository on my Mac"** is checked at the bottom. This gives your project version control from day one. Click **Create**.

1.5 Xcode opens the workspace. Take a second to look at what it made for you:

**[Fig. W.4 — Xcode Workspace: Wraply project open]**

- **Left panel (Navigator):** Your project's file tree. You'll see a `Wraply` folder with `Assets.xcassets`, `ContentView.swift`, `Info.plist`, `Item.swift`, `WraplyApp.swift`, and the entitlements file.
- **Center (Editor):** Whatever file you have selected. Right now it's showing `ContentView.swift` — the template code Xcode generated.
- **Right panel (Inspectors):** Properties of the selected file or UI element. This is Xcode's version of Delphi's Object Inspector — same idea, different skin.
- **Top bar:** Run/stop buttons, scheme selector (Wraply > iPhone 16e), and status messages.

---

## _2. Creating and Connecting the Remote GitHub Repository

_2.1 Your project has a local Git repository — Xcode created it in section 1.4 when you checked "Create Git repository on my Mac." Now attach it to a remote repository on GitHub so your code lives online too. If you haven't set up your GitHub account in Xcode yet, see the previous appendix (Setting Up GitHub in Xcode) first.

_2.2 See the icon in the Navigator that looks like a square with an X in it? That's the **Source Control navigator**. Click it (or press Cmd+2). Then click the **Repositories** tab at the top. You'll see your Wraply repository listed with a "main" branch.

**[Fig. W.10 — Source Control navigator: Repositories tab showing Wraply main]**

_2.3 Right-click **Wraply** in the list and choose **New Remote**. A dialog appears.

_2.4 Fill it in:

- **Account:** Your GitHub account (e.g., "fluhartyml")
- **Name:** `Wraply`
- **Visibility:** Public

Click **Create**. Xcode pushes the template project to GitHub — your first backup.

**[Fig. W.7 — Create Remote dialog: fluhartyml/Wraply]**

_2.5 Open a browser and go to your GitHub profile. The Wraply repo is live with the template files.

**[Fig. W.8 — GitHub repo: fluhartyml/Wraply live]**

_2.6 From here on, every time you commit in Xcode (**Source Control > Commit**, or Cmd+Option+C), check "Push to remote" to send your changes to GitHub in the same step. The icon, the code, the bookmarks model — it all goes up together as you build.

---

## 3. Setting Up the App Icon

3.1 Before writing any code, give your app an icon. An app without an icon looks unfinished and Apple will reject it during review.

3.2 You need a **1024x1024 pixel PNG image**. No transparency, no rounded corners — Apple applies the corner rounding automatically. If you don't have an icon yet, design one in any image editor (Pixelmator, Photoshop, even Preview) or use an AI image generator. Save it somewhere you can find it.

3.3 In Xcode's Project Navigator (left panel), expand the `Wraply` folder and click on **Assets.xcassets**. This opens the asset catalog — it's where your app stores images, colors, and icons.

3.4 Click on **AppIcon** in the left sidebar of the asset catalog. You'll see a grid of empty slots — one for iOS (labeled "Any Appearance"), optional dark and tinted variants, and several Mac sizes at different scales (16pt, 32pt, 128pt, 256pt, 512pt at 1x and 2x).

3.5 Open Finder and navigate to your 1024x1024 icon PNG. **Drag the file from Finder directly into the iOS "Any Appearance" slot** at the top of the grid. Xcode imports it.

**[Fig. W.5 — AppIcon in Asset Catalog: iOS slot filled]**

3.6 For the Mac sizes — drag the same 1024x1024 image into each empty Mac slot. Xcode will show yellow caution triangles because the image is oversized for the smaller slots (you're putting a 1024px image in a 16pt slot). This is fine. Xcode downscales automatically at build time. The warnings are cosmetic, not errors. Your app will build, run, and pass App Store review.

**[Fig. W.6 — AppIcon in Asset Catalog: All slots filled, caution triangles on Mac sizes]**

3.7 If you want to be thorough and eliminate the warnings, you can create properly sized versions of your icon in an image editor:
- 16x16, 32x32 (for 16pt 1x and 2x)
- 32x32, 64x64 (for 32pt 1x and 2x)
- 128x128, 256x256 (for 128pt 1x and 2x)
- 256x256, 512x512 (for 256pt 1x and 2x)
- 512x512, 1024x1024 (for 512pt 1x and 2x)

Drag each sized image into its matching slot. But again — one 1024x1024 image in every slot works. Don't let the warnings stop you.

3.8 The **Dark** and **Tinted** appearance slots are optional. If you want your icon to look different in Dark Mode or when the user has tinted icons enabled in iOS settings, drag variant images into those slots. Otherwise leave them empty — your default icon shows everywhere.

---

## 4. Understanding the Template Code

**[Fig. W.9 — ContentView.swift with the template code Xcode generated]**

_4.1 Click on **ContentView.swift** in the Navigator. Xcode generated this when you created the project. It's the first screen your app shows. Right now it's a SwiftData template with a list of Items — not a web browser. We're going to replace all of it, but first let's understand what's here.

4.2 The top of the file:

```swift
import SwiftUI
import SwiftData
```

These two lines load the tools you need. `SwiftUI` draws the screen. `SwiftData` saves data to disk. Think of `import` like plugging in a power tool — Swift is the workbench, these are the tools on it.

4.3 The struct:

```swift
struct ContentView: View {
```

This creates a **view** — a thing that draws on screen. The `: View` part is a promise: "this struct will have a `body` property that returns something visible." It's like Delphi's `TForm` — a container that holds your UI.

4.4 Everything inside `var body: some View { }` is what appears on screen. The template has a `NavigationSplitView` with a list — we don't need any of that. We're building a browser.

---

## _5. Creating the Web View Wrapper

**CAUTION:** We're creating this file BEFORE we touch ContentView. Here's why — the new ContentView code we're about to write in section 6 calls `WebViewRepresentable`. If that file doesn't exist yet, Xcode throws an error: "Cannot find 'WebViewRepresentable' in scope." Xcode doesn't care that you're about to create it — if a file references something that doesn't exist right now, it won't compile. Always create dependencies first, then the code that uses them.

_5.1 SwiftUI doesn't have a built-in web view. Apple's web view is `WKWebView` from WebKit — it's a UIKit component. To use a UIKit component in SwiftUI, you wrap it in a `UIViewRepresentable`. This is a bridge between the old world (UIKit) and the new world (SwiftUI).

_5.2 Create a new Swift file: **File > New > File** (or Cmd+N). Pick **Swift File**. Name it `WebViewRepresentable.swift`. Click **Create**.

_5.3 Replace the contents with:

```swift
//
//  WebViewRepresentable.swift
//  Wraply
//

import SwiftUI
import WebKit

struct WebViewRepresentable: UIViewRepresentable {
    let webView: WKWebView
    
    func makeUIView(context: Context) -> WKWebView {
        webView.allowsBackForwardNavigationGestures = true
        return webView
    }
    
    func updateUIView(_ uiView: WKWebView, context: Context) {
        // SwiftUI calls this when state changes.
        // We handle loading in ContentView, so nothing needed here.
    }
}
```

_5.4 That's the whole bridge. `makeUIView` creates the web view once. `updateUIView` gets called when SwiftUI's state changes — we don't need it because `ContentView` handles loading. The `allowsBackForwardNavigationGestures` line lets the user swipe left/right to go back and forward, just like Safari.

---

## _6. Building the Browser View

_6.1 Now we replace ContentView. Delete everything inside `ContentView.swift`. Replace it with this:

```swift
//
//  ContentView.swift
//  Wraply
//
//  Created by [Your Name] on [Today's Date].
//

import SwiftUI
import WebKit

struct ContentView: View {
    @State private var urlString: String = "https://www.apple.com"
    @State private var webView = WKWebView()
    
    var body: some View {
        VStack(spacing: 0) {
            // URL Bar
            HStack {
                TextField("Enter URL", text: $urlString)
                    .textFieldStyle(.roundedBorder)
                    .autocorrectionDisabled()
                    .textInputAutocapitalization(.never)
                    .keyboardType(.URL)
                    .onSubmit {
                        loadURL()
                    }
                    .font(.system(size: 18))
                
                Button("Go") {
                    loadURL()
                }
                .font(.system(size: 18))
                .buttonStyle(.borderedProminent)
            }
            .padding()
            
            // Web View
            WebViewRepresentable(webView: webView)
        }
        .onAppear {
            loadURL()
        }
    }
    
    private func loadURL() {
        var address = urlString.trimmingCharacters(in: .whitespacesAndNewlines)
        if !address.hasPrefix("http://") && !address.hasPrefix("https://") {
            address = "https://" + address
        }
        if let url = URL(string: address) {
            webView.load(URLRequest(url: url))
        }
    }
}
```

_6.2 Let's break that down:

- `@State private var urlString` — this holds the text in the URL bar. The `@State` wrapper means SwiftUI watches it — when it changes, the screen updates. Same concept as Delphi's `Edit1.Text` property, but SwiftUI tracks changes automatically instead of you writing an `OnChange` event.
- `TextField("Enter URL", text: $urlString)` — the URL input field. The `$` means two-way binding — typing in the field updates `urlString`, and changing `urlString` in code updates the field. The modifiers (`.autocorrectionDisabled()`, `.textInputAutocapitalization(.never)`, `.keyboardType(.URL)`) tell the keyboard not to autocorrect URLs, not to capitalize, and to show the URL keyboard with `.com` and `/` keys.
- `Button("Go")` — triggers `loadURL()` when tapped.
- `loadURL()` — takes whatever's in the URL bar, adds `https://` if missing, and tells the web view to load it.

_6.3 Notice that `WebViewRepresentable(webView: webView)` works now — you created that file in section 5. If you'd tried this code first, Xcode would have thrown "Cannot find 'WebViewRepresentable' in scope" because the file didn't exist yet. Order matters.

---

## 7. Adding Navigation Controls

7.1 A browser needs back, forward, and refresh buttons. Open `ContentView.swift` and add a toolbar below the URL bar.

7.2 Replace the `VStack` in `body` with:

```swift
var body: some View {
    VStack(spacing: 0) {
        // Toolbar
        HStack {
            Button(action: { webView.goBack() }) {
                Image(systemName: "chevron.left")
                    .font(.system(size: 20))
            }
            .disabled(!webView.canGoBack)
            
            Button(action: { webView.goForward() }) {
                Image(systemName: "chevron.right")
                    .font(.system(size: 20))
            }
            .disabled(!webView.canGoForward)
            
            Button(action: { webView.reload() }) {
                Image(systemName: "arrow.clockwise")
                    .font(.system(size: 20))
            }
            
            Spacer()
            
            // URL Bar
            TextField("Enter URL", text: $urlString)
                .textFieldStyle(.roundedBorder)
                .autocorrectionDisabled()
                .textInputAutocapitalization(.never)
                .keyboardType(.URL)
                .onSubmit {
                    loadURL()
                }
                .font(.system(size: 18))
            
            Button("Go") {
                loadURL()
            }
            .font(.system(size: 18))
            .buttonStyle(.borderedProminent)
        }
        .padding(.horizontal)
        .padding(.vertical, 8)
        
        Divider()
        
        // Web View
        WebViewRepresentable(webView: webView)
    }
    .onAppear {
        loadURL()
    }
}
```

7.3 Now you have back (chevron left), forward (chevron right), and refresh (arrow clockwise) buttons to the left of the URL bar. The `.disabled` modifier grays out back/forward when there's nothing to go back or forward to — the web view tracks its own navigation history.

7.4 The `Image(systemName:)` uses **SF Symbols** — Apple's built-in icon library. Over 5,000 icons, all free, all scale with Dynamic Type. You don't need to ship any icon assets for UI buttons.

---

## 8. Adding the Share Sheet

8.1 A browser should let you share the current page. Add a share button to the toolbar.

8.2 Add this state variable at the top of `ContentView`:

```swift
@State private var showShareSheet = false
```

8.3 Add the share button after the refresh button in the HStack:

```swift
Button(action: { showShareSheet = true }) {
    Image(systemName: "square.and.arrow.up")
        .font(.system(size: 20))
}
```

8.4 Add the share sheet modifier to the `VStack`, right before `.onAppear`:

```swift
.sheet(isPresented: $showShareSheet) {
    if let url = webView.url {
        ShareLink(item: url)
    }
}
```

8.5 Now tapping the share icon opens the standard iOS share sheet with the current URL. The user can AirDrop it, copy it, send it in Messages, save it to Notes — all the system share extensions work automatically.

---

## 9. Adding Bookmarks with SwiftData

9.1 A browser needs bookmarks. We already picked SwiftData when creating the project, so the infrastructure is there. We need a data model and a bookmarks view.

9.2 Delete `Item.swift` (the template model) — select it in the Navigator, press Delete, choose "Move to Trash."

9.3 Create a new file: **File > New > File > Swift File**. Name it `Bookmark.swift`:

```swift
//
//  Bookmark.swift
//  Wraply
//

import SwiftData
import Foundation

@Model
class Bookmark {
    var title: String
    var urlString: String
    var dateAdded: Date
    
    init(title: String, urlString: String, dateAdded: Date = .now) {
        self.title = title
        self.urlString = urlString
        self.dateAdded = dateAdded
    }
}
```

9.4 The `@Model` macro tells SwiftData to persist this class — save it to disk, load it back, track changes. Three properties: a title, a URL string, and when it was saved. That's it. No Core Data XML files, no migration code, no fetch request boilerplate. SwiftData handles all of it.

9.5 Create another new file: `BookmarksView.swift`:

```swift
//
//  BookmarksView.swift
//  Wraply
//

import SwiftUI
import SwiftData

struct BookmarksView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss
    @Query(sort: \Bookmark.dateAdded, order: .reverse) private var bookmarks: [Bookmark]
    
    var onSelect: (String) -> Void
    
    var body: some View {
        NavigationStack {
            List {
                if bookmarks.isEmpty {
                    Text("No bookmarks yet.")
                        .foregroundStyle(.secondary)
                        .font(.system(size: 18))
                } else {
                    ForEach(bookmarks) { bookmark in
                        Button {
                            onSelect(bookmark.urlString)
                            dismiss()
                        } label: {
                            VStack(alignment: .leading) {
                                Text(bookmark.title)
                                    .font(.system(size: 18))
                                Text(bookmark.urlString)
                                    .font(.system(size: 14))
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                    .onDelete(perform: deleteBookmarks)
                }
            }
            .navigationTitle("Bookmarks")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { dismiss() }
                        .font(.system(size: 18))
                }
            }
        }
    }
    
    private func deleteBookmarks(offsets: IndexSet) {
        for index in offsets {
            modelContext.delete(bookmarks[index])
        }
    }
}
```

9.6 Back in `ContentView.swift`, add these state variables:

```swift
@Environment(\.modelContext) private var modelContext
@State private var showBookmarks = false
```

9.7 Add a bookmark button and a bookmarks list button to the toolbar (after the share button):

```swift
Button(action: { saveBookmark() }) {
    Image(systemName: "bookmark.fill")
        .font(.system(size: 20))
}

Button(action: { showBookmarks = true }) {
    Image(systemName: "book")
        .font(.system(size: 20))
}
```

9.8 Add the `saveBookmark` function:

```swift
private func saveBookmark() {
    let title = webView.title ?? urlString
    let url = webView.url?.absoluteString ?? urlString
    let bookmark = Bookmark(title: title, urlString: url)
    modelContext.insert(bookmark)
}
```

9.9 Add the bookmarks sheet modifier (after the share sheet):

```swift
.sheet(isPresented: $showBookmarks) {
    BookmarksView { urlString in
        self.urlString = urlString
        loadURL()
    }
}
```

9.10 Build and run (Cmd+R). You now have a working browser with back/forward/refresh, a URL bar, share sheet, and persistent bookmarks that survive app restarts.

---

## 10. Adding the About Section and Send Feedback

10.1 Every app needs an About screen with a way for users to send feedback. Create a new file: `FeedbackView.swift`:

```swift
//
//  FeedbackView.swift
//  Wraply
//

import SwiftUI
import MessageUI

struct FeedbackView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var feedbackType = "Bug Report"
    @State private var feedbackText = ""
    @State private var showMailCompose = false
    @State private var showMailUnavailable = false
    
    let feedbackTypes = ["Bug Report", "Feature Request"]
    let feedbackEmail = "michael.fluharty@mac.com"
    
    var body: some View {
        NavigationStack {
            Form {
                Picker("Type", selection: $feedbackType) {
                    ForEach(feedbackTypes, id: \.self) { type in
                        Text(type)
                    }
                }
                .pickerStyle(.segmented)
                .font(.system(size: 18))
                
                Section("Your Feedback") {
                    TextEditor(text: $feedbackText)
                        .frame(minHeight: 150)
                        .font(.system(size: 18))
                }
                
                Button("Send") {
                    if MFMailComposeViewController.canSendMail() {
                        showMailCompose = true
                    } else {
                        showMailUnavailable = true
                    }
                }
                .font(.system(size: 18))
                .disabled(feedbackText.isEmpty)
            }
            .navigationTitle("Send Feedback")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Cancel") { dismiss() }
                        .font(.system(size: 18))
                }
            }
            .sheet(isPresented: $showMailCompose) {
                MailComposeView(
                    recipient: feedbackEmail,
                    subject: "Wraply \(feedbackType) — v\(appVersion)",
                    body: feedbackText + "\n\n" + deviceInfo
                )
            }
            .alert("Mail Not Available", isPresented: $showMailUnavailable) {
                Button("OK") {}
            } message: {
                Text("Email \(feedbackEmail) directly.")
            }
        }
    }
    
    private var appVersion: String {
        let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "?"
        let build = Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "?"
        return "\(version) (\(build))"
    }
    
    private var deviceInfo: String {
        let device = UIDevice.current
        var systemInfo = utsname()
        uname(&systemInfo)
        let model = withUnsafePointer(to: &systemInfo.machine) {
            $0.withMemoryRebound(to: CChar.self, capacity: 1) {
                String(validatingCString: $0) ?? "Unknown"
            }
        }
        let storage = (try? URL(fileURLWithPath: NSHomeDirectory())
            .resourceValues(forKeys: [.volumeAvailableCapacityForImportantUsageKey])
            .volumeAvailableCapacityForImportantUsage)
            .map { ByteCountFormatter.string(fromByteCount: $0, countStyle: .file) } ?? "Unknown"
        
        return """
        --- Device Info ---
        App: Wraply v\(appVersion)
        Device: \(model)
        System: \(device.systemName) \(device.systemVersion)
        Storage Available: \(storage)
        Locale: \(Locale.current.identifier)
        """
    }
}

struct MailComposeView: UIViewControllerRepresentable {
    let recipient: String
    let subject: String
    let body: String
    @Environment(\.dismiss) private var dismiss
    
    func makeUIViewController(context: Context) -> MFMailComposeViewController {
        let vc = MFMailComposeViewController()
        vc.setToRecipients([recipient])
        vc.setSubject(subject)
        vc.setMessageBody(body, isHTML: false)
        vc.mailComposeDelegate = context.coordinator
        return vc
    }
    
    func updateUIViewController(_ uiViewController: MFMailComposeViewController, context: Context) {}
    
    func makeCoordinator() -> Coordinator { Coordinator(dismiss: dismiss) }
    
    class Coordinator: NSObject, MFMailComposeViewControllerDelegate {
        let dismiss: DismissAction
        init(dismiss: DismissAction) { self.dismiss = dismiss }
        func mailComposeController(_ controller: MFMailComposeViewController, didFinishWith result: MFMailComposeResult, error: Error?) {
            dismiss()
        }
    }
}
```

10.2 Create `AboutView.swift`:

```swift
//
//  AboutView.swift
//  Wraply
//

import SwiftUI

struct AboutView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var showFeedback = false
    
    var body: some View {
        NavigationStack {
            List {
                Section {
                    VStack(spacing: 8) {
                        if let icon = Bundle.main.icon {
                            Image(uiImage: icon)
                                .resizable()
                                .frame(width: 80, height: 80)
                                .clipShape(RoundedRectangle(cornerRadius: 18))
                        }
                        Text("Wraply")
                            .font(.system(size: 24, weight: .bold))
                        Text("v\(appVersion)")
                            .font(.system(size: 16))
                            .foregroundStyle(.secondary)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical)
                }
                
                Section {
                    Text("Michael Lee Fluharty")
                        .font(.system(size: 18))
                    Text("Engineered with Claude by Anthropic")
                        .font(.system(size: 18))
                        .foregroundStyle(.secondary)
                }
                
                Section {
                    Button {
                        showFeedback = true
                    } label: {
                        Label("Send Feedback", systemImage: "envelope")
                            .font(.system(size: 18))
                    }
                }
            }
            .navigationTitle("About")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { dismiss() }
                        .font(.system(size: 18))
                }
            }
            .sheet(isPresented: $showFeedback) {
                FeedbackView()
            }
        }
    }
    
    private var appVersion: String {
        let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "?"
        let build = Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "?"
        return "\(version) (\(build))"
    }
}

extension Bundle {
    var icon: UIImage? {
        if let icons = infoDictionary?["CFBundleIcons"] as? [String: Any],
           let primary = icons["CFBundlePrimaryIcon"] as? [String: Any],
           let files = primary["CFBundleIconFiles"] as? [String],
           let last = files.last {
            return UIImage(named: last)
        }
        return nil
    }
}
```

10.3 Back in `ContentView.swift`, add a state variable:

```swift
@State private var showAbout = false
```

10.4 Add an info button to the toolbar (at the end of the HStack):

```swift
Button(action: { showAbout = true }) {
    Image(systemName: "info.circle")
        .font(.system(size: 20))
}
```

10.5 Add the About sheet modifier:

```swift
.sheet(isPresented: $showAbout) {
    AboutView()
}
```

---

## 11. Updating the App Entry Point

11.1 Open `WraplyApp.swift`. The template code references `Item` which we deleted. Replace the contents:

```swift
//
//  WraplyApp.swift
//  Wraply
//

import SwiftUI
import SwiftData

@main
struct WraplyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Bookmark.self)
    }
}
```

11.2 The `.modelContainer(for: Bookmark.self)` line tells SwiftData to set up persistence for our `Bookmark` model. Every view below `ContentView` can now read and write bookmarks.

---

## 12. Build, Run, and Test

12.1 Press **Cmd+B** to build. Fix any errors — the most common ones:
- **"Cannot find 'Item' in scope"** — you have a leftover reference to the deleted `Item.swift`. Search for `Item` in the project and remove it.
- **"No such module 'WebKit'"** — make sure you wrote `import WebKit` at the top of `ContentView.swift` and `WebViewRepresentable.swift`.

12.2 Press **Cmd+R** to run on the simulator or your device. You should see:
- A URL bar at the top with back/forward/refresh/share/bookmark/bookmarks/about buttons
- Apple.com loading in the web view below
- Swipe left/right to navigate back and forward

12.3 Test the full flow:
1) Type a URL in the bar, tap Go — page loads
2) Tap the bookmark icon — saves the current page
3) Tap the book icon — bookmarks list opens, tap one to navigate
4) Tap the share icon — share sheet opens
5) Tap the info icon — About screen with Send Feedback
6) Swipe right on the web view — goes back

---

## 13. Preparing for App Store Submission

13.1 Before you archive, check these settings in the **General** tab (click the Wraply project at the top of the Navigator, then the Wraply target):

- **Display Name:** Wraply
- **Bundle Identifier:** com.ClaudeX26Bible.Wraply (or yours)
- **Version:** 1.0
- **Build:** 1.0
- **Minimum Deployments:** iOS 17.0 (SwiftData requires it)
- **Supported Destinations:** iPhone, iPad

13.2 **Set the scheme to "Any iOS Device (arm64)"** in the top bar. You can't archive with a simulator selected.

13.3 **Product > Archive**. Xcode builds the release version and opens the Organizer window when done.

13.4 In the Organizer, select your archive and click **Distribute App**. Choose **App Store Connect** > **Upload**. Follow the prompts — Xcode handles signing and uploads the build.

13.5 Go to **appstoreconnect.apple.com**. Your app appears under "Apps." Fill in:
- **App Name:** Wraply
- **Subtitle:** Wrap Any Website Into an App
- **Category:** Utilities
- **Description:** Describe what the app does
- **Keywords:** browser, web, wrapper, kiosk, bookmark
- **Screenshots:** Take them from the simulator (Cmd+S in Simulator)
- **App Icon:** Already embedded from the asset catalog
- **Build:** Select the build you just uploaded
- **Pricing:** Free

13.6 Click **Submit for Review**. Apple reviews it — usually within 24-48 hours. You'll get an email when it's approved.

---

## 14. What You Built

14.1 Wraply is a real app. It browses the web, saves bookmarks that persist across launches, shares URLs, and has a feedback channel to the developer. It's built with:

- **SwiftUI** — the user interface (Chapters 2, 6, 7, 9)
- **WebKit** — WKWebView for rendering web pages (Appendix: WebKit)
- **SwiftData** — bookmark persistence (Chapter 15)
- **MessageUI** — email feedback (Chapter 12)
- **UIViewRepresentable** — bridging UIKit into SwiftUI (Chapter 18)
- **SF Symbols** — toolbar icons (Chapter 6)
- **Git** — version control from day one (Chapter 20)

14.2 From an empty Xcode project to a published app. Every app in this book follows the same path.

---

*Wraply source code: github.com/fluhartyml/Wraply*
*Bundle ID: com.ClaudeX26Bible.Wraply*
*License: GPL v3 — Share and share alike with attribution required.*
