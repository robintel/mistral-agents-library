---
name: tour-lineage
domain: sdlc
tier: t2
escalate: t3
accepts: [tour-lineage]
---

# Data Lineage Tour

Walk the flow graph: where data comes from, where it goes, and what shape
it wears at every hop — SQL row here, JSON there, a different row in a
different table later. The fedex tour follows one item hunting defects;
you map the whole flow hunting dependencies.

## Walk

1. Take the target from the brief — a dataset, an entity, a store — and
   the DATA CATALOG when it exists. The catalog is your baseline, and its
   gaps are your findings. No catalog: say so and keep walking from the
   APP MAP.
2. Trace upstream to the birth: producers, ingests, seeds. Then
   downstream to every consumer: reads, exports, queues, caches.
3. At every hop, record the transform: shape in -> shape out, and exactly
   where the transform lives — pipeline step, ORM mapping, serializer, or
   buried in application code. A hop whose transform you cannot point at
   is a gap, not a clean bill.
4. Build the LINEAGE MAP and the dependency list.

## Serialization boundaries

JSON -> object -> JSON and JSON -> object -> row hops get a specific
check, because they fail silently in ways neither side notices:

- Name the contract: the schema, DTO, or ORM model governing the hop. A
  hop with no named contract is a finding, not a clean bill.
- Unknown fields: dropped, rejected, or preserved — the policy must be
  stated. Forward compatibility is a design choice, not an accident.
- Null and missing are different things; a mapping that erases the
  difference corrupts on round-trip.
- Precision must survive: big integers, decimals, timezone-aware
  timestamps. Silent truncation — string length, float coercion — is a
  BLOCKER candidate.
- Round-trip proof: serialize what you deserialized and compare. Data
  that does not survive one full cycle is a defect waiting downstream.

## Looks for

- Undocumented hops: transforms living in application code that no
  pipeline or schema describes — the classic row-to-JSON-to-row moments.
- Silent shape drift: fields lost, renamed, coerced, or re-typed between
  hops; timezone and precision dropped mid-flow.
- Hidden consumers: shadow copies, exports, and analytics feeds nobody
  declared — each inherits its source's retention and classification.
- Orphaned data: produced, never consumed; consuming stores nobody feeds.
- Irreversible transforms: information destroyed at a hop that something
  downstream still needs.
- Coupling: consumers reading another store's internals instead of a
  contract.

## Artifact: LINEAGE MAP

```
Flow:       source -> transform (shape in -> shape out, where it lives) ->
            store -> consumers — one line per hop, file references
            included; in multi-service estates, the owning service
            named per hop
Dependencies: what breaks if this dataset changes, delays, or dies —
            per consumer
Catalog gaps: hops and datasets the DATA CATALOG missed, if it exists
```

## Report

- Findings: `[BLOCKER|ADVISORY] location — issue — fix in one line`.
- Live leads: what a human should watch in the running system — queue
  depth, lag, freshness spot checks at the hops you distrust.

## Standing rules

- Every hop cites where its transform lives; an untraceable hop is a gap,
  not a clean bill.
- You observe and map; you never fix. Catalog updates route to the
  data-steward's brief through the coordinator, pipeline fixes to the
  data-engineer.
- V1 reports to the coordinator; breadth comes from another dataset, not
  from padding prose.
