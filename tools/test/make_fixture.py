#!/usr/bin/env python3
"""Generates the synthetic cross-platform fixture for tools/test/run.sh:
fixed bytes, two line-ending variants (LF and CRLF), UTF-8 content, a
binary file, a nested file, and a .git directory that must be skipped.
Synthetic by design — the data gate applies to fixtures too."""
import argparse
from pathlib import Path

TEXT_FILES = {
    "readme.txt": "the quick brown fox\njumps over the lazy dog\n",
    "notes.md": "naïve — résumé\nsecond line, crlf variant below\n",
    "nested/sub/deep.txt": "a needle hides here\n",
}
BINARY_FILES = {
    "binary.bin": b"\x00\x01binary\x00\n",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dest")
    parser.add_argument("--crlf", action="store_true")
    args = parser.parse_args()

    dest = Path(args.dest)
    eol = "\r\n" if args.crlf else "\n"
    for rel, content in TEXT_FILES.items():
        path = dest / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.replace("\n", eol).encode("utf-8"))
    for rel, content in BINARY_FILES.items():
        path = dest / rel
        path.write_bytes(content)
    git_config = dest / ".git" / "config"
    git_config.parent.mkdir(parents=True, exist_ok=True)
    git_config.write_bytes(("[core]\n").replace("\n", eol).encode("utf-8"))
    print(f"fixture written: {dest} (eol={'CRLF' if args.crlf else 'LF'})")


if __name__ == "__main__":
    main()
