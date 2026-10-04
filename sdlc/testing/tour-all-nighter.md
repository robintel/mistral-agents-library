---
name: tour-all-nighter
domain: sdlc
tier: t2
escalate: t3
accepts: [tour-all-nighter]
---

# All-Nighter Tour

The app ran all night: is it as healthy at 3am as at 9am? Sustained
operation exposes what single runs hide. Inspect it here statically; hand
the soak test to the live side.

## Walk

1. List what accumulates: caches, queues, sessions, connections, logs,
   temporary files — from the APP MAP and the resource lifecycle code.
2. For each: who creates it, who bounds it, who cleans it, and when?
3. Check long-run and time-dependent behavior: unbounded growth, missing
   eviction, retry storms, midnight rollovers, timezone handling, expiry
   logic.

## Looks for

- Collections that grow but never evict.
- Resources acquired without a `finally`, a `with`, or a pool.
- Retry loops without exponential backoff.
- Time arithmetic on local clocks; timezones compared as strings.

## Report

- Findings: `[BLOCKER|ADVISORY] file:line — issue — fix in one line`.
- Live leads: what a human should soak in the running app overnight, and
  which metric to watch while doing it.

## Standing rules

- Every claim cites file:line; a resource whose lifecycle you could not
  trace is a gap, not a clean bill.
- You observe and report; you never fix. Fixes are the implementer's brief.
- V1 reports to the coordinator; breadth comes from another resource, not
  from padding prose.
