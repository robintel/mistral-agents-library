---
type: language
era: legacy-enterprise
family: enterprise
---

# IBM i (AS/400)

The platform formerly known as AS/400, iSeries, System i — IBM's
midrange server platform that powers critical business applications
worldwide, especially in finance, manufacturing, and logistics. Despite
its age, IBM i remains a workhorse for enterprise applications with
unique architectural characteristics.

## Core discipline

1. **Integrated everything** — Database (Db2 for i), application server,
   file system, security, and user management are all integrated into
   one OS. This is the fundamental difference from other platforms.
2. **Single-level store** — No separate database files; all data lives
   in one address space. Eliminates I/O bottlenecks and simplifies
   backup/recovery.
3. **Business logic in the database** — RPG (Report Program Generator)
   and COBOL programs run in the same memory space as the data they
   process. This enables extremely efficient data access.
4. **Security by isolation** — Objects are owned by users, and access
   is controlled at a very granular level. No external firewalls needed
   for internal security.
5. **Work management** — Jobs (batch, interactive, subsystems) are
   managed by the system, not by external schedulers.

## Era map

- **1988-2000**: AS/400 era — RPG II/III, DDS for database, 5250 terminals
- **2000-2008**: iSeries era — RPG IV, ILE (Integrated Language Environment),
  Java support, WebSphere integration
- **2008-2015**: System i era — IBM i 6.1+, SQL as first-class citizen,
  PHP and .NET support
- **2015-2020**: IBM i 7.x — Modern RPG with free-format, Node.js,
  Python, REST services, JSON support
- **2020+**: IBM i 7.4+ — Enhanced SQL, improved REST, AI/ML
  integration, cloud readiness

## Language landscape

| Language | Era | Use Case | Modernization Path |
|----------|-----|----------|-------------------|
| RPG | 1988+ | Core business logic | RPG IV free-format, ILE |
| COBOL | 1988+ | Legacy business apps | Modern COBOL, ILE |
| CL | 1988+ | Control language, scripting | Modern CL commands |
| DDS | 1988+ | Database definition | SQL DDL |
| SQL | 2000+ | Database access | Modern SQL, stored procedures |
| Java | 2000+ | Modern applications | Latest Java, Jakarta EE |
| PHP | 2008+ | Web applications | Modern PHP |
| Node.js | 2015+ | Modern web services | Latest Node.js |
| Python | 2015+ | Scripting, AI/ML | Latest Python |

## Access patterns that matter

| Pattern | Implementation | Watch out for |
|---------|----------------|---------------|
| Database access | Embedded SQL in RPG | RPG variables vs SQL types |
| File I/O | Integrated File System (IFS) | IFS vs native DB access |
| Job scheduling | IBM i Work Management | Subsystem configuration |
| Web services | HTTP server (Apache), CGI, REST | 5250 bridge vs modern REST |
| Message queuing | IBM i Data Queues | Data queue vs message broker |
| Batch processing | Batch jobs, CL scripts | Job dependencies, scheduling |

## Modernization strategies

### 1. Reface
**When**: Keep core RPG logic, expose via modern interfaces
**Approach**:
- Wrap RPG programs with REST APIs using IBM i Integrated Web Server
- Use YAJL (Yet Another JSON Library) for RPG to JSON conversion
- Expose existing business logic as microservices

**Tools**:
- IBM i Access Client Solutions
- IBM Rational Developer for i
- Open Source: YAJL, Scott Klement's tools

### 2. Refactor
**When**: Improve existing RPG/COBOL code
**Approach**:
- Convert from RPG III to RPG IV (free-format)
- Use ILE to modularize monolithic programs
- Adopt SQL for database access instead of native file operations
- Implement modern error handling

**Tools**:
- RPG IV compiler
- IBM i ILE support
- ARCAD for IBM i (refactoring tools)

### 3. Re-architect
**When**: Break monolith into services
**Approach**:
- Identify business domains in existing programs
- Extract as separate ILE modules or services
- Use IBM i's Integrated Language Environment for inter-program calls
- Implement proper separation of concerns

**Tools**:
- IBM i Rational Developer
- ARCAD Observer for impact analysis
- Custom service frameworks

### 4. Replace
**When**: Move to modern platform
**Approach**:
- Rewrite in modern language (Java, Node.js, Python)
- Migrate data from Db2 for i to modern database
- Re-implement business logic in new environment
- Maintain integration with remaining IBM i systems

**Tools**:
- IBM i Data Migration tools
- Modern IDEs with IBM i connectivity
- Database migration tools

## Integration patterns

### IBM i to Modern Systems
```
IBM i Application → REST API → Modern System
       ↓
   Use IBM i HTTP Server
   Or: IBM i Access ODBC/JDBC
       ↓
   Transform: RPG ↔ JSON/XML
```

### Database Integration
```
Modern App → IBM i Db2 → IBM i Application
        ↓        ↓
    JDBC/ODBC  Native RPG
        ↓        ↓
    SQL Queries  Record-level access
```

### Message Integration
```
Modern System → Message Queue → IBM i
              (Kafka, RabbitMQ, IBM MQ)
                     ↓
              IBM i Data Queue
                     ↓
              RPG/COBOL Program
```

## Database considerations

### Db2 for i specifics
- **Single-level store**: No separate files; all in one address space
- **No ORM needed**: Direct access via native operations or SQL
- **Record-level access**: RPG can read/write individual records
- **SQL support**: Full SQL support but with IBM i-specific extensions
- **Commitment control**: Transaction management via commitment definitions

### Migration considerations
- **Data types**: IBM i has unique data types (packed decimal, etc.)
- **Character encoding**: EBCDIC vs ASCII conversion
- **Transaction semantics**: Different isolation levels than standard SQL
- **Performance**: Native access is faster than SQL for certain operations

## Development environment

### IDEs
- **IBM Rational Developer for i**: Full-featured IDE for RPG, COBOL, CL
- **VS Code with extensions**: IBM i extension pack for modern development
- **IBM i Access Client Solutions**: Traditional green-screen development

### DevOps
- **Source control**: Git integration via IBM i extensions
- **CI/CD**: Jenkins, GitHub Actions with IBM i plugins
- **Testing**: Unit testing frameworks for RPG (RPGUnit)
- **Deployment**: IBM i packaging and deployment tools

## Deployment considerations

### High availability
- **HA/DR**: IBM i supports PowerHA for high availability
- **Logical replication**: Db2 for i supports logical replication
- **Physical replication**: Storage-level replication options

### Scaling
- **Vertical scaling**: IBM i scales up within a single server
- **Horizontal scaling**: Limited; IBM i is not designed for distributed scaling
- **Partitioning**: Logical partitioning within a single system

## Security considerations

### Built-in security
- **User profiles**: Granular access control at object level
- **Authority lists**: Group-based permissions
- **Password policies**: Configurable complexity and expiration
- **Encryption**: Built-in encryption for data at rest and in transit

### Integration security
- **Network**: Secure connections via VPN or private networks
- **Authentication**: Mutual TLS, certificate-based authentication
- **Authorization**: Fine-grained access control for external systems
- **Audit**: Comprehensive audit logging (QAUDJRN)

## Performance considerations

### Strengths
- **Database access**: Extremely fast for record-level operations
- **Single-level store**: Eliminates I/O bottlenecks
- **Work management**: Efficient job scheduling and resource management

### Limitations
- **No horizontal scaling**: Single server architecture
- **Memory constraints**: Limited by LPAR size
- **Network latency**: Can be bottleneck for external integrations

## Common defects and mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Character encoding mismatches | Data corruption | Use proper CCSID, conversion utilities |
| Packed decimal handling | Calculation errors | Use proper data types, conversion |
| Transaction isolation | Data inconsistency | Use commitment control properly |
| Performance bottlenecks | Slow operations | Optimize native access, use SQL appropriately |
| Integration latency | Poor responsiveness | Local caching, batch processing |
| Skill shortages | Maintenance risk | Cross-training, modernization planning |

## Standing rules

- **IBM i is not legacy** — It is a modern platform with unique
  advantages for certain workloads
- **Do not rewrite what works** — If it ain't broke, modernize around it
  rather than replacing it
- **Respect the architecture** — IBM i's integrated nature is a feature,
  not a bug; work with it
- **Modernize incrementally** — Reface before refactor before replace
- **Test thoroughly** — IBM i has unique behaviors that may not be
  obvious to modern developers
- **Plan for succession** — Even if you keep IBM i, plan for when it
  eventually needs replacement
