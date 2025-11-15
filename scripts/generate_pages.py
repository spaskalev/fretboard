#!/usr/bin/env python3
"""
Read tunings from tunings.csv (three columns: notes,name,comment),
run `fretboard.py <notes>` for each, and write the combined output
to docs/index.html so it can be published to GitHub Pages.
"""
import os
import subprocess
import sys
import csv
import html
import re
from typing import List, Dict

TUNINGS_FILE = "tunings.csv"
DOCS_DIR = "docs"
OUT_FILE = os.path.join(DOCS_DIR, "index.html")

HTML_TEMPLATE_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lap steel tuning charts</title>
<style>
body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; padding: 1rem; max-width: 960px; margin: auto; }
pre { background: #f8f8f8; padding: 1rem; border-radius: 6px; overflow: auto; white-space: pre-wrap; }
h1, h2 { margin-top: 1.25rem; }
.section { margin-bottom: 1.5rem; }
.stderr { color: #b22222; font-weight: 600; }
.meta { color: #666; font-size: 0.9rem; margin-bottom: 0.5rem; }
.tuning-header { display:flex; gap:1rem; align-items:baseline; flex-wrap:wrap; }
.tuning-notes { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", monospace; font-weight:600; }
@media print {
    .pagebreak { page-break-before: always; } /* page-break-after works, as well */
}
</style>
</head>
<body>
<h1>Lap steel tuning charts</h1>
"""
HTML_TEMPLATE_TAIL = """
</body>
</html>
"""

def parse_tunings_csv(path: str) -> List[Dict[str, str]]:
    """
    Support either a CSV with headers (notes,name,comment) or a headerless CSV with
    columns in that order. Returns list of dicts with keys: notes, name, comment.
    """
    if not os.path.exists(path):
        print(f"Error: {path} not found.", file=sys.stderr)
        sys.exit(1)

    tunings = []
    with open(path, newline='', encoding='utf-8') as f:
        # Peek first row to detect header
        reader = csv.reader(f)
        all_rows = [row for row in reader if any(cell.strip() for cell in row)]
    if not all_rows:
        return tunings

    first = [c.strip().lower() for c in all_rows[0]]
    has_header = any(c in ("notes", "name", "comment") for c in first)

    if has_header:
        # Use DictReader to handle headers with varying order/casing
        with open(path, newline='', encoding='utf-8') as f:
            dict_reader = csv.DictReader(f)
            for r in dict_reader:
                notes = (r.get('notes') or r.get('Notes') or r.get('NOTES') or "").strip()
                name = (r.get('name') or r.get('Name') or r.get('NAME') or "").strip()
                comment = (r.get('comment') or r.get('Comment') or r.get('COMMENT') or "").strip()
                if notes:
                    tunings.append({"notes": notes, "name": name, "comment": comment})
    else:
        # Headerless: expect columns in order: notes, name, comment
        for row in all_rows:
            notes = row[0].strip() if len(row) >= 1 else ""
            name = row[1].strip() if len(row) >= 2 else ""
            comment = row[2].strip() if len(row) >= 3 else ""
            if notes:
                tunings.append({"notes": notes, "name": name, "comment": comment})

    return tunings

def _make_id(base: str, index: int) -> str:
    """Create a URL-safe, mostly human-readable id for an anchor.
    Append the index to guarantee uniqueness.
    """
    slug = re.sub(r"\s+", "-", base)
    # Keep only letters, numbers, dashes and underscores
    slug = re.sub(r"[^A-Za-z0-9\-_]", "", slug)
    slug = slug.strip("-_").lower()
    if not slug:
        slug = f"tuning-{index+1}"
    else:
        slug = f"{slug}-{index+1}"
    return slug

def write_section(out, tuning: Dict[str, str], stdout: str, stderr: str, returncode, section_id: str):
    notes = tuning.get("notes", "")
    name = tuning.get("name", "")
    comment = tuning.get("comment", "")

    out.write('<div class="pagebreak"> </div>')
    out.write(f'<div class="section" id="{html.escape(section_id)}">\n')
    out.write(f'<div class="tuning-header">\n')
    # Show name (if present) and notes prominently
    if name:
        out.write(f'<h2>{html.escape(name)}</h2>\n')
    out.write(f'<div class="tuning-notes">{html.escape(notes)}</div>\n')
    out.write('</div>\n')
    if comment:
        out.write(f'<div class="meta">{html.escape(comment)}</div>\n')
    if stdout:
        out.write('<pre>\n')
        out.write(html.escape(stdout))
        out.write('\n</pre>\n')
    if stderr:
        out.write('<div class="meta stderr">STDERR:</div>\n')
        out.write('<pre>\n')
        out.write(html.escape(stderr))
        out.write('\n</pre>\n')
    if returncode is not None and returncode != 0:
        out.write(f'<div class="meta">Exit code: {returncode}</div>\n')
    out.write('</div>\n')

def main():
    tunings = parse_tunings_csv(TUNINGS_FILE)
    if not tunings:
        print(f"No tunings found in {TUNINGS_FILE}.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(DOCS_DIR, exist_ok=True)

    # Precompute section ids to use in the table of contents and sections
    section_ids = []
    for i, t in enumerate(tunings):
        base = t.get('name') or t.get('notes') or f'tuning-{i+1}'
        section_ids.append(_make_id(base, i))

    with open(OUT_FILE, "w", encoding="utf-8") as out:
        out.write(HTML_TEMPLATE_HEAD)

        # Write a Table of Contents linking to each tuning section
        out.write('<nav>\n')
        out.write('<h2>Contents</h2>\n')
        out.write('<ul>\n')
        for i, t in enumerate(tunings):
            text = t.get('name') or t.get('notes') or f'Tuning {i+1}'
            out.write(f'<li><a href="#{html.escape(section_ids[i])}">{html.escape(text)}</a></li>\n')
        out.write('</ul>\n')
        out.write('</nav>\n')

        for i, tuning in enumerate(tunings):
            notes = tuning.get("notes", "")
            try:
                proc = subprocess.run(
                    [sys.executable, "fretboard.py", notes],
                    capture_output=True,
                    text=True,
                )
                stdout = proc.stdout or ""
                stderr = proc.stderr or ""
                returncode = proc.returncode
            except FileNotFoundError:
                stdout = ""
                stderr = "Error: fretboard.py not found in repository root.\n"
                returncode = None
            except Exception as e:
                stdout = ""
                stderr = f"Error running fretboard.py: {e}\n"
                returncode = None

            write_section(out, tuning, stdout, stderr, returncode, section_ids[i])

        out.write(HTML_TEMPLATE_TAIL)

    print(f"Wrote {OUT_FILE}")

if __name__ == "__main__":
    main()