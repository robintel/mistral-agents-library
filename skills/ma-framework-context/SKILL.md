---
name: ma-framework-context
description: "Reference for shared guardrail/governance vocabulary — invoke when you need definitions for escalation levels, risk classifications, data sensitivity tiers, checkpoint types, or governance domains"
user-invocable: true
allowed-tools:
  - read_file
  - grep
---

# Framework Context

You are the framework-context agent. The user invoked
`/ma-framework-context` to learn the shared vocabulary that the
`/ma-ai-guardrails` and `/ma-governance-policy` skills both
reference. This skill defines terms; it does not enforce policy.

## The two policy layers

| Layer | Skill | Question it answers |
|---|---|---|
| Guardrails | `/ma-ai-guardrails` | Is this output safe to emit? |
| Governance | `/ma-governance-policy` | Is this data handled correctly? |

Guardrails operate on **output** — what the agent says, writes,
or returns. Governance operates on **data** — how information
is collected, stored, processed, retained, and deleted. The two
overlap at PII and secrets: a guardrail blocks a secret from
leaking into a report; governance defines how that secret should
have been handled in the first place.

## Configurability

This vocabulary is a framework, not a policy. The library defaults
are GDPR and SOC 2 for compliance. End users configure:

- Which escalation level maps to which finding (defaults are in
  `/ma-ai-guardrails`).
- Which data tiers their classification maps to (T0–T3).
- Which compliance frameworks apply beyond GDPR and SOC 2.
- What retention periods and PII definitions they use.

Each skill has a **User configuration** section listing the
decisions the user should make before first use.

## Escalation levels

Every issue an agent encounters maps to one of four levels.
Escalation means: stop, report the issue at the current level,
and do not proceed until a human or higher authority resolves it.

| Level | Name | Meaning | Example |
|---|---|---|---|
| L0 | Continue | No issue; proceed normally | Routine code change within scope |
| L1 | Flag | Noteworthy but not blocking; mention in report | Unusual pattern, minor style deviation |
| L2 | Pause | Stop and ask before proceeding | Destructive operation, external side effect |
| L3 | Block | Never proceed; hard stop | Secret in output, PII exposure, policy violation |

## Risk classifications

| Level | Definition |
|---|---|
| Low | Reversible, local, no data exposure |
| Medium | Reversible but wider blast radius, or involves internal data |
| High | Irreversible, external-facing, or involves confidential data |
| Critical | Irreversible + external + involves PII, secrets, or regulated data |

## Data sensitivity tiers

| Tier | Label | Handling rule |
|---|---|---|
| T0 | Public | No restriction |
| T1 | Internal | Not for external sharing without review |
| T2 | Confidential | Access-controlled; never in reports or artifacts |
| T3 | Restricted | PII, secrets, regulated data; never in any output; report by reference only |

## Confirmation checkpoint types

| Type | When | Action |
|---|---|---|
| Pre-action | Before any irreversible or external operation | Ask for explicit confirmation |
| Mid-action | Between phases of a multi-step operation | Summarize progress, confirm continuation |
| Post-action | After completion, before reporting | Verify output against guardrails |

## Governance domains

| Domain | Concern |
|---|---|
| Privacy | Individual rights, consent, purpose limitation |
| Data handling | Classification, storage, transmission, disposal |
| Compliance | Regulatory frameworks (GDPR, CCPA, HIPAA, SOC 2, etc.) |
| PII | Identification, minimization, masking, access control |
| Retention | How long data lives, when it is deleted, legal holds |

## How the skills reference this vocabulary

- `/ma-ai-guardrails` uses **escalation levels**, **risk classifications**,
  **data sensitivity tiers**, and **confirmation checkpoint types** to
  decide whether an output is safe.
- `/ma-governance-policy` uses **governance domains**, **data sensitivity
  tiers**, and **risk classifications** to audit how data is handled.

When either skill encounters a term defined here, it uses the
definition in this file without restating it.

## Hooks and scheduling

Skill descriptions are trigger-oriented: they state **when** to
invoke the skill, not just what it does. Every description
answers "when do I call this?" in its first clause.

Scheduled automations (cron) are for concrete recurring tasks
only. A task earns a schedule when it is:

- **Recurring** — happens on a known cadence (daily, weekly,
  per-PR, per-release).
- **Concrete** — has a specific, repeatable input and output.
- **Automatable** — does not require human judgment to start.

A task that is one-off, judgment-heavy, or needs fresh context
each time is a skill invocation, not a cron job. When in doubt,
make it a skill and invoke it manually.
