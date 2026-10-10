# TODO

Open threads and parked ideas, each with its unblock condition. Read this
before proposing new work; an item leaves by being done or being killed —
never by silent accumulation.

## Next

- [ ] Wire the tool cache into the installer (tools design, pieces
      2-3): install.py must copy tools/ into the cache location and
      emit the discovery addendum into the subagent profiles —
      verbs, INDEX.md first, runtime line, report the missing verb
      rather than emulating. The ledger (orchestrator.md) is
      already shipped; the parity test (tools/test/run.sh) is green
      on WSL (LF and CRLF legs) and on the Windows filesystem via
      /mnt/c. A Windows-native leg needs a host interpreter — see
      the host-Python item below.
- [ ] Verify Vibe's Linux bundle ships rg/fd the way the Windows
      extension does (rg.exe/fd.exe next to vibe-acp.exe): if it
      does, discovery should prefer the bundled binaries for the
      list/search verbs — native and behaviorally identical on both
      platforms — and the Python cache serves only the verbs no
      binary covers. Unblock: one look inside the Linux CLI install.
- [ ] Host-Python decision for the Windows host: no interpreter
      exists (Store stubs only; the user's install path is
      install.ps1). Either winget-install Python (user approval —
      it is their machine) or accept WSL as the runtime bridge the
      discovery probe used (MSYS_NO_PATHCONV=1 for Git Bash path
      mangling). Unblock: the user's call.
- [ ] Promote the smoke to CI: the clean-room smoke ran green on
      podman (52 profiles, on-target answer, empty tool cache), and
      the parity test is green (install.ps1 == install.py,
      byte-identical). Add the GitHub Actions workflow on tag push:
      the smoke and parity jobs run the existing image; a
      windows-latest job runs install.ps1 natively to cover the
      Windows-only behavior (backslash paths, ANSI decoding).
- [ ] First real-world run: deploy per DEPLOYING.md (orchestrator
      profile + specialist subagents + workflow skills), point it at
      a real repository, and observe which tiers over- or
      under-deliver. The orchestrator's cost discipline collects the
      evidence; the parked items below unlock or die on that
      evidence.
- [ ] Verify the model catalog against the account: `GET /v1/models`
      with `MISTRAL_API_KEY` is the authoritative confirmation of the
      `-latest` aliases recorded in `manifest.yaml` (provenance and
      check date documented there).
- [ ] Catalog refresh when stale: the model-registrar proposes a refresh
      when `models.freshness.checked` ages past `models.freshness.staleness`.
- [ ] Workflow skills verified: wrote the five workflow skills
      (/orient, /tour, /coverage, /gdpr-audit, /upgrade), updated
      both installers to copy them to ~/.vibe/skills/, smoke test
      confirmed they load as slash commands. Native Windows test
      of the skills remains for the CI windows-latest job.
- [ ] Add modernization skill (/modernize): create the workflow skill
      that triggers the modernization-agent to produce MODERNIZATION
      PLANs. Unblock: modernization-agent validation on real estates.
- [ ] Add data-orchestration skill (/orchestrate-data): create the
      workflow skill that triggers the data-orchestrator for data
      synchronization and movement tasks. Unblock: data-orchestrator
      validation on real data estates.

## Parked — unblock conditions attached

- [ ] Per-language tier defaults (Rust costing more than Python, say):
      unblock when a real workload escalates repeatedly on one language.
      The fix is a manifest data change, never new agents.
- [ ] Manifest whitespace realignment: cosmetic; batch it with the next
      manifest edit.
- [ ] Domain-level routers (orchestrator triage ceiling): generalize the
      tour-coordinator pattern so the orchestrator dispatches domains,
      routers dispatch agents. Unblock: repeated misroutes or visibly
      rising triage cost on real runs.
- [ ] `accepts` taxonomy governance: one agent per class, first match
      wins; a class that overlaps between domains splits rather than
      overloads (security vs SDLC tours are the candidates). Unblock:
      the first observed misroute through routing.
- [ ] Per-domain registry split: `manifest.yaml` stays one file into the
      low hundreds of agents. Unblock: the routing table stops fitting
      a single read.

## Done or absorbed — do not reopen

- ~~first clean-room smoke run~~ — green on podman 4.9 via the host
  bridge: image built (one fix — PATH exported before the Vibe
  installer, which exits non-zero otherwise), 52 profiles installed,
  on-target 135-word answer in 13s, tool cache empty (the birth gate,
  headless).

- ~~more dialects~~ — added java, csharp, vbnet, fortran, cobol; era
  maps inside the contract, conservation contracts for the legacy pair.
- ~~data_lc expansion~~ — built as the `data/` domain: steward, auditor,
  query-optimizer, engineer, analyst.
- ~~security/ domain~~ — built: threat-modeler, supply-chain-auditor,
  data-security-auditor, qastell-guide (with its qualification gate).
