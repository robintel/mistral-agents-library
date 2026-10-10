---
type: store
family: object
---

# HPE Object Storage

Enterprise-grade object storage for HPE customers, often on-premises or
in hybrid cloud environments. Built for large-scale, compliance-heavy
enterprises. The contract abstracts HPE's enterprise specifics.

## Core discipline

1. **Multi-tenant by design** — supports multiple tenants within a
   single cluster; tenant isolation is first-class.
2. **Strong consistency** — reads after writes see the write immediately,
   matching enterprise expectations.
3. **Immutable objects** — same discipline: no partial updates; versioning
   opt-in.
4. **Erasure coding** — data is distributed across nodes with configurable
   redundancy (e.g., 10+9, 12+9). Not just replication.
5. **Quota and chargeback** — enterprise features for cost allocation
   and showback/chargeback reporting.

## Era map

- **Helion era (pre-2020)**: Integrated with OpenStack Swift
- **Container era (2020-2022)**: Native support for container images,
  object versioning, cross-cluster replication
- **Cloud era (2022+)**: Hybrid cloud object storage, S3 API compatibility
  layer, policy-based tiering

## Access patterns that matter

| Pattern | When | Watch out for |
|---------|------|---------------|
| compliance archives | regulated data | WORM (Write Once, Read Many) support |
| medical imaging | PACS, DICOM | large object handling, retrieval SLAs |
| backup/recovery | enterprise DR | snapshot consistency, restore testing |
| hybrid cloud | on-prem + public | S3 API compatibility for portability |
| chargeback | cost allocation | quota enforcement, reporting granularity |

## Integrations

- **CDC**: Notifications via AMQP or REST webhooks for object changes
- **ETL**: Integration with HPE Ezmeral Data Fabric for analytics
- **Security**: LDAP/AD, RBAC, encryption at rest (FIPS 140-2),
  customer-managed keys
- **Lifecycle**: policy-based tiering, expiration, legal hold

## Cost levers

- Storage tiers: Performance, Standard, Archive
- Redundancy levels: single-node, multi-node, multi-site
- Operations: per-request pricing; batch operations for efficiency
- Network: internal vs. external bandwidth may be priced differently

## Defects that bite

- Erasure coding rebuild after node failure consumes cluster resources
- S3 API compatibility may have edge-case differences; test with
  your SDK
- Quota limits can cause hard failures; monitor and plan
- Object names with special characters may need escaping in some clients
- Cross-cluster replication has latency; not for real-time sync
