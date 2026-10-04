# Kafka platform contract

Attaches alongside `messaging.md`. Not a database: the event
backbone — a replayable, ordered log. Most modern data
architectures are Kafka with databases hanging off it, which makes
its contracts everyone's contracts.

## Idiom

- The partition is the unit of order and of parallelism: ordering
  exists within a partition only, and the key decides the partition —
  key by the thing that needs order, and the core's hot-key rule
  applies the moment the key is popular.
- Consumer groups scale reading; offsets are the consumer's to commit
  — the processing guarantee lives at the consumer, not the broker.
- Retention is the design decision: time and size retention for
  streams, log compaction for latest-value-per-key topics — the
  table-shaped Kafka topic.
- Schemas are contracts at the boundary: a registry with enforced
  compatibility — the lineage tour's serialization rules apply to
  every event, not just databases.

## Semantics

- At-least-once is the default world: consumers are idempotent by
  design — the etl contract's law, imported whole.
- Exactly-once is a configured choice: idempotent producers plus
  transactions, priced in complexity — state it when claimed.

## Pitfalls

- Consumer lag is the health metric: monitoring it is not optional.
- Partition counts are hard to change: pre-plan the parallelism, or
  repartition as its own migration brief.
- Rebalance storms under slow consumers: timeouts tuned to the slow
  processor, not the fast average.
- Reading past retention is data loss experienced as emptiness —
  the silent one; retention is checked, not assumed.
- Compacted topics are not streams: mixing the two mental models
  corrupts both designs.
