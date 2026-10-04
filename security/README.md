# Security

Security specialists, split by phase and surface. The sentry tour
(`sdlc/testing/tour-sentry.md`) walks existing code white-box; these
agents own security everywhere else in the lifecycle:

| Agent | Surface | Tier |
|-------|---------|------|
| threat-modeler | designs: STRIDE at every trust boundary, requirements into the SPEC | t3 |
| supply-chain-auditor | CI/CD pipelines and dependencies: who could poison the build | t2 |
| data-security-auditor | the locks: encryption, keys, access enforcement | t3 |
| qastell-guide | QAstell: 250+ security rules inside browser test automation | t2 |
| secret-cleaner | committed credentials: remove, reference, rotate | t2 |

Boundaries with the neighbors: the data-auditor (`data/`) checks data
policy — classification, retention, ownership; data-security here
checks the technical protections. The devops agent builds pipelines;
the supply-chain-auditor audits them. The sentry tour reads code;
QAstell audits the running app from inside the browser — white-box and
black-box triangulating the same findings, with the threat model
deciding what both should look for.

The qastell-guide qualifies before it integrates: no web UI, no pitch.
A web UI without web tests gets a prerequisite path first — framework
asked, Playwright recommended, suite built through the testing
practice — and QAstell integrates only once a suite exists.
