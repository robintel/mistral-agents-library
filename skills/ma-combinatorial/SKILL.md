---
name: ma-combinatorial
description: "Design combinatorial test suites using pairwise or n-way coverage — invoke when a function has many parameters and exhaustive testing is impractical"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Combinatorial Test Design

You are the combinatorial-test agent. The user invoked
`/ma-combinatorial` with a target: a function, a config surface,
an API, or a file path to analyze. The output is a reduced test
suite that covers all parameter interactions at a chosen level.

## Coverage levels

| Level | Name | Guarantees | When to use |
|---|---|---|---|
| 1-way | Single | Every parameter value appears at least once | Smoke test, sanity check |
| 2-way | Pairwise | Every pair of parameter values appears together at least once | Default for most cases; catches ~80% of interaction bugs |
| 3-way | Triple-wise | Every triple of parameter values appears together | Safety-critical, high-risk interactions |
| N-way | Exhaustive | Every combination | Small parameter spaces only (product < 100) |

The default is **2-way (pairwise)**. Escalate to 3-way only when
a specific risk justifies the larger suite.

## Method

1. **Extract parameters.** Read the target and identify every
   parameter that affects behavior: function arguments, config
   keys, environment variables, feature flags, input fields.
   For each, list its possible values (or equivalence classes).
2. **Classify.** Group values into equivalence classes. Values
   that behave identically (e.g., any positive even number) count
   as one class. This reduces the parameter space.
3. **Check size.** Compute the exhaustive product. If it is under
   100, use exhaustive (n-way). Otherwise, use pairwise (2-way).
4. **Generate.** Produce the minimal test suite that covers all
   pairs (or triples). Each test case is one row: parameter
   values plus the expected outcome.
5. **Verify coverage.** Confirm that every pair (or triple)
   appears in at least one test case. Report the coverage matrix.
6. **Report.** V1: parameter table (name, values, classes),
   coverage level, test case count (vs exhaustive count), and
   the test suite itself.

## Example

A function `render_report(format, locale, timezone, currency)`:

| Parameter | Values | Classes |
|---|---|---|
| format | pdf, html, csv, json | 4 |
| locale | en-US, de-DE, ja-JP, fr-FR | 4 |
| timezone | UTC, EST, CET, JST | 4 |
| currency | USD, EUR, JPY, GBP | 4 |

Exhaustive: 4^4 = 256 cases. Pairwise: ~16-25 cases covering
every pair of values across any two parameters.

## Output format

Match the project's test framework:

- **pytest** — `@pytest.mark.parametrize` with a list of tuples.
- **Jest/Vitest** — `it.each` table.
- **JUnit** — `@ParameterizedTest` with `@MethodSource`.
- **Generic** — a markdown table: test ID, parameter values,
  expected outcome.

## Boundaries

- Combinatorial design reduces test count; it does not replace
  edge-case or boundary-value testing. Combine both.
- Do not combinatorially test parameters that are independent
  by design (e.g., a user ID and a timestamp). Only combine
  parameters that interact.
- If the exhaustive product is under 100, always use exhaustive.
  Pairwise is for when the full matrix is too large.
