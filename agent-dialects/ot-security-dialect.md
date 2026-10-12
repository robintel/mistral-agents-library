---
name: ot-security-dialect
domain: dialects
description: Dialect for Operational Technology and Industrial Control Systems security terminology and concepts
---

# OT Security Dialect

**Purpose**: Provide a **standardized language and terminology** for discussing Operational Technology (OT) and Industrial Control Systems (ICS) security. This dialect ensures consistent, accurate communication among OT engineers, IT security professionals, management, and other stakeholders.

**Motivation**: The October 2026 cyberattack on refrigeration systems demonstrated that **miscommunication between OT and IT teams** can delay detection and response. This dialect bridges the gap by defining clear, consistent terminology for OT security discussions.

## Dialect Overview

OT security has **unique terminology, concepts, and priorities** that differ from IT security:

| Aspect | IT Security | OT Security |
|--------|-------------|--------------|
| **Priority** | Confidentiality, Integrity, Availability (CIA) | Availability, Integrity, Confidentiality (AIC) |
| **Lifespan** | 3-5 years | 10-30+ years |
| **Update Cycle** | Frequent (weekly/monthly) | Infrequent (yearly or less) |
| **Failure Impact** | Data loss, privacy breach | Safety incidents, equipment damage, production loss |
| **Protocols** | TCP/IP, HTTP, DNS | Modbus, DNP3, OPC UA, Profibus, Fieldbus |
| **Legacy Systems** | Rare, replaced frequently | Common, difficult to replace |
| **Change Windows** | Frequent, planned | Infrequent, highly controlled |

## Core Terminology

### 1. OT System Classification

**Operational Technology (OT)**: Hardware and software that **detects or causes a change** through the direct monitoring and/or control of **physical devices, processes, and events**.

**Industrial Control Systems (ICS)**: General term for **supervisory control and data acquisition (SCADA) systems, distributed control systems (DCS), and other **control system configurations** such as programmable logic controllers (PLC).

**SCADA (Supervisory Control and Data Acquisition)**: System for **remote monitoring and control** of industrial processes. Typically consists of:
- Human-Machine Interface (HMI)
- Supervisory System (Data acquisition and control)
- Remote Terminal Units (RTU)
- Programmable Logic Controllers (PLC)
- Communication Infrastructure

**DCS (Distributed Control System)**: Control system where **control elements are distributed** throughout the system rather than centralized. Common in process industries (chemical, oil & gas).

**PLC (Programmable Logic Controller)**: Industrial digital computer used for **automation of industrial processes**, such as control of machinery on factory assembly lines.

**RTU (Remote Terminal Unit)**: Device that **interfaces objects in the physical world** to a distributed control system or SCADA system by **transmitting telemetry data** and **allowing remote control**.

**HMI (Human-Machine Interface)**: User interface or dashboard that **connects a person to a machine, system, or device**. In OT, typically graphical displays of process information.

**Field Device**: Any device that **interacts directly with the physical process**, including:
- Sensors (temperature, pressure, flow, level)
- Actuators (valves, motors, pumps)
- Transducers
- Transmitters

**Intelligent Electronic Device (IED)**: Device incorporating **one or more processors** with the capability to **receive or send data/control** from or to an external source.

**Example**: A refrigeration system manager is a **System Manager** (central controller) that coordinates **refrigeration controllers** and offers a **web interface** for monitoring and control.

### 2. OT Network Architecture

**Purdue Enterprise Reference Architecture (PERA) Model**: Hierarchical model for **industrial network segmentation** with levels 0-5:

- **Level 0: Physical Process** - The actual industrial process (sensors, actuators, physical equipment)
- **Level 1: Basic Control** - Direct control of physical process (PLC, RTU, local HMI, sensors, actuators)
- **Level 2: Area Supervisory Control** - Monitoring and control of multiple Level 1 devices (SCADA, DCS, HMI workstations)
- **Level 3: Site Operations** - Site-level manufacturing operations (MES, historians, engineering workstations)
- **Level 4: Site Business Systems** - Site-level business planning and logistics (PLM, site ERP)
- **Level 5: Enterprise Network** - Corporate IT systems (ERP, business analytics, email)

**Zone**: A **grouping of OT assets** with **similar security requirements**. Zones are defined based on:
- Function
- Criticality
- Sensitivity
- Risk level
- Communication requirements

**Conduit**: A **secure communication pathway** between two zones. Defines:
- Allowed protocols
- Security controls
- Authentication requirements
- Encryption requirements
- Monitoring requirements

**Demilitarized Zone (DMZ)**: A **physical or logical subnetwork** that **sits between trusted and untrusted networks**, acting as an additional layer of security.

**Example**: In the refrigeration system attack, poor **zone definition** and **conduit security** allowed attackers to move from the **Supervisory Control Zone** to the **Refrigeration Control Zone**.

### 3. OT Protocols

**Industrial Protocol**: Communication protocol **designed for industrial environments**, typically with **real-time requirements** and **tolerance for harsh conditions**.

**Common OT Protocols**:

| Protocol | Full Name | Typical Use | Security Features | Security Concerns |
|----------|-----------|-------------|-------------------|------------------|
| **Modbus** | Modbus | PLC communication | None (original) | No authentication, clear text, no integrity |
| **Modbus TCP** | Modbus TCP/IP | PLC communication over TCP/IP | None (original) | No authentication, clear text, no integrity |
| **DNP3** | Distributed Network Protocol | SCADA, utilities | DNP3 Secure Authentication (SA) | Weak encryption, replay attacks, optional security |
| **OPC UA** | OPC Unified Architecture | Modern ICS, cross-platform | TLS, authentication, authorization, certificates | Complex to configure, certificate management |
| **Profibus** | Process Field Bus | Industrial fieldbus | None | No native security |
| **Profinet** | Process Field Network | Industrial Ethernet | Optional security | Often deployed without security |
| **EtherNet/IP** | Ethernet Industrial Protocol | Industrial Ethernet | CIP Security | Optional, often disabled |
| **BACnet** | Building Automation and Control Networks | Building automation | BACnet/SC | Weak encryption, optional |
| **IEC 61850** | IEC 61850 | Power utility automation | Security extensions | Complex, optional |
| **HART** | Highway Addressable Remote Transducer | Process instrumentation | None | No native security |
| **Foundation Fieldbus** | Foundation Fieldbus | Process automation | None | No native security |

**Vendor-Specific Protocols** (Refrigeration Systems):
- **Vendor Cloud Protocol**: Cloud-based monitoring and control protocol
- **System Manager Protocol**: Proprietary protocol for system manager communication
- **Controller Protocol**: Protocol for controller communication

### 4. OT Security Concepts

**Safety Instrumented System (SIS)**: System designed to **perform safety instrumented functions (SIF)** to **prevent or mitigate hazardous events** by taking the process to a safe state when predetermined conditions are violated.

**Safety Integrity Level (SIL)**: **Relative level of risk-reduction** provided by a safety function, or to specify a **target level of risk reduction**. Defined in IEC 61508:
- **SIL 1**: Lowest level of integrity
- **SIL 2**: Medium level of integrity
- **SIL 3**: High level of integrity
- **SIL 4**: Highest level of integrity

**Defense-in-Depth**: **Layered approach** to security where **multiple security controls** are implemented to **provide redundancy** in case any single control fails.

** OT Defense-in-Depth Layers**:
1. **Physical Layer**: Fencing, locks, access control, surveillance
2. **Network Layer**: DMZs, firewalls, IDS/IPS, segmentation
3. **System Layer**: Hardening, patching, configuration management
4. **Application Layer**: Secure coding, input validation, access control
5. **Data Layer**: Encryption, integrity, access control
6. **Policy Layer**: Policies, procedures, training, awareness

**Zero Trust for OT**: Security model that **eliminates the notion of trust** and **verifies every request** as if it originates from an **open network**. In OT, focuses on:
- **Device Identity**: Every device has a unique, verifiable identity
- **Least Privilege Access**: Devices have only the access they need
- **Micro-Segmentation**: Fine-grained network segmentation
- **Continuous Monitoring**: All access attempts and device behavior monitored
- **Automated Response**: Automated containment and response to threats

**Air Gap**: **Physical separation** between OT and IT networks, with **no network connection** between them. Data is transferred via **sneakernet** (physical media transfer).

**Note**: True air gaps are **rare in modern OT environments** due to the need for remote monitoring, maintenance, and integration with business systems.

**Convergence (IT/OT Convergence)**: The **integration of IT and OT systems** to **improve efficiency, visibility, and control**. Increases the need for **strong security controls** as previously isolated OT systems become accessible from IT networks.

### 5. OT Security Controls

**Security Control**: **Safeguard or countermeasure** to **avoid, counteract, or minimize security risks**.

**OT-Specific Security Controls**:

**Physical Controls**:
- **Perimeter Security**: Fencing, gates, barriers
- **Building Security**: Secure buildings, controlled entry
- **Room Security**: Secure equipment rooms, server rooms
- **Device Security**: Physical protection of devices, tamper-evident seals
- **Cable Security**: Protection of network, power, and signal cables

**Network Controls**:
- **Network Segmentation**: Divide network into zones with controlled communication
- **Firewalls**: Filter traffic between network segments
- **OT Firewalls**: Specialized firewalls for industrial protocols (Tofino, Nozomi)
- **Intrusion Detection/Prevention (IDS/IPS)**: Detect and prevent malicious network activity
- **Network Access Control (NAC)**: Control which devices can access the network
- **Virtual LANs (VLANs)**: Logical network segmentation
- **Protocol Filtering**: Allow only authorized industrial protocols
- **Deep Packet Inspection (DPI)**: Inspect packet contents for malicious activity

**System Controls**:
- **Authentication**: Verify user/device identity (username/password, certificates, biometrics)
- **Authorization**: Control access to resources (RBAC, ABAC, rule-based)
- **Accounting**: Track access and activities (logging, auditing)
- **Configuration Management**: Control and track system configurations
- **Patch Management**: Process for applying security updates
- **Application Whitelisting**: Allow only approved applications to run
- **Host-Based Firewall**: Filter network traffic at the device level
- **File Integrity Monitoring (FIM)**: Detect unauthorized changes to critical files

**Application Controls**:
- **Input Validation**: Validate all inputs to prevent injection attacks
- **Output Encoding**: Protect against injection attacks in outputs
- **Session Management**: Secure user sessions with proper controls
- **Error Handling**: Secure error messages and handling
- **Secure Coding**: Follow secure coding practices

**Data Controls**:
- **Data Classification**: Identify data sensitivity and handle appropriately
- **Encryption**: Protect data at rest and in transit
- **Data Integrity**: Ensure data accuracy and completeness
- **Data Retention**: Manage data lifecycle
- **Data Privacy**: Protect personal information

**Monitoring Controls**:
- **Network Monitoring**: Monitor network traffic for anomalies
- **Endpoint Monitoring**: Monitor endpoints for malicious activity
- **OT-Specific Monitoring**: Monitor industrial protocols and device behavior
- **Anomaly Detection**: Detect unusual patterns or behaviors
- **Log Collection**: Collect and store logs for analysis and forensic investigation

### 6. OT Vulnerability Management

**Vulnerability**: **Weakness** in an OT system, component, or process that could be **exploited by a threat actor** to perform unauthorized actions.

**Common OT Vulnerabilities**:

| Vulnerability Type | Description | Example | Mitigation |
|-------------------|-------------|---------|------------|
| **Authentication Bypass** | Attacker gains access without proper authentication | CVE-2025-41450 | Implement proper authentication, remove default credentials |
| **Buffer Overflow** | Attacker overflows buffer to execute arbitrary code | CVE-2023-25915 | Input validation, bounds checking, memory-safe languages |
| **Command Injection** | Attacker injects OS commands through application | CVE-2025-41451 | Input sanitization, parameterized commands |
| **Path Traversal** | Attacker accesses files outside intended directory | CVE-2023-25914 | Input validation, canonical path resolution |
| **Hardcoded Credentials** | Default or backdoor credentials in firmware | Refrigeration controller | Remove hardcoded credentials, use secure configuration |
| **Insecure Defaults** | Default configurations are insecure | HTTP enabled, default passwords | Change defaults, implement secure configurations |
| **Lack of Encryption** | Sensitive data transmitted or stored without encryption | Modbus TCP, configuration files | Implement encryption for sensitive data |
| **Weak Encryption** | Use of weak or deprecated encryption algorithms | DES, RC4, MD5 | Use strong, modern encryption (AES-256, SHA-256) |
| **No Input Validation** | Application accepts malformed or malicious input | Web interfaces, protocol handlers | Implement input validation and sanitization |
| **Race Conditions** | Attacker exploits timing between operations | Concurrent access vulnerabilities | Implement proper locking and synchronization |
| **Side-Channel Attacks** | Attacker extracts information via physical observations | Power analysis, timing attacks | Implement constant-time operations, add noise |
| **Supply Chain Vulnerabilities** | Vulnerabilities introduced through vendors or components | Compromised firmware, malicious components | Implement vendor security assessments, verify all components |

**Vulnerability Scoring**:
- **CVSS (Common Vulnerability Scoring System)**: Standard for assessing and conveying the characteristics and impacts of system vulnerabilities
- **OT-Specific Scoring**: Some organizations use modified CVSS for OT that weights **availability impact** more heavily

**Example: Refrigeration System Vulnerabilities**:
- **CVE-2025-41450**: Improper Authentication (CVSS 9.8 - Critical)
- **CVE-2025-41451**: OS Command Injection (CVSS 9.8 - Critical)
- **CVE-2025-41452**: Configuration Setting Vulnerability (CVSS 7.5 - High)

### 7. OT Incident Response

**Incident**: **Event** that **compromises or threatens** the **confidentiality, integrity, or availability** of OT systems or the **safety of personnel or equipment**.

**OT-Specific Incident Types**:
- **Cyberattack**: Malicious attempt to damage, disrupt, or gain unauthorized access to OT systems
- **Equipment Failure**: Hardware or software failure affecting OT systems
- **Human Error**: Mistake by personnel causing OT system issues
- **Natural Disaster**: Natural event (storm, earthquake) affecting OT systems
- **Physical Intrusion**: Unauthorized physical access to OT facilities or devices
- **Supply Chain Incident**: Issue with vendor or component affecting OT systems

**Incident Response**: **Process for detecting, responding to, and recovering from incidents**.

**OT Incident Response Phases**:
1. **Preparation**: Develop IR plan, establish team, conduct training
2. **Detection and Analysis**: Identify and confirm incidents
3. **Containment**: Isolate affected systems to prevent further damage
4. **Eradication**: Remove attacker access, close vulnerabilities
5. **Recovery**: Restore systems to safe, secure operating condition
6. **Post-Incident**: Learn from incident, improve future response

**OT-Specific Incident Response Challenges**:
- **Safety First**: All actions must prioritize safety of personnel and equipment
- **Production Impact**: Response actions must minimize disruption to production
- **Physical Consequences**: Cyber incidents can cause physical damage or safety hazards
- **Limited Forensics**: OT devices often lack logging capabilities
- **Legacy Systems**: May not support modern security controls or investigations
- **Vendor Dependencies**: May require vendor assistance for incident response

**Example**: In the refrigeration system attack, **containment** required **isolating the Refrigeration Control Zone** while **maintaining safety** (preventing equipment damage from rapid temperature changes).

### 8. OT Compliance and Standards

**Compliance**: **Adherence to laws, regulations, standards, and best practices**.

**Primary OT Security Standards**:

| Standard | Developer | Focus | Applicability |
|----------|-----------|-------|--------------|
| **IEC 62443** | ISA/IEC | Industrial automation and control systems cybersecurity | Global, all industries |
| **NIST SP 800-82** | NIST | Guide to Industrial Internet of Things (IIoT) and ICS Security | Primarily US, global influence |
| **NIST CSF** | NIST | Cybersecurity Framework | Global, all sectors |
| **NIS2 Directive** | EU | Network and Information Security Directive | EU critical infrastructure |
| **NERC CIP** | NERC | Critical Infrastructure Protection | North American power grid |
| **IEC 61508** | IEC | Functional Safety of Electrical/Electronic/Programmable Electronic Safety-related Systems | Global, all safety-critical systems |
| **IEC 61511** | IEC | Functional Safety - Safety Instrumented Systems for the Process Industry Sector | Global, process industries |
| **ISO 27001** | ISO | Information Security Management | Global, all sectors |

**IEC 62443 Series Structure**:
- **IEC 62443-1-x**: General (terminology, concepts, metrics)
  - 1-1: Terminology, concepts, and models
  - 1-2: Master glossary of terms, definitions, and abbreviations
  - 1-3: System security conformance metrics
  - 1-4: Security program life cycle requirements and guidance

- **IEC 62443-2-x**: Policies and Procedures (for integrators)
  - 2-1: Security program requirements for IACS service providers

- **IEC 62443-3-x**: System (for end users/integrators)
  - 3-1: Security technologies for industrial automation and control systems
  - 3-2: Risk assessment for system design
  - 3-3: System security requirements and security levels

- **IEC 62443-4-x**: Component (for vendors)
  - 4-1: Secure product development lifecycle requirements
  - 4-2: Technical security requirements for IACS components

**Security Levels (SL)**: In IEC 62443, **four levels** of security capability:
- **SL 1**: Protection against casual or coincidental violation
- **SL 2**: Protection against intentional violation using simple means with low resources, generic skills and low motivation
- **SL 3**: Protection against intentional violation using sophisticated means with moderate resources, IACS specific skills and moderate motivation
- **SL 4**: Protection against intentional violation using sophisticated means with extended resources, IACS specific skills and high motivation

### 9. OT Risk Management

**Risk**: **Combination of the likelihood** of an event and its **consequence**.

**OT-Specific Risk Categories**:
- **Safety Risk**: Risk to personnel or public safety
- **Equipment Risk**: Risk of damage to equipment or facilities
- **Production Risk**: Risk of production loss or downtime
- **Financial Risk**: Financial impact of incidents
- **Reputation Risk**: Damage to organizational reputation
- **Environmental Risk**: Risk of environmental damage
- **Legal/Regulatory Risk**: Risk of legal action or regulatory fines

**Risk Assessment**: **Process of identifying, analyzing, and evaluating risk**.

**OT Risk Assessment Steps**:
1. **System Characterization**: Define the OT system and its boundaries
2. **Threat Identification**: Identify potential threats to the system
3. **Vulnerability Identification**: Identify vulnerabilities that could be exploited
4. **Control Identification**: Identify existing security controls
5. **Likelihood Determination**: Assess the likelihood of threats exploiting vulnerabilities
6. **Impact Analysis**: Determine the impact if threats successfully exploit vulnerabilities
7. **Risk Determination**: Combine likelihood and impact to determine risk level
8. **Control Recommendation**: Recommend controls to reduce risk
9. **Risk Acceptance**: Document risk acceptance decisions

**Risk Matrix**:

| Likelihood \ Impact | Low | Medium | High | Critical |
|----------------------|-----|--------|------|----------|
| **Very Low** | Acceptable | Acceptable | Tolerable | Tolerable |
| **Low** | Acceptable | Acceptable | Tolerable | **Unacceptable** |
| **Medium** | Acceptable | Tolerable | **Unacceptable** | **Unacceptable** |
| **High** | Tolerable | **Unacceptable** | **Unacceptable** | **Unacceptable** |
| **Very High** | Tolerable | **Unacceptable** | **Unacceptable** | **Unacceptable** |

**Example**: Refrigeration system attack risk:
- **Likelihood**: High (known vulnerabilities, internet-exposed systems)
- **Impact**: Critical (safety, production, financial, reputation)
- **Risk Level**: **Unacceptable** (required immediate action)

### 10. OT Metrics and Measurement

**Security Metric**: **Quantifiable measure** of security or the **effectiveness of security controls**.

**OT-Specific Metrics**:

**Security Posture Metrics**:
- **Patch Compliance**: Percentage of systems with current patches (%)
- **Vulnerability Count**: Number of known vulnerabilities in environment
- **Vulnerability Severity**: Severity distribution of vulnerabilities (Critical/High/Medium/Low)
- **Security Control Coverage**: Percentage of systems with required security controls (%)
- **Compliance Score**: Compliance with applicable standards (0-100%)

**Incident Metrics**:
- **Mean Time to Detect (MTTD)**: Average time to detect incidents (hours/minutes)
- **Mean Time to Respond (MTTR)**: Average time to respond to incidents (hours/minutes)
- **Mean Time to Contain (MTTC)**: Average time to contain incidents (hours/minutes)
- **Mean Time to Eradicate (MTTE)**: Average time to eradicate threats (hours/days)
- **Mean Time to Recover (MTTR)**: Average time to recover from incidents (hours/days)
- **Incident Count**: Number of security incidents (per time period)
- **Incident Severity**: Severity distribution of incidents (Critical/High/Medium/Low)

**Operations Metrics**:
- **System Uptime**: Percentage of time systems are operational (target: >99.9%)
- **Unplanned Downtime**: Time systems are down due to unplanned events (hours/year)
- **Planned Downtime**: Time systems are down for planned maintenance (hours/year)
- **Performance**: System performance metrics (throughput, latency, etc.)

**Safety Metrics**:
- **Safety Incident Count**: Number of safety incidents (target: 0)
- **Near Miss Count**: Number of near-miss safety events
- **Safety Violation Count**: Number of safety violations
- **Safety Training Completion**: Percentage of personnel with current safety training (%)

**Example**: Refrigeration system attack metrics:
- **MTTD**: 1.5 hours (from first anomaly to incident declaration)
- **MTTC**: 4 hours (from incident declaration to containment)
- **MTTE**: 12 hours (from containment to eradication)
- **MTTR**: 6.5 hours (from start of recovery to full operation)
- **System Uptime**: 99.8% (18 hours of downtime)
- **Financial Impact**: Significant

## Common OT Security Terms and Definitions

### A
- **Access Control**: Process for **controlling who or what can access resources** in an OT system.
- **Asset**: Any **data, device, or other component** of the environment that **supports information-related activities**.
- **Authentication**: Process of **verifying the claimed identity** of a user, device, or other entity.
- **Authorization**: Process of **determining what a subject is allowed to do**.
- **Availability**: **Property** of a system being **accessible and usable** upon demand by an authorized entity.

### B
- **Backup**: **Copy of data or configuration** made for the purpose of **recovery**.

### C
- **Conduit**: **Secure communication pathway** between zones in a network architecture.
- **Confidentiality**: **Property** that information is **not made available or disclosed** to unauthorized individuals, entities, or processes.
- **Control System**: **System** that **monitors and controls** industrial processes.

### D
- **Defense-in-Depth**: **Layered security approach** with **multiple independent security controls**.
- **DMZ (Demilitarized Zone)**: **Network segment** that acts as a **buffer** between trusted and untrusted networks.

### E
- **Endpoint**: **Device** that **connects to a network** and can be a **source or destination** of network traffic.

### F
- **Fieldbus**: **Industrial network protocol** used for **real-time, distributed control** in industrial environments.
- **Firewall**: **Network security device** that **filters traffic** between network segments based on **security rules**.

### I
- **ICS (Industrial Control System)**: General term for **supervisory control and data acquisition (SCADA) systems, distributed control systems (DCS), and other **control system configurations**.
- **Integrity**: **Property** of **safeguarding the accuracy and completeness** of assets.
- **Intrusion Detection System (IDS)**: **Device or application** that **monitors network traffic** for **suspicious activity** and policy violations.
- **Intrusion Prevention System (IPS)**: **Device or application** that **monitors network traffic** and **takes action** to prevent detected threats.

### M
- **Monitoring**: **Continuous observation** of systems, networks, or activities to **detect issues** or **gather information**.

### N
- **Network Segmentation**: **Division of a network** into **smaller, isolated segments** to **limit the spread of attacks** and **improve performance**.

### O
- **OT (Operational Technology)**: **Hardware and software** that **detects or causes a change** through the direct monitoring and/or control of **physical devices, processes, and events**.

### P
- **PLC (Programmable Logic Controller)**: **Industrial digital computer** used for **automation of industrial processes**.
- **Protocol**: **Set of rules** that define how **data is transmitted** between devices.

### R
- **Risk**: **Combination of the likelihood** of an event and its **consequence**.
- **RTU (Remote Terminal Unit)**: Device that **interfaces objects in the physical world** to a distributed control system or SCADA system.

### S
- **Safety**: **Condition** of being **protected from or unlikely to cause danger, risk, or injury**.
- **SCADA (Supervisory Control and Data Acquisition)**: System for **remote monitoring and control** of industrial processes.
- **Security**: **Protection** of **assets** from **threats** to achieve **desired levels of risk**.
- **Security Control**: **Safeguard or countermeasure** to **avoid, counteract, or minimize security risks**.
- **SIS (Safety Instrumented System)**: System designed to **perform safety instrumented functions** to **prevent or mitigate hazardous events**.

### T
- **Threat**: **Potential for a person or thing** to **exploit a vulnerability** to cause **harm** to an asset.
- **Threat Actor**: **Individual or group** that **poses a threat** to an asset.

### V
- **Vulnerability**: **Weakness** in an asset or control that could be **exploited by a threat**.

### Z
- **Zone**: **Grouping of OT assets** with **similar security requirements**.
- **Zero Trust**: Security model that **eliminates the notion of trust** and **verifies every request** as if it originates from an **open network**.

## Lessons from Refrigeration System Attack for OT Terminology

**Key Terminology Gaps Identified**:
1. **Lack of OT-Specific Terms**: IT teams didn't understand OT-specific concepts like "defrost cycle" or "setpoint"
2. **Different Priorities**: IT focused on data protection, OT focused on equipment safety and availability
3. **Communication Barriers**: Different terminology for similar concepts (IT: "server", OT: "controller")
4. **Impact Misunderstanding**: IT didn't fully appreciate the physical impact of cyber incidents on OT systems

**Terminology Improvements Needed**:
1. **Develop Glossary**: Create comprehensive OT security glossary
2. **Cross-Training**: Train IT personnel on OT concepts and terminology
3. **Joint Exercises**: Conduct exercises to improve communication between IT and OT
4. **Standardized Reporting**: Use consistent terminology in incident reports and communications
5. **Vendor Coordination**: Ensure vendors use consistent terminology in documentation and communications

## Standing Rules for OT Security Communication

1. **Use Standard Terminology**: Always use the defined terminology from this dialect
2. **Define Acronyms**: Always define acronyms on first use in documents and presentations
3. **Explain OT Concepts**: When communicating with non-OT audiences, explain OT-specific concepts
4. **Prioritize Clarity**: Clear communication is more important than technical precision
5. **Avoid Jargon**: Minimize use of jargon when communicating with non-technical stakeholders
6. **Tailor Communication**: Adjust terminology and detail level based on audience
7. **Document Assumptions**: Clearly state any assumptions or definitions used
8. **Consistent Reporting**: Use consistent terminology across all reports and documents
9. **Vendor Coordination**: Ensure consistent terminology with vendors and partners
10. **Continuous Improvement**: Regularly update and improve the dialect based on feedback

## Validation Checkpoints

### Before Communication
- [ ] Terminology is consistent with this dialect
- [ ] Acronyms are defined on first use
- [ ] OT-specific concepts are explained for non-OT audiences
- [ ] Communication is tailored to audience
- [ ] Assumptions are documented

### During Communication
- [ ] Standard terminology is used consistently
- [ ] Jargon is minimized
- [ ] Concepts are explained clearly
- [ ] Questions are answered accurately
- [ ] Feedback is solicited and incorporated

### After Communication
- [ ] Effectiveness is evaluated
- [ ] Feedback is collected
- [ ] Lessons learned are documented
- [ ] Dialect is updated as needed

## Verbosity

verbosity: V2
