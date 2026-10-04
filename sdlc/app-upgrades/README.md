# Application upgrades

Four agents, split by risk class — the cut that decides procedure and
tier — rather than by layer:

| Agent | Risk class | Tier |
|-------|-----------|------|
| upgrade-planner | assessment: what moves, in what order | t3 |
| dependency-upgrader | compatibility-safe bumps (minor/patch) | t2 |
| migration-engineer | breaking upgrades (majors, frameworks, runtimes) | t3 |
| data-migration-engineer | schema and data migrations | t3 |
| rollback-operator | rehearses and executes rollback plans | t2 |

Front-end and back-end are checklists inside the executors, not separate
agents: the procedure is shared across layers, the ecosystem is data (the
manifest the brief names, plus the dialect in `shared/dialects/languages/`), and the
layer changes the verification, not the work. The data layer is the
exception — irreversibility earns it a dedicated agent.

Flow: the APP MAP from `sdlc/testing/app-cartographer.md` ->
`upgrade-planner`'s UPGRADE PLAN -> executors, one plan step per run,
green gate and rollback between steps. What only the running app can
verify ships as live-test leads, not assumptions.

Rollback plans are first-class: the rollback-operator rehearses them
against a restored backup or staging once the plan exists, and executes
them exactly as written when a green gate fails — reverse apply order,
stop on the first divergence, never improvised.
