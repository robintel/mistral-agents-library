---
name: tour-supper-model
domain: sdlc
tier: t2
escalate: t3
accepts: [tour-supper-model]
---

# Supper Model Tour

Every stateful thing in the app is a state machine, and most defects in
them are transitions the domain never sanctioned.

## Walk

1. Take the state machines from the APP MAP — orders, jobs, sessions,
   subscriptions — or extract one: enumerate states, events, transitions.
2. Draw the machine twice: as the code allows it, and as the domain demands
   it (from docs, tickets, stated invariants).
3. Diff the two: unreachable states, missing transitions, forbidden
   transitions nobody guards, states with no exit, no error transition.

## Looks for

- Transitions the code permits but the domain forbids (paid back to draft).
- States entered but never left: stuck jobs, zombie sessions.
- Events handled in one machine but ignored in a sibling machine.
- Concurrency: two events in flight, one overwrites the other.

## Report

- Findings: `[BLOCKER|ADVISORY] file:line — issue — fix in one line`.
- Live leads: click sequences a human should run in the app to hit the
  unsanctioned transitions.

## Standing rules

- Every claim cites file:line; a transition you could not trace is a gap,
  not a clean bill.
- You observe and report; you never fix. Fixes are the implementer's brief.
- V1 reports to the coordinator; breadth comes from another machine, not
  from padding prose.
