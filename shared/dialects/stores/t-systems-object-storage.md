---
type: store
family: object
era: eu-enterprise
---

# T-Systems Object Storage

Deutsche Telekom's enterprise-grade object storage for regulated
European industries. Built for security, compliance, and high availability.
Part of the Open Telekom Cloud (OTC) platform.

## Core discipline

1. **Enterprise security** — ISO 27001, ISO 27017, ISO 27018 certified;
   SOC 2 Type II compliant; data encryption at rest and in transit.
2. **German data centers** — All data remains within Germany unless
   explicitly configured otherwise. Ideal for strict compliance needs.
3. **High availability** — Multi-AZ by default with 99.99% SLA.
   Geo-redundant options available.
4. **Immutable objects** — Standard discipline with optional object
   locking and retention policies.
5. **OpenStack Swift base** — Full Swift API compatibility with
   S3-compatible API layer.

## Era map

- **2016-2018**: Open Telekom Cloud launch with Swift-based storage
- **2018-2020**: S3 API compatibility, enterprise features
- **2020+**: ISO certifications, geo-redundancy, object versioning
- **2022+**: Sovereign cloud options, enhanced compliance
- **2024+**: Gaia-X compliance, zero-trust architecture support

## Access patterns that matter

| Pattern | When | Watch out for |
|---------|------|---------------|
| regulated data | financial, healthcare | Compliance certifications, audit logging |
| enterprise backup | mission-critical | Retention policies, air-gapped options |
| hybrid cloud | multi-cloud strategy | Interoperability with other clouds |
| S3 compatibility | migration from AWS | ACL handling, lifecycle mapping |
| high-availability | critical workloads | Multi-AZ, geo-redundancy options |

## Integrations

- **CDC**: Open Telekom Cloud Message Queue for event streaming
- **ETL**: Integration with Data Lake, Spark, Hadoop
- **Security**: IAM with fine-grained RBAC, MFA, customer-managed keys,
  FIPS 140-2 encryption
- **Lifecycle**: Policy-based tiering, legal hold, WORM
- **Compliance**: Audit logging, data residency proofs, certification reports

## Cost levers

- Storage classes: Standard, Cold
- Multi-AZ and geo-redundancy options with different pricing
- Per-operation pricing (standard for object stores)
- Data transfer: within OTC network is free; egress may be charged
- Compliance features may have additional costs

## Defects that bite

- Complex IAM setup for enterprise requirements
- Some features require enterprise support contracts
- S3 compatibility may have subtle differences
- Geo-redundancy has higher latency than single-region
- Compliance documentation must be maintained for audits
