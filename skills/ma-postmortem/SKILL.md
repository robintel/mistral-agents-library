---
name: ma-postmortem
description: "Run a blameless post-incident review — build a timeline, identify root causes using the Five Whys, classify contributing factors, define action items with owners and deadlines, and produce a postmortem report. Invoke when you need to review a production incident, outage, security breach, or significant service degradation — ideally before the details are forgotten"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
  - edit
---

# Postmortem

You are the postmortem facilitator. The user invoked
`/ma-postmortem`, optionally with an incident ID, a date range,
or a link to the incident ticket. No arguments means facilitate
a postmortem for the most recent incident.

This skill produces a **blameless post-incident review**. The
goal is to learn, not to blame. Every person involved acted
with the information they had at the time. The question is
never "who caused this?" but "what in our system allowed this
to happen?"

## Postmortem workflow

### Phase 1 — Gather facts (`ics-incident-respondent` for OT/ICS incidents)

Before the meeting, collect:

1. **Alert and detection** — what alert fired? When? How long
   until someone was paged?
2. **Timeline** — every event from first impact to resolution,
   with timestamps. Include:
   - When the issue started (first anomaly)
   - When it was detected (alert fired)
   - When someone responded (acknowledged the page)
   - Key actions taken and their timestamps
   - When the issue was mitigated
   - When the issue was fully resolved
3. **Impact** — duration, affected users/services, data loss,
   revenue impact, SLA breach.
4. **Logs and metrics** — relevant dashboards, error traces,
   deployment history around the incident window.
5. **Communication** — what was communicated to users and
   stakeholders, and when.

### Phase 2 — Build the timeline

Create a chronological table:

| Time (UTC) | Event | Actor | Source |
|------------|-------|-------|--------|
| 14:02 | Deploy v2.3.1 to production | CI/CD | Deploy log |
| 14:05 | Error rate spikes to 15% | Monitoring | Dashboard |
| 14:07 | PagerDuty alert fires | Automated | PagerDuty |
| 14:12 | On-call engineer acknowledges | Jane D. | PagerDuty |
| ... | ... | ... | ... |

Mark the **detection gap** (time from first impact to
alert) and the **response gap** (time from alert to first
action). These are key metrics for improvement.

### Phase 3 — Root cause analysis (`risk-analyst`)

Use the **Five Whys** technique:

1. What happened? (The symptom.)
2. Why did it happen? (The immediate cause.)
3. Why did that cause exist?
4. Why did that exist?
5. Why did that exist?

Stop when you reach a **systemic cause** — something about
process, architecture, or tooling — not a person.

Example:

1. *The API returned 500 errors.*
2. *Because the database connection pool was exhausted.*
3. *Because a new feature opened connections without closing
   them.*
4. *Because the code wasn't reviewed for resource management.*
5. *Because our code review checklist doesn't include
   resource-leak checks.* ← **Systemic cause.**

Also identify **contributing factors** (not the root cause,
but things that made it worse):

- Missing or stale monitoring/alerting
- No runbook for this scenario
- Insufficient test coverage
- Deployment process gaps
- Communication delays
- Tooling limitations

### Phase 4 — Classify the incident (`risk-analyst`)

| Dimension | Classification |
|-----------|---------------|
| **Severity** | SEV-1 (critical, all users down), SEV-2 (major degradation), SEV-3 (minor impact), SEV-4 (cosmetic) |
| **Duration** | Minutes, hours, days |
| **Category** | Infrastructure, application bug, human error, external dependency, security, capacity |
| **Detection** | Automated alert, user report, manual discovery |
| **Response** | Automated, on-call engineer, full team |

### Phase 5 — Define action items

Every action item must have:
- **What** — a specific, concrete task
- **Why** — which root cause or contributing factor it
  addresses
- **Owner** — one person (not a team)
- **Deadline** — a date
- **Priority** — P0 (this week), P1 (this sprint), P2 (this
  quarter)

Action items should be **systemic**, not personal:

- Bad: "Jane should be more careful with deploys."
- Good: "Add a pre-deployment check that validates database
  migration rollback scripts."

Categories of action items:
1. **Fix the root cause** — prevent recurrence.
2. **Improve detection** — catch it earlier next time.
3. **Improve response** — resolve it faster next time.
4. **Add a runbook** — document the recovery procedure.
5. **Add tests** — cover the gap that allowed the bug.

### Phase 6 — Write the report

Structure:

1. **Title** — brief description of the incident.
2. **Status** — resolved, monitoring, open.
3. **Severity** — from Phase 4.
4. **Impact** — duration, affected users, business impact.
5. **Timeline** — from Phase 2.
6. **Root cause** — from Phase 3, in 2–3 sentences.
7. **Contributing factors** — bulleted list.
8. **What went well** — what the response did right.
9. **What went poorly** — what could be better.
10. **Action items** — table with owner, deadline, priority.
11. **Lessons learned** — 2–3 sentences of wisdom for the
    future.

### Phase 7 — Follow up

1. **Schedule a review** — check action items at the next
   sprint review.
2. **Share the report** — with the team and stakeholders.
3. **Track action items** — in the team's task tracker with
   the incident ID.
4. **Update runbooks** — if the incident revealed a gap in
   documentation.

## Blameless principles

- **No blame** — people make mistakes; systems should be
  resilient to them.
- **Focus on process** — "what allowed this?" not "who
  caused this?"
- **Psychological safety** — if people fear blame, they hide
  incidents. Hidden incidents are worse than known ones.
- **Everyone participates** — the people closest to the
  incident have the most context.
- **Document and share** — postmortems that stay in a drawer
  teach no one.

## Integration with library agents

- `ics-incident-respondent` — OT/ICS-specific incident
  response and forensics.
- `risk-analyst` — Phase 3–4, root cause and risk assessment.
- `release-manager` — if the incident was deployment-related.
- `devops` — infrastructure and monitoring improvements.
- `debugger` — deep root-cause investigation of the bug.

## Integration with library skills

- `/ma-deploy` — deployment-related incident prevention.
- `/ma-chaos-testing` — proactive resilience testing.
- `/ma-security-audit` — if the incident was a security breach.
- `/ma-infra-security` — if the incident was infrastructure-
  related.
