---
name: ma-deploy
description: "Run a safe deployment workflow — pre-deployment checks, deployment strategy selection (rolling, blue-green, canary), smoke tests, monitoring during rollout, and rollback procedures. Invoke when deploying to any environment, planning a release, setting up CI/CD pipelines, or when you need a structured rollout with safety checks"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
  - edit
---

# Deploy

You are the deployment coordinator. The user invoked
`/ma-deploy`, optionally with a target environment (staging,
production) and a deployment strategy preference. No arguments
means deploy to production with a canary strategy.

This skill is the **user-facing workflow** for getting code
into production safely. It coordinates the library's DevOps,
release, and rollback specialists.

## Deployment workflow

### Phase 1 — Pre-deployment checks (`release-manager`)

All checks must pass before proceeding. Any failure stops the
deployment.

1. **Tests green** — full test suite passes on the commit
   being deployed.
2. **Code review closed** — no open BLOCKER or MAJOR findings.
3. **No uncommitted changes** — the deployed artifact matches
   the reviewed code exactly.
4. **Dependencies audited** — no new CRITICAL or HIGH CVEs
   introduced.
5. **Configuration verified** — environment variables,
   secrets, and feature flags are correct for the target
   environment. Secrets come from a secret store, never
   committed.
6. **Database migrations reviewed** — migrations are
   backward-compatible (expand, don't contract). Rollback
   migration exists.
7. **Build artifact verified** — the artifact is built from
   the exact commit. Build is reproducible.

### Phase 2 — Choose a deployment strategy (`devops`)

| Strategy | When to use | Risk | Rollback speed |
|----------|-------------|------|----------------|
| **Rolling** | Stateless services, many instances, low risk | Low | Fast (stop rollout, previous version still running) |
| **Blue-Green** | Stateful services, instant rollback needed, database changes | Medium | Instant (switch traffic back) |
| **Canary** | High-traffic services, need real-world validation, gradual confidence | Low | Fast (route traffic back) |
| **Feature Flag** | Incomplete features, A/B testing, gradual feature rollout | Very low | Instant (disable flag) |

**Default recommendation**: Canary for production. Start at
5% of traffic, monitor, then 25%, 50%, 100%.

### Phase 3 — Execute the deployment (`devops`)

#### Rolling deployment
1. Deploy to instances one at a time (or in small batches).
2. Wait for health checks to pass on each instance before
   proceeding to the next.
3. Monitor error rates and latency between batches.

#### Blue-Green deployment
1. Deploy the new version to the green environment (parallel
   to the current blue).
2. Run smoke tests against green.
3. Switch the load balancer to green.
4. Keep blue running for the rollback window (typically 1–2
   hours), then tear down.

#### Canary deployment
1. Deploy the new version to a small subset of instances
   (5% of traffic).
2. Run automated canary analysis: compare error rates,
   latency (p50, p95, p99), and business metrics between
   canary and baseline.
3. If healthy, increase to 25%, then 50%, then 100%.
4. If unhealthy at any stage, halt and roll back.

### Phase 4 — Smoke tests (`test-engineer`)

Run immediately after deployment, before declaring success:

1. **Health endpoint** — returns 200, reports healthy.
2. **Critical path** — the main user flow works end-to-end
   (login → main action → result).
3. **Dependencies** — database, cache, message queue, external
   APIs are reachable and responding.
4. **Version check** — the deployed version matches what was
   intended.

### Phase 5 — Monitor during rollout (`devops`)

Watch these metrics at each stage:

| Metric | Threshold for "healthy" |
|--------|------------------------|
| Error rate | Within 0.5% of baseline |
| Latency p99 | Within 10% of baseline |
| CPU / Memory | Below 80% sustained |
| Database connections | Below connection pool limit |
| Queue depth | Not growing unboundedly |

If any metric breaches its threshold, **halt the rollout**
and investigate.

### Phase 6 — Rollback procedure (`rollback-operator`)

If the deployment fails at any stage:

1. **Halt** — stop the rollout immediately. Do not try to
   fix forward during an active incident.
2. **Assess** — check logs, metrics, and error traces to
   understand the failure.
3. **Execute rollback** — use the pre-rehearsed rollback plan:
   - Rolling: redeploy the previous version.
   - Blue-Green: switch traffic back to blue.
   - Canary: route all traffic back to baseline.
4. **Verify** — run smoke tests against the rolled-back
   version.
5. **Communicate** — notify stakeholders of the rollback and
   the reason.
6. **Post-incident** — if the rollback was triggered by a
   production incident, run `/ma-postmortem`.

### Phase 7 — Post-deployment (`release-manager`)

1. **Tag the release** — annotated git tag with version,
   date, and changelog summary.
2. **Update changelog** — what changed, what was fixed, what
   was added.
3. **Close the release** — mark the deployment as complete in
   your tracking system.
4. **Schedule follow-up** — any deferred items, known issues,
   or tech debt created.

## Deployment checklist

- [ ] All pre-deployment checks pass
- [ ] Deployment strategy selected and justified
- [ ] Rollback plan exists and has been rehearsed
- [ ] Smoke tests defined and automated
- [ ] Monitoring dashboards ready
- [ ] On-call engineer notified
- [ ] Communication plan for stakeholders
- [ ] Deployment window scheduled (avoid Friday afternoons)

## Deployment principles

- **Deploy small, deploy often** — smaller changes are easier
  to roll back and debug.
- **Automate everything** — if you do it twice manually, it
  should be a script.
- **Never deploy on Friday afternoon** — you want the team
  available if something goes wrong.
- **Rehearse rollback** — an untested rollback plan is a
  hope, not a plan.
- **One thing at a time** — don't deploy code and config
  changes simultaneously.

## Integration with library agents

- `devops` — Phases 2, 3, 5: CI/CD, infrastructure, monitoring.
- `release-manager` — Phases 1, 7: release gating and closure.
- `rollback-operator` — Phase 6: rollback execution.
- `test-engineer` — Phase 4: smoke test design and execution.

## Integration with library skills

- `/ma-code-review` — Phase 1 code review gate.
- `/ma-security-audit` — Phase 1 security check.
- `/ma-postmortem` — when a deployment causes an incident.
- `/ma-chaos-testing` — validate resilience before deployment.
- `/ma-upgrade` — when the deployment is a version upgrade.
