#!/usr/bin/env python3
"""autocorrect: fact-check added/changed markdown content on a pull request.

Files under shared/ are audited in full, not just their diff lines: every
line there is paid again as context on every downstream task, so one
hallucination propagates everywhere.

Exit codes: 0 = all claims supported, or nothing checkable, or no API key
(skips gracefully); 1 = contradicted or unverified claims found.

Stdlib only. Enabled by the MISTRAL_API_KEY repository secret.
"""
import json
import os
import subprocess
import sys
import urllib.request

MODEL = os.environ.get("AUTOCORRECT_MODEL", "mistral-medium-latest")
API_KEY = os.environ.get("MISTRAL_API_KEY", "")
GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")
BASE = os.environ.get("BASE_REF", "origin/main")
MAX_CHARS = 12000  # per-file payload cap

PROMPT = """You are the fact-checker agent of the Mistral Agents Library.
Verify every checkable factual claim in the content below (identifiers like
CVE/CVSS/CISA/DSA/RFC, versions, years, numbers, product and vendor names,
model names, dated events) against your knowledge.

Return STRICT JSON only, no prose, no code fences:
{"findings": [{"claim": "text of the claim", "verdict": "supported|contradicted|unverified", "correction": "corrected wording or null", "note": "one-line justification"}]}

Rules:
- Style and opinion are not claims; skip them.
- "contradicted" requires a concrete correction in the correction field.
- If you cannot verify a claim, verdict is "unverified" - never guess.
- If there is nothing checkable, return {"findings": []}.
"""


def git(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


def changed_files():
    files = git(f"git diff --name-only --diff-filter=ACMR {BASE}...HEAD")
    keep = []
    for f in (ln.strip() for ln in files.splitlines()):
        if f == "manifest.yaml" or f.endswith(".md"):
            if os.path.isfile(f):
                keep.append(f)
    return sorted(set(keep))


def added_lines(path):
    diff = git(f"git diff {BASE}...HEAD --unified=2 -- {path}")
    return "\n".join(ln[1:] for ln in diff.splitlines()
                     if ln.startswith("+") and not ln.startswith("+++"))


def extract_json(text):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON in model output")
    return json.loads(text[start:end + 1])


def fact_check(path, content, mode):
    body = {"model": MODEL, "messages": [
        {"role": "system", "content": PROMPT},
        {"role": "user",
         "content": f"File: {path} (auditing {mode})\n\n{content}"}]}
    req = urllib.request.Request(
        "https://api.mistral.ai/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {API_KEY}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        payload = json.load(resp)
    return extract_json(payload["choices"][0]["message"]["content"])


def post_comment(report):
    if not GH_TOKEN:
        return
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    try:
        with open(event_path) as fh:
            event = json.load(fh)
        number = event["pull_request"]["number"]
        repo = os.environ["GITHUB_REPOSITORY"]
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/issues/{number}/comments",
            data=json.dumps({"body": report}).encode(),
            headers={"Authorization": f"Bearer {GH_TOKEN}",
                     "Accept": "application/vnd.github+json"})
        urllib.request.urlopen(req, timeout=60).read()
    except Exception as exc:  # posting is best-effort; the check stands
        print(f"autocorrect: could not post PR comment: {exc}")


def main():
    files = changed_files()
    if not files:
        print("autocorrect: no checkable content changed.")
        return 0
    if not API_KEY:
        print("autocorrect: MISTRAL_API_KEY is not configured — "
              "the fact-check gate is skipped. Add the repository secret "
              "to enable it.")
        return 0

    all_findings = []
    for f in files:
        if f.startswith("shared/"):
            with open(f, encoding="utf-8", errors="replace") as fh:
                content, mode = fh.read()[:MAX_CHARS], "full file (shared/)"
        else:
            content, mode = added_lines(f)[:MAX_CHARS], "added lines"
        if not content.strip():
            continue
        print(f"autocorrect: fact-checking {f} ({mode})...")
        try:
            result = fact_check(f, content, mode)
            findings = result.get("findings", [])
        except Exception as exc:
            findings = [{"claim": f"(fact-check of {f} failed)",
                         "verdict": "unverified",
                         "correction": None,
                         "note": f"model call failed: {exc}"}]
        for finding in findings:
            finding["file"] = f
        all_findings.extend(findings)

    bad = [x for x in all_findings
           if x.get("verdict") in ("contradicted", "unverified")]
    supported = sum(1 for x in all_findings if x.get("verdict") == "supported")

    lines = ["## autocorrect: fact-check report",
             "",
             f"Model: `{MODEL}` — {len(all_findings)} claims checked, "
             f"{supported} supported, {len(bad)} needing attention.",
             ""]
    if all_findings:
        lines += ["| Claim | Verdict | Correction / note | File |",
                  "|---|---|---|---|"]
        for x in all_findings:
            corr = x.get("correction") or x.get("note") or ""
            lines.append(f"| {x.get('claim', '')} | {x.get('verdict', '')} "
                         f"| {corr} | {x.get('file', '')} |")
    else:
        lines.append("Nothing checkable found in the changed content.")
    report = "\n".join(lines)

    print(report)
    post_comment(report)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
