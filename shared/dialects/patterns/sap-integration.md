---
type: pattern
family: enterprise
---

# SAP Integration

Integrate with SAP systems — the backbone of European enterprise IT.
This contract covers the patterns, APIs, and pitfalls of connecting
non-SAP systems to SAP, or modernizing SAP landscapes themselves.

## SAP Landscape Components

| Component | Role | Integration Method |
|-----------|------|-------------------|
| **ECC / S/4HANA** | ERP core | BAPI, IDoc, OData, RFC |
| **BW/4HANA** | Data warehouse | OData, CDS Views, DSO |
| **C/4HANA** | CRM | OData, SOAP, REST |
| **SCM** | Supply chain | IDoc, BAPI, RosettaNet |
| **Fiori** | UI layer | OData, REST, SAPUI5 |
| **BTP (Business Technology Platform)** | Cloud services | REST, OData, Events |

## Integration Methods

### 1. BAPI (Business Application Programming Interface)
**When**: Real-time transactional integration with SAP business logic
**Contract**: 
- Remote-enabled function modules exposed as RFC
- ABAP-based, runs in SAP application server
- Synchronous by default; can be made asynchronous

**Pitfalls**:
- Requires ABAP development on SAP side
- Performance: network round-trip for each call
- Authorization: SAP user with appropriate roles
- Error handling: BAPI may return complex structures

**Best practices**:
- Batch BAPI calls when possible
- Use connection pooling for high-volume
- Cache reference data to minimize calls
- Implement retry logic with exponential backoff

### 2. IDoc (Intermediate Document)
**When**: Asynchronous, document-based integration
**Contract**:
- Standardized XML or flat-file format
- Message types define the document structure
- Port definitions configure the communication

**Pitfalls**:
- Complex configuration required in SAP
- Message mapping can be brittle
- Error handling requires manual intervention
- Performance: batch-oriented, not real-time

**Best practices**:
- Use IDoc extensions (Z-IDocs) for custom data
- Implement acknowledgment handling
- Monitor IDoc status tables (EDIDS, EDIDC)
- Set up alerts for stuck IDocs

### 3. OData (Open Data Protocol)
**When**: Real-time read access to SAP data; modern preferred method
**Contract**:
- RESTful API based on OASIS standard
- Exposes SAP data as entities with relationships
- Supports filtering, sorting, pagination
- Read-heavy; limited write support

**Pitfalls**:
- Performance: large queries can timeout
- Complex filtering may not be supported
- Write operations have limitations
- Version differences between SAP versions

**Best practices**:
- Use $select to limit fields (improves performance)
- Implement pagination with $top and $skip
- Cache frequently accessed data
- Use batch requests for multiple operations

### 4. RFC (Remote Function Call)
**When**: Direct ABAP function calls from external systems
**Contract**:
- Synchronous or asynchronous calls
- Can execute any ABAP function module
- Runs in SAP dialog or background process

**Pitfalls**:
- Security risk: direct code execution in SAP
- Performance: dialog RFC can consume SAP work processes
- State management: stateless by default
- Error handling: exceptions propagate to caller

**Best practices**:
- Use asynchronous RFC for long-running operations
- Limit to read-only where possible
- Validate all inputs to prevent injection
- Monitor SAP work process usage

### 5. Web Services (SOAP/REST)
**When**: Standards-based integration, often for CRM (C/4HANA)
**Contract**:
- WSDL-based SOAP services for older SAP systems
- REST services for newer cloud-based systems
- Enterprise Services in SOA Manager

**Pitfalls**:
- SOAP: heavy XML, complex WSDL
- Performance: SOAP overhead can be significant
- Authentication: Multiple options (Basic, X.509, SAML)

**Best practices**:
- Use REST when available (simpler, better performance)
- Implement proper WS-Security headers
- Cache WSDL locally to avoid runtime fetching

## SAP-Specific Patterns

### The Integration Layer Pattern
```
External System → Integration Layer → SAP
                  ↓
            Transform, Route, Buffer, Retry
                  ↓
              Handle SAP-specific protocols
```

The integration layer:
- **Transforms** between external and SAP formats
- **Routes** to the appropriate SAP system and interface
- **Buffers** to handle SAP rate limits and availability
- **Retries** failed operations with proper backoff
- **Log** all operations for audit and troubleshooting

### The Event-Driven Pattern
```
SAP Event → Message Queue → External System
  (IDoc, BAPI event, CDSHook)
```

Use SAP's event capabilities:
- **Change Documents**: Track changes to business objects
- **IDoc triggers**: Fire on business events
- **BAPI events**: Custom events from ABAP
- **CDS Views with hooks**: Modern S/4HANA approach

### The Batch Pattern
```
External System ← Batch Job ← SAP
        (File transfer, IDoc batch)
```

For high-volume, non-real-time integration:
- Use file-based transfer (CSV, XML, IDoc files)
- Schedule batch jobs during off-peak hours
- Implement file validation and reconciliation
- Use SAP's batch input (BDC) for data loading

## SAP Modernization Paths

### From ECC to S/4HANA
- **Data migration**: Use SAP Migration Cockpit or custom tools
- **Custom code**: Analyze and adapt Z-programs
- **Integration**: Review and update all interfaces
- **Testing**: Comprehensive regression testing required

### From On-Premise to Cloud (RISE with SAP)
- **Lift and shift**: Move existing systems to cloud infrastructure
- **System conversion**: Convert to S/4HANA in the cloud
- **New implementation**: Start fresh with cloud-native S/4HANA

### From Monolith to Microservices
- **API-first**: Expose SAP functionality via APIs
- **Event-driven**: Use SAP Event Mesh for asynchronous communication
- **Sidecar pattern**: Deploy integration services alongside SAP

## SAP-Specific Data Considerations

### Master Data
- **Material Master**: Central to supply chain integration
- **Customer/Vendor Master**: Critical for CRM and procurement
- **G/L Accounts**: Financial data for reporting
- **Change management**: Master data changes must sync across systems

### Transactional Data
- **Sales Orders**: Real-time or batch depending on volume
- **Purchase Orders**: Often integrated with procurement systems
- **Inventory**: Real-time availability critical
- **Production Orders**: Shop floor integration

### Organizational Data
- **Company Codes**: Legal entity boundaries
- **Plants**: Physical locations
- **Storage Locations**: Inventory management
- **Sales Organizations**: Sales structure

## Security Considerations

- **Authentication**: SAP supports multiple methods (Basic, X.509, SAML, OAuth)
- **Authorization**: SAP roles and authorizations map to external permissions
- **Data protection**: PII, financial data, and business secrets in SAP
- **Audit logging**: SAP Change Documents and external audit trails
- **Compliance**: GDPR, SOX, industry-specific regulations

## Performance Optimization

- **Connection pooling**: Reuse SAP connections for multiple operations
- **Bulk operations**: Use batch processing instead of individual calls
- **Caching**: Cache reference data and infrequently changed data
- **Parallel processing**: Execute independent calls in parallel
- **Compression**: Use compression for large data transfers

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Connection leaks | SAP work process exhaustion | Connection pooling, timeout monitoring |
| Long-running transactions | Lock contention | Keep transactions short, use async RFC |
| Data format mismatch | Integration failures | Schema validation, transformation testing |
| Authorization errors | Security failures | Role mapping, error handling |
| SAP system unavailability | Downtime | Retry logic, circuit breaker pattern |
| IDoc processing errors | Data loss | Monitoring, alerting, manual intervention |

## Standing Rules

- **Never trust SAP to be available** — always implement retry and fallback
- **Validate all inputs** — SAP systems are sensitive to malformed data
- **Monitor end-to-end** — from external system through integration to SAP
- **Test in a sandbox first** — SAP changes can have unexpected side effects
- **Document all mappings** — field-level documentation prevents integration drift
- **Plan for upgrades** — SAP upgrades can break existing integrations
