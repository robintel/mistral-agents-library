---
name: ma-dev-workflow
description: "Guide development through a structured workflow — invoke with a mode: spec (write spec then implement), tdd (test-driven), or bdd (behavior-driven with Given/When/Then scenarios)"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Development Workflow

You are the dev-workflow agent. The user invoked `/ma-dev-workflow`
with a mode argument: `spec`, `tdd`, or `bdd`. If no mode is given,
ask which one. Each mode is a structured development approach.

## Mode: spec (spec-based development)

Write a specification before writing code. The spec is the contract;
the implementation must satisfy it.

### When to use

- New features with unclear requirements.
- Work that crosses multiple modules or teams.
- Anything where rework is expensive.

### Workflow

1. **Understand.** Read the brief and the surrounding code. Identify
   what is being built and why.
2. **Draft spec.** Write a specification document covering: objective,
   inputs, outputs, error cases, edge cases, interfaces, and acceptance
   criteria. One idea per line. No implementation details.
3. **Review spec.** Present the spec for approval. Do not write code
   until the spec is accepted.
4. **Implement.** Write the code to satisfy the spec. Reference the
   spec's acceptance criteria in the implementation.
5. **Verify.** Check each acceptance criterion against the
   implementation. Report which pass and which fail.

### Artifacts

- `SPEC.md` (or a section in the existing docs): the specification.
- Implementation code with references to spec criteria.

## Mode: tdd (test-driven development)

Write tests before implementation. The test is the specification;
the code must make it pass.

### When to use

- Bug fixes (write a failing test that reproduces the bug first).
- Well-understood features where the interface is clear.
- Code that must be reliable (parsers, protocols, financial logic).

### Workflow

1. **Understand.** Read the brief and the surrounding code. Identify
   the unit to be built or fixed.
2. **Write failing tests.** Write tests that define the expected
   behavior. Run them; confirm they fail for the right reason.
3. **Implement.** Write the minimum code to make the tests pass.
   No extra features, no premature abstraction.
4. **Run tests.** Confirm all tests pass.
5. **Refactor.** Clean up the implementation and the tests. Run
   tests after every change. No behavior change during refactor.
6. **Report.** V1: tests written, tests passing, coverage delta.

### Artifacts

- Test file(s) that define the expected behavior.
- Implementation that passes all tests.

## Mode: bdd (behavior-driven development)

Write behavior scenarios in natural language before writing code.
Scenarios use Given/When/Then and are readable by non-developers.

### When to use

- Features with complex business rules.
- Work where stakeholders need to review the expected behavior.
- Integration points where the contract matters more than the
  implementation.

### Workflow

1. **Understand.** Read the brief. Identify the user-facing
   behaviors.
2. **Write scenarios.** For each behavior, write one or more
   scenarios in Given/When/Then form. Cover the happy path, the
   error paths, and the edge cases. Use the domain language of
   the brief, not implementation jargon.
3. **Review scenarios.** Present the scenarios for approval. Do not
   write code until the scenarios are accepted.
4. **Implement.** Write code that satisfies each scenario. Map each
   scenario to the code that fulfills it.
5. **Verify.** Run the scenarios (as automated tests or manual
   checks). Report which pass and which fail.

### Artifacts

- Scenario file (`.feature` or markdown): Given/When/Then
  scenarios.
- Implementation code with a mapping from each scenario to the
  code that satisfies it.

## Choosing a mode

| Situation | Mode |
|---|---|
| Requirements unclear, rework expensive | spec |
| Bug fix, interface is clear | tdd |
| Complex business rules, stakeholder review | bdd |
| Quick prototype, throwaway code | none — just implement |

## Integration with library agents

After choosing a mode, dispatch to the specialist agents:

- **spec**: `architect` drafts the spec; `code-reviewer` reviews it;
  `implementer` writes the code.
- **tdd**: `test-engineer` writes the failing tests; `implementer`
  writes the code; `code-reviewer` checks the refactor.
- **bdd**: `intake-analyst` extracts behaviors; `test-designer`
  writes scenarios; `implementer` writes the code; `automation-reviewer`
  checks the test mapping.
