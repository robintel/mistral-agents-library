#!/usr/bin/env bash
# Windows-installer parity test: install.ps1 (under the
# cross-platform pwsh) and install.py must compose byte-identical
# profile batches from the same manifest — the release test
# DEPLOYING.md names, made executable. No model calls, no API key:
# pure composition, so it runs anywhere the image runs.
#
# Scope, honestly: on identical Linux paths this proves the two
# composition engines agree byte for byte. It cannot cover
# Windows-native behavior — backslash library paths, ANSI decoding,
# ExecutionPolicy — that needs the future windows-latest CI job.
set -euo pipefail

LIBRARY="${LIBRARY:-/library}"

fail() { echo "parity: FAIL — $*" >&2; exit 1; }
note() { echo "parity: $*"; }

[ -f "$LIBRARY/manifest.yaml" ] || fail "library not mounted at $LIBRARY"

PY_DEST="$HOME/parity-python"
PS_DEST="$HOME/parity-powershell"
rm -rf "$PY_DEST" "$PS_DEST"

# 1. Both installers, same manifest, separate destinations.
python3 "$LIBRARY/install.py" --dest "$PY_DEST"
pwsh -NoProfile -File "$LIBRARY/install.ps1" -Dest "$PS_DEST"

# 2. Same batch shape.
py_count=$(ls "$PY_DEST" | wc -l)
ps_count=$(ls "$PS_DEST" | wc -l)
[ "$py_count" -gt 0 ] || fail "install.py wrote no profiles"
[ "$py_count" -eq "$ps_count" ] \
  || fail "profile counts differ: python $py_count vs powershell $ps_count"

# 3. Byte-identical content.
if diff -r "$PY_DEST" "$PS_DEST" > /tmp/parity-diff.txt; then
  note "PASS — byte-identical: $py_count profiles, both installers"
else
  head -20 /tmp/parity-diff.txt >&2
  fail "batches differ — first 20 diff lines above"
fi
