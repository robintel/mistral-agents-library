---
type: platform
family: enterprise
era: japan-focused
---

# Fujitsu Enterprise Systems

Fujitsu's enterprise computing platforms, including mainframe systems
(GS21, PrimePower) and modern server platforms. Widely used in Japanese
corporations, government agencies, and financial institutions. Known for
high reliability, scalability, and compatibility with legacy applications.

## Platform Families

### Mainframe Systems (Legacy)
| System | Era | Architecture | Modernization Path |
|--------|-----|--------------|-------------------|
| **GS21** | 2000s | COBOL, Assembler, TPF | Reface via web services |
| **PrimePower** | 2000s+ | UNIX-based, COBOL, Java | Gradual migration |
| **BS2000** | 1980s-2000s | COBOL, Natural, ADABAS | Legacy preservation |

### Modern Systems
| System | Era | Architecture | Use Case |
|--------|-----|--------------|----------|
| **PRIMEHPC** | 2015+ | HPC, AI/ML, x86 | High-performance computing |
| **PRIMEQUEST** | 2010+ | x86, Linux, Windows | Enterprise servers |
| **PRIMERGY** | 2000+ | x86 servers | Standard enterprise |

## Core discipline

1. **Reliability first** — Fujitsu enterprise systems are designed
   for 99.999% uptime with extensive redundancy and failover capabilities.
2. **Legacy compatibility** — Modern Fujitsu systems maintain backward
   compatibility with legacy applications and data formats.
3. **Japanese enterprise focus** — Optimized for Japanese business
   practices, regulations, and character sets (JIS, Shift-JIS, EUC-JP).
4. **Hybrid ready** — Designed to integrate with cloud services while
   maintaining on-premises control.
5. **Security** — Meets Japanese government and financial regulations
   with built-in encryption and access controls.

## Era map

- **1980s-1990s**: Mainframe era — GS series, BS2000, COBOL-heavy
- **2000-2010**: UNIX transition — PrimePower, open systems adoption
- **2010-2020**: x86 adoption — PRIMERGY, PRIMEQUEST, modernization
- **2020+**: Cloud integration — Hybrid cloud, multi-cloud support
- **2024+**: AI/ML acceleration — PRIMEHPC FX for AI workloads

## Development patterns

### Legacy Application Modernization

#### COBOL Applications
- **Reface**: Wrap COBOL programs with REST APIs
- **Refactor**: Modularize monolithic COBOL programs
- **Re-architect**: Split into microservices using Fujitsu middleware
- **Replace**: Rewrite in modern language (Java, C#)

#### Database Access
- **ADABAS**: Native Fujitsu database (still in use)
- **Rdb**: Relational database (Oracle-compatible)
- **PostgreSQL**: Open-source option on PRIMERGY

#### Character Encoding
- **JIS X 0201**: Roman characters
- **Shift-JIS**: Extended Japanese characters
- **EUC-JP**: Unix Japanese encoding
- **UTF-8**: Modern standard (but may have legacy issues)

## Integration patterns

### Fujitsu to Modern Systems
```
Fujitsu Application → Middleware → Modern System
              ↓
        Interstage, SOA, REST APIs
              ↓
        Data transformation (JIS → UTF-8, etc.)
```

### Database Integration
```
Modern App → Fujitsu Database → Fujitsu Application
        ↓          ↓
    JDBC/ODBC    Native access
        ↓          ↓
    SQL Queries  COBOL/RPG programs
```

### Hybrid Cloud Integration
```
On-Prem Fujitsu → Cloud Services
        ↓
    Fujitsu Cloud Service K5
    or
    AWS/Azure/GCP via VPN
        ↓
    Data synchronization, API gateways
```

## Fujitsu-specific tools

### Middleware
- **Interstage**: Fujitsu's application server and integration platform
- **SYMFOWARE**: Transaction processing monitor (TPF-compatible)
- **SystemWalker**: System management and monitoring

### Development Tools
- **COBOL85**: Fujitsu COBOL compiler with extensions
- **COBOL Server**: Modern COBOL execution environment
- **Java Development**: Full Java SE/EE support
- **Cloud Services**: Fujitsu Cloud Service K5 (IaaS/PaaS)

## Modernization strategies

### 1. Reface
**When**: Keep core Fujitsu logic, expose via modern interfaces
**Approach**:
- Use Interstage to create REST APIs for COBOL programs
- Implement SOAP or REST web services
- Use message queues for asynchronous integration

### 2. Refactor
**When**: Improve existing COBOL/Java applications
**Approach**:
- Modularize monolithic programs
- Adopt modern COBOL standards (COBOL85)
- Use Interstage for service-oriented architecture
- Implement proper error handling and logging

### 3. Re-architect
**When**: Split monolith into services
**Approach**:
- Identify business domains in existing applications
- Extract as separate services using Interstage
- Use Fujitsu's middleware for service communication
- Implement proper separation of concerns

### 4. Replace
**When**: Move to modern platform
**Approach**:
- Rewrite COBOL applications in modern language
- Migrate ADABAS data to relational database
- Implement business logic in modern environment
- Maintain integration with remaining Fujitsu systems

## Performance considerations

### Strengths
- **High availability**: Designed for 99.999% uptime
- **Scalability**: Vertical scaling within large systems
- **Reliability**: Hardware redundancy and failover
- **Compatibility**: Runs legacy and modern applications

### Limitations
- **Proprietary**: Some Fujitsu-specific features may not be portable
- **Skill shortages**: COBOL and mainframe skills are rare
- **Cost**: Enterprise systems can be expensive to maintain
- **Modern features**: Some modern capabilities may require add-ons

## Security considerations

### Built-in security
- **Access control**: Fine-grained user and group permissions
- **Encryption**: Data encryption at rest and in transit
- **Audit logging**: Comprehensive operation logging
- **Compliance**: Meets Japanese regulations (FIPS 140-2, etc.)

### Integration security
- **Network**: Secure connections via VPN or private networks
- **Authentication**: Certificate-based, MFA, LDAP integration
- **Authorization**: Role-based access control for external systems
- **Data protection**: Japanese character set handling, encryption

## Common defects and mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Character encoding issues | Data corruption | Use proper encoding, conversion utilities |
| Legacy data format issues | Integration failures | Data transformation, validation |
| Skill shortages | Maintenance risk | Cross-training, documentation |
| Proprietary lock-in | Migration difficulty | Abstract proprietary features |
| Performance bottlenecks | Slow operations | Optimize queries, use caching |

## Standing rules

- **Respect the legacy** — Fujitsu systems often run mission-critical
  applications that cannot be easily replaced
- **Modernize incrementally** — Reface before refactor before replace
- **Plan for the future** — Even with modernization, plan the eventual
  migration path
- **Document everything** — Legacy systems often lack documentation;
  create it as you modernize
- **Test thoroughly** — Fujitsu systems have unique behaviors and
  integrations that require careful testing
- **Consider hybrid** — Fujitsu systems integrate well with cloud;
  consider hybrid architectures for modernization
