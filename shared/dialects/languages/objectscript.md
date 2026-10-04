# ObjectScript dialect

**Status: experimental and conservation** — never validated against a
production estate; findings get practitioner review. Pairs with
`stores/cache-iris.md`: globals are the storage, this is the voice.

InterSystems' language, MUMPS-descended: the traversal verbs over
globals are the access primitives, and healthcare runs on them.

## Eras

Error handling is the visible era: $ZTRAP legacy code versus the
$ETRAP and TRY/CATCH era — write the mechanism the codebase uses,
never mixing one estate's error idiom into another's.

## Idiom

- The verbs are the query language: $ORDER walks a subscript level,
  $QUERY walks whole structures, $DATA tests existence and
  children — every global traversal is a query, priced like one
  (the cache-iris contract's law, spoken here).
- $INCREMENT is the atomic counter: lock-free and correct — prefer it
  over read-modify-write for counters.
- TSTART/TCOMMIT/TROLLBACK are the transaction boundary: paired with
  journaling, stated in the design.
- The class model (persistent classes generating global storage) is
  the modern era; pure global code is the elder — write the era the
  application uses.

## Pitfalls

- $ORDER and $QUERY have different shapes: mixing them on
  multi-dimensional structures skips levels or revisits them.
- Kill of a subtree: the delete that deletes more than it looked
  like it would — named, planned, approved.
- $DATA's ten return values: existence and has-children are
  different questions; know which one you asked.
- Error traps across routine boundaries: the era mismatch, in
  production clothes.
