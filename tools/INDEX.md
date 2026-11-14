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
| vetted/context/query.py | query knowledge graph | vetted (shipped) | python 3.7+ | library; knowledge persistence |
| vetted/context/store.py | store knowledge entities | vetted (shipped) | python 3.7+ | library; knowledge persistence |
| vetted/context/session.py | manage agent sessions | vetted (shipped) | python 3.7+ | library; knowledge persistence |
| vetted/context/summarize.py | summarize context | vetted (shipped) | python 3.7+ | library; knowledge persistence |

Shipped tools enter as vetted: the clean-room parity run is their
approved first run. Born tools keep the session's permission gate —
a script the user has not agreed to run once is a draft, not an
entry.

## Context Tools

The context tools provide persistent knowledge graph operations:

- **query.py**: Execute queries against the knowledge graph using the DSL
- **store.py**: Store and retrieve entities and relationships
- **session.py**: Manage session lifecycle and context snapshots
- **summarize.py**: Token-aware context summarization

All tools are read-only by default for agents. Write operations require
explicit approval or are performed by the context-manager agent.

Data location: `~/.mistral-agents/knowledge/`
