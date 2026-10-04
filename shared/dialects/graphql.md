# GraphQL dialect

Attaches alongside the implementation language's contract for schema
and resolver work. GraphQL is a contract language: the schema is the
promise, and every discipline follows from keeping it.

## Eras

The stable core: schema and resolver discipline, unchanged since
2015. The composable era: federation over schema stitching in
multi-service estates. The production era: persisted queries for
client traffic. Write the era the estate runs.

## Idiom

- Schema-first: explicit types; non-null only where the promise is
  real — nullable is a design decision, never a default.
- Resolvers stay thin: a resolver assembles, it does not fetch. The
  N+1 resolver is the classic GraphQL defect; DataLoader-style
  batching where fan-out is real.
- Connections (cursor pagination) for any list that grows: offsets
  lie under concurrent writes.
- Errors are partial: the response contract is data plus errors —
  each error carries code, path, and message; a swallowed failure
  surfacing as an empty object is a contract violation.

## Structure

- Query cost is the server's problem: depth and complexity limits
  guard the resolvers — an unbounded query is DoS wearing GraphQL
  clothes.
- Federation and schema composition are architecture decisions with
  their own brief, never a ride-along on a resolver fix.

## Testing

- The schema is the contract: query tests assert shapes, not
  resolver internals — the automation-reviewer's intent rule applies
  double here.

## Pitfalls

- N+1: one resolver firing one fetch per item.
- A list field without pagination: the schema quietly promising
  unbounded results.
- Introspection and query depth unguarded in production.
- Resolver errors surfacing as nulls the client cannot distinguish
  from real nulls.
