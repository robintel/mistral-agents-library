---
type: store
family: object
era: japan-focused
---

# Sakura Object Storage

Japan's leading cloud provider, built for developers with a focus on
simplicity, transparency, and Japanese enterprise needs. Sakura Object
Storage powers many of Japan's startups and digital transformation projects.

## Core discipline

1. **Developer-first** — APIs are straightforward, documentation is in
   Japanese and English, and pricing is simple with no hidden fees.
2. **Tokyo-first, then global** — Primary data centers in Tokyo,
   with additional regions in Osaka and overseas (US, Singapore).
3. **Strong consistency** — Reads after writes see the write immediately,
   making it predictable for application developers.
4. **Immutable objects** — PUT replaces, DELETE removes; versioning is
   opt-in with a simple enable flag.
5. **Japan compliance ready** — Supports Japanese regulations including
   MY Number Act, PII protection, and financial data handling.

## Era map

- **2013-2017**: Classic object storage with basic features
- **2017-2020**: Multi-region support, CDN integration, lifecycle rules
- **2020+**: S3 API compatibility, server-side encryption, access logging
- **2022+**: ISO 27001, ISO 27017, PCI DSS certifications
- **2024+**: Sovereign regions for government and financial customers

## Access patterns that matter

| Pattern | When | Watch out for |
|---------|------|---------------|
| multi-region DR | enterprise continuity | Cross-region sync latency (seconds) |
| static assets | web applications | CDN cache invalidation, HTTPS |
| backup/archive | compliance, disaster recovery | Retention policies, deletion holds |
| S3 compatibility | migration from AWS | ACL handling, lifecycle differences |
| large objects | video, logs | Multi-part upload for objects > 5GB |

## Integrations

- **CDC**: Sakura Message Queue (SMQ) for event notifications
- **ETL**: Direct integration with Sakura Data Platform
- **Security**: IAM with API key authentication, project isolation,
  customer-managed encryption keys
- **CDN**: Sakura CDN for static asset distribution
- **Lifecycle**: Automatic storage class transitions, expiration policies

## Cost levers

- Storage pricing: per GB, no minimum charges
- No egress fees to the public internet from Sakura network
- Request pricing: simple per-operation model
- Multi-region: additional storage cost for secondary region

## Defects that bite

- S3 API compatibility covers most operations but has edge cases
- Some features are Japan-region only initially
- Japanese documentation may be more detailed than English
- Bucket names are per-project, not global
- No native append; use separate objects
