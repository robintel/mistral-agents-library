# PL/I dialect

**Status: experimental and conservation** — never validated against a
production estate; findings get practitioner review. Pairs with the
mainframe store contracts (ims, vsam) and db2 work.

IBM's 1964 language, alive in banking estates: explicit precision,
powerful enough to be dangerous, and validated by decades of batch
output.

## Preservation over modernization

- Old, load-bearing, and correct by evidence: the cobol contract's
  law — regression baselines from job output before any change;
  improvement ideas go in findings, never the diff.

## Idiom

- Attributes explicit on every declaration: defaults are silent
  decisions the compiler makes for you, and PL/I's defaults are
  famously surprising. FIXED DECIMAL for money; the precision is
  the contract.
- ON-conditions instead of error returns: ON ENDFILE, ON ERROR —
  handlers establish the failure behavior up front; unhandled
  conditions are the classic silent-wrong-result bug.
- %INCLUDE for shared copybooks: the same role as COBOL's, versioned
  as code.

## Structure

- ALLOCATE and FREE with based storage: pointers are powerful and
  exact — dangling based references are the sharp edge.
- REENTRANT for CICS: the runtime contract decides the rules.

## Pitfalls

- Silent conversions: PL/I converts automatically between types and
  precisions — every mixed expression is a decision, not a
  convenience.
- Default attributes on undeclared data: the trap with a
  fifty-year reputation.
- GET/PUT edit-directed formats: the format is the interface.
- Pointer arithmetic on based variables: power, priced in care.
