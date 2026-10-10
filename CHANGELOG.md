# Changelog

User-facing changes to the Mistral Agents Library. One line each,
imperative mood. This file follows the release-manager's own rule:
changelogs are for users, not for git history. Format per
[Keep a Changelog](https://keepachangelog.com); semver: breaking = major,
feature = minor, fix = patch.

## [0.28.0] — 2026-10-10

### Added

- Add Phase 3 IoT industrial protocol dialects: Modbus (RTU/TCP with
  PDU/ADU structure, function codes, addressing, error handling, timing),
  OPC UA (information model, services, transport mechanisms, security),
  PROFINET (RT classes, DCP, MRP/MRPD redundancy, PTP synchronization).

## [0.27.0] — 2026-10-10

### Added

- Add Salesforce integration dialect: REST, SOAP, Bulk, Streaming, and
  Metadata APIs; OAuth 2.0 flows (Web Server, User-Agent, JWT Bearer);
  data models for standard and custom objects; migration patterns for
  legacy CRM to Salesforce; governor limits and query optimization
  strategies; modernization approaches and best practices.

## [0.26.0] — 2026-10-10

### Added

- Add Tier 2 European dialects: Scaleway Object Storage (French cloud),
  T-Systems Object Storage (German telecom), Sovereign Cloud/
  Gaia-X patterns (EU data sovereignty).
- Add Tier 2 Japanese dialects: NTT Communications Cloud Storage,
  IIJ G.IO Object Storage.
- Add Tier 3 legacy dialects: IBM i (AS/400) integration (European
  enterprise legacy), Fujitsu Enterprise systems (Japanese legacy).

## [0.25.0] — 2026-10-10

### Added

- Add Tier 1 European dialects: OVHcloud Object Storage (GDPR-compliant
  European cloud).
- Add Tier 1 Japanese dialects: Sakura Object Storage (Japanese market
  leader).
- Add SAP integration patterns dialect: comprehensive enterprise
  integration (BAPI, IDoc, OData, RFC, Web Services).

## [0.24.0] — 2026-10-10

### Added

- Add modernization-agent: architectural transformation with explicit
  hybrid (on-prem + cloud) support.
- Add data-orchestrator: data movement and synchronization coordination.
- Add object storage dialects: S3 (AWS), Google Cloud Storage, Azure
  Blob Storage, HPE Object Storage.
- Add data-sync pattern dialect: synchronization strategies and CDC
  (Change Data Capture) patterns.

## [0.23.0] — 2026-10-10

### Added

- Add the five workflow skills: `skills/orient/SKILL.md` through
  `skills/upgrade/SKILL.md` implement /orient, /tour, /coverage,
  /gdpr-audit, and /upgrade as slash commands in the CLI and VS
  Code. Both installers (install.py and install.ps1) now copy
  skill directories to `~/.vibe/skills/`; smoke test confirmed
  they load and respond.

### Fixed

- Fix TOML generation in install.py: display_name suffix now properly
  quoted inside toml_string to generate valid TOML profiles.

## [0.22.0] — 2026-10-07

### Added

- Add the clean-room smoke test: `smoke/Dockerfile` (the environment
  spec — Vibe CLI + Python, nothing library-specific baked in) and
  `smoke/smoke.sh` (install into the container HOME, run the
  orchestrator in the CLI's verified programmatic mode against the
  library itself, assert shape: answer present and on-target, target
  unmodified, tool cache empty — the birth gate, headless). First
  end-to-end run green on podman 4.9: 52 profiles, on-target
  135-word answer in 13s; one image fix found on first contact —
  PATH must be exported before the Vibe installer, which exits
  non-zero when its own command is not on PATH. DEPLOYING.md
  documents the recipe, the podman variant, and the mode-600
  hardening note.
- Add the Windows-installer parity test: `smoke/parity.sh` runs
  install.ps1 under the cross-platform pwsh (pinned 7.6.6 in the
  image, plus libicu76 for Debian trixie — .NET aborts without ICU)
  and diffs it byte-for-byte against install.py's batch: 52
  profiles, byte-identical, no API key needed. The release test
  DEPLOYING.md names is now executable; Windows-native behavior
  remains for the future windows-latest CI job.

## [0.21.0] — 2026-10-05

### Added

- Document the scaling limits and their escape hatches: the README
  gains a "Scaling limits" section (orchestrator triage ceiling
  solved by domain routers, `accepts` taxonomy governance, manifest
  split threshold), and TODO parks each limit with its unblock
  condition.

## [0.20.0] — 2026-10-05

### Added

- Add the data gate to the tool cache: tools are logic, never data.
  Before a run is proposed, the draft is scanned for credentials,
  PII, and embedded data (pattern and entropy, per the
  secret-cleaner's hunt); credentials become references, payloads
  become synthetic fixtures or arguments, and a draft that cannot
  be cleaned is not proposed. The scan is recorded as a `# data:
  clean` header line next to the run-proof, and the tool-steward
  re-scans at audit — a failure returns the tool to draft, the
  finding named by relationship, never by value.

## [0.19.0] — 2026-10-05

### Added

- Add the tool cache and the tool-steward: a user-local library of
  reusable agent-born tools (`~/.mistral-agents/tools/` — INDEX.md,
  adhoc/, vetted/) governed per standards rule 8. The birth gate: a
  tool enters the cache only after the user agreed to run it at
  least once — the session's permission prompt is the gate, the
  approved run recorded as provenance in the header; drafts stay
  out. The tool-steward audits (provenance first, then the elegance
  bar and security applied double), deduplicates, promotes
  adhoc -> vetted with user veto, retires, and proposes native
  promotion (config.toml mcp_servers or tool_paths) — proposed,
  sketched, applied only by the user. The orchestrator gathers the
  cache as a capability and dispatches the steward when ad-hoc
  additions accumulate.

## [0.18.0] — 2026-10-05

### Added

- Add the ambient pass to tour-config: the world the app assumes
  against the world it runs in — OS and platform from base images,
  manifests, and shebangs; container versus systemd versus bare
  metal; locale, timezone, and filesystem assumptions; declared
  verified against actual where the environment is observable, and
  the pass self-disclaims where the platform genuinely does not
  matter.
- Add Environment to the APP MAP and platform to the ORIENTATION
  stack: the map records the world the app assumes — OS, platform,
  containerization, expected services, locale and timezone.
- Sharpen the integrations boundary: the orchestrator discovers, the
  brief names, the specialist uses only what is named — session
  capabilities never enter the APP MAP; the map records artifacts,
  not connections.

## [0.17.0] — 2026-10-05

### Added

- Add integration support: the patterns/integrations contract —
  capabilities discovered never assumed; idempotency on write-side
  calls; rate limits and pagination as real constraints; errors
  from the remote mapped honestly; authentication lives in the
  integration. Orchestrator gains capability discovery at budgeting
  and a capabilities line in the BRIEF; standards rule 7; DEPLOYING.md
  documents the alignment with the two native mechanisms —
  config.toml MCP servers and Mistral-managed connectors — plus the
  platform Connectors API for API deployments.

## [0.16.0] — 2026-10-05

### Added

- Add `tour-adversary`: the malevolent-user walk — legitimate
  features chained into illegitimate outcomes, privilege skipped
  through behavior, export and reporting as exfiltration, runtime
  third-party blast radius. Distinct from sentry (code) and
  supply-chain (pipeline): this tours behavior, and its live leads
  are literal step-by-step attack scripts.

## [0.15.0] — 2026-10-05

### Added

- Add the one-command install: install.py, with install.ps1 as
  the no-Python Windows companion. Reads manifest.yaml and
  composes every agent into a self-contained Vibe profile — shared
  standards + body + deployment addendum, the tier's model, the
  role's tool surface — installs the batch to ~/.vibe/agents/
  (orchestrator selectable, specialists as subagents), prunes
  stale generated profiles while leaving hand-written ones alone,
  and optionally writes the target repo's thin AGENTS.md. Every
  generated file is round-trip validated (Python installer);
  reruns are idempotent. Both installers compose byte-identical
  profiles on Linux, macOS, and Windows: CRLF checkouts and
  Windows path backslashes are normalized. Quick start in the
  README; DEPLOYING.md documents the mapping.

## [0.14.0] — 2026-10-05

### Added

- Add DEPLOYING.md with the schema verified from the mistral-vibe
  source: profiles carry their instructions inline (one TOML per
  agent, name = filename); safety values, agent_type, enabled_tools,
  and per-tool permissions confirmed. A live test deployment was
  installed to ~/.vibe/agents/ (orchestrator + app-cartographer
  subagent) and the VS Code smoke-test steps recorded.

## [0.13.0] — 2026-10-04

### Added

- Add assembly and embedded support: asm-x86-64 (the System V ABI as
  the contract, AT&T vs Intel as the syntax era) and asm-arm
  (AArch64/AArch32/Cortex-M profiles, AAPCS), both standalone
  language contracts; the embedded pattern contract (volatile
  hardware registers, no heap in ISRs, cycle budgets, atomicity on
  8-bit MCUs); platform contracts for arduino (AVR/SAMD eras,
  String as the heap-fragmenter) and esp32 (Xtensa vs RISC-V eras,
  FreeRTOS discipline, brownout as the classic mystery); c and cpp
  route firmware work to the embedded pattern.

## [0.12.0] — 2026-10-04

### Added

- Add the legacy mainframe store contracts, conservation and
  experimental: ims (hierarchical DL/I paths, PSBs as code), vsam
  (the KSDS/ESDS/RRDS organizations, CI splits), idms (CODASYL sets,
  currency as state), adabas (descriptors as access paths, the
  holding queue), cache-iris (globals as schemaless storage,
  subscript-level locking). They attach standalone: the nosql core
  descends from disciplines these stores invented.
- Add the legacy estate languages, conservation and experimental:
  pli (explicit attributes, ON-conditions, silent conversions), natural
  (the access verbs as descriptor discipline, paired with adabas),
  objectscript ($ORDER/$QUERY as the query language, paired with
  cache-iris), xbase (the DBF family — DELETE as a mark, PACK as a
  rebuild, index corruption as the classic failure).

## [0.11.0] — 2026-10-04

### Changed

- Restructure `shared/dialects/` into role folders: languages/ (16),
  engines/ (sql core + 7), stores/ (nosql core + 6), brokers/
  (messaging core + 7), platforms/ (hadoop, spark), patterns/ (etl).
  Conservation stays a status, not a folder; cores live with their
  families; attachment paths updated throughout.

## [0.10.0] — 2026-10-04

### Added

- Add the graphql dialect: schema-first contracts, thin resolvers
  (the N+1 resolver named as the classic defect), cursor connections,
  partial-error responses, depth and complexity guarding.
- Add the etl pattern contract — a new contract kind, attached by the
  shape of the work (the data-engineer's pipeline briefs): idempotency
  as the law, T-placement as a priced decision (PII shaped before it
  lands pre-empts the GDPR finding), backfill as a designed capability,
  reconciliation at every hop.
- Add engine contracts: sqlite (type affinity, per-connection foreign
  keys), sqlserver (compatibility-level eras, NOLOCK as a dirty-read
  generator), snowflake (compute-time cost dial, auto-suspend
  mandatory) — SQL coverage reaches seven engines.
- Add the dynamodb store contract: single-table design, conditional
  writes as the concurrency tool, hot partitions at AWS scale.
- Add platform contracts: kafka (the replayable log — partitions as
  order, consumer idempotency, at-least-once as the default world)
  and spark (DataFrames over the RDD era, shuffle as the cost,
  streaming with checkpointing as contract).
- Add the messaging two-layer: messaging.md core — guarantees
  vocabulary, idempotent consumers, dead-lettering as designed
  capability, replay as policy — plus broker contracts: rabbitmq
  (topology as design, quorum-era queues), sqs (visibility-timeout
  leases, DLQ redrive), ibm-mq (syncpoint, queue managers, the
  oldest broker alive), solace (per-message direct-vs-guaranteed,
  VPN tenancy), activemq (Classic-to-Artemis era), nats (core
  at-most-once versus JetStream, stated per integration). Kafka
  joins its siblings under the core.

## [0.9.0] — 2026-10-04

### Added

- Add NoSQL contracts: nosql.md modeling core — access-pattern-first,
  denormalization, consistency as a dial — plus cassandra store
  contract (partition-key design, quorum math, tombstones). Hadoop
  covered as a platform (HDFS, the compute eras), with HBase named as
  its own contract when used. The stores share no language: the core
  is thin, the store contract carries the weight.
- Add NoSQL store contracts: mongodb, redis, hbase, elasticsearch —
  attaching with the modeling core, each with its era map (MongoDB
  4.0 transactions, Elasticsearch typed queries dying across 6/7,
  HBase 1.x/2.x, Redis deployment modes).
- Add the bigquery engine contract: cost is bytes scanned — SELECT *
  is a financial event; partitioning and clustering are the cost
  mechanism; the dry-run API prices a query before it runs.

## [0.8.0] — 2026-10-04

### Added

- Add dialects: c, cpp, ruby, perl, php, javascript — sixteen
  contracts total. Proper eras throughout: the -std= flag for C, the
  standard era for C++, Ruby's keyword-argument boundary, Perl's
  legacy/modern discipline, PHP's typed-signature eras, and
  JavaScript's ES5 -> ES2015 -> module-era ladder.
- Add SQL engine contracts: postgres, mysql, oracle — two-layer with
  the vendor-neutral sql core; each engine carries its era map
  (Oracle 10/11/12c, MySQL 5.7/8.0 and sql_mode, Postgres version
  thresholds).

## [0.7.0] — 2026-10-04

### Added

- Add discovery depth to the app-cartographer: skim answers "what is
  this repo?" with a user-facing ORIENTATION; map stays the working
  APP MAP; the tours are the deep phase. Depth is chosen by the brief,
  never paid by default.

## [0.6.0] — 2026-10-04

### Added

- Add Eras sections to python (2 vs 3), rust (editions), go (version
  thresholds), typescript (module systems): the build names the era;
  ports are migration briefs, never ride-alongs.

## [0.5.0] — 2026-10-04

### Added

- Add dialects: java, csharp, vbnet, fortran, cobol. Era maps inside
  the contract — the build names the era, never a modernization
  ride-along; fortran and cobol get conservation contracts, where
  preservation beats idiom and the running system is the spec. The
  legacy pair ships experimental: never validated against a real
  estate, findings get practitioner review.

## [0.4.0] — 2026-10-04

### Added

- Add `gdpr-auditor`: GDPR readiness assessment for EU-bound systems —
  applicability first, "not applicable" a complete result; findings
  framed as exposure, never verdicts.
- Add `tour-config`: configuration surfaces — shared credentials,
  dev-in-prod values, environment drift, dead settings; secrets
  reported by relationship, never by value.
- Add `security/secret-cleaner`: remove committed credentials, wire
  references, plan rotation; history scrubs proposed, never run.
- Add the shared secret-hygiene standard: values never enter reports
  or artifacts; harness-level redaction documented for deployment.

## [0.3.0] — 2026-10-04

### Added

- Add `tour-rush-hour`: non-functional paths — slow algorithms, races,
  and logging discipline (volume, consistency, sensitive material).

### Changed

- Update copyright attribution: link qastell.eu; add the EU development
  statement to LICENSE and README.

## [0.2.0] — 2026-10-04

### Added

- Add the `data/` domain (renamed from `data_lc`): data-steward with the
  DATA CATALOG, data-auditor, query-optimizer.
- Add the `security/` domain: threat-modeler, supply-chain-auditor,
  data-security-auditor, and qastell-guide with its qualification gate.
- Add the tours: lineage (data flow graph, serialization boundaries with
  round-trip proof), siren (error paths), sentry (trust boundaries, t3).
- Add `shared/dialects/sql.md`.
- Add estate-aware discovery and touring: multi-root classification,
  cross-repo test discovery, per-service tours with systemic-finding
  elevation.
- Add TODO.md: open threads with unblock conditions.

## [0.1.0] — 2026-10-04

### Added

- Add the core: orchestrator (BRIEF/REPORT protocol, scoped coordinators),
  manifest registry, model catalog with user-approved refresh,
  model-registrar, shared standards and the elegance bar.
- Add `sdlc/app-dev`: intake-analyst, architect, code-developer,
  scaffolder, implementer, code-reviewer, debugger, devops,
  release-manager.
- Add `sdlc/testing`: app-cartographer, the test pipeline (test-designer,
  test-automator, automation-reviewer), suite health (suite-reviewer,
  flaky-test-analyst), the coverage loop (coverage-manager,
  unit-test-writer), tour-coordinator and eight tours.
- Add `sdlc/app-upgrades`: upgrade-planner, dependency-upgrader,
  migration-engineer, data-migration-engineer, rollback-operator.
- Add `data_lc`: data-engineer, data-analyst.
- Add dialects: python, typescript, go, rust.
