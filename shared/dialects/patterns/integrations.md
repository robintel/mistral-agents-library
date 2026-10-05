# Integrations pattern contract

Attaches by the shape of the work — any task calling external
systems through the runtime's tools: Mistral-managed connectors,
MCP servers, or platform connector tools in API deployments. The
mechanism is the harness's; the discipline is yours.

## The law of the session

- Capabilities are discovered, never assumed: the toolset available
  in this session is the source of truth; a tool not in it does not
  exist. A needed capability that is absent: report `needs-input`
  with the exact setup step (a `[[mcp_servers]]` entry, a connector
  in the platform directory) — never simulate the integration.
- Read the tool's documented surface before calling it: its name,
  description, and argument shapes are the contract — guessing them
  is inventing API surface, the qastell-guide's sin on the far side
  of a wire.

## Calling discipline

- Idempotency applies to write-side calls: the etl law — a retried
  write that double-applies is the integration bug class. Know
  which calls are safe to retry, and say so in the plan.
- Rate limits and pagination are real: honor the remote's backoff
  signals, and assume paginated results — one page is a sample, not
  the population (the lineage tour's hidden-consumers rule, across
  the wire).
- Errors from the remote are siren territory: map the remote's
  failure to what it means for the task, honestly — never swallow a
  connector error into a success.
- Consistency windows: remote systems are eventually consistent; a
  write followed by an immediate read may not see the write — state
  the expectation instead of discovering it in a bug.

## Secrets and trust

- Authentication lives in the integration: connectors hold their
  OAuth, MCP servers hold their keys — values never enter briefs,
  reports, or code. The secret-hygiene standard applies with extra
  force past a trust boundary.
- Unvetted servers are never suggested: connecting a new MCP server
  is a user decision with security weight — the platform's own
  guidance — so recommend only what the user or their administrator
  has vetted.
