# Knowledge Graph & Context Persistence

The knowledge graph is the persistent memory layer for the Mistral Agents Library. It enables:

- **Cross-session context** - Agents remember what they learned in previous sessions
- **Shared knowledge** - Multiple agents can query and update the same knowledge base
- **Token-optimized context** - Query relevant information without sending entire files
- **Provenance tracking** - Every piece of knowledge knows where it came from
- **Relationship mapping** - Understand dependencies between entities

## Architecture

```
~/.mistral-agents/knowledge/
├── graph/                    # Persistent knowledge graph
│   ├── entities.jsonl        # All entities (repos, files, findings, etc.)
│   ├── relationships.jsonl   # Relationships between entities
│   └── index.json            # Search index for fast queries
├── sessions/                 # Session-specific context
│   └── {session_id}/
│       ├── context.json      # Session context snapshot
│       ├── decisions.jsonl   # Decisions made during session
│       └── metadata.json     # Session metadata (timestamp, agents used)
└── cache/                    # Cached external data
    └── {cache_key}/         # Cached API responses, file contents, etc.
```

## Entity Types

| Type | Description | Properties |
|------|-------------|------------|
| Agent | An AI agent | name, domain, tier, capabilities |
| Repository | A code repository | path, fingerprint, language, dependencies |
| File | A source file | path, repo, hash, language, lines_of_code |
| Finding | A discovery or issue | severity, type, location, description, provenance |
| Decision | A choice made | context, rationale, outcome, timestamp |
| Dataset | A data collection | name, schema, size, location, classification |
| Task | A unit of work | id, objective, status, assigned_agent, artifacts |
| Session | An agent session | id, start_time, end_time, agents_used, outcomes |

## Relationship Types

| Type | Description | Example |
|------|-------------|---------|
| produces | Agent produces artifact | Agent -> File |
| consumes | Agent consumes input | Agent -> Dataset |
| depends_on | Dependency relationship | File -> File |
| references | Citation/reference | Finding -> File |
| owns | Ownership | Agent -> Task |
| contains | Containment | Repository -> File |
| validates | Validation relationship | Agent -> Finding |
| resolves | Resolution | Task -> Finding |

## Usage

### For Agents

```yaml
# In a brief, request context from the knowledge graph
context:
  auto: true
  query: "GET entities WHERE type=Finding AND repo='/path/to/repo'"
  max_tokens: 2000
```

### For the Orchestrator

```python
# Store session context
context_manager.store_session(session_id, {
    'findings': [...],
    'decisions': [...],
    'artifacts': [...]
})

# Query for relevant context
context = context_manager.query(
    repo_fingerprint='abc123',
    entity_type='Finding',
    max_tokens=4000
)
```

## Token Optimization

The knowledge graph provides several mechanisms to minimize token usage:

1. **Summarization** - Entities are stored with both full data and summaries
2. **Lazy loading** - Only load details when needed
3. **Token budgeting** - Query results respect token limits
4. **Compression** - Use efficient serialization for large data

## Provenance

Every entity and relationship tracks:
- **source** - Who created it (agent name, session ID)
- **timestamp** - When it was created/modified
- **confidence** - How certain we are (0-1)
- **version** - For tracking changes over time

## Security & Privacy

- **Isolation** - Knowledge is scoped by session and repository
- **No PII** - Personal or sensitive data is never stored
- **Access control** - Agents only access knowledge relevant to their task
- **Expiration** - Session-specific data can be auto-deleted

## Implementation Notes

See the [implementation guide](IMPLEMENTATION.md) for technical details on building context-aware agents.
