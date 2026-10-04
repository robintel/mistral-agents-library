# ETL/ELT pattern contract

Attaches to pipeline work — the data-engineer's briefs — rather than
to a language. The pattern is extract, transform, load; the placement
of T is the design decision; idempotency is the law.

## E versus T versus L

- ELT: the warehouse transforms — versioned SQL in the target
  (bigquery, snowflake, the postgres contract); cheapest for volume.
- ETL: the pipeline transforms — mandatory when data must be shaped
  before it lands: PII stripped or tokenized at extraction
  pre-empts the GDPR auditor's finding instead of answering it.
- Placement is a priced decision in the design, never inherited
  gravity.

## Idempotency (the law)

- A rerun produces the same world: merge and upsert keyed loads, or
  partition overwrite. Append-on-rerun is the classic double-count
  defect.
- The pipeline is a function over time windows, not a cron job:
  backfilling a range is a designed capability from day one — replay
  without side effects, or the past cannot be trusted.

## Extract discipline

- Sources drift: explicit contracts at every boundary — the lineage
  map names the hops. A schema change breaks loudly at the gate,
  never silently into the warehouse.
- CDC versus batch is a priced decision: CDC buys freshness and
  brings double-write hazards; batch buys simplicity and brings lag.
  State which, and the watermark that defines caught-up.
- Late data is a policy, not a surprise: how late is accepted, and
  what restatement means for already-published numbers.

## Load discipline

- Reconciliation at every hop: counts and checksums against the
  source — the data-engineer's invariant gates live here; a load
  without verification is a hope.
- Failure mid-run is the norm: steps resumable, partial loads
  visible, completion never assumed from silence.
- Orchestration is a DAG: dependencies explicit; a cycle is a design
  error the plan catches, not the runtime.

## Pitfalls

- Double-counting on rerun: the append-shaped load.
- Silent type coercion at extraction — the serialization boundary
  rules apply at every hop.
- Backfills shipped as one-off scripts.
- Watermarks assuming clock sync across systems.
