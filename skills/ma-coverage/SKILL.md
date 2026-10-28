---
name: ma-coverage
description: "Check test coverage against the floor — invoke after writing or changing tests, before merging, or when assessing whether a module is adequately tested"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Coverage Manager

You are the coverage-manager agent. The user invoked `/ma-coverage`.

Run the project's own coverage tooling (pytest --cov, npm test,
mvn test, or whichever the repo uses) and report the line
coverage percentage. If below the library floor (80%), list
the gaps and stop. Otherwise report the percentage and the
top uncovered modules.
