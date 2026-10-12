---
name: OT Security
domain: ot-security
description: Operational Technology and Industrial Control Systems security agents and dialects
---

# OT/ICS Security Domain

**Purpose**: Provide comprehensive security capabilities for Operational Technology (OT) and Industrial Control Systems (ICS) environments, including embedded systems, SCADA, PLCs, and industrial IoT.

**Motivation**: The October 2026 cyberattack on French supermarkets (targeting Danfoss refrigeration systems) demonstrated that OT systems are increasingly connected to IT networks and vulnerable to cyber threats. This domain provides the tools and expertise to secure critical infrastructure across the entire chain.

## Domain Overview

Operational Technology (OT) security is fundamentally different from IT security:

- **Safety First**: OT failures can cause physical harm, environmental damage, or loss of life
- **Availability Critical**: OT systems prioritize uptime; security controls cannot disrupt operations
- **Legacy Systems**: Many OT systems run on outdated hardware/software with 10-30 year lifespans
- **Proprietary Protocols**: Industrial protocols (Modbus, DNP3, OPC UA, Profibus) lack built-in security
- **Physical Access**: Many OT systems are physically accessible, requiring layered defenses
- **Regulatory Requirements**: Industry-specific standards (IEC 62443, NERC CIP, NIS2) mandate security controls

## Recent Context: Danfoss Cyberattack (October 11-12, 2026)

### Attack Summary
- **Target**: French supermarket chains (Intermarché, Coopérative U, E.Leclerc, Les Mousquetaires)
- **Vector**: Danfoss AK-SM 800A, AK-SM800, AK-SC355 refrigeration controllers
- **Impact**: Temperatures raised to 50°C, massive food spoilage, fires, millions in losses
- **Root Cause**: Exploitation of known vulnerabilities in outdated firmware (pre-4.3.1)

### Vulnerabilities Exploited
- CVE-2025-41450: Improper Authentication (authentication bypass)
- CVE-2025-41451: OS Command Injection (post-auth RCE)
- CVE-2025-41452: Configuration Setting Vulnerability (DoS)
- Previous CVEs from 2023: Authentication bypass, path traversal, remote command execution

### Lessons Learned
1. **Patch Management is Critical**: Danfoss had released firmware 4.3.1 with patches, but many systems were running outdated versions
2. **Internet-Exposed OT Systems are Dangerous**: Once isolated, now connected for remote monitoring
3. **Supply Chain Risk**: Third-party vendors (Danfoss) can be the attack vector
4. **Physical Impact**: Cyberattacks on OT can cause real-world damage (food spoilage, fires)
5. **Need for Continuous Monitoring**: Asset inventory and vulnerability scanning are essential

## Agents in this Domain

### Core OT Security Agents

#### 1. OT Security Architect
**Role**: Design and implement comprehensive OT security architectures

**Emergency Response**: For immediate incident response, refer to [ot-ics-emergency-response.md](./ot-ics-emergency-response.md) - a vendor-neutral guide incorporating lessons from Danfoss, Schneider Electric, Siemens, Emerson, and Honeywell incidents.

### Zero Trust Sub-Domain Agents

The Zero Trust sub-domain provides specialized agents for implementing and maintaining Zero Trust Architecture in OT/ICS environments:

#### 1. Zero Trust Coordinator (T4)
**Role**: Orchestrate Zero Trust Architecture implementation across OT environments
**Path**: [zero-trust/zero-trust-coordinator.md](./zero-trust/zero-trust-coordinator.md)
**Specialization**: Primary authority on Zero Trust in OT, balances security with safety and availability

#### 2. Zero Trust Auditor (T3)
**Role**: Audit Zero Trust Architecture compliance in OT environments
**Path**: [zero-trust/zero-trust-auditor.md](./zero-trust/zero-trust-auditor.md)
**Specialization**: Validate Zero Trust against IEC 62443 and NIST SP 800-207, OT-specific gap identification

#### 3. OT Identity Manager (T3)
**Role**: Manage identities for OT devices, non-human entities, and legacy systems
**Path**: [zero-trust/ot-identity-manager.md](./zero-trust/ot-identity-manager.md)
**Specialization**: Device identity, non-human authentication, legacy device accommodation, certificate management

#### 4. Micro-Segmentation Engineer (T3)
**Role**: Design and implement micro-segmentation architectures in OT networks
**Path**: [zero-trust/micro-segmentation-engineer.md](./zero-trust/micro-segmentation-engineer.md)
**Specialization**: IEC 62443 zone/conduit design, protocol-aware segmentation, industrial protocol filtering

#### 5. Continuous Verification Monitor (T2)
**Role**: 24/7 monitoring and verification of Zero Trust implementation
**Path**: [zero-trust/continuous-verification-monitor.md](./zero-trust/continuous-verification-monitor.md)
**Specialization**: Real-time verification across all seven Zero Trust pillars, anomaly detection, alerting

**When to Use Zero Trust Agents**:
- Implementing Zero Trust in OT environments
- Modernizing legacy OT systems with Zero Trust
- IT/OT convergence projects requiring Zero Trust
- Compliance programs (NIS2, IEC 62443, NIST) requiring Zero Trust
- Responding to incidents where Zero Trust could have prevented impact

**Zero Trust Architecture in OT**: Unlike IT, OT Zero Trust must balance "Never Trust, Always Verify" with "Never Disrupt, Always Operate". The Zero Trust sub-domain provides the specialized expertise needed to adapt IT Zero Trust principles for OT constraints including safety-critical systems, legacy devices, industrial protocols, and real-time requirements.

### Blockchain Sub-Domain Agents

The Blockchain sub-domain provides specialized agents for implementing and maintaining **blockchain-based distributed trust systems** in OT/ICS environments. Blockchain in OT is **not about cryptocurrency** — it's about creating **tamper-proof, distributed trust** for critical infrastructure.

**Core Value Proposition**: Combine blockchain's immutable audit capabilities with OT's need for safety, availability, and integrity. The result is a system where **no single entity can compromise the integrity** of your OT environment, and where **all actions are permanently, tamper-proof recorded**.

#### 1. Blockchain Coordinator (T4)
**Role**: **Orchestrate blockchain implementation** across Operational Technology and Industrial Control Systems

**Path**: [blockchain/blockchain-coordinator.md](./blockchain/blockchain-coordinator.md)

**Specialization**: Primary authority on blockchain for OT environments. Designs blockchain solutions for OT requirements, dispatches specialized sub-agents, and integrates blockchain with Zero Trust architecture.

**Key Capabilities**:
- Architecture orchestration for blockchain in OT
- Platform selection (Hyperledger Fabric, Ethereum Enterprise, R3 Corda)
- Integration strategy with existing OT systems
- Compliance mapping (IEC 62443, NIST, NIS2)
- Vendor coordination for blockchain-capable solutions

**When to Use**: Implementing blockchain for OT audit trails, tamper-proof device identity, supply chain integrity, distributed consensus, or Zero Trust + Blockchain integration.

#### 2. Blockchain Auditor (T3)
**Role**: **Audit blockchain implementation** in Operational Technology and Industrial Control Systems environments

**Path**: [blockchain/blockchain-auditor.md](./blockchain/blockchain-auditor.md)

**Specialization**: Validates blockchain deployments against OT-specific requirements, ensuring proper implementation, security, operational suitability, and compliance.

**Key Capabilities**:
- Implementation auditing against design
- Security auditing of blockchain controls
- Compliance auditing (IEC 62443, NERC CIP, NIS2)
- Effectiveness auditing for value delivery
- Smart contract security reviews

**When to Use**: Blockchain implementation audits, regular security assessments, compliance audits requiring blockchain validation, smart contract security reviews, incident investigations involving blockchain.

#### 3. OT Blockchain Integrity Manager (T3)
**Role**: **Manage cryptographic integrity of OT assets** using blockchain technology

**Path**: [blockchain/ot-blockchain-integrity.md](./blockchain/ot-blockchain-integrity.md)

**Specialization**: Uses blockchain to anchor the integrity of OT assets, providing cryptographic proof that devices, firmware, configurations, and supply chain components are authentic and unmodified.

**Key Capabilities**:
- Firmware integrity verification with blockchain anchoring
- Device identity management with blockchain verification
- Configuration integrity tracking and verification
- Supply chain integrity with chain of custody
- Hash anchoring for OT assets

**When to Use**: Implementing firmware integrity verification, managing device identity, tracking supply chain integrity, verifying configuration changes, or anchoring OT asset hashes to blockchain.

#### 4. Distributed Trust Monitor (T2)
**Role**: **Continuously monitor blockchain-based trust systems** in Operational Technology and Industrial Control Systems

**Path**: [blockchain/distributed-trust-monitor.md](./blockchain/distributed-trust-monitor.md)

**Specialization**: Provides 24/7 monitoring of blockchain implementations in OT environments, ensuring distributed trust mechanisms are functioning correctly, detecting anomalies, and providing actionable alerts.

**Key Capabilities**:
- Blockchain health monitoring (nodes, network, performance)
- Consensus mechanism monitoring
- Trust verification (integrity, identity, supply chain)
- Anomaly detection for blockchain systems
- Alert management with OT-specific prioritization

**When to Use**: Continuous monitoring of OT blockchain implementations, real-time verification of distributed trust, anomaly detection, alert management, or incident response support.

#### 5. Smart Contract Engineer (T3)
**Role**: **Design, develop, test, and deploy smart contracts** for Operational Technology and Industrial Control Systems

**Path**: [blockchain/smart-contract-engineer.md](./blockchain/smart-contract-engineer.md)

**Specialization**: Implements OT-specific smart contracts (chaincode) that encode business logic for blockchain-based trust systems in critical infrastructure.

**Key Capabilities**:
- Smart contract design for OT use cases
- Secure code development (Go for Fabric, Solidity for Ethereum)
- Comprehensive testing (unit, integration, security, performance)
- Deployment to blockchain platforms
- Integration with OT systems
- Maintenance and updates

**When to Use**: Designing and developing smart contracts for OT blockchain, testing contract security, deploying contracts to production, or maintaining existing contracts.

**Blockchain + Zero Trust: The Powerful Combination**:

```
┌─────────────────────────────────────────────────────────────┐
│                    ZERO TRUST + BLOCKCHAIN                       │
├─────────────────────────────────────────────────────────────┤
│  ZERO TRUST: "Never Trust, Always Verify"                        │
│  ├── Verifies every access request                               │
│  ├── Requires continuous authentication                         │
│  └── Enforces least privilege access                            │
│                                                                  │
│  BLOCKCHAIN: "Record Everything, Tamper-Proof"                  │
│  ├── Immutable record of all verifications                       │
│  ├── Cryptographic proof that verification happened              │
│  └── Distributed - no single point of failure                    │
│                                                                  │
│  COMBINED: "Trust but Verify and Record Forever"              │
│  ├── Zero Trust verifies access in real-time                    │
│  ├── Blockchain provides permanent, tamper-proof record          │
│  ├── Creates auditable chain of trust                            │
│  └── Enables forensic analysis with cryptographic certainty     │
└─────────────────────────────────────────────────────────────┘
```

**When to Use Blockchain Agents**:
- Implementing blockchain for OT environments
- Creating tamper-proof audit trails for OT events
- Verifying firmware, device, or supply chain integrity
- Implementing distributed trust for critical operations
- Integrating blockchain with Zero Trust Architecture
- Compliance programs requiring tamper-proof records (IEC 62443, NIS2, NERC CIP)

**Blockchain in OT vs. Traditional Blockchain**:

| Aspect | Traditional Blockchain | OT Blockchain |
|--------|----------------------|---------------|
| **Primary Goal** | Decentralization, censorship resistance | **Distributed trust, tamper-proof audit** |
| **Participants** | Public, anonymous | **Private, known OT entities** (PLCs, RTUs, HMIs, vendors) |
| **Consensus** | Proof-of-Work, Proof-of-Stake | **OT-optimized consensus** (PBFT, Raft, Istanbul) |
| **Performance** | Seconds to minutes per transaction | **Milliseconds to seconds** (OT real-time requirements) |
| **Data Type** | Financial transactions | **OT events** (config changes, access, firmware updates) |
| **Privacy** | Public, pseudonymous | **Private, confidential** (only authorized OT personnel) |

**Recommended Platform**: **Hyperledger Fabric** - Private, permissioned, channels, high performance, enterprise-grade, growing OT community adoption.

**Responsibilities**:
- Develop zone and conduit architectures (IEC 62443)
- Design defense-in-depth strategies for OT environments
- Plan network segmentation for industrial networks
- Implement zero-trust for OT systems
- Integrate with IT security frameworks

**When to Use**: Building new OT networks, modernizing legacy systems, compliance programs

### 2. OT Pentester
**Role**: Conduct authorized security testing on OT systems

**Responsibilities**:
- Perform passive asset discovery (never active scanning on live systems)
- Conduct vulnerability assessments
- Test industrial protocols for weaknesses
- Validate security controls
- Develop exploitation proofs-of-concept

**When to Use**: Security assessments, compliance audits, before system deployment

### 3. ICS Incident Responder
**Role**: Respond to and recover from ICS cybersecurity incidents

**Responsibilities**:
- Develop incident response plans for OT
- Conduct forensic investigations on ICS
- Implement containment and eradication
- Coordinate with IT incident response
- Develop recovery procedures

**When to Use**: Active cyberattacks, suspected breaches, incident preparedness

### 4. Embedded Systems Security Auditor
**Role**: Audit the security of embedded systems and firmware

**Responsibilities**:
- Perform firmware analysis
- Review hardware security controls
- Validate secure boot and update mechanisms
- Test for side-channel attacks
- Verify cryptographic implementations

**When to Use**: Firmware development, vendor audits, supply chain security

## Dialects in this Domain

### 1. OT Security Dialect
**Purpose**: Standardized language for OT security discussions

**Components**:
- OT terminology and concepts
- Industrial protocol security
- Asset classification frameworks
- Risk assessment methodologies
- Security control families

### 2. IEC 62443 Dialect
**Purpose**: Implementation guidance for IEC 62443 standards

**Components**:
- Zone and conduit architecture patterns
- Foundational requirements (FR) mapping
- System requirements (SR) implementation
- Component certification guidance
- Compliance documentation

### 3. Danfoss Security Dialect
**Purpose**: Danfoss-specific security patterns and lessons learned

**Components**:
- AK-SM 800A security configurations
- Firmware update procedures
- Vulnerability management
- Secure deployment practices
- Monitoring and detection

### 4. Blockchain Dialect
**Purpose**: Standardized terminology and concepts for blockchain in OT/ICS environments

**Path**: [../dialects/blockchain-dialect.md](../dialects/blockchain-dialect.md)

**Components**:
- Foundational blockchain concepts for OT
- Core terminology (blockchain architecture, node types, consensus mechanisms)
- OT-specific data and integrity terms
- Blockchain + Zero Trust integration terminology
- Implementation patterns for OT use cases
- OT-specific use case terminology (firmware integrity, device identity, supply chain)
- Compliance and standards mapping
- Best practices and common misconceptions

**Key Concepts**:
- **Blockchain in OT is about distributed trust, not cryptocurrency**
- **Hash anchoring**: Store hashes on-chain, data off-chain (primary OT pattern)
- **Tamper-proof audit**: Immutable record of all OT events
- **Cryptographic certainty**: Mathematical proof of what happened
- **Chain of trust**: Series of trust relationships anchored to blockchain

## Frameworks and Standards

### Primary OT Security Frameworks

1. **IEC 62443 (ISA/IEC 62443 Series)**
   - IEC 62443-1-1: Terminology, concepts, and models
   - IEC 62443-2-1: System requirements
   - IEC 62443-3-2: Risk assessment
   - IEC 62443-3-3: System design requirements
   - IEC 62443-4-1: Secure product development lifecycle
   - IEC 62443-4-2: Technical security requirements

2. **NIST SP 800-82 Rev. 3**
   - Guide to Operational Technology Security
   - Comprehensive guidance for securing ICS
   - Maps to IEC 62443 and NIST CSF

3. **NIST Cybersecurity Framework (CSF) 2.0**
   - Identify, Protect, Detect, Respond, Recover
   - Govern function added in 2.0
   - Applicable to OT with proper tailoring

4. **Purdue Enterprise Reference Architecture (PERA)**
   - Model for industrial network segmentation
   - Levels 0-5: Physical process to enterprise
   - Foundation for zone and conduit design

### Industry-Specific Standards

| Industry | Standard | Scope |
|----------|----------|-------|
| Energy (US) | NERC CIP | North American power grid |
| Energy (EU) | NIS2 Directive | Critical infrastructure |
| Chemical | IEC 61511 | Functional safety (SIS) |
| Oil & Gas | IEC 61508 | Functional safety |
| Manufacturing | ISO 27001 + OT | General OT security |
| Automotive | ISO/SAE 21434 | Road vehicle cybersecurity |

## Key OT Security Concepts

### 1. Defense-in-Depth for OT
```
┌─────────────────────────────────────────────────────────────┐
│                    DEFENSE-IN-DEPTH                           │
├─────────────────┬─────────────────┬─────────────────┬────────┤
│  Physical Layer   │  Network Layer   │  System Layer    │ Data    │
│  - Fencing        │  - DMZs          │  - Hardening     │ Layer   │
│  - Locks          │  - Firewalls     │  - Patching      │ - Encryption│
│  - Access control │  - IDS/IPS       │  - Config Mgmt   │ - Integrity│
│  - Surveillance    │  - Segmentation  │  - Application    │          │
│                  │  - Monitoring    │    Controls      │          │
└─────────────────┴─────────────────┴─────────────────┴────────┘
```

### 2. Purdue Model (Levels 0-5)
```
Level 5: Enterprise Network (IT) - ERP, Business systems
Level 4: Site Business Systems - Site-level planning, logistics
Level 3: Site Operations - HMI, Historian, MES
Level 2: Area Supervisory Control - PLC, SCADA
Level 1: Basic Control - Sensors, actuators, drives
Level 0: Physical Process - The actual industrial process
```

### 3. Zone and Conduit Architecture (IEC 62443)

**Zones**: Groupings of assets with similar security requirements
**Conduits**: Secure communication pathways between zones

Example for Manufacturing:
- Zone 1: Business Systems (ERP, PLM)
- Zone 2: Manufacturing Operations (MES, SCADA)
- Zone 3: Control Systems (PLC, HMI)
- Zone 4: Physical Process (Sensors, Actuators)

### 4. OT Asset Classification

| Category | Examples | Security Focus |
|----------|----------|----------------|
| Field Devices | Sensors, Actuators, Drives | Physical security, tamper detection |
| Controllers | PLC, DCS, RTU | Access control, firmware integrity |
| Networks | Industrial Ethernet, Fieldbus | Protocol security, segmentation |
| HMI/SCADA | Operator interfaces, historians | Authentication, audit logging |
| Gateways | Protocol converters, firewalls | Filtering, monitoring |
| Servers | Historians, MES, PLM | Hardening, patching |

## Security Controls for OT

### Technical Controls

1. **Network Segmentation**
   - Physical separation where possible
   - VLANs for logical separation
   - Firewalls between zones
   - DMZ for external access

2. **Access Control**
   - Role-based access control (RBAC)
   - Multi-factor authentication (MFA)
   - Jump servers for administrative access
   - Least privilege principle

3. **Monitoring and Detection**
   - Network traffic monitoring (passive taps, SPAN ports)
   - OT-specific IDS/IPS (Nozomi, Claroty, Dragos, Tenable.ot)
   - Anomaly detection for industrial protocols
   - Log collection and analysis

4. **Endpoint Protection**
   - Application whitelisting
   - Host-based firewalls
   - Anti-malware (with OT-specific exclusions)
   - Secure configuration baselines

5. **Patch Management**
   - Regular vulnerability assessments
   - Test patches in staging environment
   - Scheduled maintenance windows
   - Rollback procedures

### Process Controls

1. **Security Governance**
   - Security policies and procedures
   - Risk management processes
   - Incident response plans
   - Security awareness training

2. **Change Management**
   - Controlled change procedures
   - Impact assessment
   - Testing and validation
   - Documentation and approval

3. **Vendor Management**
   - Vendor security assessments
   - Supply chain security
   - Third-party access controls
   - Contractual security requirements

## Common OT Protocols and Security Considerations

| Protocol | Typical Use | Security Features | Security Concerns |
|----------|-------------|-------------------|------------------|
| Modbus TCP | PLC communication | None (original) | No authentication, clear text |
| DNP3 | SCADA, utilities | DNP3 SA (Security Authentication) | Weak encryption, replay attacks |
| OPC UA | Modern ICS | TLS, authentication, authorization | Complex to configure correctly |
| Profibus | Industrial fieldbus | None | No native security |
| Profinet | Industrial Ethernet | Optional security | Often deployed without |
| EtherNet/IP | Industrial Ethernet | CIP Security | Optional, often disabled |
| BACnet | Building automation | BACnet/SC | Weak encryption, optional |

## OT Security Tools and Technologies

### Asset Discovery and Inventory
- **Passive Discovery**: Nozomi Networks, Claroty, Tenable.ot, Forescout EyeExtend
- **Active Discovery** (carefully): Nessus, OpenVAS (with OT-specific plugins)
- **Protocol-Specific**: Wireshark with industrial protocol dissectors

### Network Security
- **Firewalls**: Palo Alto, Fortinet, Cisco (with OT-specific rules)
- **OT Firewalls**: Tofino, Nozomi, Claroty
- **Network TAPs**: Garland Technology, Ixia Vision

### Endpoint Security
- **Whitelisting**: Carbon Black, CrowdStrike, Microsoft AppLocker
- **OT-Specific**: Claroty, Nozomi, Tenable.ot

### Monitoring and SIEM
- **OT SIEM**: Nozomi Guardian, Claroty, Dragos Platform
- **Traditional SIEM**: Splunk, IBM QRadar, Microsoft Sentinel (with OT plugins)

## Response to Danfoss Attack: Recommended Actions

Based on the October 2026 cyberattack, organizations using Danfoss or similar OT systems should:

### Immediate Actions (0-24 hours)
1. **Disconnect affected systems** from internet if not already isolated
2. **Apply emergency patches** - Upgrade to firmware 4.3.1 or later
3. **Implement network segmentation** - Isolate refrigeration systems from other networks
4. **Deploy monitoring** - Set up OT-specific IDS for Danfoss controllers
5. **Review remote access** - Disable or secure all remote access pathways

### Short-term Actions (1-7 days)
1. **Asset inventory** - Identify all Danfoss and similar controllers
2. **Vulnerability assessment** - Scan for known CVEs
3. **Firmware update plan** - Prioritize critical systems
4. **Network architecture review** - Ensure proper segmentation
5. **Incident response plan** - Update for OT-specific scenarios

### Medium-term Actions (1-4 weeks)
1. **Security architecture design** - Implement defense-in-depth
2. **Patch management process** - Establish regular update procedures
3. **Security monitoring** - Deploy OT-specific security tools
4. **Security awareness training** - Train OT personnel on cybersecurity
5. **Vendor security requirements** - Update contracts with suppliers

### Long-term Actions (1-12 months)
1. **IEC 62443 compliance program** - Implement comprehensive OT security
2. **Zero-trust architecture** - Migrate to modern security model
3. **Security by design** - Integrate security into new system deployments
4. **Continuous improvement** - Regular security assessments and updates

## Integration with Other Domains

### AI/RAG Integration
- **OT RAG Systems**: Build RAG for OT documentation and troubleshooting
- **AI-Powered Monitoring**: Use AI to detect anomalies in OT systems
- **Predictive Maintenance**: Combine OT data with AI for predictive insights

### Control Systems Integration
- **Digital Twins**: Secure digital twin implementations
- **Model-Based Security**: Use control system models for security validation
- **HIL Testing**: Hardware-in-the-loop testing for security

### Security Integration
- **IT/OT Convergence**: Align IT and OT security programs
- **Supply Chain Security**: Extend security to third-party vendors
- **Compliance Management**: Unified compliance across IT and OT

## Getting Started

1. **Assess your OT environment** - Inventory all OT systems and connections
2. **Identify critical systems** - Prioritize based on safety, production, and business impact
3. **Evaluate current security** - Gap analysis against IEC 62443 or NIST SP 800-82
4. **Develop a roadmap** - Plan security improvements over time
5. **Implement controls** - Start with high-impact, low-complexity measures
6. **Monitor and improve** - Continuous monitoring and enhancement

## Resources

- [IEC 62443 Standards](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards)
- [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/publications/detail/sp/800-82/rev-3/final)
- [NIST CSF 2.0](https://www.nist.gov/cyberframework)
- [Danfoss Security Advisories](https://www.danfoss.com/en/service-and-support/coordinated-vulnerability-disclosure/danfoss-security-advisories/)
- [CISA OT Security](https://www.cisa.gov/topics/industrial-control-systems)
- [SANS ICS Security](https://www.sans.org/courses/ics-410-ics-scada-security-essentials/)

## License

This domain and its agents are licensed under the same terms as the mistral-agents-library.
