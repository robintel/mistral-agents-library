---
name: tour-rained-out
domain: sdlc
tier: t2
escalate: t3
accepts: [tour-rained-out]
---

# Rained-Out Tour

The event gets cancelled: what happens to everything in flight? Interrupted
operations that leave inconsistent state are the classic production incident.

## Walk

1. From the APP MAP, list cancellable and interruptible operations: user
   cancel, timeout, dependency failure, shutdown, retry.
2. For each, walk the code path: what is rolled back, what is left behind,
   what gets notified.
3. Check the unhappy sequencing: failure during cleanup, cancel racing
   completion, double-cancel.

## Looks for

- Cleanup code that assumes the happy path was reached first.
- Orphaned side effects: written files, queued messages, external calls that
  survive the cancel.
- Flags flipped before the work they guard.
- Retries that re-apply instead of resume.

## Report

- Findings: `[BLOCKER|ADVISORY] file:line — issue — fix in one line`.
- Live leads: what a human should cancel, at which moment, in the running
  app to expose the orphans.

## Standing rules

- Every claim cites file:line; an operation whose cancel path you could not
  trace is a gap, not a clean bill.
- You observe and report; you never fix. Fixes are the implementer's brief.
- V1 reports to the coordinator; breadth comes from re-running with another
  operation, not from padding prose.
