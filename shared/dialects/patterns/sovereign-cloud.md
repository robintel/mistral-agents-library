---
type: pattern
family: compliance
---

# Sovereign Cloud / Gaia-X

European data sovereignty framework: data that must remain under European
jurisdiction, with no exposure to non-EU laws (e.g., US CLOUD Act).
Gaia-X is the European initiative for sovereign, interoperable cloud services.

## Core Principles

1. **Data Sovereignty** — Data owners retain full control; service
   providers cannot access data without explicit consent.
2. **Transparency** — Clear visibility into where data is stored and
   how it is processed.
3. **Interoperability** — Avoid vendor lock-in; data can be moved between
   compliant providers.
4. **Security** — Enterprise-grade security with European certifications.
5. **Compliance** — Meets GDPR, EU Data Protection Directive, and
   industry-specific regulations.

## Gaia-X Architecture

### Roles
- **Data Owner**: The entity that owns the data (your organization)
- **Data Provider**: The cloud provider hosting the data (OVHcloud, T-Systems, etc.)
- **Service Provider**: The entity providing cloud services
- **Federation Services**: Gaia-X services for identity, compliance, interoperability

### Layers
```
Application Layer     ← Your workloads
      ↓
Federation Layer       ← Gaia-X services (identity, compliance, billing)
      ↓  
Data Layer             ← Actual data storage (object, block, database)
      ↓
Infrastructure Layer   ← Physical data centers in EU jurisdiction
```

## Compliance Requirements

### Data Residency
- **Storage Location**: Data must be stored in EU data centers
- **Processing Location**: Data processing must occur in EU
- **Personnel Access**: Only EU-based personnel with appropriate clearance
- **Legal Jurisdiction**: Contracts under EU law, not US or other

### Certifications
- **ISO 27001**: Information security management
- **ISO 27017**: Cloud services security
- **ISO 27018**: PII protection in public clouds
- **SOC 2 Type II**: Service organization controls
- **C5**: German cloud computing compliance (BSI C5)
- **SecNumCloud**: French sovereign cloud certification

### Data Protection
- **Encryption**: At rest (AES-256) and in transit (TLS 1.2+)
- **Key Management**: Customer-controlled keys; no provider access
- **Access Control**: Fine-grained RBAC with MFA
- **Audit Logging**: Comprehensive logging of all data access

## Sovereign Cloud Providers

| Provider | Region | Certifications | Specialty |
|----------|--------|---------------|----------|
| OVHcloud | France, Germany, UK | ISO 27001, SOC 2, SecNumCloud | Developer-friendly |
| T-Systems | Germany | ISO 27001, ISO 27017, ISO 27018, C5 | Enterprise, telecom |
| Scaleway | France, Netherlands, Poland | ISO 27001, SOC 2 | Startup/SMB focus |
| PlusServer | Germany | ISO 27001, BSI C5 | Mid-market |

## Integration Patterns

### 1. Sovereign Object Storage
**Use Case**: Store regulated data with full sovereignty guarantees
**Contract**: Use sovereign-certified object storage providers
**Watch Out For**:
- Verify data center locations (must be EU)
- Confirm no data leaves EU jurisdiction
- Check personnel access controls

### 2. Hybrid Sovereign
**Use Case**: Some data sovereign, some data global
**Contract**:
- Sovereign storage for regulated data
- Standard cloud for non-regulated data
- Clear data classification and separation
**Watch Out For**:
- Data leakage between sovereign and non-sovereign
- Compliance scope (which regulations apply)
- Audit trail across both environments

### 3. Multi-Cloud Sovereign
**Use Case**: Avoid lock-in while maintaining sovereignty
**Contract**:
- Use Gaia-X federation services
- Data portable between compliant providers
- Unified identity and compliance management
**Watch Out For**:
- Interoperability testing between providers
- Performance differences between providers
- Cost variations across providers

## Implementation Checklist

- [ ] **Data Classification**: Identify which data requires sovereignty
- [ ] **Provider Selection**: Choose Gaia-X compliant providers
- [ ] **Contract Review**: Verify EU jurisdiction clauses
- [ ] **Architecture Design**: Ensure data stays in EU
- [ ] **Access Controls**: Implement sovereign-grade IAM
- [ ] **Encryption**: Customer-managed keys only
- [ ] **Audit Setup**: Comprehensive logging and monitoring
- [ ] **Compliance Testing**: Validate against applicable regulations
- [ ] **Exit Strategy**: Document data portability process

## Migration to Sovereign Cloud

### From Existing Cloud
1. **Inventory**: Identify all data and workloads
2. **Classify**: Determine which need sovereignty
3. **Select Provider**: Choose Gaia-X compliant provider
4. **Design Architecture**: Sovereign-first design
5. **Migrate Data**: Use secure transfer methods
6. **Test**: Verify data residency and compliance
7. **Cutover**: Switch to sovereign environment
8. **Audit**: Validate compliance with third-party audit

### From On-Premises
1. **Assess**: Current data and compliance requirements
2. **Select**: Gaia-X compliant provider
3. **Design**: Hybrid or full cloud architecture
4. **Migrate**: Secure data transfer
5. **Validate**: Compliance and data integrity
6. **Optimize**: Cost, performance, and compliance

## Common Pitfalls

| Pitfall | Impact | Mitigation |
|---------|--------|------------|
| Assuming all EU providers are sovereign | Non-compliant storage | Verify Gaia-X certification |
| Data leaving EU jurisdiction | Compliance violation | Network egress controls, geo-fencing |
| Provider personnel access | Data exposure | Contractual restrictions, audit rights |
| No exit strategy | Vendor lock-in | Data portability testing, open formats |
| Incomplete audit logging | Compliance failure | Comprehensive logging, retention policies |

## Standing Rules

- **Sovereignty is not optional** — if data must be sovereign, verify
  before storing, not after
- **Verify, don't trust** — certificates and compliance claims must be
  independently verified
- **Design for portability** — data must be movable without business
  disruption
- **Audit everything** — you must be able to prove compliance to
  regulators
- **Document jurisdiction** — maintain clear records of where data
  is stored and processed
