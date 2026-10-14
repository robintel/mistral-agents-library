---
name: ot-ics-emergency-response
domain: ot-security
description: Vendor-neutral emergency response procedures for OT/ICS cybersecurity incidents with case studies from multiple vendors
---

# OT/ICS Cybersecurity Emergency Response Guide

**Purpose**: Provide **immediate, actionable emergency response procedures** for cybersecurity incidents affecting **Operational Technology (OT) and Industrial Control Systems (ICS)** across all vendors. Distills lessons from real-world incidents: French supermarket refrigeration attacks (Danfoss/Copeland/Dixell, 2026), TRITON/TRISIS (2017), Stuxnet (2010), Oldsmar water treatment (2021).

**Audience**: OT engineers, IT security teams, plant operators, incident responders, management.

---

## 🚨 QUICK REFERENCE: CASE STUDIES

### Danfoss / Copeland / Dixell (Refrigeration) - October 2026
- **Impact**: 350+ supermarkets (Reuters; some reports up to ~700), losses in the tens of millions of euros, temperatures pushed to ~50°C; CERT-FR alert CERTFR-2026-ALE-012 (12 Oct, updated 13 Oct)
- **CVEs**: CVE-2025-41450 (Auth Bypass), CVE-2025-41451 (RCE), CVE-2025-41452 (Config); XWEB Pro: CVE-2026-25085, CVE-2026-21718, CVE-2026-24663 (fixed in firmware 1.13)
- **Lessons**: Never expose controllers to internet, patch within 30 days, deploy anomaly detection

### Schneider Triconex SIS (TRITON/TRISIS) - 2017
- **Impact**: Malware targeting a petrochemical plant's safety instrumented system; protective functions put at risk
- **Vector**: Compromised engineering workstation and supply-chain access to the SIS controller
- **Lessons**: Safety systems need SL4 security, separate safety/control networks, control access to engineering workstations

### Siemens S7 PLCs (Stuxnet) - 2010
- **Impact**: Centrifuge destruction at an uranium enrichment facility via manipulated PLC logic; espionage-grade supply chain operation
- **Vector**: Removable media propagation, stolen digital certificates, zero-day exploits, PLC logic modification
- **Lessons**: Network segmentation mandatory, removable media control, validate PLC logic integrity, deep protocol inspection

### Water Treatment (Oldsmar, FL) - 2021
- **Impact**: Attempted remote manipulation of chemical dosing (lye) via plant operator's remote-access software (TeamViewer)
- **Vector**: Exposed remote access with shared/weak credentials
- **Lessons**: MFA and per-user remote access accounts, monitor remote sessions, alert on setpoint/parameter changes

---

## 📞 INCIDENT TRIAGE

### Classification Matrix

| Severity | Indicators | Response Time | Team |
|----------|------------|---------------|------|
| **CRITICAL** | Safety hazard, multiple sites, production stop, equipment damage | **IMMEDIATE** (0-15 min) | Full IR team |
| **HIGH** | Single site, equipment at risk, >5°C deviation, process disruption | **URGENT** (0-30 min) | OT + IT teams |
| **MEDIUM** | Anomalies, config changes, failed logins, minor issues | **4 HOURS** | Investigate |
| **LOW** | Minor alerts, non-critical systems | **24 HOURS** | Document |

### Quick Questions
1. **Safety risk?** → CRITICAL if yes
2. **Multiple sites?** → CRITICAL if 2+
3. **Production stopped?** → CRITICAL if yes
4. **Equipment at risk?** → HIGH if yes

---

## 🔥 CRITICAL INCIDENT RESPONSE

### Phase 0: SAFETY FIRST (0-5 min)

```
SAFETY CHECKLIST:
├── FIRES/EXPLOSIONS: Evacuate, call emergency
├── CHEMICAL LEAKS: Evacuate, ventilate, call hazmat  
├── EQUIPMENT DAMAGE: Isolate power if safe
├── PERSONNEL INJURIES: Provide first aid, call medical
└── PROCESS SAFETY: Check for runaway reactions
```

**RULE**: LIFE SAFETY > CYBER SECURITY - Do NOT proceed if safety uncertain

### Phase 1: IMMEDIATE CONTAINMENT (0-15 min)

**Isolation Hierarchy:**
1. **Network**: Disable remote access, block internet, isolate zone
2. **Communication**: Disable wireless, VPN, block protocols
3. **Physical**: Unplug cables ONLY if network isolation impossible

**Commands:**
```bash
# Network isolation
iptables -A INPUT -s [affected-subnet] -j DROP
netsh advfirewall firewall add rule name="Block OT" dir=in action=block remoteip=[subnet]

# Check connections  
netstat -tulnp | grep -E "(80|443|502|102|47808)"
```

**Activate Backup Systems:**
- Hot standby controllers (if available)
- Local/auto mode operation
- Manual control procedures

**Notify:**
- Internal: OT Lead, IT Lead, Operations, Safety
- External: Vendor (if applicable), CERT, Law Enforcement

---

## 🔍 FORENSIC INVESTIGATION (1-4 hours)

### Evidence Collection (Universal)

**FROM CONTROLLERS:**
- Full memory dump
- Configuration files
- Log files (system, application, web)
- Firmware version and checksum
- Process data history
- Alarm/event logs
- User accounts

**FROM NETWORK:**
- Switch/firewall logs
- IDS/IPS alerts
- NetFlow data
- DHCP logs

**FROM MONITORING:**
- SIEM alerts
- OT-specific IDS alerts
- Process variable trends
- Screenshots

### Evidence Preservation

**DO NOT:**
- ❌ Reboot without imaging
- ❌ Patch without documenting
- ❌ Delete logs
- ❌ Modify configs without backup

**DO:**
- ✅ Create forensic images
- ✅ Collect all logs
- ✅ Document current state
- ✅ Preserve memory dumps

### Universal IOCs

**Network:**
- Unusual IPs, unexpected protocols, unauthorized ports
- PLC/RTU talking to internet

**Host:**
- Unauthorized config changes, suspicious files, new accounts
- Unexpected processes (nc, netcat, python, powershell)

**Behavior:**
- Process variables outside ranges
- Unexpected alarm patterns
- Unusual network traffic
- Unauthorized access attempts

---

## 🔧 ERADICATION (4-12 hours)

### Remove Attacker Access

```bash
# Change all passwords
passwd admin
passwd [other-users]

# Remove unauthorized accounts  
userdel [suspicious-users]

# Check for backdoors
find / -name "*.sh" -newer /config/last-update
find / -name "*.py" -newer /config/last-update
crontab -l
cat /root/.ssh/authorized_keys

# Check connections
netstat -tulnp | grep ESTABLISHED
lsof -i
```

### Patch Management

```
Phase 1: Lab Testing (1-2h)
├── Download patch from vendor
├── Verify checksum
└── Test in isolated environment

Phase 2: Pilot (2-4h)
├── Deploy to 1-2 least critical systems
└── Monitor for 1-2 hours

Phase 3: Production (4-8h)  
├── Update in batches (20% at a time)
└── Verify each batch
```

### Verify Integrity
- Firmware checksums match vendor
- Configurations match backups
- No unauthorized modifications
- All accounts authorized
- Network rules intact

---

## 🔄 RECOVERY (12-48 hours)

### Restore from Backups

**Decision:**
- Configurations corrupted? → Restore from backup
- Configurations clean? → No restoration needed

**Process:**
1. Verify backup integrity
2. Restore configuration
3. Test before production
4. Document all actions

### Gradual Reconnection

```
Step 1: Test in Isolation (1h)
└── Verify local operation

Step 2: Reconnect to Local Network (2h)  
└── Verify controller communication

Step 3: Reconnect to Supervisory (4h)
└── Verify SCADA/HMI connectivity

Step 4: Reconnect to Enterprise (8h)
└── Verify read-only data flow
```

### Validation Checklist

**Systems:**
- [ ] All controllers operational
- [ ] All HMIs/SCADA functional
- [ ] All monitoring receiving data
- [ ] All variables within ranges

**Security:**
- [ ] All vulnerabilities patched
- [ ] All malicious code removed
- [ ] All passwords changed
- [ ] Network segmentation intact

---

## 📊 MONITORING AND ANOMALY DETECTION

### Universal Anomaly Rules

| Category | Critical Threshold | High Threshold |
|----------|-------------------|----------------|
| **Temperature** | >10°C above setpoint | >5°C above setpoint |
| **Pressure** | >110% of normal | <90% of normal |
| **Flow** | >120% or <80% | Unexpected changes |
| **Level** | >100% or <10% | Rapid changes |
| **Electrical** | >120% current | <90% voltage |

### Vendor-Specific Rules

**Danfoss:** Temp >50°C = CRITICAL, Rapid change >5°C/5min = CRITICAL
**Schneider:** SIS trip without cause = CRITICAL, Multiple SIS affected = CRITICAL  
**Siemens:** PLC stop without action = CRITICAL, Unexpected program changes = CRITICAL
**Emerson:** Compressor overcurrent = CRITICAL, Discharge pressure >110% = CRITICAL
**Honeywell:** Fire alarm without cause = CRITICAL, Multiple HVAC offline = HIGH

---

## 📋 CHECKLISTS

### Pre-Incident
- [ ] IR plan developed and tested
- [ ] Contact list updated
- [ ] Backups configured and tested
- [ ] Monitoring deployed
- [ ] Network segmentation implemented
- [ ] Patch management process in place
- [ ] Personnel trained

### During Incident
- [ ] Safety confirmed
- [ ] Incident classified
- [ ] Team activated
- [ ] Containment executed
- [ ] Evidence preserved
- [ ] Stakeholders notified

### Post-Incident
- [ ] Systems recovered
- [ ] IR plan updated
- [ ] RCA completed
- [ ] Improvements implemented
- [ ] Training conducted

---

## 🔗 VENDOR RESOURCES

### Security Advisories
- **Danfoss**: https://www.danfoss.com/en/service-and-support/coordinated-vulnerability-disclosure/
- **Schneider**: https://www.se.com/ww/en/work/support/local/cybersecurity/
- **Siemens**: https://cert-portal.siemens.com/productcert/en
- **Emerson**: https://www.emerson.com/en-us/automation/cybersecurity
- **Honeywell**: https://www.honeywell.com/us/en/support/cybersecurity

### Security Tools
- **Asset Discovery**: Nozomi, Claroty, Tenable.ot, Forescout
- **Vulnerability Scanning**: Nessus, Qualys with OT plugins
- **Monitoring**: Wireshark (with industrial protocol dissectors)
- **OT IDS**: Nozomi Guardian, Claroty, Dragos Platform
- **SIEM**: Splunk, QRadar, Sentinel (with OT plugins)

---

## 🛡️ BEST PRACTICES (Vendor-Neutral)

### Network Security
- Never expose OT controllers to internet
- Implement IEC 62443 zone/conduit architecture
- Use OT-specific firewalls (Tofino, Nozomi)
- Disable unused ports/services
- Filter industrial protocols

### Access Control
- Strong authentication (MFA where available)
- Least privilege principle
- Disable default credentials
- Session timeout (15 min recommended)
- RBAC implementation

### Monitoring
- Deploy OT-specific monitoring
- Monitor process variables
- Implement anomaly detection
- Collect/preserve logs (90+ days)
- Monitor unauthorized changes

### Patch Management
- Apply critical patches within 30 days
- Test in lab before production
- Staged rollout (20% batches)
- Maintain rollback capability
- Verify patch integrity

### Backup & Recovery
- Regular backups of all configs
- Test restoration regularly
- Maintain offline backups
- Document recovery procedures

---

## 🎯 STANDING RULES

1. **SAFETY FIRST**: All actions prioritize physical safety
2. **NO INTERNET ACCESS**: OT controllers never internet-exposed
3. **NETWORK SEGMENTATION**: IEC 62443 zones/conduits
4. **STRONG AUTH**: MFA + strong passwords for all OT access
5. **PATCH MANAGEMENT**: Critical patches within 30 days
6. **MONITORING**: OT-specific monitoring deployed
7. **BACKUPS**: Regular, tested backups
8. **ACCESS CONTROL**: Least privilege + RBAC
9. **PHYSICAL SECURITY**: Restrict/monitor OT access
10. **IR READY**: Tested plans ready

---

**Verbosity**: V2

**Note**: This vendor-neutral guide incorporates lessons from Danfoss, Schneider Electric, Siemens, Emerson, and Honeywell incidents. Customize for your environment.
