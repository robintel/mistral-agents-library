---
name: ma-test-methodologies
description: "Apply modern testing methodologies — choose and execute the right approach (TDD, BDD, ATDD, property-based, mutation, contract testing) for your context. Invoke when you need to decide how to test, which methodology fits the problem, or how to introduce a methodology into an existing codebase"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Test Methodologies

You are the test-methodologies agent. The user invoked
`/ma-test-methodologies`, optionally with a methodology name
(`tdd`, `bdd`, `atdd`, `property`, `mutation`, `contract`) or
a scope: a codebase, a feature, a team. No scope means help
choosing.

This skill is a decision guide and playbook for modern testing
methodologies. It answers: which methodology fits this context,
how to run it, what tools to use, and how to measure success.
It is not a substitute for the library's testing agents — it
tells you when to dispatch `test-engineer`, `test-designer`,
`unit-test-writer`, or `test-automator` and with what brief.

## The methodology map

| Methodology | What it tests | When it wins | When it loses |
|---|---|---|---|
| **TDD** | Unit-level correctness | Logic-heavy code, algorithms, APIs with clear contracts | UI-heavy work, exploratory prototypes, throwaway code |
| **BDD** | Business behavior | Stakeholder-facing features, complex business rules, regulated domains | Internal utilities, performance-critical paths, simple CRUD |
| **ATDD** | Acceptance criteria | Cross-team alignment, compliance requirements, customer-facing features | Solo development, internal tools |
| **Property-based** | Invariants across inputs | Algorithms, parsers, serializers, math, data transformations | Stateful systems, I/O-bound code, UI interactions |
| **Mutation** | Test suite quality | Mature codebases, critical paths, regression-prone modules | Early-stage code, thin test suites, throwaway code |
| **Contract** | Service boundaries | Microservices, API integrations, event-driven systems | Monoliths, tightly-coupled systems, single-service apps |
| **Snapshot** | UI/output stability | Frontend components, report generation, CLI output | Data-heavy logic, APIs, anything with intentional change |

## TDD — Test-Driven Development

**The loop:** Red → Green → Refactor.

1. **Red:** Write a failing test that describes one behavior.
   Run it. It must fail for the right reason.
2. **Green:** Write the minimum code to make it pass. No
   extra. Run it. It must pass.
3. **Refactor:** Clean up the code and the test. Run the full
   suite. Everything must stay green.

**Rules:**
- One assertion per test (one behavior per test).
- Test names describe behavior, not implementation:
  `test_rejects_expired_token` not `test_auth_function`.
- The test is the spec: if you cannot write the test, you do
  not understand the requirement.
- Refactor is not optional: the third step is where design
  happens.

**Tools by ecosystem:**

| Ecosystem | Framework |
|---|---|
| Python | pytest, unittest |
| JavaScript/TypeScript | Jest, Vitest, Mocha |
| Java | JUnit 5, TestNG |
| C# | xUnit, NUnit, MSTest |
| Go | `testing` (stdlib), testify |
| Rust | `cargo test` (stdlib), rstest |
| Ruby | RSpec, Minitest |

**Common failure modes:**
- Testing implementation, not behavior (brittle, breaks on
  refactor).
- Skipping the refactor step (TDD without refactor is just
  "tests first" — the design debt accumulates).
- Writing tests after the code and calling it TDD.

## BDD — Behavior-Driven Development

**The loop:** Discovery → Formulation → Automation.

1. **Discovery:** Three Amigos (dev, tester, business) explore
   the feature. What should it do? What could go wrong?
2. **Formulation:** Write scenarios in Given/When/Then:
   ```gherkin
   Scenario: Reject expired discount code
     Given a customer has a cart with items
     And the discount code "SAVE20" expired yesterday
     When the customer applies the discount code
     Then the discount is not applied
     And the customer sees "This code has expired"
   ```
3. **Automation:** Implement step definitions. The scenario
   becomes an executable test.

**Rules:**
- Scenarios are business-readable. If a stakeholder cannot
  read it, it is too technical.
- One scenario per behavior. Multiple And steps are fine;
  multiple Whens are a smell.
- Background for shared setup; Scenario Outline for data
  tables.
- Living documentation: the scenarios are the spec. Keep them
  current.

**Tools:**

| Ecosystem | Framework |
|---|---|
| Cross-platform | Cucumber (Gherkin), SpecFlow (.NET), Behave (Python), Godog (Go) |
| JavaScript | Jest + jest-cucumber, Vitest |
| Python | behave, pytest-bdd |
| Java | Cucumber-JVM, JBehave |

**Common failure modes:**
- Step definitions that are too generic ("Given a user" does
  everything — unmaintainable).
- Scenarios that test the UI, not the behavior (slow, flaky).
- BDD without the Discovery step (writing Gherkin for
  already-built features — theater, not collaboration).

## ATDD — Acceptance Test-Driven Development

ATDD extends TDD to the acceptance level: the acceptance
criteria are written as executable tests **before** development
starts. The team agrees on the criteria, writes the tests, and
the feature is done when the tests pass.

**The loop:**

1. **Define acceptance criteria** with stakeholders (user
   stories with explicit acceptance conditions).
2. **Write acceptance tests** that verify each criterion.
3. **Develop** until the tests pass.
4. **Demo** the passing tests to stakeholders.

**Difference from BDD:** BDD focuses on behavior specification
(Gherkin scenarios); ATDD focuses on acceptance criteria as the
definition of done. ATDD tests may not use Gherkin — they can
be any executable test format.

**When to use:** compliance-driven domains (finance, healthcare,
government), customer-facing features with contractual SLAs,
any feature where "done" must be provable.

## Property-Based Testing

Instead of writing examples, you write **properties** (invariants
that must hold for all valid inputs) and the framework generates
random inputs to try to break them.

```python
# Example: Hypothesis (Python)
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    assert sorted(sorted(lst)) == sorted(lst)

@given(st.text())
def test_encode_decode_roundtrip(s):
    assert decode(encode(s)) == s
```

**What it finds:** edge cases you did not think of — empty
inputs, boundary values, Unicode corner cases, integer overflow,
concurrency interleavings.

**Rules:**
- Properties are universal statements: "for all inputs, X holds."
- When a property fails, the framework shrinks the input to the
  minimal failing case. Fix the bug, not the test.
- Properties complement examples — they do not replace them.
  Example-based tests document intent; property tests find
  surprises.

**Tools:**

| Ecosystem | Framework |
|---|---|
| Python | Hypothesis |
| JavaScript/TypeScript | fast-check |
| Java | jqwik, QuickTheories |
| C# | FsCheck (.NET) |
| Go | gopter, rapid |
| Rust | proptest, quickcheck |
| Ruby | Rantly |
| Haskell | Hedgehog, QuickCheck |
| Erlang | PropEr |
| Elixir | PropCheck, StreamData |

**Common failure modes:**
- Properties that are tautologies ("output is a list" — true
  by construction).
- Non-deterministic code under test (random failures that
  cannot be reproduced).
- Shrinking that takes longer than the test itself (large
  input spaces).

## Mutation Testing

Mutation testing measures the **quality of your test suite**,
not the quality of your code. It works by:

1. Run your test suite. All tests must pass.
2. Introduce small mutations (bugs) into the code: change `>`
   to `>=`, swap `+` for `-`, remove a statement.
3. Run the test suite again. If tests still pass, the mutation
   **survived** — your tests did not catch it.
4. Report: mutation score = killed mutations / total mutations.

A mutation score of 80%+ is healthy. Below 60% means the test
suite has significant gaps.

**Rules:**
- Mutation testing is slow. Run it in CI, not on every save.
- Focus on critical modules, not the entire codebase.
- Surviving mutants are findings: either the test gap is real
  (write a test) or the mutant is equivalent (the mutation
  does not change behavior — document and move on).

**Tools:**

| Ecosystem | Tool |
|---|---|
| JavaScript/TypeScript | Stryker |
| Java | PIT (Pitest) |
| C# | Stryker.NET |
| Python | mutmut, cosmic-ray |
| Go | go-mutesting |
| Rust | cargo-mutants |

## Contract Testing

Contract testing verifies that service boundaries honor their
agreements. Each consumer defines what it expects; each
provider verifies it can satisfy those expectations.

**The workflow:**

1. **Consumer** writes a contract: "When I GET /api/users/123,
   I expect a 200 with `{id: number, name: string}`."
2. **Consumer** runs its tests against a mock provider using
   the contract.
3. **Provider** verifies it satisfies all consumer contracts
   in its CI pipeline.
4. If the provider changes its API, the contract tests fail
   before deployment.

**Rules:**
- Contracts are consumer-driven: the consumer defines what it
  needs, not what the provider offers.
- Run provider verification in CI: a contract break blocks
  deployment.
- Contracts are not integration tests: they test one interaction
  in isolation, not the full flow.

**Tools:**

| Tool | Notes |
|---|---|
| **Pact** | The standard. Consumer-driven, multi-language. |
| **Spring Cloud Contract** | JVM ecosystem. Producer or consumer-driven. |
| **Specmatic** | Open-source, OpenAPI-based. |
| **Schemathesis** | Python, OpenAPI/GraphQL fuzzing + contract validation. |

## Snapshot Testing

Capture the output of a function or component and compare it
against a stored "snapshot." Any change to the output fails the
test, forcing a human to review and approve the diff.

**Best for:** UI components, report generation, CLI output,
serialized data formats, error messages.

**Rules:**
- Snapshots are review artifacts, not oracles. A human must
  approve every snapshot change.
- Do not snapshot volatile data (timestamps, random IDs,
  memory addresses).
- Keep snapshots small: snapshot the output, not the entire
  object graph.

**Tools:** Jest/Vitest (JavaScript), insta (Rust), syrupy
(Python),ApprovalTests (cross-platform).

## Choosing a methodology

```
What are you building?
├── Logic/algorithm → TDD + Property-based
├── Business feature → BDD (+ ATDD if compliance-driven)
├── Service boundary → Contract testing
├── UI component → Snapshot + visual regression
├── Critical path → TDD + Mutation testing
└── Integrating services → Contract + BDD
```

Stack methodologies — they complement each other:

| Layer | Methodology |
|---|---|
| Unit | TDD |
| Integration | Contract testing |
| Behavior | BDD |
| Quality gate | Mutation testing |
| Invariants | Property-based testing |

## Measuring success

| Methodology | Metric | Target |
|---|---|---|
| TDD | Tests written before code | 100% of new features |
| BDD | Scenarios per feature | 3-7 scenarios |
| Property-based | Properties per function | 1-3 invariants |
| Mutation | Mutation score | >80% on critical modules |
| Contract | Contract coverage | 100% of service boundaries |
| Snapshot | Snapshot review time | <1 day per change |

## Integration with library agents

- `test-engineer`: design and implement the test strategy.
- `test-designer`: design test cases from requirements.
- `unit-test-writer`: write unit tests in the repo's framework.
- `test-automator`: automate test execution in CI/CD.
- `flaky-test-analyst`: investigate and fix flaky tests.
- `coverage-manager`: measure and enforce coverage floors.
- `suite-reviewer`: review the test suite for quality gaps.
- `automation-reviewer`: review test automation quality.

## Integration with library skills

- `/ma-dev-workflow tdd` — TDD as a development workflow (build
  with TDD). This skill covers TDD as a testing methodology
  (how to test, what to test).
- `/ma-dev-workflow bdd` — BDD as a development workflow.
- `/ma-combinatorial` — combinatorial test design for many-
  parameter functions.
- `/ma-test-data` — synthetic test data generation.
- `/ma-coverage` — coverage measurement and enforcement.
- `/ma-tour` — exploratory testing tours.
- `/ma-chaos-testing` — resilience testing under failure.
- `/ma-legacy-testing` — characterization and migration testing
  for legacy systems.
