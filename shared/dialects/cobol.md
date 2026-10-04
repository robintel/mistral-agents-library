# COBOL dialect

**Status: experimental** — written conservatively, never validated
against a production COBOL estate. Findings and changes that lean on
this contract get a practitioner's review before they ship.

A conservation contract, not an idiom floor. COBOL in production has
run for decades; the risk is changing what it computes, not styling
it. The repo conventions win absolutely; improvement ideas go in
findings, never into the diff.

## Form

Fixed format is the norm: columns 1-6 sequence, column 7 indicator,
Area A at 8-11 for divisions, sections, and paragraphs, Area B from
12. Respect the columns; free-form (COBOL 2002+) only where the
compiler and the repo already do. COPYBOOKs are shared API — change
one and feel it everywhere: a copybook edit is a cross-system brief
with a lineage check, never a local fix.

## Preservation over modernization

- Match the file's division structure, level numbers, paragraph
  naming, and period discipline as written.
- GO TO paragraph loops in old code: understand them, never
  restructure silently.
- PERFORM with explicit END-PERFORM in new code; in old code, respect
  the THRU structure exactly.

## Data honesty

- The PIC clause decides precision: adding digits to a field changes
  truncation everywhere it flows — treat it as a schema migration,
  with the lineage tour's map naming the consumers.
- USAGE (COMP, COMP-3) as the data division declares it: changing
  storage changes results.
- REDEFINES alias storage: write one view, change the other.

## Testing

The regression baseline is existing outputs on known inputs — report
runs, file dumps, mainframe job output. Capture before changing,
diff after.

## Pitfalls

- MOVE truncation: alphanumeric and numeric MOVEs lose digits
  silently — compare field lengths before every move in a change.
- Date fields in PIC 9(6) and the windows that read them.
- Level-77 and level-66 items where the file uses them — they are
  not yours to renumber.
