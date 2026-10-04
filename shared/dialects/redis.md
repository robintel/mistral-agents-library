# Redis store contract

Attaches alongside `nosql.md`. In-memory key-value: the data
structure is the API — pick the structure that answers the query,
not the one that stores it.

## Eras

5.0 added streams; 6.0 ACLs, TLS, RESP3; 7.0 functions and sharded
pub/sub. The deployment mode matters more than the version: single,
sentinel, or cluster — write for the mode the service runs.

## Idiom

- TTL-first for anything cache-shaped: expiry is a feature of the
  design, not an afterthought.
- SCAN for iteration; KEYS is forbidden in production — O(N) on a
  single thread is an outage in a command.
- Pipelines for round-trip cost; Lua or transactions for compound
  atomics — the single command is atomic by design.
- Locks via `SET NX EX`: advisory by nature, with hold-time sanity
  and idempotency on the thing the lock guards.

## Consistency

- Cluster mode: keys hash to slots — multi-key operations need hash
  tags, and crossing slots is a client error, not a retry.
- Persistence is a dial: RDB snapshots versus AOF durability; know
  which the service runs before promising anything about survives-
  restart.

## Pitfalls

- Big keys: one multi-megabyte value blocks the single thread —
  everything queues behind it.
- Eviction policy deciding silently: `allkeys-lru` and
  `volatile-lru` make different promises; the config is a contract.
- Pub/sub is at-most-once; streams are at-least-once — pick by the
  delivery contract, not the API that reads nicer.
- Hot keys funneling one shard: the core's hot-key shape, at
  memory speed.
