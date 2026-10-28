# Mistral Agents Library

A library of prompt-defined agents for Mistral AI, built around excellent software
development and designed to extend to other domains without touching the core.

## Prerequisites

- **Mistral API key required.** Set `MISTRAL_API_KEY` in your environment
  before using any agent. Without this key, the CLI and VS Code extension
  cannot authenticate with Mistral's API, and **no agents will function**.
  The library installation itself does not require the key (it only uses git),
  but running `vibe --agent orchestrator` or any slash command **does require it**.

## Getting started

One command, on any machine with Python 3 and Mistral Vibe:

```sh
git clone https://github.com/robintel/mistral-agents-library.git
cd mistral-agents-library
./install.py
```

On Windows, any shell installs the same batch: `install.bat`
from cmd (a thin wrapper — `powershell -ExecutionPolicy Bypass
-File .\install.ps1`, so no script-policy detour), `.\install.ps1`
from PowerShell, no Python needed, or `py install.py` with Python.
All three produce byte-identical profiles on Linux, macOS, and
Windows — CRLF checkouts and Windows path backslashes are
normalized before composing.

Then two manual steps, both short:

1. Reload the VS Code window (Developer: Reload Window), or
   restart the CLI, so Vibe picks up the new profiles.
2. Switch to the orchestrator: `vibe --agent orchestrator`, or
   Shift+Tab in the panel. Work arrives at the specialists as
   briefs from the orchestrator — the user never addresses them
   directly.

![Selecting the Orchestrator](docs/1.%20Selecting%20the%20Orchestrator.png)

What the command does: `install.py` reads `manifest.yaml` — the
single source of truth — and composes every agent into a
self-contained profile in `~/.vibe/agents/`: `shared/standards.md`
plus the agent body, the tier's model, the role's tool surface. The
orchestrator lands as a selectable profile; the 51 specialists land
as subagents it spawns by name.

Day to day:

- After pulling library changes, rerun `./install.py` — the
  install is idempotent, and a rerun prunes profiles from earlier
  installs that are no longer in the manifest. Hand-written
  profiles are left alone.
- `./install.py --check` checks if a newer version is available.
- `./install.py --update` pulls the latest changes from origin and
  reinstalls everything in one command.
- `./install.py --target /path/to/repo` writes the target repo's
  thin AGENTS.md — the pointer that binds a working repository to
  this deployment. It never overwrites an existing AGENTS.md.
- `--dest DIR` tries a batch somewhere else first; `--dry-run`
  prints the plan, writes nothing.

Version tracking: each install writes a `.mal_version` marker to the
profile directory. The installer uses this to compare local and remote
versions when checking for or applying updates.

The full mapping — profiles, subagents, skills — and its caveats:
[DEPLOYING.md](DEPLOYING.md).

## Use cases

Concrete scenarios the library handles. Each names the agents or skills
involved and the shape of the result.

### Starting work in a new codebase

```
/ma-orient → app-cartographer → tour-coordinator
```

Get oriented in under a minute, then run a broad health check. The
cartographer maps the project; the tour coordinator dispatches testing
tours and synthesizes findings. Output: orientation summary, app map,
tour report with risk findings.

### Building a new feature

```
intake-analyst → architect → implementer → test-engineer → code-reviewer
```

Or via skill: `/ma-dev-workflow spec` — write the spec first, get
approval, then implement against it. Output: spec document, working
code, passing tests, review report.

### Fixing a bug

```
orchestrator → debugger
```

Or via skill: `/ma-dev-workflow tdd` — write a failing test that
reproduces the bug, fix the code, confirm the test passes. Output:
regression test + fix.

### Running a health check before release

```
/ma-tour → /ma-coverage
```

Coordinated testing tours plus a coverage report. If coverage is below
the 80% floor, the coverage-manager lists the gaps. Output: tour
findings + coverage percentage and gaps.

### Planning dependency upgrades

```
/ma-upgrade
```

Assess the upgrade landscape: current vs latest versions, complexity,
risk, and a staged plan. Output: ordered upgrade plan with risks and
effort per stage.

### Modernizing a legacy system

```
/ma-modernize
```

Move a legacy system to a modern stack — replatform, migrate, or
full modernization. Provide the source system, target stack, and
constraints; the skill maps the current estate, designs the target,
and produces a MODERNIZATION PLAN with migration waves, green gates,
and rollback plans. Output: modernization plan + phased execution.

### Auditing for GDPR compliance

```
/ma-gdpr-audit
```

Walk the system for PII in logs, retention policies, consent mechanisms,
right-to-be-forgotten, and breach notification. Output: findings table
with risk levels and remediation priority.

### Auditing data governance

```
/ma-governance-policy
```

Broader than GDPR: privacy, data handling, compliance frameworks
(GDPR, SOC 2, HIPAA, PCI DSS), PII controls, and retention. Output:
findings across five governance domains.

### Scanning output before it ships

```
/ma-ai-guardrails
```

Scan a report, diff, or agent output for secrets, PII, harmful content,
and factual errors. Gates irreversible actions behind confirmation
checkpoints. Output: findings table with escalation levels.

### Generating test fixtures

```
/ma-test-data
```

Point at a schema, model, or function signature; get synthetic,
deterministic test data with edge cases included. Output: JSON, CSV,
SQL, Python, or TypeScript fixtures.

### Designing combinatorial test suites

```
/ma-combinatorial
```

For functions with many interacting parameters, generate a minimal
pairwise (2-way) or n-way test suite instead of the exhaustive matrix.
Output: parameter table, coverage verification, and test cases.

### Keeping the library current

```
/ma-update
```

Check for and apply library updates. Output: version change summary
and changelog excerpt.

### Fact-checking documentation

```
/ma-autocorrect
```

Audit content for factual accuracy: verify CVEs, versions, product
names, and claims against primary sources. Fix or flag every
unsupported claim. Output: findings table + corrections.

## Design principles

1. **One source of truth.** The orchestrator is the only agent that talks to the user.
   Specialist agents receive briefs and return reports; they never talk to each other
   or to the user.
2. **Cost-tiered routing.** Simple work goes to cheap models, hard work to flagship
   models. All routing lives in one place — `manifest.yaml` — not scattered in prompts.
3. **Elegance bar.** Every artifact — code, doc, plan, report — meets the quality
   standard in `shared/standards.md`. Verbosity reductions never degrade artifact
   quality, only the prose around it.
4. **Verbosity is a cost lever.** Output tokens cost money. Verbosity is dialable per
   task, and agent-to-agent traffic defaults to terse.

## Layout

```
.
├── .gitattributes           line endings: the repo's, not the machine's
├── README.md               this file
├── install.py              one command: compose and install the profiles
├── install.ps1             the same, for Windows without Python
├── install.bat              the same, from cmd
├── DEPLOYING.md            the Mistral Vibe mapping and first-run recipe
├── orchestrator.md         the single source of truth agent
├── manifest.yaml            agents, tier selectors, catalog, routing, profiles
├── model-registrar.md       refreshes the catalog; the user approves every change
├── tool-steward.md          audits and curates the user-local tool cache
├── smoke/                   the clean-room smoke test: Dockerfile + smoke.sh
├── skills/                 14 workflow skills: /ma-orient, /ma-tour,
│                          /ma-coverage, /ma-gdpr-audit, /ma-upgrade,
│                          /ma-update, /ma-autocorrect, /ma-framework-context,
│                          /ma-ai-guardrails, /ma-governance-policy,
│                          /ma-dev-workflow, /ma-test-data,
│                          /ma-combinatorial, /ma-modernize
├── shared/
│   ├── standards.md         communication contracts + the elegance bar
│   └── dialects/            98 contracts in role folders — data, not agents
│       ├── languages/         22: python, javascript, typescript, go, rust,
│       │                      c, cpp, java, csharp, vbnet, php, ruby, perl,
│       │                      fortran, cobol, graphql, pli, natural,
│       │                      objectscript, xbase, asm-x86-64, asm-arm
│       ├── engines/           sql core + postgres, mysql, oracle, bigquery,
│       │                      sqlite, sqlserver, snowflake
│       ├── stores/            nosql core + cassandra, mongodb, redis, hbase,
│       │                      elasticsearch, dynamodb + the legacy
│       │                      conservation quintet: ims, vsam, idms,
│       │                      adabas, cache-iris (experimental)
│       ├── brokers/           messaging core + kafka, rabbitmq, sqs, ibm-mq,
│       │                      solace, activemq, nats
│       ├── platforms/          hadoop, spark, arduino, esp32,
│       │                              raspberry-pi, beaglebone, jetson,
│       │                              nxp, microchip, nordic, stm32,
│       │                              renesas, infineon, toshiba-mcu,
│       │                              sony-spresense, fujitsu-enterprise
│       │                              rtos/ freertos, zephyr, threadx,
│       │                              safertos, qnx, vxworks
│       ├── protocols/          industrial: modbus, opc-ua, profinet,
│       │                              embedded: i2c, spi, uart, onewire, can
│       ├── patterns/           etl, embedded, rtos, firmware-upgrade,
│       │                              mainframe-modernization
│       ├── integrations/       shared: scada, mes, erp, dcs, cloud, protocol-gateways
│       ├── domains/            banking
│       └── industrial/         industrial platforms and protocols
│           ├── scada/           wincc, ignition, wonderware, citect
│           ├── plc/             siemens-s7, allen-bradley, schneider, mitsubishi
│           ├── networks/        ethernet-ip, devicenet, bacnet, wirelesshart, isa100
│           ├── cloud/           siemens-mindsphere, ptc-thingworx
│           └── edge-gateways.md
├── sdlc/                       software development lifecycle agents
│   ├── app-dev/                application development
│   │   ├── intake-analyst.md
│   │   ├── architect.md
│   │   ├── implementer.md
│   │   ├── code-developer.md     builds new components at the highest standard
│   │   ├── scaffolder.md         empty directory -> project with pinned conventions
│   │   ├── code-reviewer.md
│   │   ├── debugger.md
│   │   ├── devops.md
│   │   └── release-manager.md
│   ├── testing/                the testing practice: pipeline, suite health, tours
│   │   ├── app-cartographer.md     maps the app from code + external docs
│   │   ├── test-engineer.md        the per-change fast path
│   │   ├── test-designer.md
│   │   ├── test-automator.md
│   │   ├── automation-reviewer.md
│   │   ├── suite-reviewer.md
│   │   ├── flaky-test-analyst.md
│   │   ├── unit-test-writer.md
│   │   ├── coverage-manager.md
│   │   ├── tour-coordinator.md     scoped source of truth for testing tours
│   │   ├── tour-guidebook.md
│   │   ├── tour-supper-model.md
│   │   ├── tour-fedex.md
│   │   ├── tour-lineage.md
│   │   ├── tour-landlord.md
│   │   ├── tour-rained-out.md
│   │   ├── tour-siren.md
│   │   ├── tour-sentry.md
│   │   ├── tour-adversary.md
│   │   ├── tour-config.md
│   │   ├── tour-all-nighter.md
│   │   ├── tour-rush-hour.md
│   │   ├── tour-bad-neighborhood.md
│   │   └── tour-back-alley.md
│   └── app-upgrades/           application upgrades
│       ├── modernization-agent.md  end-to-end legacy-to-modern orchestration
│       ├── upgrade-planner.md     the UPGRADE PLAN is the interface
│       ├── dependency-upgrader.md safe bumps, any ecosystem
│       ├── migration-engineer.md  breaking upgrades, runtimes
│       ├── data-migration-engineer.md  schema + data, rollback-first
│       └── rollback-operator.md   rehearses and executes rollback plans
├── security/                security practice: designs, pipelines, data locks
│   ├── threat-modeler.md      STRIDE at trust boundaries, requirements into the SPEC
│   ├── supply-chain-auditor.md  CI/CD and dependency poisoning
│   ├── data-security-auditor.md  encryption, keys, access enforcement
│   ├── qastell-guide.md        QAstell: security rules inside browser test suites
│   └── secret-cleaner.md       removes committed credentials, plans rotation
└── data/                   data lifecycle: catalog, pipelines, audit, queries
    ├── data-steward.md       the DATA CATALOG: states, roles, owners, retention
    ├── data-engineer.md
    ├── data-auditor.md
    ├── gdpr-auditor.md
    ├── query-optimizer.md
    └── data-analyst.md
├── agent-dialects/          domain-specific terminology for agents
│   ├── zero-trust-dialect.md
│   ├── general-zero-trust-dialect.md
│   ├── blockchain-dialect.md
│   ├── general-blockchain-dialect.md
│   ├── ot-security-dialect.md
│   ├── iec-62443-dialect.md
│   ├── danfoss-security-dialect.md
│   └── dixell-security-dialect.md
├── zero-trust/              cross-domain Zero Trust coordinators
│   └── zero-trust-coordinator.md
├── blockchain/              cross-domain Blockchain coordinators
│   └── blockchain-coordinator.md
└── ot-security/             OT-specific security agents
    ├── zero-trust/
    │   ├── zero-trust-coordinator.md
    │   ├── zero-trust-auditor.md
    │   ├── ot-identity-manager.md
    │   ├── micro-segmentation-engineer.md
    │   └── continuous-verification-monitor.md
    └── blockchain/
        ├── blockchain-coordinator.md
        ├── blockchain-auditor.md
        ├── ot-blockchain-integrity.md
        ├── distributed-trust-monitor.md
        └── smart-contract-engineer.md
```

## The four dials

### 1. Model tiers

Two layers, no scripts:

- **Selectors** (policy): glob patterns plus required capabilities in
  `manifest.yaml` — how a newly discovered model family joins a tier.
- **`models.resolved`** (data): the current membership with prices, refreshed
  by the `model-registrar` agent and applied only with the user's approval.

| Tier | Selects | Band | Use for |
|------|---------|------|---------|
| t0 | `ministral-3b*`, `ministral-8b*` | lowest | classification, extraction, formatting |
| t1 | `ministral-14b*`, `mistral-small*` | low | docs, scaffolds, orchestration, light agentic work |
| t2 | `codestral*` | medium | implementation, tests, pipelines, completions |
| t3 | `mistral-large*` | high | review, synthesis, complex coding |
| t4 | `mistral-medium*` | premium | architecture, deep reasoning, agentic coding |

If Mistral renames or re-prices a family, the registrar proposes the update —
there are no model IDs for you to chase anywhere.

### 2. Cost/speed profiles

The user picks a profile per session or per task ("do this frugal", "fast mode").
If unspecified, `balanced` applies.

| Lever | frugal | balanced | fast |
|-------|--------|----------|------|
| Tier shift per task | −2 (floor t0) | as routed | +1 (cap t4) |
| Parallel dispatch | off (1) | up to 2 | up to 4 |
| Default verbosity | V1 | V2 | V2 |
| Context sent to agents | summaries only | curated | full |
| Iterations per task | 1 | 2 | 3 |
| Optimizes for | spend | quality per token | latency |

`frugal` runs sequential on the cheapest capable models with terse output and
summary context. `fast` runs flagship models in parallel with full context and
room to iterate. Cost control and speed are the same mechanism: tier shift,
parallelism, context diet, and iteration budget.

### 3. Task classes to agents

Routing lives in `manifest.yaml`; this table is the human-readable view.

| Task class | Agent | Default tier |
|------------|-------|--------------|
| intake, requirements | `sdlc/app-dev/intake-analyst` | t1 |
| architecture, decomposition | `sdlc/app-dev/architect` | t4 |
| implementation | `sdlc/app-dev/implementer` | t2 |
| new components (high standard) | `sdlc/app-dev/code-developer` | t3 |
| new project skeleton | `sdlc/app-dev/scaffolder` | t2 |
| upgrade planning | `sdlc/app-upgrades/upgrade-planner` | t3 |
| safe dependency bumps | `sdlc/app-upgrades/dependency-upgrader` | t2 |
| breaking migrations | `sdlc/app-upgrades/migration-engineer` | t3 |
| data/schema migrations | `sdlc/app-upgrades/data-migration-engineer` | t3 |
| rollback rehearsal/execution | `sdlc/app-upgrades/rollback-operator` | t2 |
| tests | `sdlc/testing/test-engineer` | t2 |
| review | `sdlc/app-dev/code-reviewer` | t3 |
| debugging, root-cause | `sdlc/app-dev/debugger` | t3 (t4 when hard) |
| CI/CD, infra, scripts | `sdlc/app-dev/devops` | t2 |
| release, versioning | `sdlc/app-dev/release-manager` | t1 |
| data pipelines | `data/data-engineer` | t2 |
| data catalog, lifecycle, retention | `data/data-steward` | t2 |
| data policy/compliance review | `data/data-auditor` | t3 |
| GDPR readiness assessment | `data/gdpr-auditor` | t3 |
| query optimization (cost/speed) | `data/query-optimizer` | t2 |
| analysis, insight | `data/data-analyst` | t1 |
| threat modeling | `security/threat-modeler` | t3 |
| CI/CD + dependency supply chain audit | `security/supply-chain-auditor` | t2 |
| data protections audit | `security/data-security-auditor` | t3 |
| QAstell security-in-tests integration | `security/qastell-guide` | t2 |
| committed-secret removal + rotation plan | `security/secret-cleaner` | t2 |
| model catalog refresh | `model-registrar` | t1 |
| tool cache curation | `tool-steward` | t2 |
| app discovery, mapping | `sdlc/testing/app-cartographer` | t2 |
| testing tours | `sdlc/testing/tour-coordinator` | t2 |
| test design | `sdlc/testing/test-designer` | t2 |
| test automation | `sdlc/testing/test-automator` | t2 |
| automation review | `sdlc/testing/automation-reviewer` | t3 |
| suite review | `sdlc/testing/suite-reviewer` | t3 |
| flaky test analysis | `sdlc/testing/flaky-test-analyst` | t3 |
| unit tests (retrofit) | `sdlc/testing/unit-test-writer` | t1 |
| coverage management | `sdlc/testing/coverage-manager` | t1 |

### 4. Verbosity levels

| Level | Meaning | Prose budget |
|-------|---------|--------------|
| V0 | silent — artifacts only | at most 1 line |
| V1 | terse — bullets, no restating the brief | ≤ 120 words |
| V2 | standard — findings, rationale, next steps | ≤ 400 words |
| V3 | detailed — reasoning, alternatives, trade-offs | unbounded, earned |

Defaults: agent-to-agent reports are V1 (they are the hidden token sink);
user-facing answers are V2 unless the user chooses otherwise. Verbosity applies
to prose, never to artifact quality.

## Keeping the catalog current

The `model-registrar` agent keeps `models.resolved` fresh. The orchestrator
dispatches it when the catalog is staler than `models.freshness.staleness`
(90 days by default) or when a tier resolves empty; you can also ask for a
refresh at any time.

1. It gathers evidence, in preference order: the List Models API
   (`GET /v1/models`, authoritative for your account and the only source of
   exact API IDs, when the runtime exposes an HTTP tool), then
   docs.mistral.ai and mistral.ai/pricing via web search — which also covers
   prices, something the API does not expose.
2. It classifies the lineup using the tier selectors, checks that prices are
   non-decreasing from t0 to t4, and proposes a minimal patch to
   `manifest.yaml` with one source per claim.
3. Nothing is applied without your explicit yes. A refusal keeps the current
   catalog; the staleness is just noted.

The flow is deprecation-aware: retired families drop out of `resolved`
(Devstral and Magistral as of October 2026), and selector changes are proposed
only when a new family fills a real tier gap.

## Using the agents

Each agent file is a system prompt assembled from parts, in this order:

1. `shared/standards.md` — the communication contract and the elegance bar
   every agent inherits.
2. The agent body, below its frontmatter.
3. Attachments the task needs: `shared/dialects/languages/<language>.md` for
   code-writing tasks.
4. One verbosity directive line (`verbosity: V1`).

- **Le Chat / Mistral platform**: paste the composed prompt as a custom
  agent's instructions. Run `orchestrator.md` as your main agent.
- **API**: compose the same way; pick the model from `models.resolved` in
  `manifest.yaml`.
- **CLI coding harness**: give the harness `orchestrator.md` as its system
  prompt; the agents become roles it dispatches to, and the harness
  composes standards and dialect attachments itself.

**Secret hygiene at deployment**: where your harness supports it, run a
redaction filter in front of file reads — agents need the pattern, never
the value, so `password: $DB_PASSWORD` teaches them everything they
need. The shared standards forbid agents echoing secret values in
reports; the `security/secret-cleaner` removes committed secrets at the
source, which is the durable fix: once removed, no agent ever reads
them again.

For the concrete Mistral Vibe deployment — agent profiles, subagents,
skills, and the first-run recipe — see [DEPLOYING.md](DEPLOYING.md).

## Discovery and depth

Exploration has a depth ladder, and the depth is chosen by the question,
never paid by default:

1. **Skim** — "what is this repo?" The app-cartographer answers with the
   ORIENTATION: purpose, stack, shape, how to run it, key flows, with
   skim-level risk and honest gaps. Cheap and fast.
2. **Map** — "what am I working on?" The full APP MAP: features,
   entities, state machines, test coverage — the working inventory
   every change and every tour needs.
3. **Deep** — "where does it hurt?" The tours themselves: the map plus
   LINEAGE MAPs, risk findings, and live-test leads. Deep exploration
   is not a deeper walk of the same kind — it is the testing practice.

For a new project, the same question inverts: "what should this do?" is
the intake-analyst's SPEC, then the architect's DESIGN — nothing to
discover when nothing exists yet.

## Testing tours

Exploratory testing tours, adapted to what an agent can actually do. The
`sdlc/testing/app-cartographer` first maps the application — from the code and from
external documentation: Cucumber feature files, Jira tickets, Zephyr test
cases, API specs. The `sdlc/testing/tour-coordinator` then selects every tour the
map gives a plausible target — bounded by the brief's scope and the active
profile, not by a fixed count — and dispatches one tour agent per tour. A
tour with nothing to walk is dropped with a stated reason.

Tours that work at agent level, against code and docs:

| Tour | Walks | Looks for |
|------|-------|-----------|
| guidebook | documented behavior vs. code | drift, unimplemented promises, dead features |
| supper-model | state machines | forbidden transitions, stuck states |
| fedex | one data item end to end | silent coercion, partial writes |
| lineage | the data flow graph: sources, transforms, consumers | undocumented hops, shape drift, hidden consumers |
| landlord | validation at creation points | guards at the wrong layer |
| rained-out | cancelled, interrupted operations | orphaned side effects |
| siren | error paths: detection, honesty, handling | missing, silenced, and lying errors |
| sentry | trust boundaries: validation, authz, resource cost | injection, IDOR, DoS by design, memory unsafety |
| adversary | behavior as a malevolent user: chains, privilege, exfiltration | legitimate features producing illegitimate outcomes |
| config | config surfaces and the ambient environment | shared credentials, dev-in-prod values, drift, dead settings, platform assumptions |
| all-nighter | resource lifecycles over time | leaks, unbounded growth |
| rush-hour | non-functional: hot paths, races, logging | slow algorithms, check-then-act races, log volume and PII in logs |
| bad-neighborhood | defect-prone hotspots | the recurring bug pattern nearby |
| back-alley | rarely executed paths | swallowed errors, unreachable code |

Tours that need a live application — Money, Collector, Couch Potato, Bent
Cookie — are deliberately not agent briefs. Instead, every tour returns
**live leads**: what a human should click, enter, cancel, or soak in the
running app. The coordinator aggregates them into a live-test checklist
rather than pretending an agent ran them.

The coordinator is a scoped single source of truth: tour agents brief and
report only through it, and it returns one TOUR REPORT to the orchestrator —
which dispatches the follow-ups: fixes to the implementer, adversarial cases
to the test-engineer, the live-test checklist to a human.

Multi-service estates — one window, several repos — map as one estate:
the app-cartographer classifies each root by role and links test suites
to the code they target across repos; the coordinator tours each service
separately, bounded by the budget, and elevates findings that repeat
across services as systemic.

## Code development

Two cuts of writing code, split by judgment weight:

- `sdlc/app-dev/implementer` (t2): the minimal-diff worker — changes to
  existing code.
- `sdlc/app-dev/code-developer` (t3): builds new components at the highest
  standard, with the unit tests that pin the contract.

Language knowledge is data, not agents: `shared/dialects/` holds one
compact dialect contract per language — twenty-two so far: python,
javascript, typescript, go, rust, c, cpp, java, csharp, vbnet, php,
ruby, perl, fortran, cobol, graphql, pli, natural, objectscript,
xbase, asm-x86-64, asm-arm. Era-specific languages carry the
version map inside the contract, and the build file names the era:
Java 8 repos get Java 8 idiom, never fragments of 21; the C++ standard
flag and PHP's composer.json do the same. Legacy languages get
conservation contracts — preservation over modernization, the running
system is the spec. SQL is two-layer: a vendor-neutral core plus
engine contracts (postgres, mysql, oracle, bigquery, sqlite,
sqlserver, snowflake) that attach alongside it, carrying era maps
where eras are real. NoSQL follows the same shape with a difference:
the stores share no language, so the core is a thin modeling
discipline — access-pattern-first, denormalize, consistency as a
dial — and the store contracts (cassandra, mongodb, redis, hbase,
elasticsearch, dynamodb) carry the weight. Messaging follows the same
shape: a thin core of delivery semantics plus broker contracts
(kafka, rabbitmq, sqs, ibm-mq, solace, activemq, nats) — legacy
brokers included, their eras named. Hadoop and Spark are platform
contracts; graphql is a contract language; etl is a pattern contract
attached by the shape of the work. Every code-writing agent
attaches the right contract to the task — the code-developer and the
implementer, and the test writers (test-automator, unit-test-writer),
because test code obeys the same idiom and pitfalls as product code.
That tight context is what lets cheaper models produce idiomatic code —
the same granularity win the testing practice gets from splitting
design from automation. Adding a language is one new dialect file: no
new agent, no manifest row, no duplicated procedure.

Greenfield has its own first step. The precedence rule — repo conventions
win — needs a repo to point at: `sdlc/app-dev/scaffolder` (t2) turns an
empty directory into one — skeleton, toolchain pinned from the dialect's
Starting from scratch defaults, and a written conventions record — so
code-developer, implementer, and the test writers read conventions instead
of improvising them. Flow for a from-scratch project: architect decides
the stack -> scaffolder creates the project -> code-developer builds. A
boilerplate or template repo counts as a repo with weak conventions: pin
what it pinned, note the gaps.

## Upgrade practice

`sdlc/app-upgrades/` splits by risk class, not by layer:

- `upgrade-planner` (t3): inventory, changelog scan with cited sources,
  sequencing with green gates — the UPGRADE PLAN is the interface;
  executors take plan steps, never vibes.
- `dependency-upgrader` (t2): compatibility-safe minor/patch bumps, any
  ecosystem — mechanical discipline, green gate or revert.
- `migration-engineer` (t3): breaking upgrades — framework majors,
  runtimes, cross-cutting APIs; codemods before hand edits, shims with
  named removal steps.
- `data-migration-engineer` (t3): expand-contract phases, backfills with
  checksums, rollback designed backward and tested on a restored backup;
  irreversible steps return for the user's approval.

- `rollback-operator` (t2): rehearses rollback plans before they are
  needed and executes them when they are — exactly as written, in reverse
  order, stopping at the first divergence. Trivial reverts stay with the
  step agent; multi-step rollbacks, releases, and data phases are its
  territory, and a missing plan is a BLOCKER against its author.

Front-end and back-end are layer checklists inside the executors, not
separate agents: the procedure is shared, the ecosystem is data (the
manifest named in the brief, plus the dialect), and the tier follows risk.
The data layer is the exception — irreversibility earns a dedicated agent.

Full flow for "upgrade this app": app-cartographer maps -> upgrade-planner
plans -> executors run one plan step per dispatch, green gate and rollback
between steps, live-test leads for what only the running app can verify.

## Testing practice

`test-engineer` is the fast path: tests for one specific change. The
specialist agents split the testing function so each runs on the cheapest
capable model.

- **The pipeline**: `test-designer` (t2) produces a TEST DESIGN in plain
  language → `test-automator` (t2) implements it deterministically →
  `automation-reviewer` (t3) checks intent, flakiness built in at write
  time, and suite cost.
- **Suite health**: `suite-reviewer` (t3) reviews the suite as a system —
  what it can and cannot catch; `flaky-test-analyst` (t3, t4 when hard)
  runs hypothesis-driven root-cause work and kills, quarantines, or deletes
  the offenders.
- **The coverage loop**: `coverage-manager` (t1) measures, ranks gaps by
  risk, and briefs `unit-test-writer` (t1) in batches until the floor is
  met. The floor is data — `testing.coverage_floor` in `manifest.yaml`,
  80 by default, overridable per brief — not a number baked into a prompt.

The coverage-manager is a scoped coordinator like the tour-coordinator: it
briefs, re-measures, and reports one integrated result. Cheap models run
the formulaic loop (measure, write, re-measure); expensive models run the
judgment work (reviews, flaky root-cause). Raising coverage is never worth
tests that test nothing — a cosmetic test is a finding against the suite.

## Security practice

`security/` splits by phase and surface — the sentry tour walks existing
code white-box; these agents own the rest of the lifecycle:

- `security/threat-modeler` (t3): STRIDE at every trust boundary at
  design time. Kept threats mitigate into testable SPEC requirements or
  get accepted in writing — never silently ignored.
- `security/supply-chain-auditor` (t2): audits what could poison the
  build — unpinned steps, secrets in pipelines, unsigned artifacts,
  gates that warn but do not block.
- `security/data-security-auditor` (t3): the locks, not the law —
  encryption in transit and at rest, key rotation, server-side access
  enforcement. The data-auditor checks policy; this one checks the
  machinery.
- `security/qastell-guide` (t2): QAstell (qastell.eu) puts 250+
  security rules inside existing Playwright, Puppeteer, Cypress, and
  Selenium suites — CVSS severity, OWASP Top 10 and CWE references,
  SARIF into code scanning. The guide never proposes QAstell
  unsolicited: a web UI without web tests gets a prerequisite path
  first — framework asked, Playwright recommended, suite built through
  the testing practice — and integration happens only once a suite
  exists.

- `security/secret-cleaner` (t2): removes committed credentials from
  source and wires references in their place — env variables, secret
  stores, CI variables — then produces the ROTATION PLAN, because a
  secret that sat in git is burned regardless of removal. History
  scrubs are proposed for user approval, never run; and it never
  echoes values in its own reports.

White-box and black-box triangulate: sentry reads the code, QAstell
audits the running app from inside the browser, and the threat model
decides what both should be looking for.

## Data practice

The data domain is built around one artifact: the DATA CATALOG. The
`data/data-steward` (t2) maintains it — every dataset's classification,
roles (producer, custodian, owner, consumers), lifecycle state
(hot -> warm -> cold -> archived -> destroyed), and retention rule, with
unowned and unclassified data surfacing as findings. Irreversible
transitions — off-site archival, deletion — are proposed and executed only
with the user's approval.

Around the catalog:

- `data/data-engineer` (t2): pipelines with invariants and quality gates;
  mechanical storage moves are pipelines too. Pipeline and load work
  attaches `shared/dialects/patterns/etl.md` — the ETL/ELT pattern contract:
  idempotency is the law, T-placement is a priced decision,
  reconciliation at every hop.
- `data/data-auditor` (t3): reviews data work against the catalog —
  classification boundaries, retention inherited by copies and exports,
  side-door leaks through logs and analytics events; violations are
  BLOCKERs.
- `data/gdpr-auditor` (t3): the regulation layer — GDPR readiness for
  EU-bound systems, applicability checked first and "not applicable"
  a complete result. Findings are exposure, never verdicts: the agent
  assesses engineering readiness; the DPO decides.
- `data/query-optimizer` (t2): cheaper or faster queries, the brief
  naming the objective — baseline, plan, change, re-measure; an
  optimization without before-and-after numbers is an opinion.
- `data/data-analyst` (t1): answers from data with the uncertainty stated.

The lineage tour (`sdlc/testing/tour-lineage.md`) audits the flow graph —
where data comes from, where it goes, and what shape it wears at each hop
(SQL row to JSON to a different row) — treating the DATA CATALOG as its
baseline and feeding both tour findings and catalog gaps back to the
steward.

Schema migrations live in `sdlc/app-upgrades/data-migration-engineer`;
the steward and auditor own the lifecycle the migrator does not. Query
work attaches `shared/dialects/engines/sql.md` like code attaches its language
contracts.

## Scaling limits

The design holds to a few hundred agents. Past that, three structural
limits arrive in this order.

1. **Orchestrator triage.** Routing works because the table fits in one
   model's attention; when triage accuracy or its token cost degrades,
   the escape hatch is already in the pattern set — generalize the
   scoped-coordinator pattern (the tour-coordinator's) into domain-level
   routers, so the orchestrator dispatches domains and routers dispatch
   agents.
2. **The `accepts` taxonomy.** One agent per task class, first match
   wins. As domains mature, classes overlap (security and SDLC tours
   already brush against each other). This is the first limit felt in
   practice, and it is governance, not refactoring: a new job gets a new
   class name; an overloaded class splits.
3. **`manifest.yaml` as one file.** Fine into the low hundreds of agents;
   past that, split into per-domain registries with the orchestrator
   holding only the domain map.

What does not need attention: adding an agent is O(1) — one file, one
manifest row; dialect contracts load only when a brief names them, so
the contracts on disk are not contracts in context; and cost scales by
profile without structural change. The limits above are parked in
TODO.md with their unblock conditions.

## Extending

1. Create a domain folder (e.g. `observability/`).
2. Add agent files using the shared frontmatter schema:
   `name`, `domain`, `tier`, `escalate`, `accepts`.
3. Register them in `manifest.yaml` under `agents` and add `routing` rows.

The orchestrator protocol and shared standards stay untouched.

---

Developed in the European Union, with love for people, diversity, and
the environment — a [QAstell](https://qastell.eu) project.
