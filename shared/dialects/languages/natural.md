# Natural dialect

**Status: experimental and conservation** — never validated against a
production estate; findings get practitioner review. Pairs with
`stores/adabas.md`: the language and the database were born together.

Software AG's 4GL (1979) — the language of ADABAS estates, and the
reason descriptor discipline (see adabas.md) decides performance.

## Preservation over modernization

- DDMs (the data views) are code: versioned with the programs,
  changed with plans, baselines from job output — the adabas
  contract's law, shared.

## Idiom

- The access verbs are the performance discipline: FIND seeks on
  descriptors; HISTOGRAM counts descriptor values; READ PHYSICAL is
  the scan, priced at file size. A FIND on a non-descriptor is a
  finding, not a query.
- END TRANSACTION and BACKOUT are the transaction boundary — the
  ADABAS holding queue drains or accumulates by this discipline
  alone.
- Programs, subprograms, and maps are separate module kinds: a map
  (screen) is code with a lifetime and a diff, treated like one.

## Pitfalls

- Record holds accumulating across a long-running loop: the
  database-wide concurrency tax, one program at a time.
- Re-finding inside loops without the ISN discipline: rereads are
  scans wearing a loop.
- Blank-versus-null in ADABAS fields: the layout is a contract, like
  a copybook — Natural's semantics differ from the file's.
- Numeric edit formats deciding output silently: the format is the
  interface, stated, not inherited.
