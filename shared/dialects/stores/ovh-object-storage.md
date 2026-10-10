---
type: store
family: object
era: eu-focused
---

# OVHcloud Object Storage

European object storage with a strong focus on data sovereignty, GDPR
compliance, and cost predictability. OVHcloud is France's largest cloud
provider and a major alternative to US hyperscalers in Europe. The
contract abstracts OVHcloud's specifics into behavior that code depends on.

## Core discipline

1. **GDPR by default** — All data stored in OVHcloud data centers remains
   within European jurisdiction; no US PATRIOT Act exposure. This is the
   primary value proposition.
2. **No hidden costs** — Bandwidth and operations pricing is transparent
   and predictable; no egress fees within the same region.
3. **Multi-region by design** — OVHcloud operates data centers across
   Europe (France, Germany, UK, Poland) with automatic geo-redundancy
   options.
4. **Immutable objects** — same discipline as other object stores:
   PUT replaces, DELETE removes, no partial update.
5. **OpenStack Swift heritage** — OVHcloud Object Storage is built on
   OpenStack Swift, so Swift API compatibility is first-class.

## Era map

- **2011-2018**: Classic OpenStack Swift-based object storage
- **2018-2022**: S3 API compatibility layer added; multi-region
  replication; cold storage tier
- **2022+**: Strong consistency options; Gaia-X compliance certification;
  automated lifecycle management
- **2024+**: Sovereign Cloud offering with additional isolation guarantees

## Access patterns that matter

| Pattern | When | Watch out for |
|---------|------|---------------|
| GDPR-compliant archives | regulated EU data | Region selection, data residency proof |
| multi-region replication | DR, global apps | Replication lag (minutes), cost of cross-region |
| static website hosting | simple sites | DNS configuration, HTTPS certificates |
| S3 API compatibility | migration from AWS | Edge cases in ACLs, lifecycle policies |
| cold archive | infrequent access | Retrieval time (hours), minimum storage duration |

## Integrations

- **CDC**: OVHcloud Logs Data Platform (LDP) for event streaming
- **ETL**: Compatible with Spark, Hadoop via Swift/HDFS connectors
- **Security**: IAM, project-based isolation, customer-managed keys,
  encryption at rest (AES-256)
- **Lifecycle**: Automatic transitions between storage classes
- **Sovereign**: Gaia-X compliant regions with additional certification

## Cost levers

- Storage classes: Standard, High Performance, Cold Archive
- No egress fees within OVHcloud network or to the public internet
- Request pricing: per operation (PUT, GET, LIST, DELETE)
- Multi-region replication: additional storage cost for secondary region

## Defects that bite

- S3 API compatibility is not 100%; test with your SDK before migration
- Cold Archive retrieval takes up to 6 hours; plan accordingly
- Bucket names must be globally unique within your account
- No native append; use separate objects for append-like behavior
- Region selection is critical for GDPR; verify before storing PII
