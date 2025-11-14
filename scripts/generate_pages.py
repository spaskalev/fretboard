#!/usr/bin/env python3
"""
Read tunings from tunings.txt (one per line), run `fretboard.py <tuning>` for each,
and write the combined output to docs/index.html so it can be published to GitHub Pages.
"""
import os
import subprocess
import sys
import html

TUNINGS_FILE = "tunings.txt"
DOCS_DIR = "docs"
OUT_FILE = os.path.join(DOCS_DIR, "index.html")

HTML_TEMPLATE_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fretboard outputs</title>
<style>
body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; padding: 1rem; max-width: 900px; margin: auto; }
pre { background: #f8f8f8; padding: 1rem; border-radius: 6px; overflow: auto; white-space: pre-wrap; }
h1, h2 { margin-top: 1.25rem; }
.section { margin-bottom: 1.5rem; }
.stderr { color: #b22222; font-weight: 600; }
.meta { color: #666; font-size: 0.9rem; }
</style>
</head>
<body>
<h1>Fretboard outputs</h1>
"""

HTML_TEMPLATE_TAIL = """
</body>
</html>
"""

def write_section(out, tuning, stdout, stderr, returncode):
    out.write(f'<div class="section">\n')
    out.write(f'<h2>{html.escape(tuning)}</h2>\n')
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
    if not os.path.exists(TUNINGS_FILE):
        print(f"Error: {TUNINGS_FILE} not found.", file=sys.stderr)
        sys.exit(1)

    with open(TUNINGS_FILE, "r", encoding="utf-8") as f:
        tunings = [line.strip() for line in f if line.strip()]

    if not tunings:
        print("No tunings found in tunings.txt.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(DOCS_DIR, exist_ok=True)

    with open(OUT_FILE, "w", encoding="utf-8") as out:
        out.write(HTML_TEMPLATE_HEAD)
        for tuning in tunings:
            try:
                proc = subprocess.run(
                    [sys.executable, "fretboard.py", tuning],
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

            write_section(out, tuning, stdout, stderr, returncode)

        out.write(HTML_TEMPLATE_TAIL)

    print(f"Wrote {OUT_FILE}")

if __name__ == "__main__":
    main()