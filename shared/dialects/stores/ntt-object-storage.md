---
type: store
family: object
era: japan-focused
---

# NTT Communications Object Storage

NTT Communications (NTT Com) object storage: enterprise-grade cloud
services from Japan's telecommunications giant. Known for high reliability,
global network, and enterprise support. Ideal for Japanese enterprises
and multinational companies operating in Japan.

## Core discipline

1. **Enterprise reliability** — 99.99% SLA with financially backed
   guarantees; global network backbone ensures low latency.
2. **Japanese compliance** — Meets Japanese regulations including
   MY Number Act, Personal Information Protection Act (PIPA),
   and Financial Instruments and Exchange Act (FIEA).
3. **Global reach, Japan-first** — Data centers in Japan (Tokyo,
   Osaka) with global connectivity via NTT's Tier-1 network.
4. **Immutable objects** — Standard object store: PUT replaces,
   DELETE removes; versioning and object locking available.
5. **Multi-protocol support** — S3-compatible API, Swift API, and
   REST API for flexibility.

## Era map

- **2015-2018**: Enterprise cloud platform with object storage
- **2018-2020**: S3 compatibility, lifecycle management, encryption
- **2020+**: Multi-region replication, compliance certifications
- **2022+**: ISO 27001, ISO 27017, ISO 27018 certifications
- **2024+**: Enhanced Japan-specific compliance, global edge caching

## Access patterns that matter

| Pattern | When | Watch out for |
|---------|------|---------------|
| enterprise archives | compliance, long-term retention | Retention policies, legal hold |
| global distribution | multinational companies | CDN integration, latency optimization |
| backup/DR | business continuity | Cross-region replication, restore testing |
| S3 compatibility | migration, multi-cloud | API differences, authentication |
| high-availability | critical workloads | Multi-AZ, geo-redundancy SLA |

## Integrations

- **CDC**: NTT Com Message Queue for event notifications
- **ETL**: Integration with data platforms, analytics tools
- **Security**: IAM with RBAC, MFA, customer-managed keys, encryption
- **Lifecycle**: Automatic tiering, expiration, object locking
- **Network**: NTT global backbone for low-latency access

## Cost levers

- Storage classes: Standard, Infrequent Access, Archive
- Multi-region replication: additional storage and network costs
- Data transfer: NTT network may offer better pricing than public internet
- Operations: per-request pricing standard for object stores
- Enterprise support: premium features and SLAs available

## Defects that bite

- Enterprise features may require consultation with NTT
- S3 compatibility good but verify edge cases
- Some features Japan-region only initially
- Multi-region replication has latency; not for real-time sync
- Documentation primarily in Japanese for some features
