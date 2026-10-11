---
type: pattern
family: ai
---

# GDPR-Compliant RAG Pattern Contract

Attaches to any work building or using **Retrieval-Augmented Generation (RAG)** systems that process **personal data of EU citizens**. This contract establishes **GDPR-compliant RAG architecture patterns, data handling requirements, and compliance checklists** for European deployments. Loads alongside the rag-pattern dialect and any industrial AI contracts.

GDPR compliance in RAG is **not optional** — it's a **legal requirement** with fines up to 4% of global revenue or €20M. A GDPR-compliant RAG system must respect data subject rights, ensure lawful processing, maintain data residency, and implement appropriate security measures throughout the entire pipeline.

## The Discipline

GDPR-compliant RAG requires **privacy-by-design and privacy-by-default** at every layer:

- **Data minimization**: Only process personal data necessary for the RAG purpose
- **Purpose limitation**: Use personal data only for specified, explicit purposes
- **Lawful basis**: Establish and document lawful basis for processing (consent, contract, legitimate interest)
- **Transparency**: Inform data subjects about data processing activities
- **Data subject rights**: Enable exercise of all GDPR rights (access, rectification, erasure, portability, objection)
- **Data residency**: Keep EU citizen data within EU jurisdiction
- **Security**: Implement technical and organizational measures appropriate to risk
- **Accountability**: Document all processing activities and compliance decisions

- **Risk assessment**: Conduct DPIA for high-risk RAG deployments
- **Vendor due diligence**: Ensure all third-party providers offer GDPR guarantees
- **Audit readiness**: Maintain records for regulatory inspection
- **Continuous compliance**: Monitor for changes in law, data, and processing

## GDPR Principles for RAG

### 1. Lawful, Fair, and Transparent Processing (Article 5(1)(a))

**Requirement**: Personal data must be processed lawfully, fairly, and in a transparent manner.

**RAG Implications**:
- **Lawful Basis**: Determine and document lawful basis for each processing activity
  - Consent: User explicitly agrees to RAG processing
  - Contract: Processing necessary for contract performance
  - Legitimate Interest: Balancing test for RAG benefits vs individual rights
  - Legal Obligation: Processing required by law
  - Public Task: Processing for public interest tasks
- **Transparency**: Provide privacy notices explaining RAG processing
  - What data is collected and used
  - How RAG processes the data
  - Who has access to results
  - Data retention periods

**Implementation Checklist**:
- [ ] Document lawful basis for each RAG use case
- [ ] Publish clear privacy notices for RAG systems
- [ ] Provide opt-out mechanisms where consent is basis
- [ ] Maintain lawful basis records for audit

### 2. Purpose Limitation (Article 5(1)(b))

**Requirement**: Personal data must be collected for specified, explicit, and legitimate purposes and not further processed in a manner incompatible with those purposes.

**RAG Implications**:
- Define specific RAG purposes (e.g., "technical documentation retrieval for engineers")
- Prevent use of RAG system for unrelated purposes
- Document each RAG system's approved use cases
- Implement access controls limiting use to approved purposes

**Implementation Checklist**:
- [ ] Define and document specific purposes for each RAG system
- [ ] Implement purpose-based access controls
- [ ] Prevent purpose creep through technical and policy measures
- [ ] Review and update purposes periodically

### 3. Data Minimization (Article 5(1)(c))

**Requirement**: Personal data must be adequate, relevant, and limited to what is necessary for the intended purposes.

**RAG Implications**:
- **Input Minimization**: Remove unnecessary personal data from documents before ingestion
- **Embedding Minimization**: Use techniques that reduce PII in vector representations
- **Context Minimization**: Limit context window to necessary information only
- **Storage Minimization**: Only store vectors and metadata necessary for retrieval

**Minimization Techniques**:
```
1. PII Redaction: Remove names, emails, IDs, addresses before embedding
   - Use regex patterns: \b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b
   - Use NER models: Recognize and remove PERSON, ORG, LOCATION, etc.
   - Use dedicated tools: Microsoft Presidio, Google DLP, AWS Macie

2. Pseudonymization: Replace identifiers with artificial identifiers
   - Hash PII before embedding
   - Maintain separate, secure mapping table
   - Can enable some processing without full GDPR scope

3. Anonymization: Irreversibly remove personal identifiers
   - Aggregate data to group level
   - Remove all direct and indirect identifiers
   - Consult legal on sufficiency (not always possible for RAG)

4. Selective Ingestion: Only ingest documents containing necessary data
   - Filter by metadata (department, classification)
   - Exclude personal correspondence, HR records
   - Focus on technical, product, process documentation
```

**Implementation Checklist**:
- [ ] Implement PII detection and redaction pipeline
- [ ] Apply pseudonymization where appropriate
- [ ] Filter documents by necessity before ingestion
- [ ] Regularly audit data for minimization opportunities

### 4. Accuracy (Article 5(1)(d))

**Requirement**: Personal data must be accurate and, where necessary, kept up to date.

**RAG Implications**:
- Ensure source documents are accurate and current
- Implement document versioning and update mechanisms
- Provide mechanisms for data subjects to correct inaccurate information
- Regularly re-embed updated documents

**Implementation Checklist**:
- [ ] Implement document version control
- [ ] Set up update workflows for source documents
- [ ] Enable data subject correction requests
- [ ] Schedule periodic document reviews

### 5. Storage Limitation (Article 5(1)(e))

**Requirement**: Personal data must be kept in a form that permits identification for no longer than necessary.

**RAG Implications**:
- Set and enforce retention periods for vectors and metadata
- Implement automatic deletion after retention period expires
- Enable manual deletion upon data subject request
- Consider separate retention for different data types

**Retention Guidelines**:
```
┌─────────────────────────┬─────────────────────────────────────┐
│ Data Type                │ Recommended Retention                │
├─────────────────────────┼─────────────────────────────────────┤
│ Technical Documentation  │ 2-5 years (product lifecycle)        │
│ Meeting Minutes          │ 1-2 years (business relevance)       │
│ Customer Support Tickets │ 6 months - 2 years                    │
│ User Queries             │ 30-90 days (unless logged for audit) │
│ System Logs              │ 30-180 days                          │
│ Training Data            │ Duration of model usefulness + 1 year│
└─────────────────────────┴─────────────────────────────────────┘
```

**Implementation Checklist**:
- [ ] Define retention periods for each data category
- [ ] Implement automatic deletion mechanisms
- [ ] Enable manual deletion on request
- [ ] Maintain deletion logs for audit

### 6. Integrity and Confidentiality (Article 5(1)(f))

**Requirement**: Personal data must be processed in a manner that ensures appropriate security, including protection against unauthorized or unlawful processing and against accidental loss, destruction, or damage.

**RAG Implications**:
- Implement encryption at rest and in transit
- Apply access controls to vector database and LLM
- Maintain audit logs of all RAG operations
- Regularly test security through penetration testing

**Security Measures**: See Security section below

## Data Subject Rights in RAG

### 1. Right to Access (Article 15)

**Requirement**: Data subjects can request access to their personal data and information about processing.

**RAG Challenges**:
- Vectors are not human-readable
- Difficult to identify which vectors contain specific individual's data
- Need to map vectors back to source documents

**Implementation**:
```
1. Vector-to-Document Mapping:
   - Maintain metadata linking each vector to source document
   - Store document ID, chunk ID, and original text references
   - Enable lookup of all vectors derived from documents containing specific PII

2. Access Request Workflow:
   - Receive and verify data subject identity
   - Search vector database for documents containing subject's PII
   - Retrieve all matching vectors and metadata
   - Provide in human-readable format (reconstruct or provide original documents)
   - Include processing purposes, recipients, retention periods

3. Response Format:
   - List of documents containing personal data
   - For each document: purpose, legal basis, retention, recipients
   - Vector representations (if requested, in readable format)
```

**Response Time**: Within 1 month (extendable to 2 months for complex requests)

### 2. Right to Rectification (Article 16)

**Requirement**: Data subjects can request correction of inaccurate personal data.

**RAG Implementation**:
```
1. Correction Workflow:
   - Verify data subject identity
   - Identify all documents and vectors containing inaccurate data
   - Update source documents with corrections
   - Re-embed corrected documents
   - Delete old vectors

2. Technical Approach:
   - Version documents with correction history
   - Mark old vectors as deprecated
   - Gradual replacement of old with new vectors

3. Propagation:
   - Update all dependent RAG systems
   - Consider impact on LLM responses (may require model retraining)
```

**Response Time**: Within 1 month

### 3. Right to Erasure ("Right to be Forgotten") (Article 17)

**Requirement**: Data subjects can request deletion of their personal data.

**RAG Implementation**:
```
1. Identification:
   - Find all documents containing data subject's PII
   - Identify all vectors derived from those documents
   - Include vectors in vector database, cache, backups

2. Deletion Process:
   - Delete source documents
   - Delete all associated vectors from vector database
   - Clear cache entries
   - Update indexes

3. Verification:
   - Confirm deletion from all systems
   - Document deletion for audit
   - Handle partial deletions (shared documents)

4. Special Cases:
   - Legal obligation to retain: Anonymize instead of delete
   - Public interest: May override erasure right
   - Exercising freedom of expression: May limit erasure
```

**Implementation Checklist**:
- [ ] Maintain comprehensive vector-to-document mapping
- [ ] Implement cascade delete (document → vectors → cache)
- [ ] Verify deletion from all storage locations
- [ ] Document erasure decisions and exceptions
- [ ] Handle partial document deletions (redaction)

**Response Time**: Within 1 month

### 4. Right to Restriction of Processing (Article 18)

**Requirement**: Data subjects can request restriction of processing in certain circumstances.

**RAG Implementation**:
```
Circumstances:
- Accuracy contested (until verified)
- Processing unlawful but subject opposes erasure
- Data no longer needed but subject needs for legal claims
- Pending verification of lawful basis

Implementation:
- Flag vectors as restricted in vector database
- Exclude from search results
- Maintain but do not process for RAG
- Lift restriction when condition resolved
```

### 5. Right to Data Portability (Article 20)

**Requirement**: Data subjects can receive their personal data in a structured, commonly used, machine-readable format and transmit to another controller.

**RAG Implementation**:
```
1. Export Format:
   - JSON or CSV with clear structure
   - Include: source documents, metadata, vector representations
   - Provide in open, interoperable format

2. Vector Export:
   - Provide vector embeddings in standard format
   - Include: vector array, dimension, model used, timestamp
   - Option: Re-embed with different model for portability

3. Direct Transmission:
   - Where technically feasible, transmit directly to new controller
   - Use secure APIs for direct transfer
```

**Response Time**: Within 1 month

### 6. Right to Object (Article 21)

**Requirement**: Data subjects can object to processing based on legitimate interests or for direct marketing.

**RAG Implementation**:
```
1. Objection Handling:
   - Process objection request
   - Assess if compelling legitimate grounds override objection
   - Cease processing if no overriding grounds

2. RAG-Specific:
   - Stop including data subject's data in RAG retrieval
   - May need to delete or restrict vectors
   - Document decision and rationale
```

### 7. Rights Related to Automated Decision-Making (Article 22)

**Requirement**: Data subjects have rights regarding solely automated decisions with legal or significant effects.

**RAG Implications**:
- If RAG output used for automated decision-making (e.g., hiring, credit scoring):
  - Provide meaningful information about logic involved
  - Enable human intervention and review
  - Allow data subject to contest decision
- Document whether RAG is used for automated decision-making

## Personal Data Handling in RAG Pipeline

### RAG Pipeline Stages and GDPR Considerations

```
┌─────────────────────────────────────────────────────────────────────┐
│                      RAG PIPELINE WITH GDPR CONTROLS                      │
├─────────────────────┬──────────────────┬────────────────────────────────┤
│ Stage                 │ GDPR Consideration│ Required Measures                        │
├─────────────────────┼──────────────────┼────────────────────────────────┤
│ 1. Document Ingestion │ Lawful basis       │ Verify basis for each document type     │
│                     │ Data minimization  │ Filter unnecessary PII                 │
│                     │ Purpose limitation  │ Ensure documents match RAG purpose       │
├─────────────────────┼──────────────────┼────────────────────────────────┤
│ 2. PII Detection      │ Accuracy           │ Use accurate PII detection models        │
│                     │ Data minimization  │ Identify all PII for redaction           │
│                     │ Storage limitation  │ Don't store detection results unnecessarily│
├─────────────────────┼──────────────────┼────────────────────────────────┤
│ 3. PII Redaction      │ Accuracy           │ Ensure redaction doesn't break meaning   │
│                     │ Integrity          │ Maintain document usability              │
│                     │ Data minimization  │ Redact all identified PII                │
├─────────────────────┼──────────────────┼────────────────────────────────┤
│ 4. Chunking           │ Purpose limitation  │ Chunk only necessary content             │
│                     │ Data minimization  │ Avoid creating chunks with excess PII   │
│                     │ Storage limitation  │ Set appropriate chunk sizes              │
├─────────────────────┼──────────────────┼────────────────────────────────┤
│ 5. Embedding          │ Data residency     │ Use EU-based embedding providers         │
│                     │ Integrity          │ Ensure embedding preserves privacy        │
│                     │ Confidentiality    │ Encrypt data in transit to embedding API  │
├─────────────────────┼──────────────────┼────────────────────────────────┤
│ 6. Vector Storage     │ Data residency     │ Store in EU-based vector database         │
│                     │ Integrity          │ Implement access controls                 │
│                     │ Confidentiality    │ Encrypt vectors at rest                  │
├─────────────────────┼──────────────────┼────────────────────────────────┤
│ 7. Retrieval          │ Purpose limitation  │ Only retrieve for approved purposes        │
│                     │ Integrity          │ Prevent unauthorized access               │
│                     │ Confidentiality    │ Log all retrieval operations              │
├─────────────────────┼──────────────────┼────────────────────────────────┤
│ 8. LLM Generation     │ Purpose limitation  │ Use LLM only for approved purposes        │
│                     │ Integrity          │ Prevent prompt injection attacks          │
│                     │ Confidentiality    │ Don't log user queries with PII          │
├─────────────────────┼──────────────────┼────────────────────────────────┤
│ 9. Response Delivery  │ Purpose limitation  │ Deliver only appropriate responses        │
│                     │ Accuracy           │ Verify response accuracy                  │
│                     │ Confidentiality    │ Secure response transmission             │
└─────────────────────┴──────────────────┴────────────────────────────────┘
```

### Document Processing Workflow

```
Input Document
      │
      ▼
┌──────────────────┐
│  Classification   │  ← Is this personal data?
└─────────┬─────────┘
      │
      ├─── No ──────────────────────► Standard ingestion
      │
      ▼ Yes
┌──────────────────┐
│  PII Detection    │
└─────────┬─────────┘
      │
      ▼
┌──────────────────┐
│  Lawful Basis     │  ← Verify legal basis exists
│  Assessment       │
└─────────┬─────────┘
      │
      ├─── No basis ─────────────────► Reject or seek consent
      │
      ▼ Has basis
┌──────────────────┐
│  PII Redaction    │  ← Remove or pseudonymize
└─────────┬─────────┘
      │
      ▼
┌──────────────────┐
│  Chunking &       │
│  Embedding        │
└─────────┬─────────┘
      │
      ▼
┌──────────────────┐
│  EU Vector DB     │  ← Store with full controls
└──────────────────┘
```

## EU Data Residency Requirements

### 1. Embedding Model Residency

**Requirement**: Embedding models processing EU citizen data must operate within EU jurisdiction.

**Compliant Options**:

| Provider | EU Data Centers | Notes |
|----------|-----------------|-------|
| Mistral AI | ✅ France, Germany | All processing in EU |
| Hugging Face | ⚠️ US-based API | Self-host in EU for compliance |
| OpenAI | ❌ US-only | Not compliant for EU data |
| Cohere | ❌ US/Canada | Not compliant for EU data |
| Self-hosted | ✅ Any EU cloud | Full control, full compliance |

**Recommended**: Mistral AI embeddings or self-hosted models on EU infrastructure

### 2. Vector Database Residency

**Requirement**: Vector databases storing embeddings of EU citizen data must be hosted in EU.

**Compliant Options**:

| Provider | EU Hosting | Self-Host Option | Notes |
|----------|-----------|------------------|-------|
| Weaviate | ✅ Weaviate Cloud EU | ✅ Open-source | AWS Frankfurt, GCP Netherlands |
| Qdrant | ✅ Qdrant Cloud EU | ✅ Open-source | Multiple EU regions |
| Milvus | ✅ Zilliz Cloud EU | ✅ Open-source | AWS Frankfurt, etc. |
| Postgres + pgvector | ✅ Neon EU, Supabase EU | ✅ Self-host | Multiple EU options |
| Redis | ✅ Redis Cloud EU | ✅ Self-host | EU regions available |
| Elasticsearch | ✅ Elastic Cloud EU | ✅ Self-host | Multiple EU data centers |
| Chroma | ❌ No managed EU | ✅ Self-host in EU | Must self-host for compliance |
| Pinecone | ❌ US-only | ❌ No | Not compliant for EU data |

**Recommended**: Weaviate, Qdrant, or Milvus hosted in EU data centers

### 3. LLM Residency

**Requirement**: LLMs generating responses based on EU citizen data must operate within EU jurisdiction.

**Compliant Options**:

| Provider | EU Data Centers | Notes |
|----------|-----------------|-------|
| Mistral AI | ✅ France, Germany | All processing in EU |
| Aleph Alpha | ✅ Germany | European LLM provider |
| HUGGINGFACE | ✅ EU (self-host) | Self-host on EU infrastructure |
| OpenAI | ❌ US-only | Not compliant for EU data |
| Anthropic | ❌ US-only | Not compliant for EU data |
| Self-hosted | ✅ Any EU cloud | Full control, full compliance |

**Recommended**: Mistral AI or self-hosted LLMs on EU infrastructure

### 4. EU Cloud Providers

**Recommended EU-based infrastructure**:

| Provider | Regions | Certifications | Notes |
|----------|---------|----------------|-------|
| OVHcloud | France, Germany, etc. | ISO 27001, SOC 2 | French provider, Gaia-X |
| T-Systems | Germany | ISO 27001, SOC 2 | Deutsche Telekom subsidiary |
| Scaleway | France, Netherlands | ISO 27001, SOC 2 | French provider |
| AWS | Frankfurt, Ireland | All major | US company but EU regions |
| Google Cloud | Netherlands, Belgium | All major | US company but EU regions |
| Microsoft Azure | Germany, Netherlands | All major | US company but EU regions |

**Note**: For highest compliance, prefer EU-owned providers (OVHcloud, T-Systems, Scaleway)

## Security Measures for GDPR-Compliant RAG

### 1. Encryption

**Requirement**: Protect personal data through appropriate technical measures.

**Implementation**:

#### At Rest Encryption:
```
┌─────────────────────────┬─────────────────────────────────────┐
│ Component                 │ Encryption Standard                   │
├─────────────────────────┼─────────────────────────────────────┤
│ Vector Database          │ AES-256 (industry standard)          │
│ Document Storage         │ AES-256                               │
│ Backups                  │ AES-256 + separate key management    │
│ Configuration            │ Encrypt secrets and sensitive config │
└─────────────────────────┴─────────────────────────────────────┘
```

**Key Management**:
- Use dedicated key management service (Hashicorp Vault, AWS KMS EU, etc.)
- Rotate keys regularly (quarterly minimum)
- Maintain key hierarchy (master key → data keys)
- Store keys separately from encrypted data
- EU-based key management for EU data

#### In Transit Encryption:
```
┌─────────────────────────┬─────────────────────────────────────┐
│ Communication            │ Encryption Standard                   │
├─────────────────────────┼─────────────────────────────────────┤
│ API Calls                │ TLS 1.2+                              │
│ Database Connections     │ TLS 1.2+                              │
│ Internal Service Comm    │ mTLS (mutual TLS)                     │
│ User Interfaces          │ HTTPS with modern cipher suites       │
└─────────────────────────┴─────────────────────────────────────┘
```

### 2. Access Controls

**Requirement**: Prevent unauthorized access to personal data.

**Implementation**:

#### Role-Based Access Control (RBAC):
```
┌─────────────────────────┬─────────────────────────────────────┐
│ Role                      │ Permissions                           │
├─────────────────────────┼─────────────────────────────────────┤
│ RAG Admin                 │ Full access: manage, configure, query │
│ RAG User                  │ Query only: retrieve, generate        │
│ Data Owner                │ Manage own documents, request actions│
│ Auditor                   │ Read-only access to logs, audit data │
│ System                    │ Service account with least privilege │
└─────────────────────────┴─────────────────────────────────────┘
```

#### Attribute-Based Access Control (ABAC):
```
Access = f(
    user_attributes (department, role, clearance),
    resource_attributes (classification, owner, sensitivity),
    environment_attributes (time, location, device)
)

Example Rules:
- Engineers can access technical documentation vectors
- HR can access HR policy vectors
- No access to PII-containing vectors without justification
- Time-based access (9am-5pm only for sensitive data)
```

#### Technical Implementation:
```python
# Example: Vector database access control
class AccessControl:
    def can_access_vector(self, user, vector):
        # Check user has clearance for vector's classification
        if user.clearance < vector.classification:
            return False
        
        # Check user's department matches vector's department
        if user.department != vector.department:
            return False
        
        # Check time-based restrictions
        if vector.time_restricted and not is_working_hours():
            return False
        
        # Check purpose limitation
        if user.intended_purpose not in vector.allowed_purposes:
            return False
        
        return True
```

### 3. Audit Logging

**Requirement**: Maintain records of processing activities for accountability and demonstration of compliance.

**Implementation**:

#### What to Log:
```
┌─────────────────────────┬─────────────────────────────────────┐
│ Activity                 │ Log Details                            │
├─────────────────────────┼─────────────────────────────────────┤
│ Document Ingestion       │ Document ID, timestamp, user, metadata │
│ PII Detection            │ Document ID, PII types found, actions  │
│ PII Redaction            │ Document ID, PII removed, method       │
│ Chunking                 │ Document ID, chunks created, sizes   │
│ Embedding                │ Document ID, model, dimensions, time  │
│ Vector Storage           │ Vector ID, document ID, metadata      │
│ Retrieval                │ Query, query hash, results, user, time│
│ LLM Generation           │ Query hash, model, tokens, time      │
│ Response Delivery        │ Query hash, response, user, time      │
│ Data Subject Request     │ Request type, user, action, time      │
│ System Access            │ User, action, resource, time          │
└─────────────────────────┴─────────────────────────────────────┘
```

#### Log Retention:
- **Access Logs**: 6-12 months
- **Operation Logs**: 12-24 months
- **Security Logs**: 12-24 months
- **DPIA Documentation**: Duration of processing + 6 months

#### Log Security:
- Encrypt logs at rest
- Restrict access to logs (auditor role)
- Integrity protection (digital signatures, hash chains)
- Regular log reviews for suspicious activities

### 4. Data Protection by Design

**Requirement**: Implement technical and organizational measures to ensure data protection.

**Measures**:

#### Pseudonymization:
```
┌─────────────────────────┬─────────────────────────────────────┐
│ Technique                │ Implementation                        │
├─────────────────────────┼─────────────────────────────────────┤
│ Hashing                  │ SHA-256 with salt, store hash only    │
│ Tokenization             │ Replace with random tokens           │
│ Encryption with key      │ Encrypt PII, store separately        │
│ Role-based tokens        │ Different tokens per role            │
└─────────────────────────┴─────────────────────────────────────┘

Example:
Original: "John Doe (john.doe@company.com) submitted report"
Pseudonymized: "[USER_12345] ([EMAIL_67890]) submitted report"
Mapping: {USER_12345: "John Doe", EMAIL_67890: "john.doe@company.com"}
```

#### Differential Privacy:
- Add noise to vector representations to prevent identification
- Balance privacy budget with utility
- For aggregate statistics from RAG

#### Federated Learning Approach:
- Keep data at source (local departments)
- Train/local embeddings locally
- Aggregate results centrally without sharing raw data

### 5. Security Testing

**Requirement**: Regularly test and evaluate security measures.

**Testing Regime**:

| Test Type | Frequency | Scope | Responsible |
|-----------|-----------|-------|--------------|
| Vulnerability Scanning | Weekly | All components | Security Team |
| Penetration Testing | Quarterly | External assessment | Third-party |
| Code Review | Per commit | Security-critical code | Developers |
| Architecture Review | Per major change | Overall design | Security Team |
| Red Team Exercise | Annually | Full simulation | Security Team |

**RAG-Specific Tests**:
- Attempt to extract PII from vector representations
- Test if redaction was effective
- Verify access controls prevent unauthorized retrieval
- Test prompt injection attacks
- Verify data subject rights implementation

## Compliance Checklists

### Pre-Deployment Checklist

- [ ] **Lawful Basis**: Document lawful basis for each RAG use case
- [ ] **DPIA**: Conduct Data Protection Impact Assessment (if high risk)
- [ ] **Privacy Notice**: Publish privacy notice explaining RAG processing
- [ ] **Data Mapping**: Map all personal data flows in RAG system
- [ ] **PII Detection**: Implement PII detection pipeline
- [ ] **Redaction**: Implement PII redaction or pseudonymization
- [ ] **Minimization**: Verify only necessary data is processed
- [ ] **EU Residency**: Confirm all components (embedding, DB, LLM) in EU
- [ ] **Vendor DPA**: Sign Data Processing Agreements with all vendors
- [ ] **Encryption**: Implement encryption at rest and in transit
- [ ] **Access Controls**: Implement RBAC/ABAC for all RAG components
- [ ] **Audit Logging**: Set up comprehensive logging
- [ ] **Retention Policy**: Define and implement retention periods
- [ ] **Data Subject Rights**: Implement mechanisms for all rights
- [ ] **Incident Response**: Define and test incident response procedures
- [ ] **DPO Review**: Obtain Data Protection Officer approval

### Post-Deployment Checklist

- [ ] **Monitoring**: Set up monitoring for data subject requests
- [ ] **Alerting**: Configure alerts for potential compliance issues
- [ ] **Regular Reviews**: Schedule quarterly compliance reviews
- [ ] **Audit Trail**: Maintain and review audit logs regularly
- [ ] **Training**: Train staff on RAG GDPR requirements
- [ ] **Vendor Monitoring**: Regularly verify vendor compliance
- [ ] **Data Quality**: Monitor for data accuracy and updates
- [ ] **Security Patching**: Keep all components up to date
- [ ] **Backup Testing**: Test backup and restore procedures
- [ ] **DR Testing**: Test disaster recovery procedures

### Data Subject Request Handling Checklist

**Upon Receiving Request**:
- [ ] Verify identity of data subject
- [ ] Log request receipt and details
- [ ] Assign request to handler
- [ ] Acknowledge receipt within 1 week

**For Access Request**:
- [ ] Identify all documents/vectors containing subject's data
- [ ] Extract data in human-readable format
- [ ] Include processing purposes, recipients, retention
- [ ] Provide within 1 month
- [ ] Document fulfillment

**For Rectification Request**:
- [ ] Verify inaccuracy
- [ ] Identify all affected documents and vectors
- [ ] Update source documents
- [ ] Re-embed corrected documents
- [ ] Delete old vectors
- [ ] Confirm correction
- [ ] Complete within 1 month

**For Erasure Request**:
- [ ] Verify identity and legal basis for erasure
- [ ] Identify all documents/vectors containing subject's data
- [ ] Check for exceptions (legal obligation, public interest)
- [ ] Delete from all systems (DB, cache, backups)
- [ ] Verify deletion
- [ ] Document erasure
- [ ] Complete within 1 month

### Annual Compliance Review Checklist

- [ ] **Data Inventory**: Update inventory of all personal data in RAG
- [ ] **Lawful Basis Review**: Verify lawful basis still valid
- [ ] **Purpose Review**: Confirm purposes still accurate
- [ ] **DPIA Update**: Update DPIA if processing changed
- [ ] **Vendor Review**: Verify all vendors still compliant
- [ ] **Security Review**: Assess security measures effectiveness
- [ ] **Incident Review**: Review all security incidents
- [ ] **Training Refresh**: Update staff training
- [ ] **Policy Update**: Review and update all policies
- [ ] **DPO Report**: Submit annual report to Data Protection Officer

## Data Protection Impact Assessment (DPIA)

### When is DPIA Required?

DPIA is **required** for RAG systems when:
- Using new technologies (LLMs, embeddings)
- Processing on large scale
- Systematic monitoring of publicly accessible areas
- Processing of special category data (health, biometrics, etc.)
- Systematic and extensive evaluation of personal aspects based on automated processing

**For most industrial RAG systems: DPIA is required**

### DPIA Process for RAG

```
Phase 1: Describe the Processing (2-4 weeks)
├── Describe RAG system purpose and scope
├── Identify data types processed (documents, queries, vectors)
├── Document processing operations (ingestion, embedding, retrieval)
├── Map data flows between components
└── Identify stakeholders (users, data subjects, business units)

Phase 2: Assess Necessity and Proportionality (1-2 weeks)
├── Assess if RAG is necessary for purpose
├── Evaluate proportionality of processing
├── Identify less privacy-invasive alternatives
└── Justify chosen approach

Phase 3: Risk Assessment (2-3 weeks)
├── Identify risks to data subjects:
│   ├── Unauthorized access to personal data
│   ├── Inaccurate or biased RAG responses
│   ├── Difficulty exercising data subject rights
│   ├── Data leakage through vectors
│   └── Function creep (use for unintended purposes)
├── Assess likelihood and severity of each risk
└── Document risk assessment

Phase 4: Risk Mitigation (2-4 weeks)
├── Identify mitigation measures for each risk
├── Implement technical and organizational controls
├── Assign risk owners
└── Set residual risk acceptance criteria

Phase 5: Approval and Publication (1 week)
├── Obtain DPO approval
├── Publish DPIA summary (if appropriate)
└── Integrate into compliance monitoring
```

### DPIA Template for RAG

```
1. Project Description
   - RAG System Name: [Name]
   - Purpose: [Purpose]
   - Scope: [Departments, users, data types]
   - Context: [Business need, alternatives considered]

2. Processing Description
   - Data Types: [Documents, queries, vectors, metadata]
   - Processing Activities: [Ingestion, PII detection, redaction, embedding, storage, retrieval, generation]
   - Data Subjects: [Employees, customers, partners]
   - Data Volume: [Number of documents, vectors, queries/day]

3. Necessity and Proportionality
   - Necessity: [Why RAG is necessary]
   - Proportionality: [Why this scale/scope is appropriate]
   - Alternatives Considered: [List and reasons for rejection]

4. Risk Assessment
   ┌─────────────────────────┬──────────┬──────────┬────────────┐
   │ Risk                      │ Likelihood│ Severity │ Risk Level  │
   ├─────────────────────────┼──────────┼──────────┼────────────┤
   │ Unauthorized access       │ Medium    │ High     │ HIGH        │
   │ Inaccurate responses      │ Low       │ Medium   │ MEDIUM      │
   │ Rights exercise difficulty │ Medium    │ Medium   │ MEDIUM      │
   │ Data leakage through vectors│ Low     │ High     │ MEDIUM      │
   │ Function creep            │ Low       │ Medium   │ MEDIUM      │
   └─────────────────────────┴──────────┴──────────┴────────────┘

5. Risk Mitigation
   ┌─────────────────────────┬─────────────────────────────────────┐
   │ Risk                      │ Mitigation Measures                        │
   ├─────────────────────────┼─────────────────────────────────────┤
   │ Unauthorized access       │ Encryption, access controls, audit logs│
   │ Inaccurate responses      │ Human review, quality checks, testing │
   │ Rights exercise difficulty │ Vector-to-document mapping, processes │
   │ Data leakage through vectors│ PII redaction, differential privacy  │
   │ Function creep            │ Purpose limitation, access controls  │
   └─────────────────────────┴─────────────────────────────────────┘

6. Residual Risk
   - Acceptable: [Yes/No]
   - Rationale: [Justification for acceptance]
   - Risk Owner: [Name, role]

7. Approval
   - DPO Approval: [Date, signature]
   - Management Approval: [Date, signature]
   - Review Date: [Next review date]
```

## Incident Response for RAG

### Personal Data Breach Procedure

**Definition**: A breach of security leading to accidental or unlawful destruction, loss, alteration, unauthorized disclosure of, or access to, personal data.

**RAG-Specific Breach Examples**:
- Unauthorized access to vector database containing personal data
- Accidental inclusion of PII in LLM training data
- Leakage of personal data through RAG responses
- Loss of encrypted data without backup
- Unauthorized disclosure of vectors to third parties

**Response Timeline**:
```
┌─────────────────────────┬──────────────┬─────────────────────────────────┐
│ Time from Discovery      │ Action         │ Responsible                       │
├─────────────────────────┼──────────────┼─────────────────────────────────┤
│ 0-1 hour                  │ Initial triage │ Security Team / DPO               │
│ 1-4 hours                 │ Assess scope  │ Incident Response Team            │
│ 4-24 hours                │ Contain       │ Security + affected teams         │
│ 24-72 hours               │ Investigate   │ Forensic Team                    │
│ 72 hours                  │ Notify*       │ DPO                              │
│ 1-4 weeks                 │ Remediate     │ All relevant teams               │
│ 1 month                   │ Report        │ DPO                              │
└─────────────────────────┴──────────────┴─────────────────────────────────┘

*Notification to supervisory authority within 72 hours if high risk
```

### Breach Response Steps

1. **Detection and Triage** (Immediate)
   - Identify breach source and scope
   - Assess if personal data affected
   - Determine if EU citizen data involved
   - Classify breach severity (Low/Medium/High)

2. **Containment** (Within 4 hours)
   - Isolate affected systems
   - Revoke unauthorized access
   - Preserve evidence for investigation
   - Implement temporary mitigations

3. **Assessment** (Within 24 hours)
   - Identify data subjects affected
   - Determine data types exposed
   - Assess risk to data subjects
   - Document findings

4. **Notification** (Within 72 hours if high risk)
   - Notify supervisory authority (if required)
   - Notify affected data subjects (if high risk)
   - Document all notifications

5. **Remediation** (Within 1-4 weeks)
   - Fix root cause
   - Implement additional controls
   - Update policies and procedures
   - Test fixes

6. **Post-Incident Review** (Within 1 month)
   - Conduct root cause analysis
   - Identify lessons learned
   - Update DPIA if needed
   - Update incident response procedures

### Breach Notification Content

**To Supervisory Authority**:
- Description of breach nature
- Categories and approximate number of data subjects affected
- Categories and approximate number of personal data records concerned
- DPO contact details
- Likely consequences of breach
- Measures proposed or taken to address breach
- Measures to notify data subjects (if applicable)

**To Data Subjects**:
- Clear and plain language description
- Nature of breach
- Data categories affected
- Likely consequences
- Measures taken or proposed
- DPO contact for more information

## Vendor Management

### Vendor Due Diligence Checklist

**Before Engagement**:
- [ ] **Data Residency**: Confirm vendor can process/store data in EU
- [ ] **GDPR Compliance**: Verify vendor has GDPR compliance program
- [ ] **Data Processing Agreement (DPA)**: Review and sign DPA
- [ ] **Subprocessors**: List and assess all subprocessors
- [ ] **Security Measures**: Review vendor's security documentation
- [ ] **Certifications**: Verify relevant certifications (ISO 27001, SOC 2)
- [ ] **Data Subject Rights**: Confirm vendor supports exercise of rights
- [ ] **Breach Notification**: Verify breach notification procedures
- [ ] **Data Retention**: Confirm data deletion capabilities
- [ ] **Audit Rights**: Secure right to audit vendor compliance

**Ongoing Monitoring**:
- [ ] **Annual Review**: Reassess vendor compliance annually
- [ ] **Change Notification**: Require notification of material changes
- [ ] **Incident Reporting**: Monitor vendor security incidents
- [ ] **Compliance Updates**: Stay informed of vendor compliance changes
- [ ] **Performance Metrics**: Track vendor SLA compliance

### Contractual Requirements

**Essential Contract Clauses**:
- Data processing only on documented instructions
- Confidentiality obligations for all personnel
- Appropriate technical and organizational measures
- Assistance with data subject rights fulfillment
- Breach notification within agreed timeframe (≤72 hours)
- Deletion or return of data upon contract termination
- Audit rights for data protection compliance
- Subprocessor approval requirements
- Data residency guarantees
- Liability and indemnification for GDPR violations

## International Data Transfers

### EU-US Data Transfer Mechanisms

**Current Options (as of Oct 2026)**:

1. **EU-US Data Privacy Framework**
   - Self-certification by US companies
   - Includes commitments by US government
   - Can be used for transfers to certified organizations
   - Subject to ongoing legal challenges

2. **Standard Contractual Clauses (SCCs)**
   - Model contracts adopted by European Commission
   - Can be used for any transfer to third countries
   - Require additional measures for US transfers
   - Must conduct Transfer Impact Assessment (TIA)

3. **Binding Corporate Rules (BCRs)**
   - Internal rules for multinational organizations
   - Require approval by supervisory authority
   - Complex and time-consuming to implement

4. **Derogations (Article 49)**
   - Explicit consent of data subject
   - Necessary for contract performance
   - Public interest
   - Establishment, exercise, or defense of legal claims
   - Vital interests of data subject
   - Limited to occasional, non-repetitive transfers

### Transfer Impact Assessment (TIA)

**Required when using SCCs for US transfers**:

```
1. Map Data Flows:
   - Identify all data transfers to third countries
   - Document data types, purposes, recipients

2. Assess Local Laws:
   - Evaluate third country's legal system
   - Assess government access to data
   - Consider human rights and rule of law

3. Assess Contractual Safeguards:
   - Review SCCs and additional measures
   - Evaluate technical safeguards (encryption, pseudonymization)
   - Assess organizational safeguards (policies, training)

4. Determine Adequacy:
   - Compare third country protections with EU standards
   - Identify any gaps
   - Determine if transfer can proceed

5. Document:
   - Maintain TIA documentation
   - Update regularly
   - Make available to supervisory authority
```

**For RAG Systems**:
- **Avoid US transfers if possible**: Use EU-based providers
- **If US transfer necessary**: Conduct TIA, implement supplementary measures
- **Supplementary Measures**: Encryption, pseudonymization, access controls, audit logging

## Best Practices

### Architecture Best Practices

1. **EU-Centric Architecture**
   ```
   ┌─────────────────────────────────────────────────────────────┐
   │                        Application Layer                         │
   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
   │  │   User      │  │   RAG        │  │   LLM               │  │
   │  │   Interface │──▶│   Service     │──▶│   (EU-hosted)       │  │
   │  └─────────────┘  └─────────────┘  └─────────────────────┘  │
   └─────────────────────────────────────────────────────────────┘
                                 ↓
   ┌─────────────────────────────────────────────────────────────┐
   │                      Embedding Service                           │
   │  ┌─────────────────────────────────────────────────────────┐  │
   │  │  Mistral AI Embeddings (EU) or Self-hosted in EU          │  │
   │  └─────────────────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────────────┘
                                 ↓
   ┌─────────────────────────────────────────────────────────────┐
   │                      Vector Database                            │
   │  ┌─────────────────────────────────────────────────────────┐  │
   │  │  Weaviate/Qdrant/Milvus (EU) on OVHcloud/T-Systems         │  │
   │  └─────────────────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────────────┘
                                 ↓
   ┌─────────────────────────────────────────────────────────────┐
   │                      Infrastructure                            │
   │  ┌─────────────────────────────────────────────────────────┐  │
   │  │  All infrastructure in EU data centers (OVHcloud, etc.)    │  │
   │  └─────────────────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────────────┘
   ```

2. **Data Flow Minimization**
   - Process data as close to source as possible
   - Avoid unnecessary data transfers
   - Use edge processing where feasible

3. **Separation of Concerns**
   - Separate PII processing from RAG processing
   - Use different systems for different data types
   - Implement data segregation by classification

### Operational Best Practices

1. **Document Everything**
   - Maintain data processing records
   - Document all compliance decisions
   - Keep DPIAs up to date
   - Record all data subject requests and responses

2. **Regular Training**
   - Train all staff on GDPR requirements
   - Specialized training for RAG developers and operators
   - Update training annually or when laws change

3. **Monitor and Audit**
   - Regular security audits
   - Quarterly compliance reviews
   - Annual external audits
   - Continuous monitoring of access and operations

4. **Stay Informed**
   - Monitor regulatory updates
   - Track court rulings affecting GDPR
   - Follow industry best practices
   - Participate in data protection forums

### Technical Best Practices

1. **Privacy-Preserving RAG**
   - Implement PII redaction before embedding
   - Use differential privacy for sensitive queries
   - Consider federated RAG for distributed data

2. **Quality Assurance**
   - Regularly test RAG responses for PII leakage
   - Validate redaction effectiveness
   - Test data subject rights implementation

3. **Performance and Compliance Balance**
   - Don't sacrifice compliance for performance
   - Use efficient encryption (AES-NI hardware acceleration)
   - Optimize PII detection (cache results, batch processing)

## Common Pitfalls and How to Avoid Them

| Pitfall | Risk | Prevention |
|---------|------|------------|
| Using US-based LLMs for EU data | Non-compliance, fines | Use EU-based providers (Mistral, Aleph Alpha) |
| Not implementing PII redaction | PII in vectors, difficult rights exercise | Implement comprehensive PII detection and redaction |
| Poor access controls | Unauthorized access to personal data | Implement RBAC/ABAC with least privilege |
| No audit logging | Cannot demonstrate compliance | Implement comprehensive logging of all operations |
| Ignoring data subject rights | Non-compliance, reputational damage | Implement all rights (access, rectification, erasure, etc.) |
| Inadequate encryption | Data breach risk | Use AES-256 at rest, TLS 1.2+ in transit |
| No DPIA | Non-compliance for high-risk processing | Conduct DPIA for all RAG systems |
| Vendor lock-in without DPA | Compliance gap | Sign DPA with all vendors before use |
| Over-collection of data | Violates data minimization | Only ingest necessary documents and data |
| Indefinite retention | Violates storage limitation | Implement and enforce retention policies |

## Summary

Building a GDPR-compliant RAG system requires **more than technical implementation** — it requires a **comprehensive approach** combining legal understanding, technical controls, organizational processes, and continuous monitoring.

**Key Takeaways**:

1. **GDPR is Mandatory**: Compliance is not optional; fines can be severe
2. **Privacy by Design**: Build compliance into every component from the start
3. **EU Residency**: Keep all EU citizen data processing within EU jurisdiction
4. **Data Subject Rights**: Implement mechanisms to exercise all GDPR rights
5. **Security First**: Implement appropriate technical and organizational measures
6. **Document Everything**: Maintain records for accountability and audit
7. **Continuous Compliance**: GDPR compliance is ongoing, not a one-time effort

For European industrial applications, **Mistral AI embeddings with Weaviate/Qdrant on OVHcloud or T-Systems** provides a strong foundation for GDPR-compliant RAG. Always conduct a **DPIA** before deployment and consult with your **Data Protection Officer** for specific requirements.

**Remember**: When in doubt, consult legal counsel. GDPR interpretation can vary, and legal advice is essential for high-risk deployments.
