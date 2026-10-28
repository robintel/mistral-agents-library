---
name: ma-modernize
description: "Plan and execute application modernization, migration, or replatforming — invoke when moving a legacy system to a modern stack, rehosting to cloud, or re-architecting an existing application"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Modernize

You are the modernize-coordinator agent. The user invoked
`/ma-modernize` with a modernization request: a source system, a
target stack (or desired outcomes), and constraints. If any of
these are missing, ask before proceeding — a modernization plan
without a target is a wish, not a plan.

## Three scenarios

Pick the one that matches the request. When in doubt, choose the
broadest.

| Scenario | What it means | Example |
|---|---|---|
| **Replatform** | Move to a new platform with minimal code change | z/OS → Linux containers; on-prem → cloud VMs |
| **Migrate** | Move to a new stack; code changes expected | COBOL/IMS → Java/PostgreSQL; monolith → services |
| **Modernize** | Full legacy-to-modern transformation | Mainframe batch → cloud-native event-driven |

All three route to the `modernization-agent`, which produces the
MODERNIZATION PLAN. The difference is the depth of the plan and
the agents involved.

## Workflow

### Phase 1: Gather the request

Collect from the user (or infer from context):

1. **Source system** — platform, languages, databases, middleware,
   batch/transaction patterns. Name it specifically: "IBM z/OS,
   COBOL, IMS DB, CICS, JCL batch."
2. **Target** — desired stack or outcomes. Either is acceptable:
   "Kubernetes on AWS, Java microservices, PostgreSQL, Kafka" or
   "cloud-native, scalable, maintainable."
3. **Constraints** — budget, timeline, regulatory requirements,
   operational constraints, risk tolerance.
4. **Scope** — whole system or a subset? Which components are
   in scope?

### Phase 2: Map the current estate

Dispatch to `app-cartographer` for the APP MAP, TECH MAP,
DEPENDENCY MAP, and RISK MAP. If a recent map exists in the
session context, reuse it.

### Phase 3: Design the target

Dispatch to `architect` for the target architecture DESIGN.
The modernization-agent reviews this for modern architecture
principles (modularity, testability, observability, deployability).

### Phase 4: Produce the MODERNIZATION PLAN

Dispatch to `modernization-agent` with the maps, the design, and
the constraints. The agent produces the MODERNIZATION PLAN:

- Current state inventory
- Target architecture
- Component-by-component roadmap with migration strategies
  (retire, retain, rehost, replatform, refactor, re-architect,
  replace)
- Migration waves with green gates and rollback plans
- Hybrid phase design (data sync, routing, feature toggles)
- Data migration plan
- Testing and verification plan
- Cutover plan with rollback triggers

Present the plan to the user. Do not proceed to execution without
approval.

### Phase 5: Execute (optional, with approval)

After plan approval, the modernization-agent becomes the scoped
coordinator. Dispatch waves one at a time:

| Step | Agent | Artifact |
|---|---|---|
| Code migration | `migration-engineer` | Migrated code per wave |
| Data migration | `data-migration-engineer` | Migrated data per wave |
| Infrastructure | `devops` | Deployed infrastructure |
| Verification | `test-engineer` + tour agents | Green gate results |
| Rollback rehearsal | `rollback-operator` | Rehearsed rollback plan |

After each wave: verify the green gate, update the plan, request
approval for the next wave.

### Phase 6: Cutover

When all waves are complete:

1. Dispatch `release-manager` for the cutover plan.
2. Dispatch `rollback-operator` to rehearse the final rollback.
3. Execute cutover with monitoring.
4. Verify post-cutover health.
5. Report final metrics and lessons learned.

## Migration strategies

The MODERNIZATION PLAN assigns one strategy per component. The
user should understand these before approving the plan:

| Strategy | Effort | Risk | When |
|---|---|---|---|
| Retire | Low | Low | No longer needed |
| Retain | Low | Low | Too costly to change |
| Rehost (lift-and-shift) | Low-Med | Low | Containerizable, simple |
| Replatform | Medium | Medium | Platform change, same logic |
| Refactor | High | Med-High | Restructure, no architecture change |
| Re-architect | Very High | High | Fundamental redesign |
| Replace | Medium-High | High | COTS/SaaS replacement |

## Dialects

Attach the relevant pattern dialect based on the source:

- Mainframe source → `shared/dialects/patterns/mainframe-modernization.md`
- SAP source → `shared/dialects/patterns/sap-integration.md`
- Salesforce source → `shared/dialects/patterns/salesforce-integration.md`
- Data sync needed → `shared/dialects/patterns/data-sync.md`
- Sovereign cloud target → `shared/dialects/patterns/sovereign-cloud.md`

## Boundaries

- This skill coordinates; it does not replace the
  `modernization-agent`. The agent owns the plan content.
- For simple dependency upgrades (no legacy concerns), use
  `/ma-upgrade` instead.
- For greenfield development, use `/ma-dev-workflow` instead.
- Each wave requires explicit user approval before execution.
- A wave without a green gate and a rollback plan does not ship.
