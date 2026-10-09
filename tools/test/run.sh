#!/usr/bin/env bash
# Cross-platform behavior parity for the shipped cache tools. Runs the
# seeded read-only scripts against a synthetic fixture in two line-ending
# variants (LF and CRLF) and asserts: (1) output is byte-identical across
# variants, (2) byte-identical to the checked-in expected outputs, and
# (3) the exit codes the script headers document. No model calls; runs
# anywhere bash + python3 exist (WSL, Linux, macOS, CI). A Windows-host
# leg needs a Windows-native python — the environment finding that
# produced this test in the first place.
set -euo pipefail

PY="${PY:-python3}"
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

fail() { echo "tools-parity: FAIL — $*" >&2; exit 1; }
note() { echo "tools-parity: $*"; }

command -v "$PY" >/dev/null 2>&1 || fail "no $PY on PATH"
FIND="$HERE/../vetted/read-only/find.py"
GREP="$HERE/../vetted/read-only/grep.py"
[ -f "$FIND" ] && [ -f "$GREP" ] || fail "seeded tools not found"

"$PY" "$HERE/make_fixture.py" "$TMP/lf fixture" >/dev/null || fail "fixture (LF) failed"
"$PY" "$HERE/make_fixture.py" --crlf "$TMP/crlf fixture" >/dev/null || fail "fixture (CRLF) failed"

check() {
  # check <name> <expected-file> <wanted-exit> <cmd...>
  local name="$1" expected="$2" want="$3"; shift 3
  local out="$TMP/$name.out" got
  set +e; "$@" > "$out"; got=$?; set -e
  [ "$got" -eq "$want" ] || fail "$name: exit $got, want $want"
  cmp -s "$out" "$expected" || fail "$name: output differs from $expected"
}

for leg in "lf fixture" "crlf fixture"; do
  root="$TMP/$leg"
  note "leg: $leg"
  check find        "$HERE/expected/find.out"       0 "$PY" "$FIND" "$root"
  check find-name   "$HERE/expected/find-name.out"  0 "$PY" "$FIND" "$root" --name '*.txt'
  check find-missing "$HERE/expected/find-missing.out" 1 "$PY" "$FIND" "$root/no-such-dir"
  check grep-fox    "$HERE/expected/grep-fox.out"    0 "$PY" "$GREP" fox "$root"
  check grep-utf8   "$HERE/expected/grep-utf8.out"   0 "$PY" "$GREP" naïve "$root"
  check grep-absent "$HERE/expected/grep-absent.out" 1 "$PY" "$GREP" absent-xyz "$root"
done

note "PASS: both legs byte-identical to expected, exit codes as documented"
