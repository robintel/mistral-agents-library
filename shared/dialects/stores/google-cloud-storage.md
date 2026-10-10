---
type: store
family: object
---

# Google Cloud Storage

Object storage with strong consistency and deep integration with Google
Cloud's ecosystem. The contract abstracts GCS's specifics into the
behavior that code depends on.

## Core discipline

1. **Strong consistency by default** — reads after writes see the write
   immediately, including LIST after PUT/DELETE. This is the key
   differentiator from S3.
2. **Objects are immutable** — same as S3: PUT replaces, DELETE removes,
   no partial update. Versioning is opt-in.
3. **Unified namespace** — all buckets share a global namespace;
   bucket names must be globally unique DNS names.
4. **Metadata travels with the object** — same discipline as S3.
5. **Resumable uploads** — the preferred path for large objects
   (supports resume after failure); simpler than S3's multi-part.

## Era map

- **2010-2020**: Classic GCS — buckets, objects, strong consistency
- **2020+**: Fine-grained IAM, VPC Service Controls, dual-region
  buckets, turndown for object lifecycle
- **2023+**: Autoclass for automatic storage class transitions

## Access patterns that matter

| Pattern | When | Watch out for |
|---------|------|---------------|
| write-once, read-many | static sites, archives | CDN integration |
| global distribution | multi-region apps | multi-region bucket for low latency |
| nearline/coldline | infrequent access | minimum storage duration charges |
| Hadoop/Spark | big data | GCS connector, service account impersonation |
| Firestore export/import | managed DB | gsutil for bulk operations |

## Integrations

- **CDC**: Pub/Sub notifications for object changes (the GCS answer to
  S3 Event Notifications)
- **ETL**: Dataflow, Dataproc, BigQuery native support
- **Security**: IAM, ACLs (legacy), VPC Service Controls, Customer-Supplied
  Encryption Keys (CSEK)
- **Lifecycle**: age-based transitions, delete actions

## Cost levers

- Storage classes: Standard, Nearline, Coldline, Archive
- Operations: Class A (writes, deletes) vs. Class B (reads)
- Network: egress within same region is free; cross-region is charged
- Request pricing: LIST is expensive; design prefix structure carefully

## Defects that bite

- No native append; use separate objects or resumable uploads with
  composite objects
- Object versioning is not retroactive; enable before you need it
- Bucket deletion is not immediate (soft delete, then purge)
- 5 TB object limit; for larger, use composite objects
