# TOOL CATALOG

Discovery starts here: map your verb to a tool, check the runtime
line, then invoke. A runtime you do not have: report the missing
verb by name — never emulate a tool silently, never assume a tool
exists because it did in another session.

Headers carry the contract: purpose, provenance, `data: clean`, and
the stable interface. The tool-steward audits and curates; entries
without an honest header are drafts, not tools.

| name | verb | status | runtime | provenance |
|---|---|---|---|---|
| vetted/read-only/find.py | list files recursively | vetted (shipped) | python 3.7+ | library; parity test tools/test/run.sh |
| vetted/read-only/grep.py | search file contents | vetted (shipped) | python 3.7+ | library; parity test tools/test/run.sh |

Shipped tools enter as vetted: the clean-room parity run is their
approved first run. Born tools keep the session's permission gate —
a script the user has not agreed to run once is a draft, not an
entry.
