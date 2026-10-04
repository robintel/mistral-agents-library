# VSAM store contract

**Status: experimental and conservation** — never validated against a
production estate; findings get practitioner review. Attaches
standalone.

Not a database: IBM's file access method — the storage layer under
COBOL applications and half the mainframe's data. The dataset
organization is the design decision, made at creation and expensive
to revisit.

## The organizations

- KSDS (key-sequenced): keyed access, logical order — the default
  for record-by-key work.
- ESDS (entry-sequenced): append-only arrival order; in-place updates
  only at the same record length.
- RRDS (relative record): fixed-length slots by number — the
  array on disk.
- LDS (linear): raw bytes; the application carries every rule.

## Preservation over modernization

- JCL and IDCAMS definitions are code: DEFINE, REPRO, VERIFY —
  versioned with the application, migration steps included.
- The copybook defines the record; the record layout is the schema.

## Pitfalls

- CI and CA splits: random inserts into a KSDS without free space
  chosen at creation fragment the dataset — performance decays
  silently until the next reorganization.
- Uncataloged datasets after a move: the application breaks on the
  name, not the data.
- Key compression and record-length changes are migrations, not edits.
- ESDS updates of different length: silently impossible — the
  record's shape is a contract.
