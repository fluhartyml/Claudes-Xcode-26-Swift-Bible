#!/usr/bin/env python3
"""
Proofing HTML generator for Swift Bible book.
Usage: python3 make-proof.py <source.md> <output.html> [highlight_lines]
  highlight_lines: comma-separated list like "3,5,10-15" or "all" or empty

Reads figure-map.json (same dir) to embed images for [Fig. W.N — ...] lines.
"""
import sys, html, pathlib, json, re, datetime

FIG_RE = re.compile(r"\[Fig\.\s+(W\.\d+[a-z]?)\s*[—-]\s*([^\]]+)\]")

def render_md_line(line):
    """Render a single markdown line to HTML, preserving one-row-per-line.
    Does inline formatting + simple block detection for headings and bullets."""
    stripped = line.strip()
    if not stripped:
        return "&nbsp;"

    # Headings: ## Title
    m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
    if m:
        level = len(m.group(1))
        inner = render_inline(m.group(2))
        return f'<span class="h h{level}">{inner}</span>'

    # Horizontal rule
    if stripped == "---":
        return '<span class="hr">— — — — — — — — — —</span>'

    # Post-it callout: > text
    m = re.match(r"^>\s*(.*)$", stripped)
    if m:
        inner = render_inline(m.group(1)) if m.group(1) else "&nbsp;"
        return f'<span class="postit">📌 {inner}</span>'

    # Bullet item: - item or * item
    m = re.match(r"^(\s*)[-*]\s+(.*)$", line)
    if m:
        indent = m.group(1)
        inner = render_inline(m.group(2))
        return f'{html.escape(indent)}<span class="bullet">•</span> {inner}'

    # Numbered list: 13.1 text  or  1. text
    m = re.match(r"^(\d+\.(?:\d+)?)\s+(.*)$", stripped)
    if m:
        num = m.group(1)
        inner = render_inline(m.group(2))
        return f'<span class="listnum">{html.escape(num)}</span> {inner}'

    return render_inline(line)

def render_inline(text):
    """Inline markdown → HTML. Order matters (code before bold before italic)."""
    # Escape first, then apply markdown replacements on the escaped text.
    s = html.escape(text)
    # Inline code `...`
    s = re.sub(r"`([^`]+)`", r'<code>\1</code>', s)
    # Bold **...**
    s = re.sub(r"\*\*([^*]+)\*\*", r'<strong>\1</strong>', s)
    # Italic *...* (single asterisks, avoiding collision with bold already converted)
    s = re.sub(r"(?<!\*)\*([^*\s][^*]*?)\*(?!\*)", r'<em>\1</em>', s)
    return s

def parse_highlights(spec, total):
    if not spec:
        return set()
    if spec.strip().lower() == "all":
        return set(range(1, total + 1))
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return out

def main():
    src = pathlib.Path(sys.argv[1])
    dst = pathlib.Path(sys.argv[2])
    spec = sys.argv[3] if len(sys.argv) > 3 else ""
    lines = src.read_text().splitlines()

    # Persistent highlights: accumulate across refreshes unless spec starts with !
    state_path = dst.with_suffix(".highlights.json")
    reset = spec.startswith("!")
    if reset:
        spec = spec[1:]
    prior = set()
    if state_path.exists() and not reset:
        try:
            prior = set(json.loads(state_path.read_text()))
        except Exception:
            prior = set()
    new_hl = parse_highlights(spec, len(lines))
    hl = prior | new_hl
    state_path.write_text(json.dumps(sorted(hl)))

    map_path = pathlib.Path(__file__).parent / "figure-map.json"
    fig_map = json.loads(map_path.read_text()) if map_path.exists() else {}

    rows = []
    for i, line in enumerate(lines, start=1):
        cls = "hl" if i in hl else ""
        rendered = render_md_line(line)
        rows.append(
            f'<tr class="{cls}"><td class="num">{i}</td>'
            f'<td class="prose">{rendered}</td></tr>'
        )
        m = FIG_RE.search(line)
        if m:
            fig_id, caption = m.group(1), m.group(2).strip()
            img_path = fig_map.get(fig_id)
            resolved = (dst.parent / img_path) if img_path else None
            if resolved and resolved.exists():
                rows.append(
                    f'<tr class="fig"><td class="num">&nbsp;</td>'
                    f'<td class="prose"><div class="figbox">'
                    f'<div class="figlabel">{fig_id} &mdash; {html.escape(caption)}</div>'
                    f'<img src="{html.escape(img_path)}" alt="{html.escape(caption)}"></div></td></tr>'
                )
            else:
                rows.append(
                    f'<tr class="fig-missing"><td class="num">&nbsp;</td>'
                    f'<td class="prose"><div class="figbox missing">'
                    f'<div class="figlabel">{fig_id} &mdash; NOT YET ASSIGNED</div>'
                    f'</div></td></tr>'
                )

    # Derive header/footer content
    book_title = "Claude's Xcode 26 Swift Bible"
    # Try to pull the first H1/H2 from the source as section title
    section_title = src.stem.replace("-", " ").title()
    for ln in lines:
        m = re.match(r"^#{1,2}\s+(.*)$", ln.strip())
        if m:
            section_title = m.group(1)
            break
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    page = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{html.escape(src.name)}</title>
<style>
  @font-face {{
    font-family: 'FiraCode Nerd Font';
    src: url('../OEBPS/FiraCodeNerdFont-Regular.ttf') format('truetype');
    font-weight: normal; font-style: normal;
  }}
  @font-face {{
    font-family: 'FiraCode Nerd Font';
    src: url('../OEBPS/FiraCodeNerdFont-Bold.ttf') format('truetype');
    font-weight: bold; font-style: normal;
  }}
  body {{ font-family: 'FiraCode Nerd Font', monospace; font-size: 18pt;
         line-height: 1.6; margin: 0; padding: 60px 24px 50px;
         background: #000; color: #4ec94e; }}
  header.book, footer.book {{
    position: fixed; left: 0; right: 0; z-index: 10;
    background: #000; border-color: #1e2a1e;
    font-family: -apple-system, sans-serif; font-size: 11pt;
    color: #7a7; padding: 8px 24px;
    display: flex; justify-content: space-between; align-items: center;
  }}
  header.book {{ top: 0; border-bottom: 1px solid #1e2a1e; }}
  footer.book {{ bottom: 0; border-top: 1px solid #1e2a1e; }}
  header.book .title {{ font-weight: bold; color: #8fff8f; }}
  header.book .section {{ font-style: italic; color: #6a8a6a; }}
  footer.book .meta {{ color: #385a38; }}
  h1.banner {{ font-size: 12pt; margin: 0 0 24px; color: #7a7;
             font-family: -apple-system, sans-serif; font-weight: normal; }}
  table {{ border-collapse: collapse; width: 100%; max-width: 1000px;
          table-layout: fixed; }}
  td {{ padding: 2px 14px; vertical-align: top; }}
  td.num {{ color: #385a38; text-align: right; user-select: none;
           border-right: 1px solid #1e2a1e; width: 48px;
           font-family: ui-monospace, Menlo, monospace; font-size: 11pt;
           padding-top: 8px; }}
  td.prose {{ white-space: normal; word-wrap: break-word;
             overflow-wrap: anywhere; }}
  tr.hl td.prose {{ background: #3a3400; color: #ffe066; }}
  tr.hl td.num {{ background: #5a4f00; color: #ffd633; }}
  tr.hl td.prose strong {{ color: #fff4a8; }}
  tr.hl td.prose code {{ background: #2a2a10; color: #ffe066; }}
  .h {{ font-family: 'FiraCode Nerd Font', monospace; font-weight: bold; color: #8fff8f; }}
  .h1 {{ font-size: 28pt; }}
  .h2 {{ font-size: 22pt; }}
  .h3 {{ font-size: 19pt; }}
  .hr {{ color: #2a4a2a; letter-spacing: 4px; }}
  .bullet {{ color: #6a8a6a; margin-right: 4px; }}
  .listnum {{ font-weight: bold; color: #8fff8f; margin-right: 6px; }}
  code {{ font-family: 'FiraCode Nerd Font', monospace; font-size: 16pt;
         background-color: #0f1a0f; padding: 2px 6px; border-radius: 3px;
         color: #a8e8a8; border: 1px solid #1e2a1e; }}
  strong {{ color: #b8ffb8; }}
  em {{ color: #7ed67e; font-style: italic; }}
  .postit {{ display: block; background: #3a3400; border-left: 5px solid #e0c000;
           padding: 10px 14px; margin: 6px 0; border-radius: 3px;
           box-shadow: 1px 2px 6px rgba(255,220,0,0.15);
           font-size: 16pt; line-height: 1.5; color: #ffe066; }}
  .postit strong {{ color: #fff4a8; }}
  .figbox {{ margin: 1.5em 0; text-align: center; }}
  .figbox.missing {{ padding: 12px; background: #f5f5f5;
                   border: 1px dashed #bbb; color: #888;
                   border-radius: 6px; }}
  .figlabel {{ font-size: 14pt; color: #888; font-style: italic;
             margin-top: 0.5em;
             font-family: 'FiraCode Nerd Font', monospace; }}
  .figbox img {{ max-width: 100%; height: auto; display: block;
               margin: 0 auto; border-radius: 6px; }}
</style></head><body>
<header class="book">
  <span class="title">{html.escape(book_title)}</span>
  <span class="section">{html.escape(section_title)}</span>
</header>
<h1 class="banner">{html.escape(str(src))} &mdash; proofing view (line numbers and yellow highlights are for review only — not in the published book)</h1>
<table>{''.join(rows)}</table>
<footer class="book">
  <span class="meta">{html.escape(src.name)}</span>
  <span class="meta">rendered {stamp} &middot; {len(lines)} lines &middot; {len(hl)} highlighted</span>
</footer>
</body></html>"""
    dst.write_text(page)
    print(f"wrote {dst} ({len(lines)} lines, {len(hl)} highlighted)")

if __name__ == "__main__":
    main()
