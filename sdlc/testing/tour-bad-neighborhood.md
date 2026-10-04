---
name: tour-bad-neighborhood
domain: sdlc
tier: t2
escalate: t3
accepts: [tour-bad-neighborhood]
---

# Bad-Neighborhood Tour

Bugs cluster. Where a bug lived, more live: find the neighborhoods and
probe them.

## Walk

1. Rank areas by defect history: recent bug-fix commits (search the log for
   fix/close/revert references), hotspot churn, high complexity.
2. Walk the worst few neighborhoods like a reviewer with suspicion: what
   did the past bugs here have in common?
3. Extend the pattern: which other code shares the same shape?

## Looks for

- The recurring defect pattern — off-by-one, missing null check, race — in
  code adjacent to past fixes.
- Changes that fixed symptoms and left the cause in place.
- High-churn files with no test coverage standing over them.

## Report

- Findings: `[BLOCKER|ADVISORY] file:line — issue — fix in one line`.
- Live leads: inputs or sequences a human should try in the running app to
  confirm the suspected clusters.

## Standing rules

- Every claim cites file:line or a commit reference; an area you could not
  assess is a gap, not a clean bill.
- You observe and report; you never fix. Fixes are the implementer's brief.
- V1 reports to the coordinator; breadth comes from another neighborhood,
  not from padding prose.
