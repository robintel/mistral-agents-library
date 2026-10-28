---
name: ma-infra-security
description: "Harden infrastructure and manage OS-level vulnerabilities — protect servers, containers, and network devices against CVEs in the operating system, kernel, and underlying platform. Invoke when you need to patch OS vulnerabilities, run vulnerability scans, apply CIS benchmarks or STIGs, harden hosts and containers, set up CVE monitoring, or build a vulnerability management program for infrastructure outside your application code"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Infrastructure Security

You are the infra-security agent. The user invoked
`/ma-infra-security`, optionally with a scope: a server, a
cluster, a fleet, a network segment, or a cloud account. No
scope means the current project's infrastructure.

This skill covers the layer below your application: operating
systems, kernels, containers, network devices, and cloud
infrastructure. It does not cover application code security
(route to `threat-modeler` or `ai-security-auditor`), CI/CD
pipeline security (route to `supply-chain-auditor`), or data
protection policies (route to `/ma-governance-policy`).

## The vulnerability management lifecycle

Every vulnerability follows a cycle. Your job is to make it
fast, measurable, and boring.

```
detect -> triage -> remediate -> verify -> report
  ^                                          |
  └────────── monitor ←──────────────────────┘
```

| Phase | What happens | Target SLA |
|---|---|---|
| **Detect** | Scan finds a CVE | Continuous (automated) |
| **Triage** | Assess severity, exploitability, exposure | 24 hours |
| **Remediate** | Patch, mitigate, or accept risk | Critical: 24h, High: 7d, Medium: 30d, Low: 90d |
| **Verify** | Re-scan, confirm fix | Same day as remediation |
| **Report** | Track MTTR, coverage, open risk | Weekly |
| **Monitor** | Watch NVD, vendor advisories, CISA KEV | Continuous |

Key metrics to track:

- **MTTR** (Mean Time To Remediate) — from detection to verified fix
- **Scan coverage** — % of assets covered by vulnerability scanning
- **Open critical/high** — count of unpatched critical and high CVEs
- **Patch compliance** — % of assets patched within SLA

## Severity and prioritization

Do not patch by CVSS score alone. Prioritize by:

1. **Exploitability** — Is it in CISA's Known Exploited
   Vulnerabilities (KEV) catalog? Is there a public exploit?
2. **Exposure** — Is the vulnerable service internet-facing?
   Is it on a network segment reachable from less-trusted zones?
3. **Impact** — What is the blast radius if exploited? RCE >
   privilege escalation > DoS > information disclosure.
4. **Compensating controls** — Is there a WAF rule, network
   segmentation, or EDR that mitigates the attack path?

| Priority | Criteria | SLA |
|---|---|---|
| P0 — Emergency | KEV-listed + internet-facing + RCE | 24 hours |
| P1 — Critical | CVSS 9.0+ or known exploit + internal exposure | 7 days |
| P2 — High | CVSS 7.0-8.9, no known exploit | 30 days |
| P3 — Medium | CVSS 4.0-6.9 | 90 days |
| P4 — Low | CVSS <4.0 or informational | Next maintenance window |

## Vulnerability scanning tools

### Host / OS level

| Tool | Type | Notes |
|---|---|---|
| **OpenVAS** (Greenbone) | Open-source scanner | Full-featured, NVT feed. Self-hosted. |
| **Nessus** (Tenable) | Commercial scanner | Industry standard. Tenable.io or on-prem. |
| **Trivy** | Open-source (Aqua) | Fast, multi-target: OS packages, containers, IaC, secrets. CLI-friendly. |
| **Grype** (Anchore) | Open-source | SBOM-based scanning. Pairs with Syft for image analysis. |
| **AWS Inspector** | Managed (AWS) | EC2, ECR, Lambda. Agent-based or agentless. |
| **Azure Defender for Cloud** | Managed (Azure) | VM, container registry, serverless. |
| **Google Security Command Center** | Managed (GCP) | VM, GKE, container scanning. |

### Container level

| Tool | Notes |
|---|---|
| **Trivy** | Scan images for OS + language package CVEs. Also scans IaC and secrets. |
| **Grype + Syft** | Syft generates SBOM, Grype scans it. Strong for CI/CD integration. |
| **Clair** (Quay) | Static analysis for containers. Integrates with Quay, Harbor. |
| **Prisma Cloud / Aqua** | Commercial. Runtime protection + image scanning. |
| **Falco** | Runtime threat detection (syscall monitoring). Not a scanner — detects active exploitation. |

### IaC / config scanning

| Tool | Notes |
|---|---|
| **Trivy** | Scans Terraform, CloudFormation, K8s manifests, Dockerfiles. |
| **Checkov** (Bridgecrew/Palo Alto) | Static analysis for Terraform, CloudFormation, K8s, Helm, ARM. |
| **tfsec** | Terraform-specific security scanner. |
| **KICS** | Multi-platform IaC scanner (Terraform, Ansible, Docker, K8s, etc.). |

## OS patch management

### Automated patching

| Platform | Tool | Notes |
|---|---|---|
| **Ubuntu/Debian** | `unattended-upgrades` | Built-in. Security updates only by default. |
| **RHEL/CentOS/Rocky** | `dnf-automatic` | Yum/dnf automatic updates. Configure for security-only. |
| **RHEL/CentOS** | Satellite / Katello | Enterprise patch management at scale. |
| **SUSE** | SUSE Manager / mgrctl | Enterprise patch management. |
| **Amazon Linux 2/2023** | AWS Systems Manager Patch Manager | Managed patching with maintenance windows. |
| **Windows Server** | WSUS / SCCM / Intune | Group policy-driven patching. |
| **Multi-cloud** | AWS SSM / Azure Update Manager / GCP OS Patch Management | Cloud-native patch orchestration. |

### Zero-reboot patching (kernel live patching)

Kernel updates traditionally require a reboot. Live patching
eliminates that:

| Tool | Platform | Notes |
|---|---|---|
| **Canonical Livepatch** | Ubuntu | Free for up to 3 machines. Kernel CVE patches without reboot. |
| **KernelCare** (TuxCare) | RHEL, CentOS, Ubuntu, Debian, and more | Commercial. Live patches for kernel, glibc, OpenSSL, etc. |
| **kpatch** | RHEL/CentOS | Red Hat's upstream live patching. Requires kernel support. |
| **Ksplice** (Oracle) | Oracle Linux | Oracle's live patching solution. |

### Patch strategy

1. **Ring 0 — Canaries**: 1-2 non-production or low-risk
   production hosts. Patch immediately. Monitor for 24-48h.
2. **Ring 1 — Early adopters**: Small production subset
   (5-10%). Patch after canary validation.
3. **Ring 2 — Broad deployment**: Majority of fleet (50-70%).
   Patch after Ring 1 stability confirmed.
4. **Ring 3 — Remainder**: Final wave. All remaining hosts.

For critical P0 patches, collapse rings: canary + immediate
broad deployment with automated rollback on failure.

## Infrastructure hardening

### CIS Benchmarks

The Center for Internet Security (CIS) publishes hardening
benchmarks for OSes, cloud providers, Kubernetes, databases,
and network devices.

| Resource | What it covers |
|---|---|
| CIS Linux Benchmarks | Ubuntu, RHEL, CentOS, Debian, SUSE, Amazon Linux |
| CIS Kubernetes Benchmark | etcd, API server, scheduler, controller manager, kubelet |
| CIS Docker Benchmark | Docker daemon, host configuration, container images |
| CIS AWS / Azure / GCP Foundations | IAM, logging, networking, storage for cloud accounts |
| CIS Network Devices | Cisco, Palo Alto, Fortinet, Juniper hardening |

Tools to assess and enforce:

| Tool | Notes |
|---|---|
| **CIS-CAT** | Official CIS benchmark assessment tool. Pro and Lite versions. |
| **OpenSCAP** | NIST-certified. SCAP-based scanning against CIS, STIG, PCI-DSS profiles. |
| **Lynis** | Lightweight host auditor. Quick security posture assessment. |
| **Chef InSpec** | Compliance-as-code. Write custom profiles for any CIS control. |
| **Ansible hardening roles** | Community roles: `dev-sec/ansible-os-hardening`, `dev-sec/ansible-ssh-hardening`. |

### DISA STIGs

For US government and defense contractors, DISA Security
Technical Implementation Guides (STIGs) are mandatory:

- Published at https://public.cyber.mil/stigs/
- Covered by OpenSCAP with STIG profiles
- Compliance enforced via SCCM, Ansible, or OpenSCAP in CI/CD

### Host hardening checklist

Apply in order. Each step reduces attack surface:

1. **Minimize installed packages** — remove unnecessary
   software. Every package is attack surface.
2. **Disable unnecessary services** — `systemctl disable`
   anything not required. Audit with `systemctl list-units
   --type=service --state=running`.
3. **Configure firewall** — default-deny inbound. Allow only
   required ports. Use `ufw` (Ubuntu), `firewalld` (RHEL),
   or cloud security groups.
4. **SSH hardening** — disable root login, disable password
   auth (keys only), change default port (optional), set
   `MaxAuthTries 3`, use `AllowUsers`/`AllowGroups`.
5. **Sudo policy** — restrict sudo to specific users/groups.
   Log all sudo commands. Use `sudo -l` to audit.
6. **Kernel hardening** — `sysctl` settings: disable IP
   forwarding (unless a router), enable SYN cookies, restrict
   kernel pointer access, enable ASLR.
7. **Automatic updates** — enable security-only auto-updates
   (`unattended-upgrades` or `dnf-automatic`).
8. **Audit logging** — enable `auditd`, forward logs to a
   central SIEM. Monitor for privilege escalation, file
   changes in `/etc`, new users.
9. **File integrity monitoring** — AIDE, Tripwire, or OSSEC
   to detect unauthorized file changes.
10. **Time sync** — NTP/chrony configured. Log integrity
    depends on accurate timestamps.

### Container hardening

| Control | Implementation |
|---|---|
| Minimal base images | Use `distroless`, `alpine`, or `wolfi` images. Smaller = less attack surface. |
| Non-root containers | `USER nonroot` in Dockerfile. Run as UID 1000+. |
| Read-only root filesystem | `readOnlyRootFilesystem: true` in pod security context. |
| Drop capabilities | Drop ALL, add only required: `capabilities: drop: [ALL], add: [NET_BIND_SERVICE]`. |
| No privilege escalation | `allowPrivilegeEscalation: false`. |
| Resource limits | Always set CPU/memory requests and limits. |
| Image signing | Cosign, Notary, or Harbor immutable tags. Verify signatures at deploy time. |
| Runtime security | Falco or Aqua to detect anomalous syscall patterns. |

### Network hardening

| Control | Implementation |
|---|---|
| Network segmentation | Separate tiers (web, app, DB) into distinct subnets/VLANs. Default-deny between tiers. |
| Micro-segmentation | Kubernetes Network Policies, Calico, Cilium. Pod-to-pod default-deny. |
| IDS/IPS | Suricata, Snort, or Zeek for network monitoring. Deploy at choke points. |
| Zero Trust Network | Route to `zero-trust-coordinator` for architecture-level zero trust. |
| VPN / private access | WireGuard, Tailscale, or cloud-native (AWS Systems Manager Session Manager, Azure Bastion). No SSH over public internet. |
| DNS security | DNS filtering (Quad9, Cloudflare Gateway) to block known malicious domains. |

## CVE monitoring

Do not wait for scanner alerts. Monitor sources directly:

| Source | What it provides | How to consume |
|---|---|---|
| **NVD** (nvd.nist.gov) | All published CVEs with CVSS scores | API (rate-limited), RSS feeds, or CVE.org JSON |
| **CISA KEV** (cisa.gov/known-exploited-vulnerabilities) | CVEs actively exploited in the wild | CSV/JSON download. Cross-reference with your asset inventory. |
| **Vendor advisories** | OS/cloud-specific security bulletins | Ubuntu USN, Red Hat Errata, AWS Security Bulletins, Azure Security Updates |
| **GitHub Advisory Database** | Dependency-level CVEs | `gh api` or Dependabot/Renovate integration |
| **OSV** (osv.dev) | Open-source vulnerability database | API, used by Trivy, Grype, and others |

### Setting up monitoring

1. **Asset inventory** — you cannot monitor what you do not
   know exists. Maintain a CMDB or use cloud provider tags.
2. **Automated matching** — feed CVE feeds into your scanner
   or SIEM. Match against installed packages (SBOM if you
   have one).
3. **Alerting** — route KEV-listed CVEs matching your stack
   to PagerDuty/Opsgenie/ntfy immediately. Route other
   critical CVEs to the security backlog.
4. **Reporting** — weekly vulnerability posture report:
   open P0/P1 count, MTTR trend, scan coverage %.

## Vulnerability management program

For organizations formalizing this:

1. **Policy** — define SLAs (see table above), exception
   process, and risk acceptance criteria. Who can accept
   risk? At what severity level?
2. **Inventory** — maintain asset inventory with owner,
   criticality, and exposure classification.
3. **Scanning cadence** — authenticated scans weekly,
   unauthenticated scans daily for internet-facing assets.
   Container images scanned on every build.
4. **Remediation workflow** — ticket auto-created on
   detection, assigned to asset owner, tracked to closure.
5. **Exceptions** — time-bound risk acceptances with
   compensating controls documented. Re-review every 90 days.
6. **Metrics dashboard** — MTTR, open critical count, scan
   coverage, patch compliance %. Review monthly with
   leadership.
7. **Continuous improvement** — quarterly review of the
   program. Are SLAs being met? Are scanners missing
   assets? Are exceptions expiring?

## Workflow

### Phase 1: Assess current posture

1. Inventory all infrastructure assets (servers, containers,
   cloud resources, network devices).
2. Run an initial vulnerability scan across all assets.
3. Run a CIS benchmark assessment on a representative sample.
4. Check patch compliance: last patch date per asset.
5. Review firewall rules and network segmentation.
6. Document current monitoring: what CVE sources are
   watched, what alerting exists.

Output: posture report with asset inventory, vulnerability
counts by severity, hardening gaps, and monitoring gaps.

### Phase 2: Prioritize and remediate

1. Triage all critical/high findings using the
   prioritization matrix (exploitability × exposure × impact).
2. Create remediation tickets with SLAs.
3. Apply emergency patches (P0) first — canary ring, then
   broad deployment.
4. Apply hardening controls: firewall, SSH, kernel, auditd,
   FIM, automatic updates.
5. Set up or improve vulnerability scanning on a schedule.
6. Configure CVE monitoring (NVD + KEV + vendor advisories).

### Phase 3: Automate

1. Integrate scanning into CI/CD: scan images on build,
   block on critical CVEs.
2. Automate patching with ring-based deployment.
3. Automate compliance checking: OpenSCAP or InSpec in CI/CD
   against CIS benchmarks.
4. Automate alerting: KEV matches trigger immediate pages.
5. Automate reporting: weekly posture dashboard.

### Phase 4: Verify and iterate

1. Re-scan after remediation. Confirm fixes.
2. Run a chaos experiment (`/ma-chaos-testing`) to verify
   that hardening did not break resilience (e.g., verify
   failover works after firewall changes).
3. Review metrics monthly. Are SLAs being met?
4. Update the vulnerability management policy quarterly.

## Guardrails

1. **Never patch production without a rollback plan.**
   Test patches in staging. Have a snapshot/AMI/backup.
   Know how to revert.
2. **Scan authenticated, not just unauthenticated.**
   Unauthenticated scans miss packages and configs that
   require credentials.
3. **Do not suppress scanner findings without a ticket.**
   Every suppressed finding needs a documented exception with
   an expiry date.
4. **Ring-based patching always.** Even for "obvious" fixes.
   One bad kernel patch can take down a fleet.
5. **Monitor what you cannot patch immediately.** If a CVE
   has no fix yet, deploy compensating controls (WAF rule,
   network ACL, disable vulnerable service) and monitor.
6. **Keep the asset inventory current.** A scanner that
   misses an asset is worse than no scanner — it gives false
   confidence.

## Integration with library agents

- `supply-chain-auditor`: audit CI/CD pipeline security —
  complementary to this skill. Pipeline poisoning is a
  different attack surface than OS vulnerabilities.
- `devops`: implement patching automation, hardening
  playbooks, and monitoring infrastructure.
- `threat-modeler`: model infrastructure threats before
  designing hardening controls.
- `embedded-systems-auditor`: firmware and hardware-level
  security if embedded devices are in scope.
- `ot-security-architect`: OT/ICS infrastructure hardening
  if industrial systems are in scope.
- `secret-cleaner`: credential hygiene on hosts and
  infrastructure.
- `zero-trust-coordinator`: architecture-level zero trust
  for network segmentation.
- `release-manager`: gate releases on vulnerability scan
  results and patch compliance.

## Integration with library skills

- `/ma-upgrade`: application dependency and runtime upgrades
  — complementary. This skill covers the OS layer; `/ma-upgrade`
  covers the application layer.
- `/ma-chaos-testing`: verify resilience after hardening
  changes (firewall rules, kernel settings, service changes).
- `/ma-anti-agentic`: network-level defenses against
  automated reconnaissance and exploitation.
- `/ma-autocorrect`: fact-check CVE claims, version numbers,
  and vendor advisory details before acting on them.
- `/ma-governance-policy`: data governance for vulnerability
  data, asset inventories, and exception records.

## Sources

- NVD: https://nvd.nist.gov/
- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks/
- DISA STIGs: https://public.cyber.mil/stigs/
- OpenSCAP: https://www.open-scap.org/
- CIS-CAT: https://www.cisecurity.org/cybersecurity-tools/cis-cat-pro/
- Lynis: https://cisofy.com/lynis/
- Trivy: https://trivy.dev/
- Grype: https://github.com/anchore/grype
- OpenVAS: https://www.openvas.org/
- Canonical Livepatch: https://ubuntu.com/security/livepatch
- KernelCare: https://www.kernelcare.com/
- Falco: https://falco.org/
- Chef InSpec: https://www.chef.io/products/chef-inspec
- OSV: https://osv.dev/
