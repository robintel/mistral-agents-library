# Context Tools

Vetted tools for knowledge graph operations in the Mistral Agents Library.

## Overview

These tools provide persistent knowledge management for agents, enabling:

- **Cross-session memory** - Agents remember what they learned in previous sessions
- **Shared knowledge** - Multiple agents can query and update the same knowledge base
- **Token-optimized context** - Query relevant information without sending entire files
- **Provenance tracking** - Every piece of knowledge knows where it came from

## Tools

### 1. Query Engine (`query.py`)

Executes queries against the knowledge graph using the DSL defined in `knowledge/SCCHEMA.md`.

**Features:**
- Parse and execute knowledge graph queries
- Token-aware result summarization
- Fast indexing for common queries
- Support for GET queries with conditions

**Example:**
```python
from query import QueryEngine

engine = QueryEngine()
result, error = engine.query(
    "GET entities WHERE type=Finding AND repo_id=repo:abc123",
    max_tokens=2000
)

if result:
    print(f"Found {result.total_count} entities")
    for entity in result.entities:
        print(entity)
```

### 2. Storage Engine (`store.py`)

Stores and retrieves entities and relationships from the knowledge graph.

**Features:**
- Append-only JSON Lines storage
- Automatic deduplication by ID
- Schema validation
- Index maintenance
- Session scoping
- Cache management

**Example:**
```python
from store import StorageEngine

engine = StorageEngine()

# Store an entity
entity = {
    "id": "finding:repo:abc123:auth-issue",
    "type": "Finding",
    "severity": "HIGH",
    "title": "Auth Issue",
    "description": "Issue found in auth system"
}

result, errors = engine.store_entity(entity, session_id="session:xyz")

if result.stored:
    print(f"Stored entity: {result.entity_id}")
```

### 3. Session Manager (`session.py`)

Manages agent sessions and their context.

**Features:**
- Session creation and lifecycle management
- Context snapshots
- Decision tracking
- Token usage tracking
- Session history

**Example:**
```python
from session import SessionManager

manager = SessionManager()

# Create a new session
session = manager.create_session(user_intent="Fix auth bug")

# Add agents used
manager.add_agent_used("tour-sentry")
manager.add_agent_used("implementer")

# Store context snapshot
manager.store_context_snapshot({
    "findings": [...],
    "decisions": [...]
})

# End session
manager.end_session()
```

### 4. Summarizer (`summarize.py`)

Provides token-aware summarization of entities and context.

**Features:**
- Token budgeting
- Field prioritization
- Multi-level summaries (brief, standard, detailed, full)
- Entity grouping
- Context block creation

**Example:**
```python
from summarize import Summarizer, SummarizationOptions

summarizer = Summarizer()

# Summarize entities
options = SummarizationOptions(
    max_tokens=2000,
    summary_level="standard"
)

summary_entities, truncated = summarizer.summarize_entities(entities, options)

# Create context block
context_block = summarizer.create_context_block(
    entities, relationships, options
)
```

## Integration

### With the Orchestrator

The context manager integrates with the orchestrator through the brief/report protocol:

**Requesting context in a brief:**
```yaml
BRIEF b1
objective: Fix SQL injection vulnerability
context:
  auto: true
  query: "GET entities WHERE type=Finding AND category=security AND severity=HIGH"
  max_tokens: 2000
task_class: implementation
...
```

**Storing findings in a report:**
```yaml
REPORT b1
status: done
artifacts: [patch:auth.py]
findings:
  - id: finding:repo:abc123:auth-sql-inj-001
    type: Finding
    severity: HIGH
    title: SQL Injection Fixed
    description: Replaced string concatenation with parameterized queries
    provenance:
      source: implementer
      session_id: session:xyz789
...
```

### With Specialist Agents

Specialist agents can use the context tools to:

1. **Query for relevant context:**
   ```python
   from tools.vetted.context.query import get_query_engine
   
   engine = get_query_engine()
   result, error = engine.query(
       "GET entities WHERE type=File AND path LIKE '%auth%'",
       max_tokens=1000
   )
   ```

2. **Store findings:**
   ```python
   from tools.vetted.context.store import get_storage_engine
   
   engine = get_storage_engine()
   engine.store_entity(finding_data, session_id=current_session.id)
   ```

3. **Track session state:**
   ```python
   from tools.vetted.context.session import get_session_manager
   
   manager = get_session_manager()
   manager.store_decision(decision_data)
   ```

## Data Location

All data is stored in `~/.mistral-agents/knowledge/`:

```
~/.mistral-agents/knowledge/
├── graph/
│   ├── entities.jsonl        # All entities
│   ├── relationships.jsonl   # All relationships
│   └── index.json            # Search index
├── sessions/
│   └── {session_id}/
│       ├── context.json      # Session context
│       ├── decisions.jsonl   # Session decisions
│       └── metadata.json     # Session metadata
└── cache/                    # Cached external data
```

## Usage Patterns

### Pattern 1: Session Continuation

```python
# At session start
manager = SessionManager()
session = manager.create_session(user_intent="Continue security audit")

# Check for previous sessions on this repo
query_engine = QueryEngine()
prev_sessions, _ = query_engine.query(
    f"GET entities WHERE type=Session AND metadata.repo_id={repo_id}",
    max_tokens=500
)

if prev_sessions:
    # Load previous findings
    prev_findings, _ = query_engine.query(
        f"GET entities WHERE type=Finding AND repo_id={repo_id}",
        max_tokens=1000
    )
    # Include in current context
    context["previous_findings"] = prev_findings
```

### Pattern 2: Multi-Agent Coordination

```python
# Agent A (tour-sentry) discovers findings
storage = StorageEngine()
for finding in findings:
    storage.store_entity(finding, session_id=session.id)

# Agent B (implementer) queries for work
graph = QueryEngine()
open_findings, _ = graph.query(
    "GET entities WHERE type=Finding AND status=open AND severity=HIGH",
    max_tokens=2000
)

# Process findings
for finding in open_findings:
    # Do work...
    pass
```

### Pattern 3: Context Optimization

```python
# Request minimal context first
context_block = summarizer.create_context_block(
    entities, relationships,
    SummarizationOptions(max_tokens=500, summary_level="brief")
)

# If more detail needed
if context_block.truncated:
    detailed_context = summarizer.create_context_block(
        entities, relationships,
        SummarizationOptions(max_tokens=4000, summary_level="detailed")
    )
```

## Security

### Data Protection

- **No secrets** - API keys, passwords, tokens are never stored
- **No PII** - Personal data is never stored
- **Hash sensitive values** - If you must reference, use hash
- **Redact in transit** - Remove sensitive data before storing

### Validation

All entities are validated before storage:
- Required fields present
- Field types correct
- Enum values valid
- Size limits respected

### Access Control

- **Session isolation** - Agents can only access their own session's data by default
- **Repo scoping** - Context is filtered by repository
- **Read-only by default** - Agents can query; only context-manager can write

## Performance

### Targets

- **Query response time:** < 100ms for simple queries
- **Storage throughput:** 100+ entities/second
- **Index update time:** < 500ms after entity storage
- **Token optimization:** < 10% over budget in 95% of cases

### Optimization Techniques

1. **Indexing** - Maintain indexes for frequently queried fields
2. **Caching** - Cache common queries
3. **Lazy loading** - Only load entity details when needed
4. **Batching** - Batch writes for performance

## Testing

Each tool can be tested independently:

```python
# Test query engine
from query import QueryEngine, QueryResult

engine = QueryEngine()

# Test basic query
result, error = engine.query("GET entities WHERE type=Repository")
assert error is None
assert isinstance(result, QueryResult)

# Test with conditions
result, error = engine.query("GET entities WHERE type=Finding AND severity=HIGH")
assert error is None
```

```python
# Test storage engine
from store import StorageEngine, StoreResult

engine = StorageEngine()

# Test entity storage
entity = {"id": "test:1", "type": "Test", "value": "test"}
result, errors = engine.store_entity(entity)
assert result.stored
assert len(errors) == 0

# Test retrieval
stored = engine._find_entity("test:1")
assert stored is not None
```

## Integration with Mistral Vibe

The tools integrate with Mistral Vibe through:

1. **MCP Server** - Exposes context operations as MCP tools
2. **Connector** - Provides HTTP API for context operations
3. **Direct Import** - Python agents can import and use directly

## Future Enhancements

1. **Vector search** - Semantic search using embeddings
2. **Graph algorithms** - Path finding, clustering, recommendations
3. **Automated summarization** - AI-powered context summarization
4. **Sync with external systems** - Integration with databases, issue trackers
5. **Distributed storage** - Support for multi-machine deployments
