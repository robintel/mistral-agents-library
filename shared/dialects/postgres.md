# PostgreSQL engine contract

Attaches alongside `sql.md`; extends, never restates. Postgres
richness is idiom: reach for the engine's own types and clauses before
building machinery.

## Eras

Version thresholds that change idiom: 9.6 (`ON CONFLICT`), 10
(declarative partitioning), 12 (CTE inlining — the fence semantics
changed), 14 (multirange), 15 (MERGE). `SELECT version()` names the
era; write it.

## Idiom

- `jsonb` over `json` for stored documents — indexed, with `@>` and
  `?` operators.
- `RETURNING` over a second query for INSERT/UPDATE results.
- `DISTINCT ON` for per-group-first queries — no window-function
  ceremony needed.
- Arrays and ranges as first-class types before junction-table and
  interval-arithmetic machinery.

## Structure

- Partial indexes where the predicate matters; expression indexes
  where the transform matters.
- CTEs were optimization fences before 12: know the version before
  assuming inlining.

## Errors

- `ON CONFLICT` for idempotent upserts; advisory locks for
  application-level coordination — never table locks held while a
  user thinks.

## Pitfalls

- `count(*)` on big tables is a full scan: use estimates where an
  estimate is honest.
- NULLs in unique indexes: multiple NULLs allowed by default.
- `timestamptz` stores UTC and renders per session — naive
  timestamps are the bug.
- Sequences are not gap-free and do not roll back: by design, not a
  defect.
