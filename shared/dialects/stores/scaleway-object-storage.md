---
type: store
family: object
era: eu-focused
---

# Scaleway Object Storage

French cloud provider's object storage: developer-friendly, transparent
pricing, and open-source heritage. Built on OpenStack Swift with a focus
on simplicity and predictability. Popular with European startups and
SMBs for its straightforward approach.

## Core discipline

1. **Predictable pricing** — No hidden fees; clear per-GB and per-operation
   pricing with no surprises. Egress to the public internet is free.
2. **Developer experience** — Simple API, good documentation, Terraform
   provider, and SDK support.
3. **European data centers** — Paris, Amsterdam, Warsaw; all within EU
   jurisdiction for GDPR compliance.
4. **Immutable objects** — Standard object store discipline: PUT replaces,
   DELETE removes, no partial updates.
5. **OpenStack Swift compatible** — Full Swift API support alongside
   S3-compatible API.

## Era map

- **2015-2018**: Classic Swift-based object storage
- **2018-2020**: S3 API compatibility, lifecycle management
- **2020+**: Cold storage tier, versioning, bucket policies
- **2022+**: Multi-region replication, object locking
- **2024+**: Enhanced observability, compliance certifications

## Access patterns that matter

| Pattern | When | Watch out for |
|---------|------|---------------|
| static hosting | simple websites | Automatic index.html, error pages |
| backup/archive | compliance, DR | Lifecycle policies, versioning |
| developer artifacts | CI/CD pipelines | Access control, retention |
| S3 compatibility | migration | Edge cases in ACLs, CORS |
| analytics | big data | Direct integration with data platforms |

## Integrations

- **CDC**: Scaleway Message Queuing (SMQ) for event notifications
- **ETL**: Compatible with Spark, Presto, and open-source tools
- **Security**: IAM, project isolation, TLS 1.2+, object encryption
- **Lifecycle**: Automatic transitions, expiration, object locking
- **CDN**: Scaleway CDN for static asset distribution

## Cost levers

- Storage: per GB, no minimum
- Operations: per request (GET, PUT, LIST, DELETE)
- No egress fees to public internet
- Cold storage: lower cost for infrequently accessed data
- Multi-region replication: additional storage cost

## Defects that bite

- S3 compatibility covers most operations but test thoroughly
- Cold storage retrieval can take hours
- No native append; use separate objects
- Lifecycle rules can take up to 24 hours to execute
- Bucket names are per-project, not global
