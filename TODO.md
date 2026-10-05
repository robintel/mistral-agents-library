# TODO

Open threads and parked ideas, each with its unblock condition. Read this
before proposing new work; an item leaves by being done or being killed —
never by silent accumulation.

## Next

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
- [ ] Workflow skills (/orient, /tour, /coverage, /gdpr-audit,
      /upgrade): the profiles ship via `install.py`; the SKILL.md
      content does not exist yet. Write the five skills, then teach
      `install.py` to place them in `~/.vibe/skills/`.

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

- ~~more dialects~~ — added java, csharp, vbnet, fortran, cobol; era
  maps inside the contract, conservation contracts for the legacy pair.
- ~~data_lc expansion~~ — built as the `data/` domain: steward, auditor,
  query-optimizer, engineer, analyst.
- ~~security/ domain~~ — built: threat-modeler, supply-chain-auditor,
  data-security-auditor, qastell-guide (with its qualification gate).
