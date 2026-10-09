#!/usr/bin/env python3
"""purpose:   portable recursive content search — one verb: search files
provenance: shipped in mistral-agents-library; verified by tools/test/run.sh
runtime:    python 3.7+, stdlib only
data:       clean

interface:  grep.py PATTERN ROOT
            output: path:lineno:line — POSIX paths, LF endings, sorted
            exit:   0 matches found, 1 no matches, 2 error (bad pattern,
                    missing root, usage)

PATTERN is a Python regular expression. Skips .git directories and
binary files (a NUL byte marks binary). Output is byte-identical on
every platform: paths are POSIX-normalized, stdout is forced to UTF-8
with LF endings, sorting is on the path string, not the OS collation.
"""
import re
import sys
from pathlib import Path


def fail_usage(message):
    print(f"grep.py: {message}", file=sys.stderr)
    raise SystemExit(2)


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if len(argv) != 2:
        fail_usage("usage: grep.py PATTERN ROOT")
    pattern_text, root = argv
    try:
        pattern = re.compile(pattern_text)
    except re.error as error:
        fail_usage(f"bad pattern: {error}")

    base = Path(root)
    if not base.is_dir():
        print(f"grep.py: no such directory: {root}", file=sys.stderr)
        return 2

    files = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(base)
        if any(part == ".git" for part in rel.parts):
            continue
        files.append(rel.as_posix())

    matches = 0
    for rel in sorted(files):
        data = (base / rel).read_bytes()
        if b"\x00" in data:
            continue
        text = data.decode("utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                print(f"{rel}:{lineno}:{line}")
                matches += 1
    return 0 if matches else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
