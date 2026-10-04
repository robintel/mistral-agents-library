# Cassandra store contract

Attaches alongside `nosql.md`. Wide-column: the partition is the
unit of scale and the boundary of the query.

## Eras

3.x materialized views are legacy — treat them as a warning, not a
tool; 4.x the maintenance-quality era; 4.1+ SAI (Storage-Attached
Indexing) replaces secondary indexes for patterns that must filter.
Write the era the cluster runs — `SELECT release_version()` names it.

## Idiom

- The partition key is the schema: it decides which queries can be
  served at all. Tables are designed per query pattern, not per
  entity — duplication is the design, not a compromise.
- Clustering columns order and group within the partition; ORDER BY
  works within partitions only.
- One partition per query on hot paths: crossing partitions is an
  analytics decision, never an OLTP default.

## Consistency

- Read-your-writes: QUORUM writes with QUORUM reads; LOCAL_QUORUM
  for latency-sensitive single-dc paths; ONE only where staleness is
  priced and stated.
- Last-write-wins is clock skew wearing a smile: conflicting writes
  are an application design question, never settled by the OS clock.

## Pitfalls

- Unbounded partitions: time-series without bucketing reads the
  whole partition to answer "the latest".
- Hot partitions: naive keys funneling one tenant to one node.
- Tombstones: deletes are writes — mass delete then read is a repair
  storm; design deletion as partition expiry (TTL) where possible.
- `ALLOW FILTERING`: the query that works on ten rows and dies on
  ten million.
- Written-empty versus never-written read the same and behave
  differently at compaction.
