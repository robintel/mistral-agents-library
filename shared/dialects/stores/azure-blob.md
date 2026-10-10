---
type: store
family: object
---

# Azure Blob Storage

Microsoft's object storage with tiered access and deep integration with
Azure services. The contract focuses on behavior relevant to code that
stores and retrieves blobs.

## Core discipline

1. **Three service levels** — Blob Storage (objects), File Storage
   (SMB), and Table Storage (NoSQL key-value). This contract is for
   Blob Storage.
2. **Containers, not buckets** — the top-level namespace is called a
   container; it behaves the same as buckets in other systems.
3. **Strong consistency for most operations** — reads after writes see the
   write immediately for most operations, but LIST may lag briefly.
4. **Immutable by default** — same discipline: PUT replaces, DELETE
   removes; versioning and snapshots are opt-in.
5. **Access tiers within the same account** — Hot, Cool, Archive per
   blob or per container; change tier without moving data.

## Era map

- **2011-2018**: Classic Blob Storage — containers, blobs, basic tiers
- **2018+**: Premium SSD (block blobs), Hierarchical Namespace for
  Azure Data Lake Storage Gen2 compatibility
- **2020+**: Object-level immutability policies, static website hosting
- **2022+**: Azure Data Lake Storage Gen2 (ADLS Gen2) unifies Blob
  with hierarchical file system semantics

## Access patterns that matter

| Pattern | When | Watch out for |
|---------|------|---------------|
| hot/cool/archive tiers | cost optimization | rehydration time for Archive (hours) |
| hierarchical namespace | analytics, HDFS | ADLS Gen2 required; different auth model |
| static websites | hosting | $web container; no server-side logic |
| Azure Functions | serverless | blob triggers via Event Grid |
| SQL bulk import/export | data loading | bcp utility or PolyBase |

## Integrations

- **CDC**: Event Grid for blob created/deleted/modified events
- **ETL**: Azure Data Factory, Synapse, Databricks
- **Security**: RBAC, SAS tokens, Azure AD Kerberos, Customer-Managed
  Keys (CMK)
- **Lifecycle**: tier transitions, delete, snapshot policies

## Cost levers

- Access tiers: Hot, Cool, Archive; per-GB pricing
- Operations: write, read, list, delete have different prices
- Data transfer: egress is charged; use Azure CDN for static content
- Geo-redundant vs. locally redundant storage — HA vs. cost

## Defects that bite

- Event Grid event delivery is at-least-once; handle duplicates
- Archive tier requires rehydration before access (hours); plan ahead
- Blob name case-sensitive; Linux vs. Windows client quirks
- Container names must be lowercase; no dots
- No native append; use Block Blobs with separate blocks
