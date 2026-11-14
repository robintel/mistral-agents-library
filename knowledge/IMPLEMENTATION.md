# Knowledge Graph Implementation Guide

This guide covers implementing the knowledge graph and context persistence in your Mistral Agents Library deployment.

## Quick Start

### 1. Install the Knowledge Graph

The knowledge graph is automatically installed with the library. No additional setup is required.

### 2. Verify Installation

```bash
# Check that context tools exist
ls -la ~/.mistral-agents/tools/vetted/context/

# Check knowledge directory
ls -la ~/.mistral-agents/knowledge/
```

### 3. Run a Test Query

```python
from tools.vetted.context.query import QueryEngine

engine = QueryEngine()
result, error = engine.query("GET entities WHERE type=Repository", max_tokens=1000)

if result:
    print(f"Found {result.total_count} repositories")
else:
    print(f"Error: {error.message}")
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Orchestrator                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  1. User Request → Classify → Budget → Dispatch              │ │
│  │  2.                           ↑                                 │ │
│  │  3.                           │ Context Manager               │ │
│  │  4.                           ↓                                 │ │
│  │  5. Agent Briefs ← Query ← Knowledge Graph                  │ │
│  │  6. Agent Reports → Store → Knowledge Graph                   │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Knowledge Graph                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Entities      │  │ Relationships   │  │     Index       │  │
│  │  - Agents       │  │  - contains     │  │  - By type      │  │
│  │  - Repositories │  │  - depends_on   │  │  - By property  │  │
│  │  - Files        │  │  - references   │  │  - By source    │  │
│  │  - Findings     │  │  - produces     │  │  - By target    │  │
│  │  - Decisions    │  │  - resolves     │  │                 │  │
│  │  - Tasks        │  │  - ...          │  │                 │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
│  Session Data   │ │    Cache    │ │ External Systems│
│  - Context       │ │  - API      │ │  - Git          │
│  - Decisions     │ │  - Files    │ │  - Issue Tracker│
│  - Metadata      │ │  - Query    │ │  - CI/CD        │
└─────────────────┘ └─────────────┘ └─────────────────┘
```

## Integration Steps

### Step 1: Update the Orchestrator

Modify the orchestrator to use the context manager for:
- Session management
- Context injection into briefs
- Findings storage from reports

**In `orchestrator.md`, add context management:**

```markdown
## Context Management

At the start of each session:
1. Create a new session with `context-manager`
2. Load relevant context from previous sessions
3. Include optimized context in initial briefs

At the end of each session:
1. Store session outcomes
2. Persist findings and decisions
3. Update knowledge graph

During agent dispatch:
1. Query knowledge graph for relevant entities
2. Include token-optimized context in brief
3. Track provenance of all knowledge
```

### Step 2: Modify Agent Briefs

Update brief templates to include knowledge graph queries:

**Before:**
```yaml
context:
  - file: src/auth.py
  - file: tests/auth_test.py
  - summary: "Previous findings about auth..."
```

**After:**
```yaml
context:
  auto: true
  query: "GET entities WHERE type IN [File, Finding] AND repo_id=repo:abc123 AND path LIKE '%auth%'"
  max_tokens: 2000
  summarize: standard
```

### Step 3: Update Agent Reports

Ensure agents return structured data for storage:

**Before:**
```yaml
findings:
  - Fixed SQL injection vulnerability in auth.py
```

**After:**
```yaml
findings:
  - id: finding:repo:abc123:auth-sql-inj-001
    type: Finding
    severity: HIGH
    category: security
    title: SQL Injection Vulnerability Fixed
    description: Replaced string concatenation with parameterized queries
    location:
      file_id: file:repo:abc123:src:auth.py
      line: 42
    status: resolved
    provenance:
      source: implementer
      session_id: session:xyz789
```

### Step 4: Add Context Manager to Routing

The context manager is already added to `manifest.yaml`:

```yaml
- { name: context-manager, path: knowledge/context-manager.md, domain: knowledge, tier: t2, escalate: t3, accepts: [context-management, knowledge-query, knowledge-store] }

# Routing
context-management: context-manager
knowledge-query: context-manager
knowledge-store: context-manager
```

### Step 5: Test the Integration

Run a test session to verify everything works:

```bash
# Start a new session
vibe --agent orchestrator

# Ask the orchestrator to do some work
# It should automatically use the knowledge graph
```

## API Reference

### Query Engine

```python
from tools.vetted.context.query import QueryEngine, QueryResult

engine = QueryEngine()

# Basic query
result, error = engine.query(
    "GET entities WHERE type=Finding AND severity=HIGH"
)

# With token limit
result, error = engine.query(
    "GET entities WHERE type=File AND repo_id=repo:abc123",
    max_tokens=2000
)

# Get relationships
result, error = engine.query(
    "GET relationships WHERE type=contains AND source_id=repo:abc123"
)
```

### Storage Engine

```python
from tools.vetted.context.store import StorageEngine, StoreResult

engine = StorageEngine()

# Store an entity
entity = {
    "id": "finding:repo:abc123:issue-001",
    "type": "Finding",
    "severity": "MEDIUM",
    "title": "Code smell detected",
    "description": "Function too long"
}

result, errors = engine.store_entity(entity, session_id="session:xyz")

# Store a relationship
relationship = {
    "id": "rel:repo:abc123:contains:file:001",
    "type": "contains",
    "source_id": "repo:abc123",
    "target_id": "file:repo:abc123:src:main.py"
}

result, errors = engine.store_relationship(relationship, session_id="session:xyz")

# Cache external data
engine.cache_data("api:github:repos:abc123", repo_data, ttl_seconds=3600)

# Get cached data
cached = engine.get_cached_data("api:github:repos:abc123")
```

### Session Manager

```python
from tools.vetted.context.session import SessionManager, Session

manager = SessionManager()

# Create session
session = manager.create_session(user_intent="Fix auth bug")

# Add metadata
manager.store_metadata({"repo_id": "repo:abc123", "priority": "high"})

# Add agents used
manager.add_agent_used("orchestrator")
manager.add_agent_used("tour-sentry")

# Store context snapshot
context = {
    "findings": [...],
    "decisions": [...],
    "artifacts": [...]
}
manager.store_context_snapshot(context)

# Store a decision
decision = {
    "question": "Should we upgrade Flask?",
    "answer": "Yes",
    "rationale": "Security improvements"
}
manager.store_decision(decision)

# End session
session = manager.end_session()
```

### Summarizer

```python
from tools.vetted.context.summarize import Summarizer, SummarizationOptions

summarizer = Summarizer()

# Summarize entities
options = SummarizationOptions(
    max_tokens=2000,
    summary_level="standard",
    include_types=["Finding", "File"]
)

summary_entities, truncated = summarizer.summarize_entities(entities, options)

# Create context block
context_block = summarizer.create_context_block(
    entities, relationships, options
)

# Create text summary
text_summary = summarizer.create_text_summary(entities, max_lines=10)
```

## Usage Examples

### Example 1: Continuing a Multi-Session Task

```python
# Session 1: Discovery
from tools.vetted.context.session import SessionManager
from tools.vetted.context.store import StorageEngine

manager = SessionManager()
storage = StorageEngine()

# Start session
session = manager.create_session(user_intent="Security audit of my-project")

# Discover findings
findings = [...]  # From tour-sentry

# Store findings
for finding in findings:
    storage.store_entity(finding, session_id=session.id)

# End session
manager.end_session()

# --- Later, in Session 2 ---

# Start new session
session2 = manager.create_session(user_intent="Fix security issues")

# Query for previous findings
from tools.vetted.context.query import QueryEngine

engine = QueryEngine()
result, _ = engine.query(
    "GET entities WHERE type=Finding AND status=open",
    max_tokens=2000
)

# Include in context
brief_context = {
    "auto": True,
    "query": "GET entities WHERE type=Finding AND status=open AND repo_id=repo:abc123",
    "max_tokens": 2000
}
```

### Example 2: Repository Analysis

```python
from tools.vetted.context.query import QueryEngine
from tools.vetted.context.store import StorageEngine

# Create repo entity
repo = {
    "id": "repo:abc123",
    "type": "Repository",
    "path": "/home/user/my-project",
    "fingerprint": compute_fingerprint(),
    "language": "python",
    "framework": "flask"
}

storage = StorageEngine()
storage.store_entity(repo)

# Analyze files
for file_path in list_files("/home/user/my-project"):
    file_entity = {
        "id": f"file:repo:abc123:{file_path}",
        "type": "File",
        "path": file_path,
        "repo_id": "repo:abc123",
        "hash": compute_file_hash(file_path),
        "language": detect_language(file_path),
        "lines_of_code": count_lines(file_path)
    }
    storage.store_entity(file_entity)
    
    # Create relationship
    storage.store_relationship({
        "id": f"rel:repo:abc123:contains:{file_entity['id']}",
        "type": "contains",
        "source_id": "repo:abc123",
        "target_id": file_entity["id"]
    })

# Query for large files
engine = QueryEngine()
large_files, _ = engine.query(
    "GET entities WHERE type=File AND lines_of_code > 500",
    max_tokens=1000
)
```

### Example 3: Tracking Decisions

```python
from tools.vetted.context.session import SessionManager

manager = SessionManager()

# Make a decision
decision = {
    "id": "decision:session:xyz:upgrade-flask",
    "type": "Decision",
    "context": "Security audit revealed Flask 1.x vulnerabilities",
    "question": "Should we upgrade Flask to 2.x?",
    "answer": "Yes",
    "rationale": "Flask 2.x fixes security issues and is backward compatible",
    "alternatives_considered": ["Use middleware", "Pin version"],
    "impact": "High - requires testing all endpoints",
    "owner": "orchestrator",
    "status": "approved"
}

manager.store_decision(decision)

# Later, query for decisions
from tools.vetted.context.query import QueryEngine

engine = QueryEngine()
decisions, _ = engine.query(
    "GET entities WHERE type=Decision AND status=approved",
    max_tokens=1000
)

for decision in decisions:
    print(f"{decision['question']}: {decision['answer']}")
```

### Example 4: Context-Optimized Briefs

```python
from tools.vetted.context.query import QueryEngine
from tools.vetted.context.summarize import Summarizer, SummarizationOptions

# Query for relevant context
engine = QueryEngine()
result, _ = engine.query(
    "GET entities WHERE type IN [File, Finding] AND repo_id=repo:abc123",
    max_tokens=4000
)

# Summarize for brief
summarizer = Summarizer()
options = SummarizationOptions(
    max_tokens=2000,
    summary_level="standard"
)

context_block = summarizer.create_context_block(
    result.entities, result.relationships, options
)

# Use in brief
brief = {
    "objective": "Fix security issues",
    "context": {
        "auto": True,
        "entities": context_block["entities"],
        "relationships": context_block["relationships"],
        "token_count": context_block["token_count"]
    }
}
```

## Migration Guide

### From File-Based Context

If you're currently passing files directly in context:

**Before:**
```yaml
context:
  - file: src/auth.py
  - file: tests/auth_test.py
```

**After:**
```yaml
context:
  query: "GET entities WHERE type=File AND repo_id=repo:abc123 AND path IN ['src/auth.py', 'tests/auth_test.py']"
  max_tokens: 2000
```

### From Manual Summaries

If you're manually creating summaries:

**Before:**
```yaml
context:
  summary: "The auth system has 3 files with 2 known vulnerabilities..."
```

**After:**
```yaml
context:
  query: "GET entities WHERE type IN [File, Finding] AND repo_id=repo:abc123 AND path LIKE '%auth%'"
  max_tokens: 1000
  summarize: brief
```

### From In-Memory State

If agents use in-memory state:

**Before:**
```python
# In agent code
self.state = {"findings": [...], "files": [...]}
```

**After:**
```python
# Store in knowledge graph
from tools.vetted.context.store import StorageEngine

storage = StorageEngine()
for finding in findings:
    storage.store_entity(finding, session_id=session.id)

# Query when needed
from tools.vetted.context.query import QueryEngine

engine = QueryEngine()
findings, _ = engine.query(
    f"GET entities WHERE type=Finding AND provenance.source={agent_name}",
    max_tokens=2000
)
```

## Testing

### Unit Tests

Each tool has built-in validation and error handling. Test with:

```python
# Test query engine
from tools.vetted.context.query import QueryEngine

engine = QueryEngine()

# Test with empty graph
result, error = engine.query("GET entities WHERE type=Repository")
assert error is None
assert result.total_count == 0

# Test with invalid query
result, error = engine.query("INVALID QUERY")
assert error is not None
assert error.error_type == "syntax_error"
```

### Integration Tests

Test the full workflow:

```python
from tools.vetted.context import QueryEngine, StorageEngine, SessionManager

# Setup
session_manager = SessionManager()
storage = StorageEngine()
query = QueryEngine()

# Create session
session = session_manager.create_session()

# Store entities
storage.store_entity({
    "id": "repo:test",
    "type": "Repository",
    "path": "/test/repo",
    "fingerprint": "test"
}, session_id=session.id)

# Query
result, error = query.query("GET entities WHERE type=Repository")
assert result.total_count == 1

# End session
session_manager.end_session()
```

## Performance Optimization

### Indexing

The knowledge graph maintains indexes for fast querying. Common queries are:

- By entity type: `WHERE type=Finding`
- By repository: `WHERE repo_id=repo:abc123`
- By severity: `WHERE severity=HIGH`
- By relationship type: `WHERE type=contains`

### Caching

Use the cache for expensive operations:

```python
from tools.vetted.context.store import StorageEngine

storage = StorageEngine()

# Cache API response
storage.cache_data(
    "api:github:repos:abc123:issues",
    issues_data,
    ttl_seconds=3600
)

# Retrieve from cache
cached = storage.get_cached_data("api:github:repos:abc123:issues")
```

### Token Optimization

Always specify token budgets:

```python
# Bad - no token limit
result, _ = engine.query("GET entities WHERE type=File")

# Good - with token limit
result, _ = engine.query(
    "GET entities WHERE type=File AND repo_id=repo:abc123",
    max_tokens=2000
)

# Best - with summarization
result, _ = engine.query(
    "GET entities WHERE type=File AND repo_id=repo:abc123",
    max_tokens=1000,
    summarize="standard"
)
```

## Troubleshooting

### Common Issues

**Issue: No results from query**

```python
# Check if entities exist
result, _ = engine.query("GET entities WHERE type=Repository")
print(f"Total repositories: {result.total_count}")

# Check query syntax
result, error = engine.query("GET entities WHERE")
if error:
    print(f"Syntax error: {error.message}")
```

**Issue: Token budget exceeded**

```python
# Reduce max_tokens
result, _ = engine.query(query, max_tokens=1000)

# Or use more aggressive summarization
result, _ = engine.query(query, max_tokens=1000, summarize="brief")

# Or filter more specifically
result, _ = engine.query(
    "GET entities WHERE type=Finding AND severity=HIGH",
    max_tokens=1000
)
```

**Issue: Entity not stored**

```python
# Check validation errors
result, errors = storage.store_entity(entity)
if errors:
    for error in errors:
        print(f"Field {error.field}: {error.message}")

# Check required fields
print(f"Required fields for {entity['type']}: {storage.REQUIRED_FIELDS.get(entity['type'])}")
```

### Debug Mode

Enable verbose logging for debugging:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Now operations will log debug info
from tools.vetted.context.query import QueryEngine

engine = QueryEngine()
result, error = engine.query("GET entities WHERE type=Repository")
```

## Security Considerations

### Data Protection

The knowledge graph automatically:
- Scans for sensitive data (secrets, PII)
- Rejects entities with sensitive fields
- Hashes sensitive references
- Respects data classification

**Never store:**
- API keys, passwords, tokens
- Personal data (names, emails, addresses)
- Financial data
- Health data
- Any data that shouldn't be persisted

### Access Control

By default:
- Agents can only query their own session's data
- Write operations require explicit approval
- Cross-repository access is disabled
- Sensitive data is never returned in queries

**To enable cross-session access:**
```python
# In context manager
session_manager.allow_cross_session_access(session_id, target_session_id)
```

### Audit Trail

All operations are logged:

```python
# View audit log
from tools.vetted.context.query import QueryEngine

engine = QueryEngine()
audits, _ = engine.query(
    "GET entities WHERE type=AuditLog",
    max_tokens=1000
)
```

## Advanced Topics

### Custom Entity Types

You can define custom entity types:

```python
# Define custom type
custom_entity = {
    "id": "custom:my-type:001",
    "type": "CustomType",
    "custom_field": "value"
}

# Store it
storage = StorageEngine()
result, errors = storage.store_entity(custom_entity)

# Query it
engine = QueryEngine()
result, _ = engine.query("GET entities WHERE type=CustomType")
```

**Best practices:**
- Use descriptive type names
- Define required fields
- Document the schema
- Consider adding to SCHEMA.md

### Custom Relationship Types

```python
# Define custom relationship
relationship = {
    "id": "rel:custom:001",
    "type": "custom_relationship",
    "source_id": "entity:001",
    "target_id": "entity:002",
    "properties": {
        "weight": 0.95,
        "reason": "custom reason"
    }
}

# Store it
storage = StorageEngine()
result, errors = storage.store_relationship(relationship)
```

### Batch Operations

For performance, batch operations when possible:

```python
# Store multiple entities
entities = [...]
for entity in entities:
    storage.store_entity(entity, session_id=session.id)

# Then flush index
storage.flush()
```

### Graph Algorithms

You can implement graph algorithms on top of the knowledge graph:

```python
# Find shortest path between two entities
def find_shortest_path(start_id: str, end_id: str, max_depth: int = 5):
    from tools.vetted.context.query import QueryEngine
    
    engine = QueryEngine()
    
    # BFS implementation
    visited = set()
    queue = [(start_id, [])]
    
    while queue:
        current_id, path = queue.pop(0)
        
        if current_id == end_id:
            return path
        
        if current_id in visited:
            continue
        visited.add(current_id)
        
        if len(path) >= max_depth:
            continue
        
        # Get relationships from current entity
        result, _ = engine.query(
            f"GET relationships WHERE source_id={current_id}"
        )
        
        for rel in result.relationships:
            queue.append((rel["target_id"], path + [rel]))
    
    return None  # No path found

# Usage
path = find_shortest_path("repo:abc123", "finding:repo:abc123:issue-001")
```

## Best Practices

### 1. Always Use IDs

- ✅ `repo:abc123` (good)
- ❌ `my-project` (bad - ambiguous)

### 2. Store Before Reference

Always store an entity before creating relationships to it.

### 3. Use Standard Types

Use the standard entity types when possible. Only create custom types when necessary.

### 4. Include Provenance

Always include provenance information:
- Source agent
- Session ID
- Timestamp
- Confidence level

### 5. Deduplicate

Check if an entity exists before storing:
```python
existing = storage._find_entity(entity_id)
if existing:
    # Update
    existing.update(new_data)
    storage.store_entity(existing)
else:
    # Store new
    storage.store_entity(entity)
```

### 6. Version Entities

Use semantic versioning for entities that change.

### 7. Handle Conflicts

If two agents update the same entity, latest write wins (by timestamp).

### 8. Token Budgeting

Always specify token budgets and use summarization.

### 9. Index Usage

Query using indexed fields for best performance.

### 10. Cache External Data

Cache expensive operations (API calls, file reads).

## Support

For issues or questions:

1. Check the documentation in `knowledge/`
2. Review the schema in `knowledge/SCCHEMA.md`
3. Examine example queries and usage patterns
4. Enable debug logging for troubleshooting
5. Ask in the Mistral Agents Library discussions

## Version History

- **v1.0** - Initial implementation
  - Basic entity and relationship storage
  - Query engine with DSL
  - Session management
  - Token-aware summarization
  - Integration with orchestrator
