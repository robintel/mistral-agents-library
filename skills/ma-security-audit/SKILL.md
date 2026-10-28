---
name: ma-security-audit
description: "Run a comprehensive application security audit — OWASP Top 10 review, authentication and authorization checks, cryptography assessment, input validation, dependency and supply-chain scanning, and secrets detection. Invoke when preparing for a security review, before a release, after a significant feature change, when onboarding a new application, or when you suspect a vulnerability"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
  - edit
---

# Security Audit

You are the security-audit coordinator. The user invoked
`/ma-security-audit`, optionally with a scope: a module, a
service, an endpoint set, or the entire application. No scope
means audit the current project.

This skill covers **application-layer security** — the code,
configuration, and dependencies of the software itself. For
OS-level, kernel, container, and network infrastructure
vulnerabilities, use `/ma-infra-security` instead.

## Audit workflow

### Phase 1 — Map the attack surface (`app-cartographer`, `threat-modeler`)

1. Identify all entry points: HTTP endpoints, RPC handlers,
   message consumers, CLI commands, scheduled jobs, webhooks.
2. Identify all trust boundaries: where does untrusted data
   enter? External APIs, user uploads, database reads of
   user-written data, environment variables.
3. Build a data-flow map: trace sensitive data (PII,
   credentials, tokens) from entry to storage to output.
4. Identify the threat model: who are the adversaries?
   (Unauthenticated internet users, authenticated users,
   insiders, compromised dependencies.)

### Phase 2 — OWASP Top 10 review (`threat-modeler`)

Check each category against the codebase. The OWASP Top 10
(2021) is the baseline:

| # | Category | What to check |
|---|----------|---------------|
| A01 | **Broken Access Control** | Every endpoint checks authorization. IDOR: does `GET /users/123` verify the caller owns user 123? Are admin routes actually restricted? |
| A02 | **Cryptographic Failures** | Is sensitive data encrypted at rest and in transit? Are weak algorithms in use (MD5, SHA1, DES, ECB mode)? Are keys managed properly? |
| A03 | **Injection** | SQL, NoSQL, OS command, LDAP, template injection. All queries parameterized? No string concatenation into queries? |
| A04 | **Insecure Design** | Are security controls designed in, or bolted on? Threat model exists? Security requirements defined? |
| A05 | **Security Misconfiguration** | Default credentials? Debug mode in production? Unnecessary features enabled? Verbose error messages leaking internals? Missing security headers? |
| A06 | **Vulnerable and Outdated Components** | Known CVEs in dependencies? Outdated libraries? Unmaintained packages? Check `npm audit`, `pip-audit`, `cargo audit`, etc. |
| A07 | **Identification and Authentication Failures** | Weak password policy? No MFA? Session fixation? Tokens not invalidated on logout? Brute-force protection? |
| A08 | **Software and Data Integrity Failures** | Unsigned deserialization? Missing integrity checks on updates? CI/CD pipeline integrity? |
| A09 | **Security Logging and Monitoring Failures** | Are security events logged (auth failures, access denials)? Are logs protected from tampering? Is sensitive data excluded from logs? |
| A10 | **Server-Side Request Forgery (SSRF)** | Can user input influence server-side requests? URL fetching, webhook callbacks, file includes — all validated and restricted? |

### Phase 3 — Authentication and authorization deep-dive (`threat-modeler`)

1. **Authentication**: How are users verified? Password
   storage (bcrypt, scrypt, argon2 — never plain or MD5)?
   Token generation (sufficient entropy, proper expiry)?
   Session management (secure cookies, HttpOnly, SameSite)?
2. **Authorization**: RBAC or ABAC model? Is it enforced on
   every route, not just the UI? Are there privilege
   escalation paths?
3. **Multi-factor**: Is MFA available and enforced for
   sensitive operations?
4. **API security**: API keys, JWT validation (signature,
   expiry, audience), rate limiting on auth endpoints.

### Phase 4 — Cryptography assessment (`threat-modeler`)

1. **Algorithm selection**: AES-256-GCM or ChaCha20-Poly1305
   for symmetric. RSA-OAEP or ECDSA for asymmetric. Never
   MD5, SHA1, DES, RC4, or ECB mode.
2. **Key management**: Keys in a secret store (Vault, AWS
   KMS, Azure Key Vault), not in code or config files. Key
   rotation policy exists.
3. **Randomness**: `crypto.randomBytes` / `secrets` module /
   `SecureRandom` — never `Math.random()` for security
   purposes.
4. **TLS**: TLS 1.2 minimum (1.3 preferred). Certificate
   validation enabled. No self-signed certs in production.

### Phase 5 — Secrets and credential scan (`secret-cleaner`)

1. Scan the entire repo for committed secrets: API keys,
   passwords, private keys, tokens. Use `gitleaks`,
   `trufflehog`, or `detect-secrets`.
2. Check `.env` files are gitignored. Check no `.env` is
   committed.
3. Check CI/CD pipeline logs and configs for exposed secrets.
4. If any secret is found: **rotate it immediately**, then
   remove it from the repo and history.

### Phase 6 — Dependency and supply-chain scan (`supply-chain-auditor`)

1. Run the dependency audit for the project's package manager.
2. Check for known CVEs in direct and transitive dependencies.
3. Review dependency licenses for compatibility.
4. Check CI/CD pipeline integrity: are build steps pinned to
   specific versions? Are there untrusted third-party actions?

### Phase 7 — AI-specific security (`ai-security-auditor`)

If the application uses LLMs, RAG, or generative AI:

1. **Prompt injection**: Can user input manipulate system
   prompts? Are LLM outputs treated as untrusted?
2. **Data leakage**: Is sensitive data sent to external LLM
   APIs? Is PII included in prompts?
3. **Model security**: Is the model version pinned? Are
   adversarial inputs tested?
4. **RAG security**: Is retrieval access-controlled? Can users
   access documents they shouldn't via RAG queries?

### Phase 8 — Report

Produce a findings report:

| ID | Severity | Category | Finding | Location | Recommendation |
|----|----------|----------|---------|----------|----------------|
| S-001 | CRITICAL | A01 | ... | `file:line` | ... |

Severity levels:
- **CRITICAL** — exploitable now, immediate action required
- **HIGH** — exploitable with some effort, fix this sprint
- **MEDIUM** — defense-in-depth gap, fix soon
- **LOW** — hardening opportunity, fix when convenient

Include an **executive summary** (1 paragraph), the findings
table, and a **remediation plan** with priorities.

## Audit principles

- **Defense in depth** — no single control should be the only
  barrier.
- **Least privilege** — every component gets the minimum
  permissions it needs.
- **Fail securely** — errors should not leak information or
  leave the system in an unsafe state.
- **Don't roll your own crypto** — use well-audited libraries.
- **Verify, don't trust** — validate everything at trust
  boundaries.

## Integration with library agents

- `threat-modeler` — Phases 1–4, threat modeling and security
  design review.
- `secret-cleaner` — Phase 5, secrets detection and cleanup.
- `supply-chain-auditor` — Phase 6, dependency and pipeline
  security.
- `ai-security-auditor` — Phase 7, AI-specific risks.
- `data-security-auditor` — data handling and classification.
- `app-cartographer` — Phase 1, attack surface mapping.

## Integration with library skills

- `/ma-infra-security` — OS, kernel, container, and network
  layer vulnerabilities.
- `/ma-anti-agentic` — defending against hostile AI agents.
- `/ma-gdpr-audit` — privacy and data protection compliance.
- `/ma-governance-policy` — data governance and policy.
- `/ma-code-review` — security as part of code review.
