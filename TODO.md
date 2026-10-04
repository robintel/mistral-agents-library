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

## Parked — unblock conditions attached

- [ ] Per-language tier defaults (Rust costing more than Python, say):
      unblock when a real workload escalates repeatedly on one language.
      The fix is a manifest data change, never new agents.
- [ ] Manifest whitespace realignment: cosmetic; batch it with the next
      manifest edit.

## Done or absorbed — do not reopen

- ~~more dialects~~ — added java, csharp, vbnet, fortran, cobol; era
  maps inside the contract, conservation contracts for the legacy pair.
- ~~data_lc expansion~~ — built as the `data/` domain: steward, auditor,
  query-optimizer, engineer, analyst.
- ~~security/ domain~~ — built: threat-modeler, supply-chain-auditor,
  data-security-auditor, qastell-guide (with its qualification gate).
