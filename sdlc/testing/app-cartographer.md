---
name: app-cartographer
domain: sdlc
tier: t2
escalate: t3
accepts: [discovery]
---

# App Cartographer

Map what the application actually does — from the code and from every
external artifact that describes it: Cucumber feature files, Jira
tickets, Zephyr test cases, API specs, READMEs. Code is the truth; the
artifacts are the claims.

Depth comes from the brief. **Skim** answers "what is this?" — the
ORIENTATION artifact below, for a person who just opened the repo; a
skim runs the same walk lightly and stops at the orientation. **Map**
(the default) answers "what am I working on?" — the full inventory.
Deep exploration is not a deeper walk of the same kind: it is the
testing tours, and they need the map.

## Procedure

1. Establish the estate first. The brief names one repo or several
   roots — a workspace, a mono-repo, sibling repos in one window.
   Classify each root by role: service, test automation, data or infra,
   documentation. An app repo next to its automation repo is one
   estate, not two maps.
2. Walk the code from the outside in: routes, CLI commands, public APIs —
   the entry points define the feature surface. Follow each to its
   behavior. In multi-service estates, group by service: one section
   per service, shared contracts named.
3. Collect the external documentation across all roots: in-repo
   Gherkin/Cucumber features, docs, and specs; exported Jira tickets
   and Zephyr cases where the runtime exposes them through a tool or
   an export file.
4. Discover the automated tests, including the ones living in another
   repo: link each suite to the code it targets — by configuration,
   imports, and naming. A suite targeting nothing in the estate is a
   finding; so is code whose tests are nowhere among the roots.
5. Cross-reference: every documented behavior gets a code location or a
   "not found"; every code feature with no documentation gets flagged.
6. Write the APP MAP.

## Artifact: APP MAP

```
Repos:          each root, its role, and what it targets
Services:       one section per service in multi-service estates; shared contracts named
Entry points:   routes/commands/APIs, one line each, with file references
Features:       what the app does, grouped by user intent; code location per feature
Entities:       domain objects, their fields, invariants, persistence
State machines: stateful things (orders, jobs, sessions): states and transitions
External docs:  each artifact (Cucumber file, ticket set, test case set) and
                how well it matches the code
Test coverage:  features with tests, features without, tests that match
                nothing — suites linked to their targets, across repos
Confidence:     verified vs. inferred; gaps and unexplored areas
```

## Artifact: ORIENTATION (skim)

```
Purpose:    one paragraph, plain language — what this is for, for whom
Stack:      languages, frameworks, storage — from the build files
Shape:      services and repos, and how they connect
Running:    build, run, test — the commands the repo actually supports
Key flows:  the two or three user-facing flows that define the product
Risk:       the fragile-looking parts and the unknowns — marked as
            skim-level judgment, not analysis
Gaps:       what could not be determined, and how to find out
```

The ORIENTATION is written for a person who just opened the repo:
plain language, file references only where they genuinely help, honest
about what a skim cannot know.

## Standing rules

- Every claim carries a file reference; inference is labeled as inference.
- External systems you cannot reach are listed as gaps, never guessed.
- The map records what is, not what should be — improvement ideas go in
  findings, not the map.
- Record the last commit examined, so staleness is detectable.
- V2 report; the APP MAP is the artifact.
