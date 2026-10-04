# DynamoDB store contract

Attaches alongside `nosql.md`. The AWS-native key-value and
document store: single-digit milliseconds at any scale, and every
discipline exists because scale punished the alternative.

## Eras

The billing era matters: provisioned capacity with autoscaling for
steady load, on-demand for spiky — the choice is priced, never
defaulted. Transactions arrived 2018 (TransactWriteItems); global
tables for multi-region after.

## Idiom

- Partition key plus sort key is the whole schema: access-pattern-
  first is not advice here, it is the physics.
- Single-table design is the native idiom: one table, many entity
  types, composite keys doing the work relations do elsewhere —
  counterintuitive and correct, and it depends on GSI overloads
  planned as carefully as the base table.
- GSIs are writes: every one taxes every put — sparse indexes (a
  GSI that only holds rows where a field exists) are the craft.
- Conditional writes are the concurrency tool: optimistic locking by
  expression, never read-modify-write without a condition.

## Consistency

- Eventually consistent by default; strongly consistent reads on
  request, priced in capacity. State which one every read needs.

## Pitfalls

- Hot partitions: the core's key-distribution rule, at AWS scale.
- Scan operations: the ALLOW FILTERING cousin — batch-and-index
  instead, or move the query to a system shaped for it.
- The 400KB item limit, quietly refusing to grow.
- Projection of all attributes into every GSI: write amplification
  as a schema decision.
- Server-side aggregation does not exist: the pipeline layer carries
  it, per the nosql core.
