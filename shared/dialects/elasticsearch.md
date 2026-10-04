# Elasticsearch store contract

Attaches alongside `nosql.md`. Search engine: the mapping is the
schema, the analyzer decides relevance, and both are hard to
change later.

## Eras

Mapping types died across 6 and 7 — code written with typed queries
does not run on 7+; 8.0 turned security on by default. The era
changes client code, not just server behavior; write for the
cluster's version.

## Idiom

- Explicit mappings in production; `dynamic: strict` — dynamic
  mapping is for exploration, and an unbounded mapping is an
  incident with a delay.
- text and keyword are different fields for the same value: analyzed
  for search, raw for filters and aggregation — declare both
  (`fields: { raw }`).
- `term` queries on keyword, `match` on text — term-on-text is the
  classic silent zero-results bug.
- Deep pagination uses `search_after` with a point-in-time; from +
  size is capped, and the cap is a good thing.

## Consistency

- Near real-time: the refresh interval (default 1s) is the gap
  between write and visibility — state it in the design, don't
  discover it in the bug report.
- Replicas scale reads; primaries take writes — plan accordingly.

## Pitfalls

- Mappings are immutable: a field-type change is a reindex, priced
  and planned like any migration.
- Mapping explosion: too many fields hits the index limit — the
  flattened type or nested design exists for this.
- Shard sizing: many small shards tax the master; few huge ones
  recover slowly. Neither is free; pick deliberately.
