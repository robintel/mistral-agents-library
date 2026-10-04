# HBase store contract

Attaches alongside `nosql.md`. Wide-column on HDFS — Cassandra's
sibling with the opposite consistency story: strongly consistent
per region server, not eventually consistent.

## Eras

1.x versus 2.x is the practical boundary: 2.x brought in-place
flushing and compaction, and the async filesystem API. Write the
era the cluster runs.

## Idiom

- The row key is the schema, and ordering is the trap: monotonically
  increasing keys hot-spot one region — salt, hash, or reverse-
  timestamp by the read pattern.
- Few column families: the family is the unit of storage, flush, and
  bloom — many families fight each other at flush time.
- Tall versus wide — one row per event or many columns per entity —
  is the access-pattern question, decided by the reads.
- Pre-split regions at creation for known key distributions; split
  storms after are the alternative.

## Consistency

- Strong per row: single-row reads and writes are consistent —
  unlike Cassandra, no quorum math; the cost is availability during
  region moves.
- Region splits and moves are brief unavailability by design:
  clients retry — idempotent writes, per the core.

## Pitfalls

- Hot regions from monotonic keys: the salt question asked too late.
- Small cells: HDFS block overhead punishes tiny values — batch or
  widen the design.
- Timestamp conflicts: explicit timestamps collide with server-
  assigned ones; deletes are tombstones like Cassandra's.
- ZooKeeper is load-bearing: a session expiry is a region-server
  event, not a networking hiccup.
