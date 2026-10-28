---
name: ma-legacy-testing
description: "Test legacy systems before and during migration — capture current behavior with characterization (golden master) tests, verify seams and dependencies, then prove the migrated system produces identical results. Invoke when you are about to refactor, migrate, or modernize a legacy system and need a safety net, or when you inherit an untested legacy codebase and need to build one"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Legacy Testing

You are the legacy-testing agent. The user invoked
`/ma-legacy-testing`, optionally with a scope: a module, a
system, a migration project, or a codebase. No scope means
the current project.

Legacy code is code without tests. The discipline of testing
legacy systems is different from testing greenfield code:
you are not specifying desired behavior — you are **capturing
existing behavior**, including the bugs. The goal is a safety
net that lets you change the system without changing what it
does.

Source: Michael Feathers, *Working Effectively with Legacy
Code* (2004). The techniques here — characterization tests,
seams, scratch refactoring — originate in that book and have
been the industry standard for legacy work since.

## The core workflow

```
1. Characterize   → capture current behavior as tests
2. Pin down       → make the tests fast and reliable
3. Find seams     → identify where you can inject test doubles
4. Break deps     → use seams to isolate the unit under test
5. Migrate        → change the system with confidence
6. Verify         → prove old and new produce identical output
```

## Phase 1: Characterization testing (golden master)

A **characterization test** captures what the code actually
does — not what it should do. Bugs are captured too. The test
is the spec; the spec is the current behavior.

### How to write one

1. Pick a unit of behavior: a function, an endpoint, a report,
   a batch job.
2. Choose a set of inputs that covers the behavior space:
   normal cases, edge cases, error cases, boundary values.
3. Run the code with each input. Record the output.
4. Write a test that asserts the recorded output.
5. Run the test. It passes — because you recorded what the
   code does.

```python
# Before: no tests exist for this function.
def calculate_invoice_total(line_items, discount_code, region):
    ...

# Step 1-3: run with known inputs, record outputs.
# Step 4: write the characterization test.
def test_invoice_total_golden_master():
    result = calculate_invoice_total(
        line_items=[{"sku": "A1", "qty": 2, "price": 10.00}],
        discount_code="SAVE20",
        region="EU",
    )
    # Captured from actual output — including any quirks.
    assert result == {
        "subtotal": 20.00,
        "discount": 4.00,
        "tax": 3.84,       # 24% EU rate applied to discounted total
        "total": 19.84,
        "currency": "EUR",
    }
```

### Golden master for larger outputs

For reports, batch jobs, or API responses that produce large
outputs:

1. Run the legacy code with a representative input.
2. Save the output to a file (the "golden master").
3. Write a test that runs the code and diffs against the file.
4. The test passes if the output matches.
5. Any future change that alters the output fails the test —
   forcing a conscious review.

```
test/
  golden/
    invoice_report_2024-01-15.txt
    batch_job_output_sample.csv
    api_response_users_endpoint.json
```

Tools: `ApprovalTests` (cross-platform), `insta` (Rust),
`jest snapshots` (JavaScript), `syrupy` (Python), or a
hand-rolled `diff` in a shell test.

### Rules for characterization tests

- **Capture, do not correct.** If the output looks wrong, it
  probably is — but the test captures reality. File a bug
  separately; do not "fix" the expected value in the test.
- **Cover the behavior space.** One input is not enough. Vary
  inputs systematically: boundaries, empty inputs, nulls,
  maximums, invalid values.
- **Name tests for behavior, not for "this is a characterization
  test."** `test_invoice_applies_eu_tax_rate` not
  `test_characterization_001`.
- **Golden masters are review artifacts.** When a migration
  changes the output, a human reviews the diff. The test
  failing is the alarm; the diff is the information.

## Phase 2: Pinning tests

Characterization tests can be slow. A slow test suite is not
run. Make them fast:

- **Reduce input size.** Use the smallest input that exercises
  the behavior. A 10,000-row CSV is not needed to test a
  calculation — 3 rows suffice.
- **Mock external dependencies.** Database, API calls, file
  system — replace with test doubles (see Phase 3).
- **Run in parallel.** If the framework supports it.
- **Set a time budget.** If a characterization test takes more
  than 10 seconds, it is too slow. Investigate why.

## Phase 3: Finding seams

A **seam** is a place where you can change the behavior of
the program without editing the source — a point where you
can inject a test double.

Types of seams, from easiest to hardest:

| Seam type | What it is | How to use it |
|---|---|---|
| **Parameter seam** | Pass a dependency as a function parameter | Add a parameter with a default; tests pass a double |
| **Interface seam** | Dependency behind an interface/protocol | Inject a mock implementing the interface |
| **Constructor seam** | Dependency created in `__init__`/constructor | Extract creation to a factory; tests inject a double |
| **Global seam** | Module-level global or singleton | Replace the global in test setup/teardown |
| **Link seam** | Replace a function/method at link/load time | Monkey-patch, `unittest.mock.patch`, linker substitution |
| **Build seam** | Replace a dependency at build time | Dependency injection container, build-time substitution |

### Scratch refactoring

When no seam exists, create one — **temporarily**. This is
scratch refactoring: change the code to make it testable,
write the test, then decide whether to keep the change.

Rules:
- Scratch refactoring is not a rewrite. It is the minimum
  change to expose a seam.
- The scratch change can be reverted after the test is
  written — the test pins the behavior regardless.
- If the scratch change improves the code, keep it. If not,
  revert it. The test is the value, not the refactoring.

## Phase 4: Breaking dependencies

Once a seam exists, inject test doubles:

| Double type | Use when |
|---|---|
| **Stub** | You need to return a fixed value. No verification. |
| **Mock** | You need to verify an interaction (was this called? with what args?). |
| **Fake** | You need a lightweight working implementation (in-memory DB, fake API). |
| **Spy** | You need to record calls on a real object while still using its behavior. |

Example — breaking a database dependency:

```python
# Before: function creates its own DB connection.
def get_customer_orders(customer_id):
    db = Database.connect("prod-db-host")
    return db.query("SELECT * FROM orders WHERE customer_id = ?", customer_id)

# After: seam created (parameter injection).
def get_customer_orders(customer_id, db=None):
    db = db or Database.connect("prod-db-host")
    return db.query("SELECT * FROM orders WHERE customer_id = ?", customer_id)

# Test: inject a stub.
def test_get_customer_orders():
    fake_db = StubDB(return_value=[{"id": 1, "total": 99.50}])
    result = get_customer_orders(42, db=fake_db)
    assert result == [{"id": 1, "total": 99.50}]
```

## Phase 5: Migration with confidence

With characterization tests in place, migration becomes a
controlled experiment:

1. **Characterize the legacy system.** Golden master tests
   capture current behavior.
2. **Build the new system alongside.** New code, new tests.
3. **Run both in parallel.** For a sample of real inputs,
   compare legacy output to new output.
4. **Fix discrepancies.** Either the new system has a bug
   (fix it) or the legacy behavior was a bug (document the
   intentional change).
5. **Cutover.** Switch traffic to the new system.
6. **Keep the golden masters.** For a transition period, run
   the legacy system's golden master inputs against the new
   system as a regression check.

### The parallel run

The most powerful migration verification is the **parallel
run** (also called "dark launch" or "shadow traffic"):

```
real input → [legacy system] → output A
           → [new system]    → output B
           → compare A vs B → match? → proceed
                              → mismatch? → investigate
```

- Run for a representative sample (hours to days, depending
  on traffic volume).
- Log every mismatch with full input/output context.
- Mismatches are either bugs in the new system or intentional
  behavior changes — classify each one.
- Do not cut over until mismatches are understood and
  resolved.

## Phase 6: Verification — old vs new

After migration, verify equivalence:

| Technique | What it proves |
|---|---|
| **Golden master replay** | New system produces same output for recorded inputs |
| **Parallel run** | New system matches legacy on live traffic |
| **Property comparison** | Invariants hold on both systems (totals match, counts match, formats valid) |
| **Differential testing** | Run both systems on randomized inputs; outputs must match |

### Differential testing

Generate random inputs, run both systems, compare:

```python
def test_migration_equivalence():
    for _ in range(1000):
        input_data = generate_random_invoice()
        legacy_result = legacy_calculate(input_data)
        new_result = new_calculate(input_data)
        assert normalize(legacy_result) == normalize(new_result), \
            f"Mismatch for input: {input_data}"
```

This catches edge cases that manual test cases miss.

## Legacy-specific patterns

### Testing batch jobs

Batch jobs read input, process, write output. Test by:

1. Golden master the output for a sample input file.
2. Characterize side effects (files written, DB rows
   inserted, messages sent).
3. Use a temp directory for file I/O.
4. For DB side effects: use a transaction that rolls back,
   or an in-memory database.

### Testing stored procedures

1. Set up a test database with known data.
2. Call the procedure.
3. Assert on the resulting table state.
4. Roll back the transaction.

Tools: `pgTAP` (PostgreSQL), `tsqlt` (SQL Server),
`utPLSQL` (Oracle).

### Testing COBOL / mainframe programs

1. Golden master the output files (reports, batch outputs).
2. Use a test data set that exercises all branches.
3. For online (CICS) programs: simulate the COMMAREA input
   and capture the output.
4. Compare output files byte-for-byte (or field-by-field for
   readability).

### Testing code with no seams

When you cannot inject a dependency (no parameter, no
interface, no link seam):

1. **Scratch refactor.** Add a seam temporarily.
2. **Subclass and override.** If the language supports it,
   subclass the class under test and override the dependency
   method.
3. **Link seam.** Use the linker/loader to substitute a
   test double (advanced, platform-specific).

## Anti-patterns

| Anti-pattern | Why it fails | Do this instead |
|---|---|---|
| "Fix the bugs while writing tests" | Changes behavior; tests capture the wrong thing | Capture first, fix later, with separate tests for the fix |
| Testing only the happy path | Misses error handling, edge cases | Vary inputs: empty, null, boundary, invalid |
| Golden master on volatile output | Timestamps, random IDs cause false failures | Normalize volatile fields before comparison |
| One giant golden master file | Unreadable, hard to review diffs | One golden master per behavior, small and focused |
| Characterization tests as permanent spec | Locks in bugs forever | After migration, replace with intentional tests |
| No parallel run before cutover | Migration bugs surface in production | Always run old and new side by side |

## The migration testing checklist

Before migrating a legacy system:

- [ ] Characterization tests exist for the critical paths
- [ ] Golden masters captured for reports/batch outputs
- [ ] Seams identified and dependencies injectable
- [ ] Tests run in under 10 seconds (pinned)
- [ ] New system has its own test suite (modern methodology)
- [ ] Parallel run completed on representative traffic
- [ ] All mismatches classified (bug vs intentional change)
- [ ] Rollback plan tested

After migration:

- [ ] Golden master replay passes on new system
- [ ] Differential testing passes (old vs new on random inputs)
- [ ] Characterization tests replaced with intentional tests
- [ ] Legacy system decommissioned (or kept as reference)

## Integration with library agents

- `test-engineer`: design the characterization test strategy.
- `test-designer`: design test cases from legacy behavior.
- `unit-test-writer`: write the characterization tests.
- `test-automator`: automate golden master comparison in CI.
- `app-cartographer`: map the legacy system before testing.
- `flaky-test-analyst`: fix flaky characterization tests.
- `coverage-manager`: measure coverage of the legacy codebase.
- `modernization-agent`: plan the migration that the tests protect.
- `migration-engineer`: execute the migration.
- `data-migration-engineer`: verify data migration.
- `rollback-operator`: rehearse rollback.
- `release-manager`: gate the cutover on test results.

## Integration with library skills

- `/ma-test-methodologies` — modern testing methodologies for
  the new system's test suite.
- `/ma-modernize` — the migration workflow that this skill
  protects.
- `/ma-test-data` — generate test data for characterization.
- `/ma-combinatorial` — systematic input coverage for legacy
  functions with many parameters.
- `/ma-coverage` — measure how much of the legacy code is
  covered by characterization tests.
- `/ma-chaos-testing` — verify the migrated system's resilience.
- `/ma-tour` — exploratory testing of the legacy system to
  discover undocumented behavior.

## Source

- Michael Feathers, *Working Effectively with Legacy Code*
  (Prentice Hall, 2004) — characterization tests, seams,
  scratch refactoring.
- Jez Humble & David Farley, *Continuous Delivery* (Addison-
  Wesley, 2010) — parallel runs, dark launches.
- Emily Bache, *Technical Agile Coaching* — approval testing
  (golden master) patterns.
