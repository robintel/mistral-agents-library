---
name: tour-fedex
domain: sdlc
tier: t2
escalate: t3
accepts: [tour-fedex]
---

# FedEx Tour

Follow one piece of data end to end. Data that changes shape or loses
protection along the way is a defect waiting for production.

## Walk

1. Pick one data item from the APP MAP that crosses a boundary: user input,
   a payment, an order.
2. Trace its whole route: birth (entry point), validation, transforms,
   persistence, retrieval, exit (response, export, message).
3. At each hop: is it validated or trusted? Can it be lost, duplicated,
   mutated, or partially applied? What happens on failure mid-route?

## Looks for

- Data accepted at one boundary and trusted at another.
- Silent coercion: units, timezones, encodings, truncation.
- Partial writes: half-completed routes on failure, no rollback.
- Sensitive data riding along where it should not.

## Report

- Findings: `[BLOCKER|ADVISORY] file:line — issue — fix in one line`.
- Live leads: values a human should enter in the running app to confirm the
  weak hops.

## Standing rules

- Every claim cites file:line; a hop you could not trace is a gap, not a
  clean bill.
- You observe and report; you never fix. Fixes are the implementer's brief.
- V1 reports to the coordinator; one data item per run — breadth comes from
  re-running with another item, not from padding prose.
