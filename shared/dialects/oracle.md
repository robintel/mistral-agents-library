# Oracle engine contract

Attaches alongside `sql.md`; extends, never restates.

## Eras

Oracle eras are real, and the code declares them: 10 (rownum paging,
sequences plus triggers for keys), 11 (LISTAGG from 11.2, PIVOT,
mature analytic functions), 12c (FETCH FIRST replaces rownum paging,
identity columns, PL/SQL in WITH clauses). The paging query is the
era marker: rownum outside 12c, FETCH FIRST inside it.

## Idiom

- Sequences with `.NEXTVAL`; 12c identity columns — never
  trigger-built keys in 12c+ code.
- MERGE for upserts: the native tool, not an INSERT/UPDATE dance.
- Recursive WITH for hierarchies; CONNECT BY where legacy code
  already speaks it — the era rule again.

## Structure

- PL/SQL is a language, not a script: packages with explicit
  interfaces, exception sections that name what failed.
- Bulk operations with BULK COLLECT and FORALL, never row-by-row
  loops — row-by-row is slow-by-slow.

## Errors

- Named exceptions; `WHEN OTHERS THEN RAISE` — never swallowed.
- SQLERRM carries the context; ORA- error numbers read as contract
  documentation.

## Pitfalls

- Empty string is NULL: `''` and NULL are the same value — the
  classic porting trap.
- DDL commits implicitly: the transaction around it dies.
- rownum applied before ORDER BY: paging without a subquery returns
  arbitrary rows.
- Dates without zones: TIMESTAMP WITH TIME ZONE, or know the
  server's contract.
