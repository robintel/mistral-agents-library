# Changelog

User-facing changes to the Mistral Agents Library. One line each,
imperative mood. This file follows the release-manager's own rule:
changelogs are for users, not for git history. Format per
[Keep a Changelog](https://keepachangelog.com); semver: breaking = major,
feature = minor, fix = patch.

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
