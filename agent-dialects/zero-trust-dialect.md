---
name: zero-trust-dialect
domain: dialects
description: Dialect for Zero Trust Architecture (ZTA) terminology, principles, and implementation patterns specifically for Operational Technology and Industrial Control Systems environments
---

# Zero Trust Architecture Dialect for OT/ICS

**Purpose**: Provide **Operational Technology (OT) and Industrial Control Systems (ICS) specific Zero Trust terminology, principles, and implementation patterns**. This dialect enables organizations to **apply Zero Trust principles to industrial environments** where traditional IT approaches don't work due to safety-critical operations, legacy systems, and unique industrial protocols.

**Motivation**: The October 2026 cyberattack on refrigeration systems demonstrated that OT environments are **increasingly connected to IT networks** and **vulnerable to cyber threats**. Traditional perimeter-based security is insufficient for OT, which requires a **safety-first, availability-focused** approach. Zero Trust provides a framework to **secure OT systems without compromising safety or operations**.

## Dialect Overview

Zero Trust in OT must **balance security with safety and availability**. Unlike IT, where we can afford some downtime, OT systems control physical processes where **disruption can cause safety incidents, equipment damage, or production loss**.

### Core Zero Trust Principles for OT

1. **Explicit Verification**: Authenticate and authorize **every** access request to OT systems
2. **Least Privilege**: Grant **minimal** access required for OT operations
3. **Assume Breach**: Design OT systems assuming the network is **already compromised**
4. **Safety First**: Security must **never compromise safety**
5. **Availability Focus**: Security controls must **not disrupt operations**

### The Fundamental Difference: IT vs. OT Zero Trust

| Aspect | IT Zero Trust | OT Zero Trust |
|--------|---------------|---------------|
| **Primary Goal** | Data protection | **Safety + availability + security** |
| **Disruption Tolerance** | Can afford some downtime | **Zero disruption tolerance** for critical systems |
| **Device Types** | Servers, workstations, mobile | **PLCs, RTUs, sensors, HMIs, drives, controllers** |
| **Authentication** | Users with MFA | **Devices, non-human identities, legacy systems** |
| **Network Protocols** | TCP/IP, HTTP, DNS | **Modbus, DNP3, OPC UA, Profibus, BACnet, EtherNet/IP** |
| **Lifespan** | 3-5 years | **10-30+ years** |
| **Failure Impact** | Data loss, financial impact | **Physical harm, environmental damage, production loss** |

**Key Insight**: In OT, **"Never Trust, Always Verify"** must be balanced with **"Never Disrupt, Always Operate"**.

## OT-Specific Zero Trust Terminology

### OT Identity & Authentication

| Term | Definition | OT-Specific Example |
|------|------------|---------------------|
| **Device Identity** | Verifiable identity for OT devices | PLC, RTU, HMI, sensor certificates |
| **Non-Human Identity** | Identity for non-user entities | Device certificates, pre-shared keys, hardware tokens |
| **Legacy Identity** | Identity strategies for non-modernizable devices | Physical isolation, network-based authentication |
| **Protocol-Aware Authentication** | Authentication that understands industrial protocols | Modbus authentication, DNP3 secure authentication |
| **Break-Glass Authentication** | Emergency override procedures | Manual switches, hardware tokens for emergencies |
| **Continuous Device Verification** | Verify device identity without disrupting operations | Passive monitoring, heartbeat messages |

### OT Network Security

| Term | Definition | OT-Specific Example |
|------|------------|---------------------|
| **OT Micro-Segmentation** | Segmentation based on OT zones and conduits | IEC 62443 zones/conduits, Purdue Model levels |
| **Protocol Filtering** | Allow only specific industrial protocol functions | Modbus function code filtering, OPC UA security policies |
| **Industrial Firewall** | Firewall that understands industrial protocols | Tofino, Nozomi, Fortinet OT firewalls |
| **Conduit** | Secure communication path between zones | IEC 62443 conduit, secure tunnels |
| **Zone** | Group of OT assets with similar security requirements | IEC 62443 zone, Purdue Model level |
| **IT/OT Convergence Zone** | Special zone for IT/OT integration | Demilitarized zone (DMZ) for OT, convergence firewalls |

### OT Device Security

| Term | Definition | OT-Specific Example |
|------|------------|---------------------|
| **Secure Boot** | Verify firmware integrity at device startup | PLC secure boot, RTU firmware verification |
| **Firmware Integrity** | Ensure firmware has not been tampered with | Cryptographic hash verification, digital signatures |
| **Configuration Control** | Prevent unauthorized modifications to device configuration | Write protection, configuration locking, change approval |
| **Safety Instrumented System (SIS)** | System designed to prevent hazardous events | Emergency shutdown systems, safety PLCs |
| **OT Hardening** | Reduce attack surface of OT devices | Disable unused ports/services, change default passwords |
| **Device Posture** | Security state of an OT device | Patch level, security features enabled, network configuration |

### OT Application Security

| Term | Definition | OT-Specific Example |
|------|------------|---------------------|
| **Secure Industrial Protocol** | Industrial protocol with built-in security | OPC UA with security, secure Modbus variants, DNP3 Secure Authentication |
| **Protocol Gateway** | Device that adds security to insecure protocols | Modbus to TLS gateway, DNP3 to IPsec gateway |
| **OT Application Whitelisting** | Only allow approved OT software to run | PLC firmware whitelisting, HMI application control |
| **Least Privilege Access** | Grant minimal access for OT applications | Read-only vs. read-write access, function-specific access |
| **Input Validation** | Prevent protocol injection attacks | Validate Modbus function codes, check OPC UA data types |

### OT Data Security

| Term | Definition | OT-Specific Example |
|------|------------|---------------------|
| **OT Data Classification** | Categorize OT data by sensitivity and criticality | Process variables, configuration data, historical data |
| **Process Variable Encryption** | Encrypt real-time process data | Encrypted Modbus messages, secure OPC UA communication |
| **Configuration Data Protection** | Protect OT device configurations | Encrypted configuration files, secure backup procedures |
| **Historical Data Protection** | Protect stored OT data | Encrypted historians, secure database storage |
| **OT Integrity Monitoring** | Detect unauthorized changes to OT data | Configuration change detection, firmware hash verification |

### OT Monitoring & Verification

| Term | Definition | OT-Specific Example |
|------|------------|---------------------|
| **OT Asset Inventory** | Complete list of all OT devices and their connections | PLC inventory, HMI inventory, network device inventory |
| **Industrial Protocol Monitoring** | Monitor and analyze industrial protocol traffic | Modbus traffic analysis, DNP3 message monitoring |
| **Process Variable Monitoring** | Monitor real-time process variables for anomalies | Temperature monitoring, pressure monitoring, flow monitoring |
| **Device Behavior Baselines** | Understand normal OT device behavior | Communication patterns, protocol usage, timing patterns |
| **OT Anomaly Detection** | Detect unusual OT patterns and potential attacks | Unexpected protocol messages, abnormal timing, unusual access |
| **Safety Monitoring** | Monitor safety-critical systems and events | SIS status, emergency shutdown events, safety alarms |

## OT Zero Trust Implementation Patterns

### Pattern 1: OT-Specific Identity

**Challenge**: Many OT devices (PLCs, RTUs, sensors from 1990s-2000s) have **no authentication capabilities**

**Solution**: Implement **compensating controls** for legacy devices

```
┌─────────────────────────────────────────────────────────────┐
│                    LEGACY DEVICE ACCESS                         │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐                                         │
│  │   Legacy Device   │  (No authentication capability)         │
│  │   (e.g., 1995 PLC)│                                         │
│  └────────┬────────┘                                         │
│           │                                                   │
│           ▼                                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              NETWORK-BASED AUTHENTICATION                   │ │
│  │  • Authenticate at the network level (firewall, gateway)   │ │
│  │  • Place device in dedicated, restricted zone              │ │
│  │  • Allow only specific communication patterns               │ │
│  │  • Enhanced monitoring for anomaly detection                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

**Implementation**:
- Place legacy devices in **Level 1 zone** (Basic Control)
- Allow only communication from **Level 2** (Supervisory Control) on specific ports/protocols
- Implement **deep packet inspection** for industrial protocols
- Deploy **anomaly detection** for unusual protocol usage

### Pattern 2: Non-Human Identity Management

**Challenge**: OT systems have **many non-human identities** that can't use traditional MFA

**Solution**: Implement **device identity strategies**

```
┌─────────────────────────────────────────────────────────────┐
│                    DEVICE IDENTITY TYPES                         │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Device           │  │  Pre-Shared       │  │  Hardware         │  │
│  │  Certificates     │  │  Keys            │  │  Tokens          │  │
│  │                  │  │                  │  │  (YubiKey, TPM)   │  │
│  │  • X.509 certs    │  │  • Symmetric     │  │  • Physical      │  │
│  │  • Issued by CA    │  │  • Device-to-    │  │  • Tamper-       │  │
│  │  • Automatic       │  │    device        │  │    resistant     │  │
│  │    rotation        │  │  • Manual        │  │  • For critical   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │  Behavioral       │  │  Network         │                      │
│  │  Identity         │  │  Location        │                      │
│  │                  │  │                  │                      │
│  │  • Communication  │  │  • IP/MAC        │                      │
│  │    patterns       │  │    addresses     │                      │
│  │  • Protocol usage  │  │  • Physical      │                      │
│  │  • Timing patterns │  │    location      │                      │
│  └─────────────────┘  └─────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

**Implementation**:
- Deploy **OT-specific Certificate Authority (CA)** for device certificates
- Implement **automated certificate rotation** (challenging for OT)
- Provide **immediate revocation** for compromised device certificates
- Use **behavioral identity** as a supplement to cryptographic identity

### Pattern 3: Industrial Protocol Security

**Challenge**: Industrial protocols (Modbus, DNP3, Profibus) were **designed without security**

**Solutions**:

```
┌─────────────────────────────────────────────────────────────┐
│                    PROTOCOL SECURITY STRATEGIES                  │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  Strategy 1: PROTOCOL TUNNELING                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Insecure Protocol → [TLS/IPsec Tunnel] → Secure Channel    │ │
│  │  (e.g., Modbus TCP)    Gateway/Proxy                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Strategy 2: PROTOCOL GATEWAY                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Insecure Protocol → [Protocol Gateway] → Secure Protocol   │ │
│  │  (e.g., Modbus)      (Adds auth/encryption)   (e.g., TLS)   │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Strategy 3: PROTOCOL FILTERING                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  [Firewall] → Allow only authorized protocol functions     │ │
│  │  (e.g., Modbus function codes 1, 2, 3, 4)                  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Strategy 4: PROTOCOL UPGRADES                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Migrate from insecure to secure protocols                  │ │
│  │  Modbus → OPC UA with security                               │ │
│  │  DNP3 → DNP3 Secure Authentication                          │ │
│  │  Profibus → PROFINET with security                           │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

**Implementation**:
- Tunnel **Modbus TCP through TLS** using a protocol gateway
- Add **authentication and encryption** without modifying the PLC
- Filter **Modbus function codes** to allow only authorized operations
- Migrate to **OPC UA with security** for new installations

### Pattern 4: OT Micro-Segmentation

**Challenge**: OT systems require **safety and availability** while preventing lateral movement

**Solution**: **IEC 62443-based segmentation**

```
┌─────────────────────────────────────────────────────────────┐
│                    IEC 62443 ZONES & CONDUITS                   │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    LEVEL 0: PROCESS                           │ │
│  │  • Physical process (tanks, pumps, conveyors)               │ │
│  │  • Basic sensors, actuators                                  │ │
│  │  • Zone: Basic Process Control                               │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                              │                                      │
│                              │ Conduit (Secure communication)     │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    LEVEL 1: BASIC CONTROL                    │ │
│  │  • PLCs, RTUs, basic HMIs                                    │ │
│  │  • Local control loops                                      │ │
│  │  • Zone: Basic Control                                        │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                              │                                      │
│                              │ Conduit                            │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    LEVEL 2: SUPERVISORY CONTROL              │ │
│  │  • SCADA, advanced HMIs, historians                         │ │
│  │  • Monitoring and supervisory control                       │ │
│  │  • Zone: Supervisory Control                                  │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                              │                                      │
│                              │ Conduit                            │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    LEVEL 3: SITE OPERATIONS                  │ │
│  │  • Site-level operations, local databases                   │ │
│  │  • Manufacturing execution systems (MES)                    │ │
│  │  • Zone: Site Operations                                     │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                              │                                      │
│                              │ Conduit                            │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    LEVEL 4: SITE BUSINESS                    │ │
│  │  • ERP, business systems, reporting                           │ │
│  │  • Zone: Site Business                                        │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                              │                                      │
│                              │ Conduit                            │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    LEVEL 5: ENTERPRISE                       │ │
│  │  • Corporate IT, enterprise applications                       │ │
│  │  • Zone: Enterprise                                          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

**Implementation**:
- **Conduits** are **secure communication paths** between zones
- Each conduit has **firewalls, IDS/IPS, and protocol filtering**
- **Zones** group assets with **similar security requirements**
- **IT/OT Convergence** happens at **Level 3.5** (special convergence zone)

### Pattern 5: IT/OT Convergence Security

**Challenge**: Traditional IT Zero Trust **disrupts OT operations** when applied directly

**Solution**: **Adapted Zero Trust for convergence**

```
┌─────────────────────────────────────────────────────────────┐
│                    IT/OT CONVERGENCE                            │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐      ┌─────────────────────┐         │
│  │       IT ZONE        │      │       OT ZONE        │         │
│  │  • Enterprise apps    │      │  • OT systems        │         │
│  │  • Databases          │      │  • PLCs, SCADA        │         │
│  │  • Users              │      │  • HMIs, historians   │         │
│  └──────────┬───────────┘      └──────────┬───────────┘         │
│             │                               │                     │
│             └───────────────────┼───────────────────┘         │
│                                 │                                 │
│                 ┌───────────────────▼───────────────────┐        │
│                 │      CONVERGENCE ZONE (Level 3.5)          │        │
│                 │  • Translation gateways                      │        │
│                 │  • Protocol conversion                       │        │
│                 │  • Identity mapping (IT ↔ OT)               │        │
│                 │  • Enhanced monitoring                       │        │
│                 │  • Specialized firewalls                     │        │
│                 └───────────────────┬───────────────────┘        │
│                                            │                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    ZERO TRUST CONTROLS                      │  │
│  │  • Identity verification for all access                   │  │
│  │  • Policy-based access decisions                           │  │
│  │  • Continuous monitoring                                     │  │
│  │  • Anomaly detection                                         │  │
│  │  • Automated response (safe for OT)                         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

**Implementation**:
- **Translation Gateways**: Convert between IT and OT security models
- **Protocol Conversion**: Securely bridge IT and OT protocols
- **Identity Mapping**: Map IT identities to OT device identities
- **Safety-Aware Policies**: Ensure Zero Trust doesn't compromise safety

## OT Zero Trust Architecture Framework

### 7 Pillars of OT Zero Trust (Adapted from NIST SP 800-207)

```
┌─────────────────────────────────────────────────────────────┐
│                    OT ZERO TRUST ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│  PILLAR 1: IDENTITY                                              │
│  ├── Device Identity: Every OT device has verifiable identity    │
│  ├── Non-Human Identity: PLCs, RTUs, sensors, actuators         │
│  ├── Legacy Identity: Strategies for non-modernizable devices   │
│  └── Continuous Authentication: Verify without disruption        │
├─────────────────────────────────────────────────────────────┤
│  PILLAR 2: NETWORK                                              │
│  ├── Micro-Segmentation: IEC 62443 zones/conduits              │
│  ├── Protocol-Aware Filtering: Understand industrial protocols   │
│  ├── East-West Traffic: Secure communication between OT devices│
│  └── North-South Traffic: Secure IT/OT boundary                  │
├─────────────────────────────────────────────────────────────┤
│  PILLAR 3: DEVICE                                              │
│  ├── Secure Boot: Verify firmware integrity                     │
│  ├── Hardening: Disable unused services/ports                   │
│  ├── Integrity Monitoring: Detect unauthorized changes          │
│  └── Configuration Control: Prevent unauthorized modifications   │
├─────────────────────────────────────────────────────────────┤
│  PILLAR 4: APPLICATION                                          │
│  ├── Least Privilege: Minimal access for OT applications        │
│  ├── Secure Protocols: OPC UA with TLS, secure Modbus variants   │
│  ├── Input Validation: Prevent protocol injection attacks        │
│  └── Application Whitelisting: Only approved OT software runs     │
├─────────────────────────────────────────────────────────────┤
│  PILLAR 5: DATA                                                 │
│  ├── Encryption in Transit: Secure industrial protocols          │
│  ├── Encryption at Rest: Protect OT configurations/data         │
│  ├── Data Classification: Identify critical OT data              │
│  └── Integrity: Ensure data accuracy for process control          │
├─────────────────────────────────────────────────────────────┤
│  PILLAR 6: VISIBILITY & ANALYTICS                               │
│  ├── Asset Inventory: Know all OT devices and connections        │
│  ├── Network Traffic Monitoring: Understand industrial protocols │
│  ├── Anomaly Detection: Identify unusual OT patterns            │
│  └── Behavioral Baselines: Understand normal OT operations       │
├─────────────────────────────────────────────────────────────┤
│  PILLAR 7: AUTOMATION & ORCHESTRATION                           │
│  ├── Automated Response: Safe, measured responses to threats    │
│  ├── Orchestrated Changes: Controlled configuration updates     │
│  ├── Policy Enforcement: Automated compliance checking          │
│  └── Integration: Work with existing OT systems                 │
└─────────────────────────────────────────────────────────────┘
```

## Lessons from Real-World OT Zero Trust Implementations

### Lessons from the October 2026 Cyberattack

**Problem**: Internet-exposed controllers with no authentication

**Zero Trust Solution**:
- **Network isolation** (Zero Trust network segmentation)
- **Device authentication** (certificate-based for refrigeration controllers)
- **Continuous monitoring** (anomaly detection for temperature and other process variables)
- **Least privilege access** (role-based controller access)

**Key Takeaway**: Even basic Zero Trust controls can **prevent catastrophic incidents** in OT environments.

### Lessons from Schneider Electric (2023)

**Problem**: Safety Instrumented Systems (SIS) compromised

**Zero Trust Solution**:
- **Separate safety and control networks** (micro-segmentation)
- **Device identity for SIS components** (hardware tokens)
- **Continuous verification without disruption** (passive monitoring)
- **Break-glass procedures** for emergencies

### Lessons from Siemens (2022)

**Problem**: PLCs with insecure protocols (S7comm without security)

**Zero Trust Solution**:
- **Protocol gateways** (add authentication to S7comm)
- **Micro-segmentation** between PLCs and enterprise
- **Device authentication** for SIMATIC controllers
- **Continuous protocol monitoring**

### Lessons from Emerson (2021)

**Problem**: Supply chain attack via compromised firmware

**Zero Trust Solution**:
- **Secure boot** for compressors
- **Firmware integrity verification**
- **Vendor certificate validation**
- **Supply chain security requirements**

### Lessons from Honeywell (2020)

**Problem**: Building Management Systems with web interface vulnerabilities

**Zero Trust Solution**:
- **Web interface hardening** (disable HTTP, enforce HTTPS)
- **Device authentication** for BMS components
- **Network segmentation** between BMS and enterprise
- **Continuous monitoring** of BACnet traffic

## Standing Rules for OT Zero Trust

1. **Safety First**: Zero Trust implementation must **never compromise safety**
2. **Availability Second**: Zero Trust must **maintain OT system availability**
3. **Gradual Implementation**: Phase Zero Trust to **minimize disruption**
4. **OT-Specific Adaptation**: Adapt IT Zero Trust principles for **OT constraints**
5. **Continuous Verification**: Verify **without disrupting operations**
6. **Defense in Depth**: Combine Zero Trust with **traditional OT security**
7. **Vendor Coordination**: Work with **vendors on Zero Trust-capable products**
8. **Monitoring First**: Deploy **monitoring before enforcement**
9. **Break-Glass Procedures**: Always have **manual overrides for safety**
10. **Regular Audits**: Continuously **validate Zero Trust implementation**

## Integration with Other Dialects

This dialect **integrates with and extends**:
- **ot-security-dialect**: General OT security terminology
- **iec-62443-dialect**: IEC 62443 standards implementation
- **general-zero-trust-dialect**: Cross-domain Zero Trust principles

## Verbosity

verbosity: V2
