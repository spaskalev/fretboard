#!/usr/bin/env python3
"""
Read tunings from tunings.txt (one per line), run `fretboard.py <tuning>` for each,
and write the combined output to docs/index.md so it can be published to GitHub Pages.
"""
import os
import subprocess
import sys

TUNINGS_FILE = "tunings.txt"
DOCS_DIR = "docs"
OUT_FILE = os.path.join(DOCS_DIR, "index.md")

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
        out.write("# Fretboard outputs\n\n")
        for tuning in tunings:
            out.write(f"## {tuning}\n\n")
            out.write("```\n")
            try:
                proc = subprocess.run(
                    [sys.executable, "fretboard.py", tuning],
                    capture_output=True,
                    text=True,
                )
                if proc.stdout:
                    out.write(proc.stdout)
                if proc.stderr:
                    out.write("\n# STDERR:\n")
                    out.write(proc.stderr)
                if proc.returncode != 0:
                    out.write(f"\n# Exit code: {proc.returncode}\n")
            except FileNotFoundError:
                out.write("Error: fretboard.py not found in repository root.\n")
            except Exception as e:
                out.write(f"Error running fretboard.py: {e}\n")
            out.write("```\n\n")

    print(f"Wrote {OUT_FILE}")

if __name__ == "__main__":
    main()