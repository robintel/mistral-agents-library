# Dixell Security Guidance - For Immediate Action

**Date**: October 13, 2026  
**Prepared by**: Mistral Agents Library  
**For**: Dixell, Copeland, and Organizations Using Dixell Equipment  
**Contact**: This document can be shared freely to help organizations secure their Dixell systems

---

## Executive Summary

On October 11-13, 2026, **Dixell XWEB refrigeration controllers were compromised** in a coordinated cyberattack affecting hundreds of French supermarkets (at least 350 per Reuters, with some reports of up to ~700). French cybersecurity agency **ANSSI** issued advisory **CERTFR-2026-ALE-012** (12 October, updated 13 October to add Copeland and Dixell xweb controllers) alongside Danfoss AK-SM/AK-SC systems.

**Impact**: 
- Massive food spoilage (temperatures raised to 50°C)
- Equipment damage from overheating
- Extended defrost cycles (8+ hours) delaying alarms
- €10+ million in losses across affected chains

**This document** provides immediate, actionable guidance based on lessons learned from the attack and proven security patterns for Dixell systems.

---

## Quick Start - Critical Actions (Next 24 Hours)

### 🚨 IMMEDIATE - Do These NOW

1. **DISCONNECT XWEB FROM INTERNET**
   - Scan for internet-exposed XWEB controllers (Shodan: `"XWEB"`, `"Dixell"`)
   - Remove all XWEB systems from direct internet access
   - Use VPN or jump hosts for remote access ONLY

2. **CHANGE ALL DEFAULT PASSWORDS**
   - XWEB PRO, XWEB-500, all field controllers
   - XWEB Pro 1.12.1 and prior used a deterministic (predictable) password generation mechanism for admin credentials (CVE-2026-21718) - update to firmware 1.13 and change all passwords
   - Enforce 12+ character complex passwords
   - Disable default credentials entirely

3. **MONITOR FOR ATTACK INDICATORS**
   - Temperature > 5°C above setpoint
   - Defrost cycles > 2 hours (normal: 30-60 min)
   - Multiple units affected simultaneously
   - Unusual Modbus write operations

4. **ISOLATE REFRIGERATION NETWORKS**
   - Physically or logically separate from IT networks
   - Implement default-deny firewall rules
   - Restrict Modbus traffic to known controllers only

5. **CHECK AIRMODBUS WIRELESS** (if used)
   - Review wireless network security
   - Consider temporarily disabling wireless if not critical
   - Monitor for unusual wireless activity

---

## What We Know About the Attack

### Attack Timeline
- **Oct 11, overnight**: Attack begins, temperatures manipulated
- **Oct 11, early morning**: Staff discover uncontrollable refrigeration computers
- **Oct 12**: ANSSI (CERT-FR) publishes CERTFR-2026-ALE-012 confirming numerous compromises of Danfoss AK-SM and AK-SC controllers
- **Oct 13**: CERT-FR updates the alert to add Copeland xweb and Dixell xweb controllers; Dixell France begins distributing security advisories

### Attack Methods Used
1. **Authentication Bypass**: Attackers bypassed XWEB authentication
2. **Configuration Manipulation**: Remote modification of:
   - Temperature setpoints (set to 50°C)
   - Defrost cycle durations (extended to 8+ hours)
   - Alarm thresholds (delayed to hide attack)
3. **Default Credential Exploitation**: Some systems had default or weak passwords
4. **Predictable Credentials**: XWEB Pro 1.12.1 and prior used deterministic (predictable) admin password generation (CVE-2026-21718)

### Affected Products
- **XWEB PRO**: Supervision platform (XWEB300D/500D/1000D/5000 PRO); versions 1.12.1 and prior affected by 23 disclosed vulnerabilities (fixed in firmware 1.13)
- **XWEB-500**: Compact monitoring unit, unsupported since 2018 (known arbitrary file write vulnerability CVE-2021-45420, no firmware fix)
- **XR Series**: Field controllers (Universal-XR, IC100CX, etc.)
- **Prime CH**: Commercial refrigeration controllers
- **AirModbus**: Wireless communication modules

---

## Network Architecture - Secure Design

### Recommended Zone Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Business Zone      │    │ Supervisory Control  │    │  Refrigeration       │
│   (IT Systems)       │◄──►│   Zone (SCADA)       │◄──►│  Control Zone        │
│                     │    │                     │    │                     │
│ - ERP, Analytics     │    │ - XWEB PRO          │    │ - XR Series         │
│ - Business Systems   │    │ - HMI Workstations   │    │ - Field Controllers │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
     IT Firewall           OT Firewall                    Physical/Wireless
                                              (Tofino, Fortinet)
```

### Firewall Rules (Critical)
- **Business ↔ Supervisory**: Read-only data flow ONLY
- **Supervisory ↔ Refrigeration**: Restricted Modbus TCP, HTTP/HTTPS to XWEB
- **Refrigeration Zone**: NO internet access, NO wireless (if possible)
- **All Zones**: Default-deny, explicit allow with logging

### Modbus Security
- Filter Modbus write operations at firewall
- Restrict Modbus to known controller IPs
- Monitor for unusual Modbus traffic patterns
- Consider VPN for Modbus over IP

---

## Monitoring - Detect the Next Attack

### Critical Monitoring Rules (Implement Immediately)

This table is the **canonical DIX-### rule mapping** and matches `agent-dialects/dixell-security-dialect.md` exactly.

| Rule ID | Condition | Severity | Response |
|---------|-----------|----------|----------|
| **DIX-001** | Temperature > 10°C above setpoint | **CRITICAL** | Isolate zone, page on-call |
| **DIX-002** | Temperature > 5°C above setpoint | HIGH | Investigate within 30 min |
| **DIX-003** | Temp < -30°C | HIGH | Investigate, alert |
| **DIX-004** | Rapid temp change (>5°C/5min) | **CRITICAL** | Isolate, page on-call |
| **DIX-005** | Defrost cycle > 2 hours | HIGH | Investigate within 30 min |
| **DIX-006** | Defrost cycle > 4 hours | **CRITICAL** | Isolate zone, page on-call |
| **DIX-007** | Multiple units affected simultaneously | **CRITICAL** | Isolate zone, page on-call |
| **DIX-008** | Communication loss to XWEB | HIGH | Check connections, restart |
| **DIX-009** | Configuration change detected | HIGH | Verify change, revert if unauthorized |
| **DIX-010** | Authentication failure (3+ times) | MEDIUM | Investigate within 4 hours |
| **DIX-011** | Unusual Modbus write operations | HIGH | Investigate, block if malicious |
| **DIX-012** | Wireless signal interference (AirModbus) | MEDIUM | Check AirModbus network |

### What to Monitor
1. **Temperature**: All refrigeration units, real-time
2. **Defrost Cycles**: Duration and timing
3. **Modbus Traffic**: Write operations, unusual patterns
4. **Configuration Changes**: Any unauthorized modifications
5. **Authentication**: Failed login attempts, successful logins
6. **Network Traffic**: Connections to/from XWEB controllers
7. **Wireless**: AirModbus network health (if used)

---

## Incident Response - When Attacked

### Phase 1: Immediate Containment (0-4 hours)
1. **Safety First**: Ensure no risk to personnel or equipment
2. **Isolate Refrigeration Control Zone** from all networks
3. **Disable remote access** to XWEB supervisors
4. **Disable AirModbus wireless** (if used)
5. **Activate manual backup controls** if available
6. **Maintain temperature control** via local operation

### Phase 2: Investigation (1-12 hours)
1. Collect logs from XWEB PRO, XWEB-500, field controllers
2. Preserve Modbus traffic logs
3. Check AirModbus wireless logs (if applicable)
4. Identify attack vector and scope
5. Determine what was accessed/modified

### Phase 3: Eradication (4-24 hours)
1. Remove malicious configurations
2. Apply emergency firmware patches
3. Reset ALL passwords and credentials
4. Reconfigure AirModbus (if compromised)
5. Verify system integrity

### Phase 4: Recovery (12-48 hours)
1. Restore from clean backups
2. Reconnect systems gradually
3. Validate temperature control
4. Test wireless connectivity (if AirModbus)
5. Monitor for recurrence

---

## Product-Specific Guidance

### XWEB PRO / XWEB-500
- **Critical**: These were the primary attack targets
- **Action**: Disable web interface if not needed
- **Patch**: Replace or isolate XWEB-500 (no firmware fix available for CVE-2021-45420)
- **Access**: Restrict to specific IP ranges only
- **Monitor**: Enable all logging, review regularly

### XR Series Field Controllers
- **Network**: Use Modbus RTU (serial) instead of TCP when possible
- **Access**: Physical access control to controller locations
- **Security**: No direct internet access, only via XWEB
- **Monitor**: Temperature and configuration changes

### AirModbus Wireless
- **Risk**: Wireless introduces additional attack surface
- **Action**: Temporarily disable if not critical for operations
- **Security**: Use dedicated wireless spectrum, encrypt if possible
- **Monitor**: Wireless intrusion detection, signal strength

---

## Patch Management - Stay Ahead

### Immediate Actions
1. **Inventory**: List all Dixell controllers (model, firmware, location)
2. **Scan**: Check for vulnerabilities (XWEB-500 arbitrary file write, etc.)
3. **Prioritize**: Internet-exposed systems first, then critical locations

### Update Process
```
Phase 1: Test (3-5 days)
├── Test firmware in lab
├── Validate compatibility
└── Verify backup/restore

Phase 2: Pilot (1-2 weeks)
├── Update 5-10% of systems (least critical)
├── Monitor for issues
└── Test rollback

Phase 3: Production (2-4 weeks)
├── Batch updates (20% at a time)
├── Avoid peak operations (hot days, holidays)
└── Maintain rollback capability
```

### Critical Updates Needed
- **XWEB-500**: Replace or isolate (no firmware fix for CVE-2021-45420)
- **XWEB PRO**: Update to latest firmware with security fixes
- **All Systems**: Change default passwords, enable authentication

---

## Known Vulnerabilities & Mitigations

### CVE-2021-45420: XWEB-500 Arbitrary File Write
- **Risk**: Remote code execution via web interface
- **Exploit**: File upload to `logo_extra_upload.cgi`
- **Mitigation**: 
  - Replace or isolate XWEB-500 (no firmware fix available)
  - Disable web interface
  - Restrict web access
  - Implement input validation

### 2026 Attack: Authentication Bypass
- **Risk**: Unauthorized access to XWEB controllers
- **Exploit**: Default credentials, predictable credential generation (CVE-2026-21718 on XWEB Pro <=1.12.1)
- **Mitigation**:
  - Change ALL default passwords
  - Update XWEB Pro to firmware 1.13+ (CVE-2026-21718) and change all admin credentials
  - Enable strong authentication (12+ chars)
  - Implement RBAC

### 2026 Attack: Configuration Manipulation
- **Risk**: Temperature and defrost cycle modification
- **Exploit**: Remote Modbus writes, configuration changes
- **Mitigation**:
  - Restrict Modbus write operations
  - Implement configuration change detection
  - Enable logging of all changes
  - Regular configuration audits

---

## Security Checklist - Verify Your Defenses

### Network Security
- [ ] XWEB controllers NOT internet-accessible
- [ ] Network segmentation implemented (IEC 62443 zones)
- [ ] Firewall rules: default-deny, explicit allow
- [ ] Modbus traffic filtered at zone boundaries
- [ ] AirModbus wireless secured (if used)

### Access Control
- [ ] ALL default passwords changed
- [ ] Strong password policy (12+ chars, complexity)
- [ ] MFA enabled (if available)
- [ ] RBAC implemented (separate roles)
- [ ] Session timeout configured (15 min)
- [ ] Failed login lockout (5 attempts)
- [ ] Date-based auth disabled

### Monitoring
- [ ] Temperature monitoring: all units, real-time
- [ ] Defrost cycle monitoring
- [ ] Modbus traffic monitoring
- [ ] Configuration change detection
- [ ] Authentication monitoring
- [ ] Alerts configured for DIX-001 to DIX-012

### Patch Management
- [ ] Firmware inventory complete
- [ ] Vulnerability scanning implemented
- [ ] Patch testing process in place
- [ ] Staged rollout procedure documented
- [ ] Rollback procedures tested

### Incident Response
- [ ] Dixell-specific IR plan developed
- [ ] On-call personnel identified (OT + IT)
- [ ] Communication channels established
- [ ] Backup configurations created
- [ ] Isolation procedures tested

---

## Vendor Contacts & Resources

### Official Resources
- **Dixell France**: https://dixell.fr/?lang=en
- **Copeland Dixell Solutions**: https://www.copeland.com/en-us/brands/dixell
- **XWEB PRO Security Bulletin**: https://webapps.copeland.com/dixell/Content/Pages/SystemSoftwareUpdate/XWEB-PRO/Security%20update%20%20XWEB-PRO%20-%20Product_Bulletin_February_2026.pdf
- **CISA Advisory ICSA-26-057-10**: https://www.cisa.gov/news-events/ics-advisories/icsa-26-057-10 (Copeland XWEB/XWEB Pro, 23 vulnerabilities, fixed in firmware 1.13)
- **ANSSI Advisory**: CERTFR-2026-ALE-012 (check ANSSI website)

### Security Tools
- **Asset Discovery**: Shodan, Nozomi, Claroty, Tenable.ot
- **Vulnerability Scanning**: Nessus (OT plugins), Qualys
- **Network Monitoring**: Wireshark (Modbus dissectors)
- **OT IDS**: Nozomi Guardian, Claroty, Dragos Platform

---

## Long-Term Security Program

### Within 1 Month
1. Complete security assessment of all Dixell systems
2. Implement all critical monitoring rules (DIX-001 to DIX-012)
3. Change all passwords, implement RBAC
4. Network segmentation completed
5. Incident response plan tested

### Within 3 Months
1. All firmware updated to latest versions
2. Wireless network security validated (if AirModbus)
3. Regular vulnerability scanning implemented
4. Security training for all personnel
5. Documentation of all security controls

### Within 6 Months
1. Annual security assessment process established
2. Patch management process automated
3. Security metrics tracking implemented
4. Vendor coordination process established
5. Lessons learned from 2026 attack documented and addressed

---

## Key Lessons from October 2026 Attack

### What Went Wrong
1. **Internet Exposure**: XWEB controllers were accessible from the internet
2. **Outdated Firmware**: Known vulnerabilities were not patched
3. **Poor Segmentation**: OT and IT networks were not properly isolated
4. **Lack of Monitoring**: No detection of temperature or defrost anomalies
5. **Weak Access Controls**: Default passwords, predictable credential generation (CVE-2026-21718)
6. **Slow Response**: Detection and containment took hours

### What Worked
1. **Backup Systems**: Some stores had manual override capabilities
2. **Vendor Support**: Dixell/Copeland provided advisories quickly
3. **Cross-Team Coordination**: IT and OT worked together effectively

### Recommendations
1. **Never expose OT controllers to the internet** - This is the #1 lesson
2. **Implement network segmentation** following IEC 62443
3. **Deploy anomaly detection** for temperature, defrost, and Modbus
4. **Apply patches within 30 days**
5. **Implement strong authentication** (MFA, strong passwords, RBAC)
6. **Test incident response plans** regularly
7. **Conduct security assessments** annually
8. **Train personnel** on OT security awareness
9. **Monitor for authentication bypass** (CVE-2026-21718, CVE-2026-25085 on XWEB Pro <=1.12.1, fixed in 1.13)
10. **Secure wireless networks** (AirModbus)

---

## About This Guidance

This document was created by the **Mistral Agents Library** to help organizations using Dixell equipment secure their systems against cyberattacks. It is based on:

- Analysis of the October 2026 cyberattack on French supermarkets
- ANSSI advisory CERTFR-2026-ALE-012
- Known vulnerabilities in Dixell systems
- Proven security patterns for refrigeration control systems
- Best practices from IEC 62443 and other OT security standards

### Related Resources in Mistral Agents Library
- **dixell-security-dialect.md**: Comprehensive dialect for Dixell systems
- **danfoss-security-dialect.md**: Lessons from Danfoss (similar attack)
- **ot-security-dialect.md**: General OT security terminology
- **iec-62443-dialect.md**: IEC 62443 compliance guidance

### How to Use This Library
The Mistral Agents Library contains **dialects** that define domain-specific terminology and security patterns. These dialects can be:

1. **Loaded by agents** to provide context-specific knowledge
2. **Used as checklists** for security assessments
3. **Referenced during incidents** for rapid guidance
4. **Shared with vendors** to improve their security

---

**This document can be freely shared with Dixell, Copeland, and any organization using Dixell equipment.**

**For the full Dixell security dialect and other resources, see**: https://github.com/robintel/mistral-agents-library/tree/main/agent-dialects

---

*Document version 1.0 | October 13, 2026 | Mistral Agents Library*
