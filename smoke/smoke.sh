#!/usr/bin/env bash
# Clean-room smoke test for the agent library.
#
# Runs inside the smoke image (smoke/Dockerfile): HOME is the
# container's, the library mounts read-only, and everything dies with
# the container. Nothing on any host is touched.
#
# Shape assertions, not prose: the model's exact words are
# nondeterministic; what must hold every time is the shape of the run.
#
# Env knobs (all optional):
#   MISTRAL_API_KEY  required — passed with -e, never baked
#   TARGET_URL       clone a fixture repo instead of the default
#                    target (the library itself — known ground truth)
#   MAX_TURNS        bound the agent's turns        (default 12)
#   TIMEOUT_SECS     bound wall time                (default 300)
set -euo pipefail

LIBRARY="${LIBRARY:-/library}"
MAX_TURNS="${MAX_TURNS:-12}"
TIMEOUT_SECS="${TIMEOUT_SECS:-300}"

fail() { echo "smoke: FAIL — $*" >&2; exit 1; }
note() { echo "smoke: $*"; }

[ -f "$LIBRARY/manifest.yaml" ] || fail "library not mounted at $LIBRARY"
[ -n "${MISTRAL_API_KEY:-}" ] || fail "MISTRAL_API_KEY not set — pass it with -e"

# 1. Install the profiles into this container's HOME, nowhere else.
python3 "$LIBRARY/install.py"
profiles="$(ls "$HOME"/.vibe/agents/ | wc -l)"
[ -f "$HOME/.vibe/agents/orchestrator.toml" ] \
  || fail "install.py wrote no orchestrator profile"
note "installed $profiles agent profiles"

# 2. The target repo. Default: the library itself — the expected
#    answer is known, so the assertion is checkable, not a matter of
#    taste. A read-only mount doubles as enforcement: no write the
#    agent attempts can land in the thing under test.
if [ -n "${TARGET_URL:-}" ]; then
  TARGET=/tmp/target
  git clone --depth 1 --quiet "$TARGET_URL" "$TARGET"
  WRITABLE_TARGET=1
else
  TARGET="$LIBRARY"
  WRITABLE_TARGET=0
fi

# 3. The run: programmatic mode (docs.mistral.ai, Vibe Code > CLI >
# Work with the CLI), our orchestrator profile, bounded turns and
# wall time — a blocked approval prompt fails loudly here instead
# of hanging CI.
START=$(date +%s)
cd "$TARGET"
set +e
timeout "$TIMEOUT_SECS" vibe --agent orchestrator \
  --prompt "What does this repository do? Answer in under 200 words." \
  --max-turns "$MAX_TURNS" \
  --output text \
  --trust > /tmp/smoke-answer.txt 2>/tmp/smoke-stderr.txt
RC=$?
set -e
ELAPSED=$(( $(date +%s) - START ))
[ "$RC" -eq 0 ] || fail "vibe exited $RC after ${ELAPSED}s; stderr: $(tail -3 /tmp/smoke-stderr.txt)"
note "run finished in ${ELAPSED}s"

# 4. Assertions.
ANSWER=$(cat /tmp/smoke-answer.txt)
WORDS=$(wc -w < /tmp/smoke-answer.txt)
[ "$WORDS" -ge 20 ] || fail "answer too short to be an answer ($WORDS words)"

if [ "$WRITABLE_TARGET" -eq 1 ]; then
  [ -z "$(git -C "$TARGET" status --porcelain)" ] \
    || fail "the target repo was modified by a read-only question"
fi

# Ground truth: pointed at the library, the answer must recognize
# what it is looking at.
if [ -z "${TARGET_URL:-}" ]; then
  echo "$ANSWER" | grep -qiE 'agent|prompt|mistral' \
    || fail "answer does not describe the agent library"
fi

# The birth gate, headless: no permission prompt was answered in this
# run, so no tool may have been born into the cache.
CACHE="$HOME/.mistral-agents/tools"
if [ -d "$CACHE/adhoc" ] && [ -n "$(ls -A "$CACHE/adhoc")" ]; then
  fail "a tool entered the cache without an approved run"
fi
if [ -d "$CACHE/vetted" ] && [ -n "$(ls -A "$CACHE/vetted")" ]; then
  fail "a tool reached vetted without an approved run"
fi

echo
echo "smoke: PASS — $WORDS words, $profiles profiles, ${ELAPSED}s"
echo "---- answer ------------------------------------------------"
cat /tmp/smoke-answer.txt
echo
echo "------------------------------------------------------------"
