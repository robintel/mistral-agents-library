# Spark platform contract

The compute engine that ate MapReduce: the big-data default above
YARN, standalone, or managed. DataFrames are the idiom; the RDD is
the era marker.

## Eras

The RDD era is over in application code: DataFrames and SQL are the
modern idiom — Catalyst optimizes what it can see, and UDFs hide the
plan from it. Spark 3's adaptive query execution (AQE) handles skew
and join strategy at runtime. Write the era the codebase and
version run.

## Idiom

- Lazy by design: transformations build the plan, actions execute
  it — the plan is readable and the reading is the debugging.
- Shuffle is the cost: same law as the hadoop contract — broadcast
  joins for small tables, partitioning aligned to the join keys.
- The driver is a single point: collect() on big results is an OOM
  with a plan; write out, never back, unless the result is small by
  design.
- Cache with a reason and an eviction plan: caching without a reuse
  count is memory spent on superstition.

## Structure

- Structured Streaming for pipelines that never end: the same
  DataFrame semantics over an unbounded table — checkpointing is
  the contract, and its storage is part of the design.
- Delta-shaped tables where the ecosystem uses them: ACID on the
  lake — the transactional habit arriving late to big data, and
  welcome.

## Pitfalls

- UDFs costing optimization: a Catalyst-invisible black box per row.
- Skew handled manually where AQE cannot: salt or isolate, in the
  plan.
- Speculative execution assuming idempotent writes — the etl law
  applies to every task, retried or first.
- local[1] and default memory settings surviving into production
  configs.
