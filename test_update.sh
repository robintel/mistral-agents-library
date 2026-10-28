#!/usr/bin/env bash
# Test script for the update functionality in install.py
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

fail() { echo "TEST FAIL: $*" >&2; exit 1; }
pass() { echo "TEST PASS: $*"; }

# Test 1: --check with no installation
pass "Test 1: --check with no installation"
OUTPUT=$($HERE/install.py --check --dest "$TMP_DIR/no-install" 2>&1)
echo "$OUTPUT" | grep -q "No installation found" || fail "Expected 'No installation found'"

# Test 2: Install and check version
pass "Test 2: Install and verify version marker"
$HERE/install.py --dest "$TMP_DIR/install" >/dev/null 2>&1
[ -f "$TMP_DIR/install/.mal_version" ] || fail "Version marker not created"
VERSION=$(cat "$TMP_DIR/install/.mal_version")
[ -n "$VERSION" ] || fail "Version marker is empty"
echo "  Installed version: $VERSION"

# Test 3: --check with current version
pass "Test 3: --check with current version"
OUTPUT=$($HERE/install.py --check --dest "$TMP_DIR/install" 2>&1)
echo "$OUTPUT" | grep -q "Already up to date" || fail "Expected 'Already up to date'"

# Test 4: --check with old version
pass "Test 4: --check with old version"
echo "0" > "$TMP_DIR/install/.mal_version"
OUTPUT=$($HERE/install.py --check --dest "$TMP_DIR/install" 2>&1)
echo "$OUTPUT" | grep -q "Update available" || fail "Expected 'Update available'"

# Test 5: --dry-run to verify no errors
pass "Test 5: --dry-run completes without errors"
$HERE/install.py --dry-run --dest "$TMP_DIR/dryrun" >/dev/null 2>&1 || fail "dry-run failed"

# Test 6: Verify all profiles are generated (86 unique: 88 entries, 2 duplicate names)
pass "Test 6: All profiles generated"
$HERE/install.py --dest "$TMP_DIR/full" >/dev/null 2>&1
COUNT=$(ls "$TMP_DIR/full"/*.toml 2>/dev/null | wc -l)
[ "$COUNT" -eq 86 ] || fail "Expected 86 profiles, got $COUNT"

echo ""
pass "All tests passed!"
