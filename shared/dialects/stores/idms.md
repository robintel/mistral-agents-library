# IDMS store contract

**Status: experimental and conservation** — never validated against a
production estate; findings get practitioner review. Attaches
standalone.

The CODASYL network database (1970s) — records in sets, owners and
members, and currency as the discipline. Alive under Broadcom in
insurance and government estates.

## Idiom

- Records and sets are the model: a set names an owner record type
  and its members; walking sets is the access pattern.
- Currency is the state: FIND/OBTAIN establish position — next, prior,
  owner, first within set — and every subsequent find depends on it.
- The subschema is the program's view: versioned code, changed with
  plans, never silently.

## Preservation over modernization

- Schema and DMCL definitions are code; capture baselines from job
  output before any change.
- Run units commit or roll back as units; the journal is the
  recovery contract.

## Pitfalls

- Currency errors: the classic network-database bug — the find that
  assumed a position nobody established.
- Set selection at STORE: where a new record connects is a design
  decision, automatic-looking defaults included.
- Calc keys and area sweeps decide performance; non-indexed walking
  is a full-database walk.
- CONNECT/DISCONNECT discipline: a record in the wrong set is found
  by the wrong programs — and not by the right ones.
