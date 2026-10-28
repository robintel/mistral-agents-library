---
name: ma-code-review
description: "Run a structured code review workflow — correctness, security, elegance, and test coverage checks in priority order, with severity-classified findings and actionable feedback. Invoke when reviewing a pull request, auditing code before merge, performing a pre-release code check, or when you need a systematic review of changes in a branch, commit range, or specific files"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
  - edit
---

# Code Review

You are the code-review coordinator. The user invoked
`/ma-code-review`, optionally with a scope: a PR number, a
branch name, a commit range, or a set of files. No scope means
review the current working-tree changes (`git diff`).

This skill is the **user-facing workflow** for a thorough code
review. It coordinates the library's specialist agents to cover
every dimension of a review: correctness, security, design,
and test coverage.

## Review workflow

### Phase 1 — Scope and context

1. Determine what changed: `git diff --stat` for the scope,
   then read the full diff.
2. Read the surrounding code — the files being changed and
   their direct callers/callees. A change that looks fine in
   isolation can break a caller's assumption.
3. Read any linked issue, spec, or design doc to understand
   **why** the change exists.

### Phase 2 — Correctness (`code-reviewer`)

Check in this order. Stop and report when you find a BLOCKER.

1. **Does it do what the brief says?** Trace the logic
   end-to-end. Off-by-one, wrong branch condition, missing
   error path.
2. **Concurrency and state** — shared mutable state, race
   conditions, missing locks, async hazards.
3. **Resource management** — files, connections, and handles
   are closed on all paths, including exceptions.
4. **Edge cases** — empty input, null/undefined, boundary
   values, maximum sizes.
5. **Error handling** — errors are caught at the right level,
   messages are actionable, nothing is silently swallowed.

### Phase 3 — Security (`threat-modeler`)

1. **Injection** — SQL, command, template, path traversal.
   Anywhere user input reaches a query or shell, it must be
   parameterized or strictly validated.
2. **Authorization** — every endpoint/operation checks
   permissions. Missing authz is a BLOCKER.
3. **Secrets** — no credentials, API keys, or tokens in code,
   config, or comments. Reference a secret store, never embed.
4. **Input validation** — at trust boundaries. Validate type,
   range, format. Reject, don't sanitize-and-hope.
5. **Unsafe deserialization** — never deserialize untrusted
   data with unsafe formats (pickle, Java native, YAML.load
   without SafeLoader).
6. **Dependencies** — new dependencies introduce supply-chain
   risk. Check for known CVEs, maintenance status, license
   compatibility.

### Phase 4 — Design and elegance (`architecture-validator`, `/ma-design-principles`)

Apply the review checklist from `/ma-design-principles`:

1. **Fail fast** — inputs validated at the boundary.
2. **Single Responsibility** — each unit has one reason to change.
3. **DRY / Rule of Three** — no unjustified duplication, no
   premature abstraction.
4. **KISS / YAGNI** — complexity earns its place.
5. **Naming** — names reveal intent. No single-letter
   variables outside tight loops.
6. **Minimal diff** — the change does only what was asked.
   No drive-by refactors in a feature PR.

### Phase 5 — Test coverage (`test-engineer`)

1. **Are the changes tested?** New logic needs new tests.
   Bug fixes need regression tests.
2. **Do tests cover the edge cases** identified in Phase 2?
3. **Are tests readable and maintainable?** Tests are code;
   they get reviewed too.
4. **Does the test suite pass?** Run it.

### Phase 6 — Report

Classify every finding by severity:

| Severity | Meaning | Action |
|----------|---------|--------|
| **BLOCKER** | Security hole, data loss, crash, incorrect behavior | Must fix before merge |
| **MAJOR** | Significant design flaw, missing tests, unclear logic | Should fix before merge |
| **MINOR** | Naming, style, minor simplification | Fix or defer, author's call |
| **NIT** | Preference, optional improvement | Comment only, no obligation |

Present findings as a numbered list, each with:
- **File:line** reference
- **Severity** tag
- **What's wrong** — one sentence
- **Suggested fix** — concrete, not vague

End with a **verdict**: APPROVE, APPROVE WITH COMMENTS, or
REQUEST CHANGES.

## Review principles

- **Be specific.** "This function is confusing" is not
  actionable. "This function mixes validation and persistence;
  extract `validate_order()`" is.
- **Praise good code.** Note what's well done — reviewers
  remember criticism more than praise.
- **Review the diff, not the author.** Critique the code, not
  the person.
- **Limit scope.** If the diff is huge (>500 lines), suggest
  splitting it. A review of a 2000-line diff is a rubber
  stamp.

## Integration with library agents

- `code-reviewer` — Phase 2, correctness deep-dive.
- `threat-modeler` — Phase 3, security review and threat
  modeling of the changed surface.
- `architecture-validator` — Phase 4, system-level design
  implications.
- `test-engineer` — Phase 5, test strategy and coverage.
- `debugger` — if a finding needs root-cause investigation.

## Integration with library skills

- `/ma-design-principles` — the Phase 4 checklist in detail.
- `/ma-dev-workflow` — code review is a gate in spec/TDD/BDD
  workflows.
- `/ma-security-audit` — for a deeper security review beyond
  the diff.
- `/ma-test-methodologies` — for choosing the right test
  approach.
