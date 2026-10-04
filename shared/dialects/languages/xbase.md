# xBase dialect

**Status: experimental and conservation** — never validated against a
production estate; findings get practitioner review. One contract for
the family: the DBF file is the database, and the language is its
voice.

## Eras

dBASE (interpreted, the origin), Clipper (compiled, the 5.x era),
FoxPro (2.x DOS, then Visual FoxPro on Windows) — the family shares
syntax; the index formats (NTX, CDX) and toolchains are the era
markers. Rushmore optimization is FoxPro's era feature: index-driven
WHERE clauses, and code that forgot it scans.

## Idiom

- The DBF file is the database: no server, no engine between —
  record and file locks are the concurrency story, and the
  application carries every integrity rule.
- Deleted records are marks: DELETE flags, RECALL restores, PACK
  rebuilds the file physically — PACK is a maintenance operation
  with a plan, never a casual verb.
- SET DELETED ON/OFF decides visibility: the setting is part of the
  program's contract, stated at the top, not inherited.
- Field names cap at ten characters: the constraint shaped decades
  of schemas; do not fight it, respect it.

## Pitfalls

- Index corruption: the classic xBase failure — the index and the
  table drift; REINDEX is a maintenance event, not a fix.
- Date fields as YYYYMMDD: the Y2K archaeology, and the reason old
  code windows on two-digit years.
- Memo files (DBT/FPT) as the blob: the pair file — one lost, both
  broken.
- Lock conflicts on shared network DBFs: retry discipline exists
  or the app teaches users to swear.
