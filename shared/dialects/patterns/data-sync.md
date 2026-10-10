---
type: pattern
family: data-movement
---

# Data Synchronization

Move data between systems, environments, or regions while maintaining
consistency, availability, and sanity. This contract covers the patterns
and pitfalls of synchronization — the difference between a working system
and a data disaster is usually in the sync discipline.

## The four synchronization strategies

### 1. Migration (one-time move)
**When**: Cutover from old to new system, decommissioning source
**Contract**: Source becomes read-only, target becomes the system of record
**Pitfalls**:
- Downtime window sizing — too short causes data loss, too long causes
  business impact
- Validation — byte-for-byte, row-for-row, or business-invariant checks
- Rollback — ability to revert to source if migration fails

### 2. Coexistence (dual-write)
**When**: Both systems must stay live; gradual cutover or permanent hybrid
**Contract**: Writes go to both systems; reads can go to either or both
**Pitfalls**:
- **Conflict resolution** — same entity updated in both places simultaneously
- **Eventual consistency** — reads may see stale data from either side
- **Dual-write failures** — partial success means inconsistent state
- **Performance** — every write is doubled; every read may need merging

### 3. Synchronization (continuous sync)
**When**: Systems must stay in sync long-term; read from one or both
**Contract**: Changes in source propagate to target, or bidirectional
**Pitfalls**:
- **CDC lag** — changes may take seconds/minutes to propagate
- **Conflict windows** — if the same entity changes in both places during
  propagation, conflict resolution kicks in
- **Sync stop** — if sync breaks, systems diverge; detection and recovery
  must be automatic or at least obvious

### 4. Active-Active (multi-master)
**When**: Both systems accept writes independently; highest availability
**Contract**: Writes accepted in both places; conflicts resolved automatically
**Pitfalls**:
- **Conflict resolution is the entire design** — last-write-wins is
  usually wrong for business data
- **Vector clocks or timestamps** — you need a deterministic way to order
  concurrent changes
- **Merge logic** — some changes cannot be automatically merged (e.g.,
  deleting then recreating an entity)

## Sync direction variants

| Direction | When | Mechanism |
|-----------|------|-----------|
| on-prem → cloud | migration, backup | batch, CDC, messaging |
| cloud → on-prem | repatriation, compliance | batch, CDC, messaging |
| bidirectional | hybrid long-term | CDC + conflict resolution |
| cloud → cloud | multi-cloud, DR | native replication |

## Change Data Capture (CDC)

The engine of synchronization. CDC captures changes at the source and
streams them to the target.

### CDC sources

| Source | Mechanism | Latency | Reliability |
|--------|-----------|---------|-------------|
| Database transaction log | Native (Debezium, AWS DMS) | ms | High |
| Event streaming | Kafka, Pulsar, Kinesis | ms-100ms | Medium |
| Application events | Domain events from app | 100ms-1s | App-dependent |
| File tail | Log files, append-only | 1s-1min | File system |
| Polling | Query for changes | 1min-1hour | Low |

### CDC patterns

- **Transactional**: Changes captured at commit time; atomic with source
- **Event-sourced**: Application emits events; CDC consumes events
- **Log-based**: Read database commit log; position-based checkpointing
- **Timestamp-based**: Query for records changed since last sync
- **Trigger-based**: Database triggers fire on change

## Conflict resolution strategies

| Strategy | When it works | When it fails |
|----------|---------------|---------------|
| Last-write-wins | Non-business data, idempotent ops | Business data, concurrent updates |
| Source-wins | Authoritative source, temporary sync | True multi-master |
| Target-wins | Target is authoritative | Data loss from source |
| Merge | Schema allows it (e.g., append-only) | Non-mergeable changes |
| Human merge | High-value, low-volume | High-volume |
| Timestamp tie-break | Total ordering available | Clock skew |
| Vector clock | Causal history available | Complex merge logic |

## The synchronization pipeline

```
Source → Capture → Buffer → Transform → Apply → Target
         ↓          ↓         ↓         ↓
      CDC/Event  Queue    Filter     Apply    Verify
      Poll       Kafka    Map       Logic    Sync
      Trigger   SQS      Enrich                Health
```

## Verification is not optional

- **Idempotency**: Can the same change be applied twice safely?
- **Ordering**: Are changes applied in the same order they were made?
- **Completeness**: Are all changes captured and applied?
- **Consistency**: Do business invariants hold after sync?
- **Latency**: How stale can the target be before it affects the business?

## Standing rules

- Every sync pipeline must have a **checkpoint** — a persistent record
  of what has been synchronized, so it can resume after failure
- Every sync must be **idempotent** — the same change applied twice must
  produce the same result
- Every sync must have a **verification step** — you must prove the sync
  worked, not assume it
- Every sync must have a **rollback** — how to undo or replay if something
  goes wrong
- **CDC > Polling** — change capture is cheaper, faster, and more reliable
  than periodic polling
- **Conflict resolution must be explicit** — if you do not define it, the
  system will do something you do not want
