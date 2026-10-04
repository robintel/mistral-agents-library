# Caché/IRIS store contract

**Status: experimental and conservation** — never validated against a
production estate; findings get practitioner review. Attaches
standalone.

InterSystems' MUMPS-lineage database: globals — sparse,
multi-dimensional, persistent arrays — are the storage; ObjectScript
is the language; healthcare's backbone (Epic among many). Schemaless
before NoSQL existed.

## Idiom

- Globals are the database: `^Patient(1701,"allergies")` — structure
  lives in the application's discipline, not a schema. The data
  dictionary is the code that writes the globals; where nobody wrote
  it down, the lineage tour's territory.
- Subscript-level locking is the concurrency unit: lock what you
  touch — `^Patient(1701)`, never `^Patient`.
- Journaling and ECP are the durability and scale contracts —
  configured infrastructure, stated like any era.

## Preservation over modernization

- Global structure changes are schema migrations: consumers mapped
  (the lineage map), baselines captured, plans approved.
- Killing a subtree is a bulk delete: named, planned, approved — the
  steward's irreversible-action rule.

## Pitfalls

- Walking undocumented globals: structure inferred from code is a
  finding, not a fact.
- Kill of a subtree: the delete that deletes more than it looked
  like it would.
- A global walk is a query, priced like one — paginated, bounded,
  and counted.
- SQL views layered over globals: translated and occasionally
  surprising — the serialization boundary rules apply.
