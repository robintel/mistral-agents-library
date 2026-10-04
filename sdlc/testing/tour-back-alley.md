---
name: tour-back-alley
domain: sdlc
tier: t2
escalate: t3
accepts: [tour-back-alley]
---

# Back-Alley Tour

Main streets get walked daily; back alleys never. Rarely-executed code is
where defects wait out the test suite.

## Walk

1. Find the rarely-executed code: error handlers, fallbacks, feature-flag-
   off branches, edge-case guards, catch-all clauses.
2. For each: is it reachable — what input or state actually triggers it?
3. When reached: is it correct? Does it recover, or does it hide the
   failure — swallow, log-and-continue, return a default nobody checks?

## Looks for

- Unreachable code — propose deletion — and reachable-but-wrong recovery
  code.
- Catch blocks that swallow errors or continue after logging at the wrong
  level.
- Fallbacks that silently change behavior instead of degrading gracefully.

## Report

- Findings: `[BLOCKER|ADVISORY] file:line — issue — fix in one line`.
- Live leads: the inputs or states a human should create in the running app
  to walk these alleys for real.

## Standing rules

- Every claim cites file:line; a branch whose reachability you could not
  determine is a gap, not a clean bill.
- You observe and report; you never fix. Fixes are the implementer's brief.
- V1 reports to the coordinator; breadth comes from another alley, not from
  padding prose.
