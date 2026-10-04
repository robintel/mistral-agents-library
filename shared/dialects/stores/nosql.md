# NoSQL modeling core

Attaches alongside a store contract (`cassandra`); extends `sql.md`'s
principles where SQL and this work meet. NoSQL stores share no
language — they share a modeling discipline: the access pattern names
the design.

## The discipline

- Model for the reads: a schema designed without its queries is a
  relational habit wearing NoSQL clothes. The first question is never
  "what are the entities" but "what are the queries".
- Denormalize without apology: duplication is storage; joins are
  latency. One table or collection per access pattern is the norm,
  not a smell.
- Consistency is a dial, not a default: know what the application
  assumes — read-your-writes, monotonic reads, eventual — and set
  reads and writes to the level that meets it, no higher.
- Retried writes are the norm: idempotent by design — upsert
  semantics or dedup keys; last-write-wins hides clock skew.
- Every partition, shard, and collection has a hot-key shape: design
  the key distribution or feel it in production.
- Aggregations that would be joins belong in the pipeline layer,
  precomputed — not requested per-read.

## Pitfalls (shared)

- Treating the store as a slower relational database with different
  syntax — the failure mode is portable across every NoSQL store.
- Secondary-index-shaped thinking on hot paths: what feels free in
  SQL is a full scan or a rebuild in many stores.
- Unbounded growth in one partition: bucket by time or tenant before
  the data arrives, not after.
