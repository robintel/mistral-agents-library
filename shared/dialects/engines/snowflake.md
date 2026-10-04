# Snowflake engine contract

Attaches alongside `sql.md`; extends, never restates. The cloud
warehouse where cost is compute time — the dial BigQuery does not
have — and where transformation in SQL is the native architecture.

## Eras

None to pin: continuous delivery, no versions to target — check
CURRENT_VERSION() and write standard SQL.

## Idiom

- Cost is warehouse size times runtime: auto-suspend is mandatory
  on every warehouse — an idle XS bills like a busy one that does
  nothing. The query-optimizer prices queries here with the
  warehouse dial, not bytes.
- No indexes exist: micro-partitions prune automatically; clustering
  keys are a hint paid for on large, slowly-mutating tables — decide
  with the pruning evidence, not intuition.
- VARIANT for semi-structured data, FLATTEN and LATERAL for reaching
  inside — JSON lands native (the etl contract's ELT placement is at
  home here).
- COPY INTO from stages for loads; zero-copy cloning for environments
  and testing — cloned access rights are the danger, not the clone.

## Structure

- Time travel is the safety net: the retention setting decides how
  deep — undelete is a feature, price it and state it.

## Pitfalls

- A warehouse that never suspends: the silent invoice.
- Oversized joins spilling to remote storage — the plan says, the
  wall clock confirms.
- Multi-cluster auto-scaling multiplying a hot warehouse instead of
  fixing the query.
- Result caches serving stale-by-design: know the staleness rules
  before promising freshness.
