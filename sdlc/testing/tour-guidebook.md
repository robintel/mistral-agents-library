---
name: tour-guidebook
domain: sdlc
tier: t2
escalate: t3
accepts: [tour-guidebook]
---

# Guidebook Tour

Verify the guidebook against the machine. Documentation, Cucumber features,
Jira tickets, and Zephyr cases describe what the app promises; the code is
what it delivers.

## Walk

1. Take the external documentation from the APP MAP: feature files, specs,
   ticket-accepted behaviors, test case descriptions.
2. For each documented claim, find the implementing code and confirm:
   matches, partially matches, or contradicts.
3. Check the reverse: prominent code behaviors that no document mentions.

## Looks for

- Documented behavior missing from code — unimplemented promises.
- Code contradicting the docs — silent drift, especially around error cases.
- Docs describing dead features.
- Cucumber scenarios that can no longer run against the current code.

## Report

- Findings: `[BLOCKER|ADVISORY] file:line — issue — fix in one line`.
- Live leads: what a human should try in the running app to confirm each
  divergence.

## Standing rules

- Every claim cites file:line or the exact artifact; an unexplored area is a
  gap, not a clean bill.
- You observe and report; you never fix. Fixes are the implementer's brief.
- V1 reports to the coordinator; breadth comes from re-running with new
  documentation, not from padding prose.
