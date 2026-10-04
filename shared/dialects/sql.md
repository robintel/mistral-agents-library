# SQL dialect

Baseline style for SQL work — the vendor-neutral core. The engine
names its contract: `postgres`, `mysql`, or `oracle` attaches
alongside this one and extends it; where the engine file is silent,
this core applies. The repo's pinned conventions win on conflict.

## Idiom

- Explicit projections; `SELECT *` never ships.
- Explicit joins with stated `ON` conditions; comma joins are legacy.
- Parameterized predicates; interpolated values are a BLOCKER in
  application code.

## Structure

- CTEs over nested subqueries for readability; the optimizer decides
  what they cost, not the fashion.
- Window functions over correlated subqueries for row-by-row reasoning.
- A comment names the index or assumption each non-obvious predicate
  relies on.

## Errors

- NULL is not a value: explicit `IS NULL` checks; three-valued logic is
  respected, never fought.
- Casts and divisions guarded explicitly; coercion is never silent in
  production queries.

## Testing

- Results compared against a known-good set, never eyeballed.

## Dependencies

- The engine and version noted where syntax depends on them.

## Starting from scratch

When no conventions exist yet, these are the pins:

- One migration tool, pinned; migrations ordered and replayable; a
  dedicated read-only role for analytics from day one.

## Pitfalls

- JSON columns: a relaxed schema hiding inside a column — validation
  moves to the reader, which never runs it.
- Functions on indexed columns in predicates — the index dies there.
- Filtering in HAVING where WHERE belongs.
- Timezone-naive timestamps; date arithmetic on strings.
- OR across columns where a UNION or a rewrite could use the index.
