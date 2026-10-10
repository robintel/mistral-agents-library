---
type: pattern
family: enterprise
---

# Salesforce Integration

Integrate with Salesforce — the world's #1 CRM platform. This contract
covers APIs, authentication, data models, governor limits, and integration
patterns for connecting external systems to Salesforce, or migrating
legacy CRM data to Salesforce.

## Core Concepts

### Salesforce Architecture
```
User Interface Layer     ← Lightning Experience, Classic UI
      ↓
Application Layer         ← Apex, Lightning Components, Flows
      ↓
Data Layer                ← Standard/Custom Objects, External Objects
      ↓
Platform Services          ← APIs, Metadata, Security, Integration
```

### Editions
| Edition | Use Case | Limits |
|---------|----------|--------|
| **Essentials** | Small teams | Basic features |
| **Professional** | Growing businesses | Limited customization |
| **Enterprise** | Large orgs | Full API access, sandbox environments |
| **Unlimited** | Enterprise scale | Highest limits, premium support |
| **Developer** | Development/testing | Free, limited users |

## Integration Methods

### 1. REST API (Modern, Preferred)
**When**: Real-time integrations, mobile apps, modern systems
**Contract**:
- Resource-based: `/services/data/vXX.X/sobjects/Account`
- CRUD operations: GET, POST, PATCH, DELETE
- Query: SOQL via GET `/services/data/vXX.X/query?q=SELECT...`
- Search: SOSL via GET `/services/data/vXX.X/search?q=FIND...`

**Pitfalls**:
- Governor limits apply (100k API calls/day for Enterprise)
- No bulk operations (use Bulk API for >200 records)
- SOQL query limits (100 queries, 50k rows)
- No JOINs in SOQL (use subqueries or multiple queries)

**Best Practices**:
- Use **Composite API** to reduce call counts (combine multiple REST calls)
- Implement **retry logic** with exponential backoff for limit exceptions
- Use **query optimization**: selective fields, proper indexing
- Cache **describe results** to minimize metadata calls

### 2. SOAP API (Legacy, Still Supported)
**When**: Enterprise integrations, legacy systems, .NET/Java
**Contract**:
- WSDL-based web service
- Enterprise WSDL (recommended) vs Partner WSDL
- Strong typing, comprehensive error handling

**Pitfalls**:
- Heavier payloads than REST (SOAP envelopes)
- Slower performance
- More complex setup
- Deprecated in some contexts

**Best Practices**:
- Use **Enterprise WSDL** for type safety
- Enable **compression** to reduce payload size
- Implement **session management** (login, session ID handling)
- Use **async processing** for long-running operations

### 3. Bulk API (High-Volume Data)
**When**: Loading/exporting 50k-200k+ records
**Contract**:
- **Bulk API 1.0**: CSV-based, batch jobs
- **Bulk API 2.0**: JSON-based, parallel processing
- Job-based: create job → add batches → close job → get results

**Pitfalls**:
- Still subject to **24-hour limit** on job execution
- **Batch size limits** (10k records/batch for Bulk 2.0)
- **Concurrent jobs limit** (5 for Bulk 2.0)
- **No real-time** — asynchronous processing

**Best Practices**:
- Use **Bulk API 2.0** (JSON) for new projects
- **Chunk data** into optimal batch sizes (10k for Bulk 2.0)
- **Monitor job status** and handle failures gracefully
- **Parallelize** jobs when possible

### 4. Streaming API (Real-Time Events)
**When**: Event-driven architectures, real-time notifications
**Contract**:
- **Platform Events**: Custom events for business processes
- **Change Data Capture**: Track record changes via Change Events
- **Standard Events**: Predefined events (e.g., Account changes)
- **Bayeux protocol**: CometD-based long polling

**Pitfalls**:
- **Event retention**: 72 hours max for Change Events
- **Ordering**: Events may not arrive in exact order
- **Delivery**: At-least-once; handle duplicates
- **Limits**: 2000 events/second per org

**Best Practices**:
- Use **Change Data Capture** for data sync (instead of polling)
- Implement **duplicate detection** (event replay IDs)
- **Filter events** at source to reduce volume
- **Monitor subscription health**

### 5. Metadata API
**When**: Dynamic schema access, custom object creation, app building
**Contract**:
- Access object metadata, field definitions, relationships
- Create/update custom objects, fields, validation rules
- Deploy components (Apex classes, triggers, etc.)

**Pitfalls**:
- **Deployments are synchronous** and can time out
- **Schema changes** can break existing integrations
- **Field-level security** affects metadata visibility

**Best Practices**:
- **Cache metadata** to reduce API calls
- **Validate before deploy** — check metadata in sandbox first
- **Use describe calls** to get field types, relationships
- **Handle FLS** (Field-Level Security) in queries

## Authentication Methods

### 1. OAuth 2.0 (Recommended)
**Flows**:
- **Web Server Flow**: Server-side apps with user context
- **User-Agent Flow**: Client-side apps (SPA, mobile)
- **JWT Bearer Flow**: Server-to-server (no user, long-lived)
- **Refresh Token Flow**: Maintain sessions without user interaction

**OAuth 2.0 Setup**:
```
1. Create Connected App in Salesforce Setup
2. Set callback URL, scopes, selected IP ranges
3. Get consumer key (client_id) and consumer secret (client_secret)
4. Exchange authorization code for access token
```

**Scopes (OAuth)**:
- `api` — Access REST/SOAP APIs
- `refresh_token` — Obtain refresh tokens
- `web` — User authentication
- `id` — User identification

### 2. Username-Password Flow (Legacy)
**When**: Server-to-server, non-user context (deprecated in favor of JWT)
**Contract**:
- POST to `/services/oauth2/token` with username, password, client_id, client_secret
- Returns access_token, instance_url, signature

**Pitfalls**:
- **Deprecated** — not recommended for new projects
- **Security risk** — password exposure
- **No refresh tokens** by default

**Best Practices**:
- Use **JWT Bearer Flow** instead
- If using, **restrict IP ranges** and enable MFA

### 3. JWT Bearer Flow (Server-to-Server)
**When**: Machine-to-machine integration, long-running services
**Contract**:
- Create **digital certificate** (self-signed or CA-signed)
- Upload to Salesforce as **Connected App**
- Sign JWT with private key, include issuer, subject, audience, expiration
- Exchange JWT for access token

**Pitfalls**:
- **Certificate management** required
- **Token expiration** (typically 2 hours)
- **User context** not available (runs as Connected App user)

**Best Practices**:
- Use **2-hour expiration** (Salesforce max)
- **Automate certificate rotation** (Salesforce requires rotation)
- **Restrict scopes** to minimum required
- **Monitor token usage**

## Data Models

### Standard Objects (Core CRM)
| Object | Purpose | Integration Notes |
|--------|---------|------------------|
| **Account** | Companies, organizations | Often the root of data relationships |
| **Contact** | People | Linked to Accounts, Leads, Opportunities |
| **Lead** | Prospects | Conversion to Account/Contact/Opportunity |
| **Opportunity** | Deals, sales | Stage, Amount, Close Date, Probability |
| **Case** | Support tickets | Status, Origin, Priority, Type |
| **Task** | Activities | WhoId (Contact/Lead), WhatId (related record) |
| **Event** | Meetings | Similar to Task but time-bound |
| **User** | System users | Profile, Role, Permission Sets |

### Custom Objects
- **Custom fields** on standard objects
- **Custom objects** (e.g., `Invoice__c`, `Contract__c`)
- **Relationships**: Lookup, Master-Detail
- **Validation rules**, **triggers**, **workflows**

### External Objects
- **OData 2.0/4.0** connectivity to external systems
- **Virtual objects** that map to external data sources
- **Synchronization** with external systems

### Data Relationships
```
Account
  ├─ Contacts (1:N)
  ├─ Opportunities (1:N)
  ├─ Cases (1:N)
  └─ Custom Objects (1:N via Lookup)

Opportunity
  ├─ Contact (Lookup)
  ├─ Account (Lookup)
  └─ Products (via OpportunityLineItem)
```

## Migration Patterns

### 1. Legacy CRM → Salesforce (Full Migration)
**Phases**:
1. **Discovery**: Map legacy data model to Salesforce schema
2. **Schema Design**: Create custom objects/fields for legacy data
3. **Data Cleansing**: Clean, deduplicate, normalize legacy data
4. **Historical Data**: Decide what to migrate (last 2 years? all?)
5. **Initial Load**: Bulk API for large datasets
6. **Delta Sync**: Catch up changes since initial load
7. **Cutover**: Switch to Salesforce, freeze legacy
8. **Validation**: Verify data integrity, report discrepancies

**Tools**:
- **Salesforce Data Loader**: GUI for small-medium volumes
- **Bulk API**: For large volumes (100k+ records)
- **Informatica Cloud**: Enterprise ETL
- **MuleSoft**: Salesforce's own integration platform

**Common Challenges**:
- **Picklist mapping**: Legacy values → Salesforce picklists
- **Data type mapping**: Legacy types → Salesforce types
- **Relationship mapping**: Foreign keys → Salesforce IDs
- **User mapping**: Legacy users → Salesforce users

### 2. Custom System → Salesforce (Partial Integration)
**Approach**: Keep custom system as primary, sync with Salesforce
**Patterns**:
- **Outbound**: Custom system pushes data to Salesforce
- **Inbound**: Salesforce data pulled into custom system
- **Bidirectional**: Two-way sync with conflict resolution

**Sync Strategies**:
- **Full sync**: Periodic complete data refresh
- **Incremental sync**: Only changes since last sync
- **Event-driven sync**: Real-time on data changes

### 3. Hybrid Integration (Best of Both Worlds)
**Use Case**: Keep some data in legacy, use Salesforce for CRM
**Architecture**:
```
Legacy System ↔ Middleware ↔ Salesforce
                ↓
        Transform, Route, Buffer
                ↓
        Handle governor limits
```

**Middleware Options**:
- **MuleSoft**: Salesforce's integration platform
- **Apache Camel**: Open-source integration framework
- **Custom**: Node.js/Python service with retry logic

## Integration Patterns

### 1. Real-Time Sync (Synchronous)
**Use Case**: Data must be consistent in real-time
**Contract**:
- REST API calls on data changes
- Immediate consistency required
- Low latency tolerance

**Implementation**:
```
Legacy System → Salesforce REST API → Salesforce
        (on create/update/delete)
```

**Watch Out For**:
- Governor limits (100k API calls/day for Enterprise)
- Network latency
- Error handling and retries

### 2. Batch Sync (Asynchronous)
**Use Case**: High-volume data, non-real-time requirements
**Contract**:
- Bulk API for large datasets
- Scheduled jobs (daily, hourly)
- Error reporting and reconciliation

**Implementation**:
```
Legacy System → Nightly Batch → Salesforce Bulk API → Salesforce
        (CSV/JSON files, 10k-200k records)
```

**Watch Out For**:
- Bulk API time limits (24 hours max)
- Data volume limits per batch
- Failed batch handling

### 3. Event-Driven Sync
**Use Case**: Real-time notifications, decoupled systems
**Contract**:
- Platform Events or Change Data Capture
- Subscribe to Salesforce events
- React to changes in external systems

**Implementation**:
```
Salesforce Event → Streaming API → External System
        (Change Data Capture, Platform Events)
```

**Watch Out For**:
- Event retention (72 hours)
- Event ordering not guaranteed
- Duplicate event handling

### 4. API-First Architecture
**Use Case**: Salesforce as backend for custom applications
**Contract**:
- Salesforce stores the data
- Custom UI or mobile app consumes Salesforce APIs
- All business logic in Apex/Triggers

**Implementation**:
```
Custom App → REST API → Salesforce → Data
        (Single Page App, Mobile App)
```

**Watch Out For**:
- Governor limits affect your app
- API call optimization critical
- Offline support complexity

## Salesforce-Specific Considerations

### Governor Limits
| Limit | Enterprise | Unlimited | Monitoring |
|-------|------------|-----------|------------|
| API calls | 100,000/day | 1,000,000/day | API usage notifications |
| SOQL queries | 100 (sync) | 100 (sync) | Query usage |
| SOQL rows | 50,000 | 50,000 | Query rows |
| DML statements | 15,000 | 15,000 | DML usage |
| DML rows | 10,000 | 10,000 | DML rows |
| CPU time | 10,000 ms | 20,000 ms | CPU time |
| Heap size | 6 MB | 12 MB | Heap usage |
| Bulk API batches | 5,000/day | 10,000/day | Bulk API usage |

**Monitoring**:
- **System Overview** in Setup → Company Information
- **Limits** page in Setup → Company Settings
- **Debug Logs** for Apex execution
- **Event Log Files** for API usage tracking

### Query Optimization
- **Selective Queries**: Filter with WHERE clause on indexed fields
- **Indexed Fields**: Standard fields (Id, Name, Email, etc.) are indexed
- **Avoid SOQL in Loops**: Major cause of governor limits
- **Use FOR loops**: `for (List<Account> accs : [SELECT Id FROM Account])`
- **Query More Select**: Fetch more fields than needed to avoid N+1 queries

### Data Skew
- **Problem**: Uneven data distribution causing performance issues
- **Example**: 10k Contacts under one Account vs. 10 Contacts each
- **Impact**: SOQL queries time out or hit limits
- **Solution**: Use `LIMIT`, filter by date ranges, avoid parent-child queries

## Modernization Approaches

### 1. Lift and Shift
**When**: Move custom Salesforce apps to Lightning Platform
**Approach**:
- Convert Visualforce pages to Lightning Web Components
- Migrate Apex to modern patterns
- Update triggers to Lightning Process Builder/Flow

### 2. Re-architecture
**When**: Modernize monolithic Salesforce orgs
**Approach**:
- Identify business domains
- Split into separate apps using **Salesforce DX**
- Implement **modular design** with unlocked packages
- Use **scratch orgs** for development

### 3. Integration with External Systems
**When**: Salesforce is part of a larger architecture
**Approach**:
- Use **Platform Events** for real-time integration
- Implement **outbound messages** for simple notifications
- Use **MuleSoft** for complex integration scenarios
- Consider **External Services** for third-party API integration

### 4. Data Migration to Salesforce
**When**: Moving from legacy CRM or custom system
**Approach**:
- **Mapping**: Legacy fields → Salesforce fields
- **Transformation**: Legacy formats → Salesforce formats
- **Validation**: Data quality checks before migration
- **Testing**: Pilot migration, user acceptance testing

## Best Practices

### Design Principles
- **Minimize API calls**: Batch operations, composite requests
- **Handle governor limits**: Design for limits from day one
- **Idempotent operations**: Safe to retry failed operations
- **Error handling**: Graceful degradation, user notifications
- **Monitoring**: Track usage, set up alerts for limit thresholds

### Code Quality
- **Apex**: Follow Salesforce naming conventions, bulkify code
- **Triggers**: One trigger per object, use handler classes
- **SOQL**: Avoid queries in loops, use selective queries
- **Testing**: 75%+ code coverage required for production

### Security
- **Field-Level Security (FLS)**: Check `describe` results for field accessibility
- **Sharing Model**: Respect object permissions, sharing rules
- **SOQL Injection**: Use bind variables, not string concatenation
- **Sensitive Data**: Encrypt sensitive fields, use Shield Platform

### Performance
- **Async Processing**: Use @future, Queueable, Batch Apex for long operations
- **Caching**: Use static variables, Platform Cache for repeated data
- **Bulk Operations**: Always consider Bulk API for 200+ records
- **Batch Size**: Optimize batch sizes (200 for Apex, 10k for Bulk API 2.0)

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| SOQL query in loop | Governor limit exceeded | Use bulk queries, FOR loops |
| DML in loop | Governor limit exceeded | Bulkify DML operations |
| No error handling | Failed operations, data loss | Implement retry logic, transactions |
| Hardcoded IDs | Deployment issues | Use describe, custom metadata types |
| No FLS checking | Security violations | Check field accessibility before access |
| No governor limit checks | Unexpected failures | Monitor limits, implement fallback |
| Synchronous long operations | Timeout errors | Use @future, Queueable, Batch Apex |
| Duplicate event handling | Data inconsistency | Use event replay IDs, deduplication |

## Standing Rules

- **Governor limits are real** — design for them from the beginning;
  you cannot exceed them regardless of your paid tier
- **Bulkify everything** — assume any operation might process
  1, 10, 100, or 10,000 records; design accordingly
- **Test at scale** — what works for 10 records may fail at 10,000
- **Monitor always** — set up alerts for API usage, limits approaching
- **Respect the platform** — Salesforce is a multi-tenant environment;
  your code affects others and vice versa
- **Use metadata** — leverage describe calls, don't hardcode field names
- **Document assumptions** — Salesforce versions, governor limits, API
  behavior can change between releases
