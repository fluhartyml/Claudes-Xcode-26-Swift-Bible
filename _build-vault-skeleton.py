#!/usr/bin/env python3
"""Create the vault folder tree and placeholder HTML for every Book/Appendix.
One-shot skeleton build. Run once from the vault root.
"""
from pathlib import Path
import string

VAULT = Path(__file__).parent.resolve()

# ---------- Book lists -------------------------------------------------------

# Part I: Swift Lexicon (A-Z)
lexicon = [(f"Book-{L}", L, f"Swift words starting with {L}") for L in string.ascii_uppercase]

# Part II-VI: numbered Books (existing content lives as .md at vault root)
numbered = [
    (2, "Introduction", [
        (1, "Introducing-Swift-And-Xcode", "Introducing Swift & Xcode", "01-Introducing-Swift-And-Xcode.md"),
        (2, "Introducing-SwiftUI-Views", "Introducing SwiftUI Views", "02-Introducing-SwiftUI-Views.md"),
        (3, "Introducing-Scenes-And-Windows", "Introducing Scenes & Windows", "03-Introducing-Scenes-And-Windows.md"),
    ]),
    (3, "The-User-Interface", [
        (4, "Gestures-And-Input", "Gestures & Input", "04-Gestures-And-Input.md"),
        (5, "Menus-And-Navigation", "Menus & Navigation", "05-Menus-And-Navigation.md"),
        (6, "Controls-Buttons-Toggles-Pickers", "Controls: Buttons, Toggles, Pickers", "06-Controls-Buttons-Toggles-Pickers.md"),
        (7, "Toolbars-And-Tab-Views", "Toolbars & Tab Views", "07-Toolbars-And-Tab-Views.md"),
        (8, "Lists-Grids-And-ForEach", "Lists, Grids & ForEach", "08-Lists-Grids-And-ForEach.md"),
        (9, "Text-And-TextField", "Text & TextField", "09-Text-And-TextField.md"),
        (10, "TextEditor-And-AttributedString", "TextEditor & AttributedString", "10-TextEditor-And-AttributedString.md"),
        (11, "FileManager-And-Documents", "FileManager & Documents", "11-FileManager-And-Documents.md"),
        (12, "Sheets-Alerts-And-Confirmations", "Sheets, Alerts & Confirmations", "12-Sheets-Alerts-And-Confirmations.md"),
    ]),
    (4, "The-Application", [
        (13, "Multi-Window-And-NavigationSplitView", "Multi-Window & NavigationSplitView", "13-Multi-Window-And-NavigationSplitView.md"),
        (14, "Clipboard-DragDrop-ShareSheet", "Clipboard, Drag & Drop, Share Sheet", "14-Clipboard-DragDrop-ShareSheet.md"),
        (15, "SwiftData-And-CoreData", "SwiftData & Core Data", "15-SwiftData-And-CoreData.md"),
        (16, "Extensions-And-Packages", "Extensions & Packages", "16-Extensions-And-Packages.md"),
        (17, "Swift-Charts-And-PDFKit", "Swift Charts & PDFKit", "17-Swift-Charts-And-PDFKit.md"),
    ]),
    (5, "Advanced-Techniques", [
        (18, "Error-Handling-And-Result-Type", "Error Handling & Result Type", "18-Error-Handling-And-Result-Type.md"),
        (19, "Building-Custom-Views-And-Modifiers", "Building Custom Views & Modifiers", "19-Building-Custom-Views-And-Modifiers.md"),
        (20, "Performance-Instruments-And-Best-Practices", "Performance, Instruments & Best Practices", "20-Performance-Instruments-And-Best-Practices.md"),
    ]),
    (6, "The-Modern-Toolchain", [
        (21, "Git-And-GitHub", "Git & GitHub", "21-Git-And-GitHub.md"),
        (22, "AI-Chatbot-Integration", "AI Chatbot Integration", "22-AI-Chatbot-Integration.md"),
    ]),
]

part_roman = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}
part_title_long = {
    1: "The Swift Language",
    2: "Introduction",
    3: "The User Interface",
    4: "The Application",
    5: "Advanced Techniques",
    6: "The Modern Toolchain",
}

appendices = [
    ("A", "GitHub-Setup", "Appendix A: GitHub Setup", "appendix-github-setup.html"),
    ("B", "Claudes-Web-Wrapper", "Appendix B: Claude's Web Wrapper", "appendix-claudes-web-wrapper-v2.html"),
    ("C", "QuickNote", "Appendix C: QuickNote", "appendix-quicknote.md"),
    ("D", "LockBox", "Appendix D: Claude's LockBox", None),
]

# ---------- Placeholder template --------------------------------------------

PLACEHOLDER_CSS = """
  :root {
    --bg: #000000;
    --fg: #FFB000;
    --bright: #FFD060;
    --dim: #996600;
    --codebg: #1a0d00;
    --border: #664500;
  }
  * { box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--fg);
    font-family: "FiraCode Nerd Font Mono", "FiraCode Nerd Font",
                 "Fira Code", "Menlo", "Courier New", monospace;
    font-size: 18pt;
    line-height: 1.55;
    max-width: 1100px;
    margin: 0 auto;
    padding: 2rem 2.5rem 6rem 2.5rem;
    text-shadow: 0 0 1px rgba(255, 176, 0, 0.35);
  }
  h1 { color: var(--bright); font-weight: normal; font-size: 32pt; margin: 1rem 0; }
  h2 { color: var(--bright); font-weight: normal; font-size: 22pt; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }
  p { margin: 0.6rem 0; }
  a { color: var(--bright); text-decoration: none; border-bottom: 1px dotted var(--dim); }
  a:hover { background: #332200; }
  code { color: var(--bright); background: var(--codebg); padding: 0.08em 0.35em; border: 1px solid #3a2400; border-radius: 3px; font-size: 0.92em; }
  header, footer { color: var(--dim); font-size: 13pt; }
  header { margin-bottom: 1.2rem; padding-bottom: 0.7rem; border-bottom: 1px solid var(--border); }
  footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border); }
  .status { color: var(--dim); font-style: italic; font-size: 15pt; border-left: 3px solid var(--dim); padding-left: 0.8rem; margin: 1.5rem 0; }
  .roll-call { border: 1px solid var(--border); padding: 0.9rem 1.2rem; margin: 1rem 0; background: #060400; font-size: 15pt; }
  .roll-call strong { color: var(--bright); }
  .nav { display: flex; gap: 2rem; margin-top: 2rem; font-size: 15pt; }
"""

PLACEHOLDER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} — Claude's Xcode 26 Swift Bible</title>
<style>{css}</style>
</head>
<body>
<header>File: <code>{relpath}</code> &middot; Placeholder</header>

<p class="status">{status}</p>

<h1>{title}</h1>

{body}

<div class="nav">
  <a href="{toc_href}">&larr; Table of Contents</a>
  <a href="{atlas_href}">Bible Atlas</a>
  <a href="{roadmap_href}">Roadmap</a>
</div>

<footer>File: <code>{relpath}</code> &middot; Claude's Xcode 26 Swift Bible &middot; Placeholder
</footer>

</body>
</html>
"""

def write_placeholder(path: Path, title: str, status: str, body: str):
    rel = path.relative_to(VAULT).as_posix()
    depth = len(path.relative_to(VAULT).parts) - 1  # how many ../ to reach vault root
    up = "../" * depth if depth > 0 else ""
    html = PLACEHOLDER_HTML.format(
        title=title,
        css=PLACEHOLDER_CSS,
        relpath=rel,
        status=status,
        body=body,
        toc_href=f"{up}table-of-contents.html",
        atlas_href=f"{up}bible-atlas.html",
        roadmap_href=f"{up}bible-roadmap.html",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html)

def book_body_lexicon(letter: str) -> str:
    """Brief description of what this letter's Book will cover."""
    samples = {
        'A': ['@State*', '<code>actor</code>', '<code>any</code>', '<code>Any</code>', '<code>AnyObject</code>', '<code>async</code>', '<code>await</code>', '<code>@autoclosure</code>', '<code>@available</code>', '<code>array</code> / <code>Array</code>'],
        'B': ['<code>Bool</code>', '<code>break</code>', '@Binding*'],
        'C': ['<code>case</code>', '<code>catch</code>', '<code>Character</code>', '<code>class</code>', '<code>closure</code>', '<code>Codable</code>', '<code>Collection</code>', '<code>Comparable</code>', '<code>continue</code>', '<code>convenience</code>', '<code>CaseIterable</code>'],
        'D': ['<code>defer</code>', '<code>deinit</code>', '<code>Decodable</code>', '<code>default</code>', '<code>Dictionary</code>', '<code>do</code>', '<code>Double</code>', '<code>dynamic</code>', '<code>@discardableResult</code>'],
        'E': ['<code>else</code>', '<code>Encodable</code>', '<code>enum</code>', '<code>Equatable</code>', '<code>Error</code>', '<code>extension</code>', '<code>@escaping</code>', '@Environment*', '@EnvironmentObject*', '<code>ExpressibleBy*</code>', '<code>#elseif</code>', '<code>#endif</code>', '<code>#error</code>'],
        'F': ['<code>fallthrough</code>', '<code>false</code>', '<code>fileprivate</code>', '<code>final</code>', '<code>Float</code>', '<code>for</code>', '<code>func</code>', '<code>@frozen</code>', '@FocusState*', '<code>#file</code>', '<code>#function</code>'],
        'G': ['generic (concept)', '<code>get</code>', '<code>guard</code>', '@GestureState*'],
        'H': ['<code>Hashable</code>'],
        'I': ['<code>if</code>', '<code>import</code>', '<code>in</code>', '<code>indirect</code>', '<code>infix</code>', '<code>init</code>', '<code>inout</code>', '<code>Int</code>', '<code>internal</code>', '<code>is</code>', '<code>Identifiable</code>', '<code>@inlinable</code>'],
        'J': ['JSON (cross-ref to <code>Codable</code> in Book C)'],
        'K': ['<code>KeyPath</code>', 'keyword (concept)'],
        'L': ['<code>lazy</code>', '<code>let</code>', '<code>#line</code>'],
        'M': ['<code>map</code>', '<code>mutating</code>', '<code>@main</code>', '<code>@MainActor</code>'],
        'N': ['<code>Never</code>', '<code>nil</code>', '<code>nonmutating</code>'],
        'O': ['<code>open</code>', '<code>operator</code>', '<code>Optional</code>', '<code>override</code>', '<code>@objc</code>', '<code>@Observable</code>', '@ObservedObject*'],
        'P': ['<code>postfix</code>', '<code>precedencegroup</code>', '<code>prefix</code>', '<code>print</code>', '<code>private</code>', '<code>protocol</code>', 'property wrapper (concept)', '@Published*', '<code>public</code>', '<code>#Predicate</code>', '<code>#Preview</code>'],
        'Q': ['<code>@Query</code> (SwiftData)'],
        'R': ['<code>Range</code>', '<code>ClosedRange</code>', '<code>RawRepresentable</code>', '<code>repeat</code>', '<code>required</code>', '<code>Result</code>', '<code>rethrows</code>', '<code>return</code>', '<code>@resultBuilder</code>'],
        'S': ['<code>Self</code>', '<code>self</code>', '<code>Sendable</code>', '<code>Sequence</code>', '<code>Set</code>', '<code>some</code>', '<code>static</code>', '<code>String</code>', '<code>struct</code>', '<code>subscript</code>', '<code>super</code>', '<code>switch</code>', '@State*', '@StateObject*', '@SceneStorage*', '<code>@Sendable</code>', '<code>#selector</code>'],
        'T': ['<code>Task</code>', '<code>TaskGroup</code>', '<code>throw</code>', '<code>throws</code>', '<code>true</code>', '<code>try</code>', '<code>typealias</code>', '<code>@testable</code>'],
        'U': ['<code>unowned</code>', '<code>@UIApplicationMain</code> (legacy)'],
        'V': ['<code>var</code>', '<code>Void</code>'],
        'W': ['<code>weak</code>', '<code>where</code>', '<code>while</code>', '<code>#warning</code>'],
        'X': ['(thin — likely empty; may consolidate with Y/Z per open question 7.8)'],
        'Y': ['(thin — likely empty)'],
        'Z': ['(thin — likely empty)'],
    }
    bits = samples.get(letter, ['(to be populated)'])
    words = ' &middot; '.join(bits)
    return f"""
<p>This is Book {letter} of the Swift Lexicon — the encyclopedia-style section of the Bible where every Swift word/operator/punctuation mark gets an entry.</p>

<div class="roll-call">
  <strong>Planned entries:</strong> {words}
</div>

<p>Entry format, cross-linking convention, and whether SwiftUI property wrappers (marked <code>*</code>) live here or in a SwiftUI mini-lexicon are all open questions (see roadmap 3.3, 3.6, 7.6).</p>

<p>This Book is part of <strong>Part I: The Swift Language</strong> — tentative; Part numbering is open question 3.1 in the roadmap (may become "Volume Zero" instead).</p>
"""

def book_body_numbered(num: int, title: str, md_source: str) -> str:
    return f"""
<p>Content for <strong>Book {num:02d}: {title}</strong> currently lives as Markdown at <code>{md_source}</code> in the vault root.</p>

<div class="roll-call">
  <strong>Migration status:</strong> HTML migration from <code>{md_source}</code> is Phase 1 of the roadmap. Until migration, use the Markdown file directly.
</div>

<p>When migration lands, this page gets the full HTML version with embedded figures, cross-references to the Swift Lexicon (Part I), and the rest of the vault. Multimedia scope (images only vs. + video vs. + audio) is open question 3.4.</p>
"""

def appendix_body(letter, title, existing_file):
    if existing_file:
        return f"""
<p>Appendix {letter}: {title[len('Appendix A: '):]} — a build-along walkthrough that ships with the Bible.</p>

<div class="roll-call">
  <strong>Existing file:</strong> <a href="../../{existing_file}">{existing_file}</a> currently holds the content at the vault root. When the Part/Book migration completes, this location becomes the canonical home.
</div>
"""
    else:
        return f"""
<p>Appendix {letter}: {title[len('Appendix A: '):]} — a build-along walkthrough that ships with the Bible.</p>

<div class="roll-call">
  <strong>Status:</strong> Planned. Not yet written.
</div>

<p>This appendix will document the LockBox build-along, referencing the LockBox Xcode project that lives at <code>Claudes-Xcode-26-Swift-Bible/Claudes LockBox/</code>.</p>
"""

# ---------- Build ------------------------------------------------------------

count = 0

# Part I: Lexicon A-Z
for slug, letter, descr in lexicon:
    path = VAULT / "Part-I-The-Swift-Language" / slug / f"{slug}.html"
    write_placeholder(
        path,
        title=f"Book {letter} — The Swift Lexicon",
        status="Status: Placeholder — Book not yet written. Scheduled for Phase 2.",
        body=book_body_lexicon(letter),
    )
    count += 1

# Parts II-VI: numbered Books
for part_num, part_slug, books in numbered:
    part_folder_name = f"Part-{part_roman[part_num]}-{part_slug}"
    for num, slug, title, md in books:
        path = VAULT / part_folder_name / f"Book-{num:02d}-{slug}" / f"Book-{num:02d}-{slug}.html"
        write_placeholder(
            path,
            title=f"Book {num:02d}: {title}",
            status=f"Status: Placeholder — Markdown source exists at <code>{md}</code>; HTML migration is Phase 1.",
            body=book_body_numbered(num, title, md),
        )
        count += 1

# Appendices
for letter, slug, title, existing in appendices:
    path = VAULT / "Appendices" / f"Appendix-{letter}-{slug}" / f"Appendix-{letter}-{slug}.html"
    status = f"Status: Placeholder — existing file at vault root: <code>{existing}</code>" if existing else "Status: Placeholder — not yet written."
    write_placeholder(
        path,
        title=title,
        status=status,
        body=appendix_body(letter, title, existing),
    )
    count += 1

print(f"Wrote {count} placeholder Books/Appendices.")
