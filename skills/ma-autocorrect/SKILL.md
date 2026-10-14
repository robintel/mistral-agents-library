---
name: ma-autocorrect
description: Fact-check library content against primary sources; fix or flag every unsupported claim
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Autocorrect

You are the autocorrect agent. The user invoked `/ma-autocorrect`,
optionally with a scope: a file or folder path. No scope means the
whole repository, audited in priority order.

## Priorities

1. `shared/` first, then `manifest.yaml`, then agent and dialect
   definitions, then docs. Every line in `shared/` is paid again as
   context on every downstream task; one hallucination there
   propagates everywhere.
2. Recently changed or added content outranks stable content. For a
   scope, read the git log or the newest entries in `CHANGELOG.md` to
   find it.

## Method

1. **Harvest.** Scan every markdown file in scope for checkable
   claims: identifiers (CVE, CVSS, CISA ICSA, DSA, CERT, RFC),
   numbers (versions, years, IO counts, percentages), named entities
   (vendors, products, standards, model names), URLs, and dated
   events. Style rules and opinions are out of scope — verify facts,
   not taste.
2. **Verify.** Each claim is checked against a primary source —
   vendor advisory, standards body, first-party documentation — via
   web search. Never verify from memory alone. A claim with no
   findable primary source is *unverified*, which is a finding, not a
   pass.
3. **Fix or flag.** What a source contradicts, correct in place
   (wrong year, wrong CVE, wrong model name). What you cannot
   confirm in the session budget, either delete or mark
   `[unverified YYYY-MM-DD]` — never leave it silent.
4. **Report.** One findings table (claim, file, verdict, source,
   correction), then the patch, then a one-line summary:
   `N claims checked, M corrected, K unverified.`

## Known failure modes

All of these were found in this repository (2026-10 audit) — look for
them explicitly: invented CVE identifiers; transposed CVSS scores;
fabricated disclosure timelines with minute-level detail; advisories
attributed to the wrong product; wrong product descriptions
(touchscreen on a DIN-rail unit); "latest version" claims that
silently age; "date-based" mechanisms with no CVE behind them;
corporate ownership that drifted after mergers; series launch years
misremembered (FX 1982 vs the real 1990); and a current product line
described as discontinued legacy.

## Boundaries

- Fix only the claim, never the surrounding style.
- A fix without a source is not a fix; it is a new hallucination.
- `manifest.yaml` model names are verified against Mistral's own
  catalog, not third-party listings.
