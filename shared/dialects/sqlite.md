# SQLite engine contract

Attaches alongside `sql.md`; extends, never restates. A file with a
parser: embedded, single-writer, and dynamically typed — the habits it
breaks are the habits relational engines teach.

## Eras

None worth tracking — the pragmas of a database file are its
configuration, and STRICT tables (3.37+) are the only opt-in era:
strict typing where the schema demands it.

## Idiom

- Type affinity, not types: the column declares affinity; a value
  can arrive as another type and come back as one. STRICT tables
  close the door where the schema says so.
- `PRAGMA foreign_keys = ON` per connection — it is not persisted,
  and the default is off: orphans insert silently otherwise.
- WAL mode for concurrent readers with the single writer;
  `busy_timeout` set on every connection, or errors under contention.
- Foreign keys and triggers are the integrity layer: no server, no
  scheduled jobs, no daemon to patch — the schema carries the rules.

## Structure

- One file, one database: backup is file-level (with the writer
  quiesced), and `:memory:` is a superpower for tests — the same
  engine, in-process, per test.

## Errors

- Constraint failures are the errors; CHECK and NOT NULL do the
  validation the type affinity does not.

## Pitfalls

- Foreign keys silently off: the per-connection default is the trap.
- No date type: dates are text or integers by convention — the
  convention must be written down and followed.
- The single-writer lock under write-heavy concurrency — SQLite
  serves reads beautifully and serializes writes absolutely.
- LIKE is case-insensitive for ASCII only, by design.
