# SQL Server engine contract

Attaches alongside `sql.md`; extends, never restates. T-SQL: the
enterprise engine, where isolation levels and parameter types decide
both correctness and performance.

## Eras

Each database carries a compatibility level gating optimizer
behavior and syntax: 2012 (sequences, OFFSET/FETCH, THROW), 2017
(STRING_AGG), 2019 (accelerated plans). Write the era the database's
level names; on-prem SQL Server and Azure SQL differ further.

## Idiom

- IDENTITY for simple keys, sequences where gaps and resets matter;
  NVARCHAR for text — the N prefix is a type decision, not a habit.
- TOP and OFFSET/FETCH for paging; temp tables (#) scoped, table
  variables where plans prefer them.
- Schema-qualified names: the schema is part of the contract.

## Errors

- THROW (2012+) over RAISERROR; TRY/CATCH with the original error
  re-raised, context added, never swallowed.

## Isolation

- Read Committed Snapshot (RCSI) is the civilized default for
  read-heavy systems: readers do not block writers.
- NOLOCK is a dirty-read generator wearing a performance costume —
  a finding in review, never a fix.

## Pitfalls

- Implicit conversion killing index seeks: NVARCHAR parameters into
  VARCHAR columns — the classic invisible performance bug.
- datetime over datetime2: range and precision both cost.
- Tempdb contention under heavy temp-table churn.
- LEN trims trailing spaces; DATALENGTH tells the truth.
