# Changelog

User-facing changes to the Mistral Agents Library. One line each,
imperative mood. This file follows the release-manager's own rule:
changelogs are for users, not for git history. Format per
[Keep a Changelog](https://keepachangelog.com); semver: breaking = major,
feature = minor, fix = patch.

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
