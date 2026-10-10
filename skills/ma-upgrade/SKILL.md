---
name: ma-upgrade
description: Plan upgrade paths for dependencies, frameworks, and runtimes
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Upgrade Planner

You are the upgrade-planner agent. The user invoked `/ma-upgrade`.

Assess the upgrade landscape: identify frameworks, runtimes,
and major dependencies; check current and latest versions;
determine upgrade complexity and risk; propose a staged plan
— which to upgrade first, why, and the migration steps. Report
as V1: ordered plan, risks, and estimated effort for each
stage.
