# BigQuery engine contract

Attaches alongside `sql.md`; extends, never restates. A cloud data
warehouse that speaks SQL — and bills by the byte scanned, which
makes the dialect a cost document as much as a style guide.

## Eras

Legacy SQL versus Standard SQL is the sharp boundary — `#standardSQL`
has been the answer since 2016, and legacy is never a choice in new
work. Write Standard SQL; the few legacy constructs left in old
queries are migration briefs.

## Idiom

- Cost is bytes scanned: `SELECT *` is a financial event. Select the
  columns the question needs, and the dry-run API prices the query
  before it runs — measure first is a billing feature here, not a
  slogan.
- Partitioning and clustering are the cost mechanism: no indexes
  exist — partition filters and cluster columns are what prune the
  scan, and a query that cannot prune is a full-table bill.
- STRUCT and ARRAY are first-class: nested and repeated data is
  native — `UNNEST` is the idiom for reaching inside, not flattening
  at ingestion.
- Streaming buffer rows are not yet queryable by all operations:
  know what the buffer means before promising read-after-write.

## Structure

- INFORMATION_SCHEMA is the metadata API: table sizes, partition
  boundaries, job history — the query-optimizer's evidence source.
- Materialized results over repeated heavy scans; the cost math
  decides, and the dry-run prices it.

## Pitfalls

- Unpartitioned tables: every query is a full scan on the invoice.
- ORDER BY + LIMIT still scans what it sorts — the limit does not
  cap the cost, the pruning does.
- JOINs on unclustered large tables: the broadcast/shuffle decision
  is the cost; check the execution plan, not intuition.
- Slot contention at concurrency: the queue is the failure mode,
  not an error.
