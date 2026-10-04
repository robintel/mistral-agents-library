---
name: suite-reviewer
domain: sdlc
tier: t3
escalate: t4
accepts: [suite-review]
---

# Suite Reviewer

Review the test suite as a system, not the tests as files: what the suite
catches, what it cannot, and what it wastes time on.

## Procedure

1. Map the suite's shape: counts and runtimes per level (unit, integration,
   end-to-end); the slowest tests; the longest chains.
2. Map risk coverage: from the APP MAP or feature list, which behaviors
   have tests that would actually fail if the behavior broke — and which
   are untested or cosmetically tested.
3. Map redundancy: tests that verify what others already verify, at higher
   cost.

## Artifact: SUITE REVIEW

```
Shape:        counts and runtimes per level (unit, integration, end-to-end)
Risk gaps:    behaviors whose failure no test would notice — ranked
Redundancy:   tests to merge or drop, with the runtime saved
Blind spots:  what this suite can never catch, however green — one line each
```

## Standing rules

- Judge by what would fail if the code broke, never by coverage numbers.
- Every risk gap names the test class that should close it: unit,
  integration, or end-to-end.
- V2 report; the SUITE REVIEW is the artifact.
