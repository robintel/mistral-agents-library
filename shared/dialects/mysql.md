# MySQL engine contract

Attaches alongside `sql.md`; extends, never restates.

## Eras

5.7 versus 8.0 is the sharp boundary: 8.0 adds CTEs, window
functions, enforced CHECK constraints, functional indexes, JSON_TABLE.
`sql_mode` names the strictness era — strict by default in 8.0, often
loose in legacy 5.x, where silent truncation was the norm. Write the
era the server runs.

## Idiom

- `utf8mb4` always: "utf8" is a three-byte lie that breaks on
  characters beyond BMP.
- Explicit column lists in every INSERT.
- InnoDB semantics: the clustered primary key orders rows — range
  scans read it.

## Structure

- Index for the queries that exist: every secondary index taxes
  every INSERT.

## Errors

- Foreign keys on for referential integrity; off is a finding, not
  a style choice.
- Deadlocks are normal InnoDB behavior at concurrency: retry with
  backoff is idiom, not failure.

## Pitfalls

- Silent coercion in loose `sql_mode`: garbage dates and truncated
  strings accepted — check the mode before trusting anything.
- No `RETURNING`: `last_insert_id()` in the same session.
- GROUP BY without full grouping columns in loose mode: garbage,
  not a feature.
- Collation decides case sensitivity: know `ci` from `cs` before
  joining.
