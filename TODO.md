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
- [x] Add modernization skill (/ma-modernize): workflow skill that
      triggers the modernization-agent to produce MODERNIZATION
      PLANs. Covers replatforming, migration, and modernization
      scenarios; coordinates six phases from request to cutover.
      Also added routing for legacy-migration, re-platform,
      re-architect, and re-factor task classes.
- [ ] Add data-orchestration skill (/orchestrate-data): create the
      workflow skill that triggers the data-orchestrator for data
      synchronization and movement tasks. Unblock: data-orchestrator
      validation on real data estates.
- [ ] accessibility-auditor agent (task class: accessibility-audit):
      WCAG 2.1/2.2 AA review of web frontends — landmarks, labels,
      roles/states, contrast (computed ratios), focus, reduced-motion.
      Evidence: the first real-world run (LaMatusa) had to be handled
      directly by the orchestrator because no routing entry existed;
      the audit carried computed data (contrast math), a severity
      ladder, and a fixed report convention. /ma-a11y-audit workflow
      skill rides along, matching /ma-gdpr-audit.
- [ ] seo-auditor agent (task classes: seo-audit, discoverability,
      local-seo): technical + local SEO review — structured data
      (schema.org), robots/sitemap, canonical history, meta surface,
      NAP consistency, GBP readiness, image/signoff crawlability.
      Evidence: handled ad hoc in the LaMatusa run; the audit shape
      is stable enough to templatize (findings ranked by local-pack
      impact).
- [ ] performance-auditor agent (task class: performance-audit /
      web-vitals): Core Web Vitals review — bundle measurement
      (real builds, chunk-split experiments), font/image render
      path, LCP/CLS/INP attribution, caching headers. Evidence:
      handled ad hoc in the LaMatusa run; distinct from
      query-optimization and chaos-testing (it is static-build
      analysis, not runtime load testing). Consider folding Lighthouse
      runs into the tool cache (~/.mistral-agents/tools/) once a
      HTTP tool exists.
- [ ] e-commerce compliance skill (not an agent): jurisdictional
      pre-launch checklist (RO/OUG consumer law, placeholders in
      legal pages, BREACH-commented audit trail). Not agent material
      — jurisdiction-specific and needs a lawyer's sign-off —
      but a checklist skill would have caught the [CUI]/[email]
      placeholder blockers in the LaMatusa run. Unblock: a second
      jurisdiction needed before writing anything generic.
- [ ] Model-catalog refresh skill (/ma-update-models, working name):
      workflow skill that triggers the model-registrar
      (routing for catalog already exists) — gather sources
      (GET /v1/models with MISTRAL_API_KEY; docs/pricing via web
      search otherwise), drop deprecated, re-tier survivors, propose
      the minimal patch, apply only on the user's explicit yes.
      Mirrors the /ma-modernize pattern: the skill is the user's
      entry point to a specialist's fixed procedure. Unblock:
      MISTRAL_API_KEY in the environment and an HTTP tool in the
      runtime — the same unblock as the catalog-verify item above,
      whose flow this skill would wrap.
- [ ] Tool-cache export skill (/ma-export-cached-tools): package
      ~/.mistral-agents/tools/ (INDEX.md first; run-proofs and
      data-clean headers travel with the tools — they are the birth
      gate, an export without them is worthless on re-import) for
      backup, machine-to-machine moves, or contributing vetted tools
      back into the library's tools/ so install.py ships them by
      default. Design question to settle before writing it: does an
      imported tool re-enter through the same birth gate, or is the
      source machine's run-proof sufficient? Unblockable only after
      the installer wiring item above ships — the round-trip
      (cache -> export -> library -> install -> cache) must be
      provable end to end first.

## Parked — unblock conditions attached

- [x] Dialects - Tier 2 (European): Scaleway Object Storage,
      T-Systems Object Storage, Sovereign Cloud/Gaia-X patterns
- [x] Dialects - Tier 2 (Japanese): NTT Communications Cloud Storage,
      IIJ G.IO Object Storage
- [x] Dialects - Tier 3 (European): IBM i (AS/400) integration patterns,
      FUJITSU Enterprise systems
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
