# Fortran dialect

**Status: experimental** — written conservatively, never validated
against a production Fortran estate. Findings and changes that lean on
this contract get a practitioner's review before they ship.

A conservation contract, not an idiom floor. Fortran in production is
old, load-bearing, and validated against numerical behavior — the risk
is changing what it computes, not styling it. The repo conventions win
absolutely; improvement ideas go in findings, never into the diff.

## Form

Fixed-form F77 and free-form F90+ are different disciplines: columns
1-6 sequence, column 7 indicator, the 72-column limit versus
free-form layout. Match the file you are editing, never mix forms in
one file, and modernize to free form only as its own brief with its
own regression baseline.

## Preservation over modernization

- Match the existing style absolutely: capitalization, column
  discipline, COMMON versus modules, the code's own control flow.
- Hot loops tuned decades ago: the comment saying "do not reorder" is
  load-bearing. Abstractions stay out.
- Adding declarations to implicitly typed code either changes nothing
  or changes everything: understand the file's typing before touching
  it.

## Numerical honesty

- Precision explicit: `REAL(KIND=...)` or `DOUBLE PRECISION` as the
  file does it; literals carry their precision (`1.0d0`, not `1.0`
  silently truncated to single).
- Preserve evaluation order in hot loops: the compiler was assumed
  into the results, not just invited.

## Testing

Old Fortran rarely has tests. The regression baseline is the output
of the existing code on known inputs — capture it before changing
anything, and diff after.

## Pitfalls

- Mixed-mode arithmetic: integer division truncates silently.
- Fixed-form column overflow: content past column 72 is ignored,
  silently.
- COMMON block aliasing; EQUIVALENCE tricks.
- Uninitialized variables that happen to be zero in the test
  environment and garbage in production.
