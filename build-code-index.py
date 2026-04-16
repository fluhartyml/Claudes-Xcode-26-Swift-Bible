#!/usr/bin/env python3
"""
Swift Bible Code Index Generator
=================================
Scans all chapter markdown files for fenced code blocks, extracts every
Swift symbol automatically (no curated list), and generates a cross-
referenced code index (code-index.md) with epub-compatible anchor refs.

Run after any chapter edit to regenerate the index:
    python3 build-code-index.py

Output: code-index.md (in the same directory as this script)
"""

import re
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent

# Chapter files in order
CHAPTER_FILES = [
    ("01", "01-Introducing-Swift-And-Xcode.md"),
    ("02", "02-Introducing-SwiftUI-Views.md"),
    ("03", "03-Introducing-Scenes-And-Windows.md"),
    ("04", "04-Gestures-And-Input.md"),
    ("05", "05-Menus-And-Navigation.md"),
    ("06", "06-Controls-Buttons-Toggles-Pickers.md"),
    ("07", "07-Toolbars-And-Tab-Views.md"),
    ("08", "08-Lists-Grids-And-ForEach.md"),
    ("09", "09-Text-And-TextField.md"),
    ("10", "10-TextEditor-And-AttributedString.md"),
    ("11", "11-FileManager-And-Documents.md"),
    ("12", "12-Sheets-Alerts-And-Confirmations.md"),
    ("13", "13-Multi-Window-And-NavigationSplitView.md"),
    ("14", "14-Clipboard-DragDrop-ShareSheet.md"),
    ("15", "15-SwiftData-And-CoreData.md"),
    ("16", "16-Extensions-And-Packages.md"),
    ("17", "17-Swift-Charts-And-PDFKit.md"),
    ("18", "18-Error-Handling-And-Result-Type.md"),
    ("19", "19-Building-Custom-Views-And-Modifiers.md"),
    ("20", "20-Performance-Instruments-And-Best-Practices.md"),
    ("21", "21-Git-And-GitHub.md"),
    ("22", "22-AI-Chatbot-Integration.md"),
    ("A", "appendix-github-setup.md"),
    ("B", "appendix-wraply.md"),
    ("C", "appendix-quicknote.md"),
]

CHAPTER_NAMES = {
    "01": "Ch 1", "02": "Ch 2", "03": "Ch 3", "04": "Ch 4",
    "05": "Ch 5", "06": "Ch 6", "07": "Ch 7", "08": "Ch 8",
    "09": "Ch 9", "10": "Ch 10", "11": "Ch 11", "12": "Ch 12",
    "13": "Ch 13", "14": "Ch 14", "15": "Ch 15", "16": "Ch 16",
    "17": "Ch 17", "18": "Ch 18", "19": "Ch 19", "20": "Ch 20",
    "21": "Ch 21", "22": "Ch 22",
    "A": "App A", "B": "App B", "C": "App C",
}

# ── Noise filter ──────────────────────────────────────────────────────
# Common English words and trivial tokens that appear in Swift code
# but add no value to a code index. Everything else gets indexed.
NOISE = {
    # Articles, prepositions, conjunctions
    "a", "an", "the", "of", "to", "is", "it", "on", "at", "by",
    "or", "and", "not", "no", "so", "as", "be", "do", "up",
    # Trivial single-char and very short tokens
    "i", "j", "k", "x", "y", "n", "s", "t", "id",
    # Common variable names that aren't meaningful as index entries
    "body", "content", "item", "items", "value", "values",
    "name", "title", "text", "message", "label", "description",
    "index", "count", "result", "error", "type", "key",
    "width", "height", "size", "color", "font", "image",
    "action", "handler", "closure", "block", "callback",
    "new", "old", "current", "selected", "active",
    "first", "last", "next", "previous", "top", "bottom",
    "left", "right", "center", "leading", "trailing",
    "min", "max", "total", "offset", "padding",
    "row", "column", "section", "header", "footer",
    "start", "end", "begin", "stop", "done", "cancel",
    "show", "hide", "open", "close", "add", "remove", "delete",
    "get", "set", "update", "save", "load", "fetch", "create",
    "data", "string", "number", "date", "url", "path", "file",
    # Swift literals and trivial keywords (too common to be useful)
    "true", "false", "nil", "self", "super",
    "var", "let", "func", "return", "if", "else", "for", "in",
    "do", "try", "catch", "throw", "throws",
    "case", "switch", "break", "continue", "default",
    "while", "repeat", "where",
    # Comment words
    "mark", "todo", "fixme", "note",
    # String content / print
    "print", "hello", "world",
}

# Minimum length for a plain word to be indexed (filters out "ok", "go", etc.)
MIN_WORD_LENGTH = 3


def extract_code_blocks(content):
    """Extract all fenced code blocks from markdown content.
    Returns list of (start_line, end_line, language, code_text)."""
    blocks = []
    lines = content.split("\n")
    in_block = False
    block_start = 0
    block_lang = ""
    block_lines = []

    for i, line in enumerate(lines, 1):
        if not in_block and re.match(r"^```(\w*)", line):
            in_block = True
            block_start = i
            block_lang = re.match(r"^```(\w*)", line).group(1)
            block_lines = []
        elif in_block and line.strip() == "```":
            in_block = False
            blocks.append((block_start, i, block_lang, "\n".join(block_lines)))
        elif in_block:
            block_lines.append(line)

    return blocks


def extract_symbols(code_text):
    """Extract every meaningful Swift symbol from a code block.
    No curated list — indexes anything that looks like code."""
    found = set()

    # 1. Property wrappers: @State, @Binding, @Observable, etc.
    for match in re.finditer(r"@[A-Z]\w+", code_text):
        found.add(match.group())

    # 2. Dot-prefixed modifiers/methods: .sheet, .font, .navigationTitle, etc.
    #    Only capture the first segment (e.g., .foregroundStyle not .foregroundStyle.blue)
    for match in re.finditer(r"\.([a-z][a-zA-Z0-9]+)", code_text):
        modifier = "." + match.group(1)
        # Skip very short ones like .id, .to — not useful index entries
        if len(match.group(1)) >= 3:
            found.add(modifier)

    # 3. Capitalized type names: Button, NavigationStack, CryoTunesKit, etc.
    #    Catches PascalCase types, structs, classes, enums, protocols
    for match in re.finditer(r"\b([A-Z][a-zA-Z0-9]+)\b", code_text):
        token = match.group(1)
        # Skip ALL_CAPS constants (like MARK, TODO)
        if not token.isupper():
            found.add(token)

    # 4. Compiler directives: #Preview, #if, #available, etc.
    for match in re.finditer(r"#[a-zA-Z]\w+", code_text):
        found.add(match.group())

    # 5. Swift keywords that are meaningful for an index
    #    (only the ones readers would actually look up)
    swift_indexed_keywords = {
        "import", "struct", "class", "enum", "protocol", "extension",
        "typealias", "associatedtype",
        "public", "private", "internal", "fileprivate", "open",
        "static", "override", "mutating", "inout",
        "some", "any", "async", "await", "actor",
        "defer", "guard", "fallthrough",
        "@main",
    }
    for kw in swift_indexed_keywords:
        if kw.startswith("@"):
            if kw in code_text:
                found.add(kw)
        else:
            if re.search(rf"\b{kw}\b", code_text):
                found.add(kw)

    # 6. Remove noise
    cleaned = set()
    for sym in found:
        # Strip prefix for noise check
        bare = sym.lstrip("@.#").lower()
        if bare in NOISE:
            continue
        if not sym.startswith(("@", ".", "#")) and len(sym) < MIN_WORD_LENGTH:
            continue
        cleaned.add(sym)

    return cleaned


def categorize_symbol(symbol):
    """Return a category string for sorting/grouping."""
    if symbol.startswith("@"):
        return "Property Wrappers & Macros"
    elif symbol.startswith("."):
        return "View Modifiers & Methods"
    elif symbol.startswith("#"):
        return "Compiler Directives"
    else:
        # Check if it's a Swift keyword (lowercase)
        if symbol[0].islower():
            return "Swift Keywords"
        else:
            return "Types, Protocols & APIs"


def sort_key(symbol):
    """Sort key: strip prefix, lowercase for alphabetical."""
    clean = symbol.lstrip("@.#")
    return clean.lower()


def build_index():
    """Main: scan all chapters, build and write the code index."""
    # symbol -> list of (chapter_id, snippet_number, line_start)
    index = defaultdict(list)
    chapter_snippet_counts = {}

    for ch_id, filename in CHAPTER_FILES:
        filepath = SCRIPT_DIR / filename
        if not filepath.exists():
            continue

        content = filepath.read_text(encoding="utf-8")
        if not content.strip():
            chapter_snippet_counts[ch_id] = 0
            continue

        blocks = extract_code_blocks(content)
        chapter_snippet_counts[ch_id] = len(blocks)

        for snippet_num, (start_line, end_line, lang, code_text) in enumerate(blocks, 1):
            symbols = extract_symbols(code_text)
            for sym in symbols:
                ref = (ch_id, snippet_num, start_line)
                if ref not in index[sym]:
                    index[sym].append(ref)

    # Group by category
    categories = defaultdict(dict)
    for symbol, refs in index.items():
        cat = categorize_symbol(symbol)
        categories[cat][symbol] = refs

    # Category display order
    cat_order = [
        "Property Wrappers & Macros",
        "Swift Keywords",
        "Compiler Directives",
        "View Modifiers & Methods",
        "Types, Protocols & APIs",
    ]

    total_entries = len(index)
    total_snippets = sum(chapter_snippet_counts.values())

    lines = []
    lines.append("# Code Index")
    lines.append("")
    lines.append("**Every Swift symbol in this book — types, modifiers, property wrappers,")
    lines.append("keywords, and APIs — cross-referenced by chapter and snippet number.**")
    lines.append("")
    lines.append(f"*{total_entries} indexed symbols across {total_snippets} code snippets.*")
    lines.append("")
    lines.append("Reference format: **Ch N–S** = Chapter N, Snippet S")
    lines.append("(e.g., Ch 6–3 = Chapter 6, Snippet 3)")
    lines.append("")
    lines.append("In the epub edition, each reference is a hyperlink to the snippet.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Stats table
    lines.append("## Snippet Counts by Chapter")
    lines.append("")
    lines.append("| Chapter | Snippets |")
    lines.append("|---------|----------|")
    for ch_id, _ in CHAPTER_FILES:
        count = chapter_snippet_counts.get(ch_id, 0)
        name = CHAPTER_NAMES.get(ch_id, ch_id)
        if count > 0:
            lines.append(f"| {name} | {count} |")
    lines.append(f"| **Total** | **{total_snippets}** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    for cat in cat_order:
        if cat not in categories:
            continue

        symbols = categories[cat]
        lines.append(f"## {cat}")
        lines.append("")

        for symbol in sorted(symbols.keys(), key=sort_key):
            refs = symbols[symbol]
            refs.sort(key=lambda r: (r[0], r[1]))
            ref_strs = []
            for ch_id, snippet_num, start_line in refs:
                name = CHAPTER_NAMES.get(ch_id, ch_id)
                ref_strs.append(f"{name}–{snippet_num}")
            refs_joined = ", ".join(ref_strs)
            lines.append(f"**`{symbol}`** — {refs_joined}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Write file
    output = SCRIPT_DIR / "code-index.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Code index written to {output}")
    print(f"  {total_entries} symbols indexed")
    print(f"  {total_snippets} code snippets across "
          f"{sum(1 for c in chapter_snippet_counts.values() if c > 0)} chapters")


if __name__ == "__main__":
    build_index()
