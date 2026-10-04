# Hadoop platform contract

Hadoop is not a NoSQL database: it is a platform — HDFS storage
underneath, compute frameworks above (MapReduce, Hive, Spark on
YARN). HBase, the database of that ecosystem, is a wide-column store
with its own contract (`hbase.md`) when it is the target. This
contract covers the platform.

## Eras

Two eras of compute: classic MapReduce, and the engines that replaced
it for most work — Hive on Tez, Spark on YARN. A MapReduce rewrite is
rarely the answer; Hadoop 3 adds erasure coding for cold storage and
changes the failure math. The cluster's running services name the
era.

## HDFS discipline

- The block (128MB default) is the design unit: many-small-files is
  the classic killer, and NameNode memory is the bill — sequence
  files, Avro, or HAR for small-file archives.
- Data locality is the entire performance game: compute where the
  blocks live; a job that ignores locality is a network job.
- Replication 3 is the default contract; erasure coding for cold
  data — know which the path uses before reasoning about failures.

## Compute discipline

- Shuffle is the cost: combiners where the operation allows; a
  shuffle-heavy plan is a design smell, not an inconvenience.
- Skew: one hot key extends the whole job — detect, salt, or
  isolate, in the plan rather than the post-mortem.
- Speculative execution covers slow nodes, never bad code.

## Pitfalls

- HDFS is append-only files: no random edits — the mental model that
  breaks first.
- Small-file storms from per-record writes.
- Reading defaults instead of the cluster's actual configuration —
  verify against the running services, not the documentation.
