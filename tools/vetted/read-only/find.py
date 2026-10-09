#!/usr/bin/env python3
"""purpose:   portable recursive file listing — one verb: list files
provenance: shipped in mistral-agents-library; verified by tools/test/run.sh
runtime:    python 3.7+, stdlib only
data:       clean

interface:  find.py ROOT [--name GLOB]
            output: relative POSIX paths, sorted, LF line endings
            exit:   0 listed, 1 root missing, 2 usage error

Skips .git directories. Output is byte-identical on every platform:
paths are POSIX-normalized, stdout is forced to UTF-8 with LF endings.
"""
import fnmatch
import sys
from pathlib import Path


def fail_usage(message):
    print(f"find.py: {message}", file=sys.stderr)
    raise SystemExit(2)


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    root = None
    pattern = None
    i = 0
    while i < len(argv):
        if argv[i] == "--name":
            if i + 1 >= len(argv):
                fail_usage("--name needs a glob")
            pattern = argv[i + 1]
            i += 2
        elif argv[i].startswith("-"):
            fail_usage(f"unknown option {argv[i]}")
        elif root is None:
            root = argv[i]
            i += 1
        else:
            fail_usage("one ROOT only")
    if root is None:
        fail_usage("usage: find.py ROOT [--name GLOB]")

    base = Path(root)
    if not base.is_dir():
        print(f"find.py: no such directory: {root}", file=sys.stderr)
        return 1

    results = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(base).as_posix()
        if any(part == ".git" for part in path.relative_to(base).parts):
            continue
        if pattern and not fnmatch.fnmatchcase(rel, pattern):
            continue
        results.append(rel)
    for rel in sorted(results):
        print(rel)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
