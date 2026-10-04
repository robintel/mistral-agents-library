# MongoDB store contract

Attaches alongside `nosql.md`. Document store: the document is the
unit, and embedding versus referencing is the design question.

## Eras

4.0 brought multi-document transactions — pre-4.0 code leans on
compensating patterns instead; 4.2 shard-key refinement, 5.0
time-series collections, 7.0 bulk write. Write the era the server
runs.

## Idiom

- Embed until the data says otherwise: unbounded growth inside a
  document (comments, events) belongs in its own collection — the
  16MB document limit is a wall, not a suggestion.
- `_id` is the natural key where one exists; ObjectIds otherwise.
- The aggregation pipeline is the analytics tool; `$lookup` is an
  analytics decision, never an OLTP default.
- Schemaless never meant schema-never: JSON Schema validation on
  collections in production — dynamic mapping is for exploration.

## Consistency

- Single-document atomicity is the default transaction unit: design
  for it before reaching for transactions.
- Read-your-writes: `w: majority` with causal-consistency sessions;
  weaker concerns are a priced, stated choice.

## Pitfalls

- Unbounded arrays growing documents toward the 16MB wall.
- Every index taxes every write: index for the queries that exist,
  and prefer covered queries.
- Dates are UTC epoch milliseconds — timezone-naive insertion is
  the classic bug.
- `$lookup` on sharded collections behaves differently by version:
  check the era before planning the pipeline.
