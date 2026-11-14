# Knowledge Graph Pattern Contract

This contract defines patterns for working with the persistent knowledge graph.
It attaches to context management tasks and provides guidelines for:
- Entity modeling
- Relationship design
- Query patterns
- Context optimization

## Core Principle

**Knowledge should be queryable, not manually curated.**

Instead of sending entire files as context, agents should:
1. Query the knowledge graph for relevant entities
2. Request token-optimized summaries
3. Store findings and decisions for future sessions

## Entity Modeling Patterns

### Pattern 1: Repository Fingerprinting

Every repository gets a unique fingerprint based on its path and content:

```python
# How to create a repo fingerprint
def create_repo_fingerprint(repo_path: str) -> str:
    # Use path hash + last commit hash if available
    path_hash = hashlib.sha256(repo_path.encode()).hexdigest()[:8]
    # In practice, include git commit hash or file hashes
    return f"repo:{path_hash}"
```

**When to use:** When you need to reference a repository across sessions.

**Example entity:**
```json
{
  "id": "repo:abc123",
  "type": "Repository",
  "path": "/home/user/my-project",
  "fingerprint": "sha256:abc123...",
  "language": "python",
  "framework": "flask",
  "size_bytes": 1024000
}
```

### Pattern 2: File Identity

Every file is uniquely identified by its repository and path:

```python
# How to create a file ID
def create_file_id(repo_id: str, file_path: str) -> str:
    # Normalize path (remove leading ./ or /)
    normalized_path = file_path.lstrip("./").replace("/", ":")
    return f"file:{repo_id}:{normalized_path}"
```

**When to use:** When referencing specific files in findings or tasks.

**Example entity:**
```json
{
  "id": "file:repo:abc123:src:auth.py",
  "type": "File",
  "path": "src/auth.py",
  "repo_id": "repo:abc123",
  "hash": "sha256:def456...",
  "language": "python",
  "lines_of_code": 150
}
```

### Pattern 3: Finding Tracking

Findings are the primary output of analysis agents. They should be:
- **Unique** - Each finding has a unique ID
- **Reproducible** - Can be re-verified
- **Actionable** - Include clear recommendations
- **Traceable** - Link to source code

```json
{
  "id": "finding:repo:abc123:auth-sql-injection-001",
  "type": "Finding",
  "severity": "HIGH",
  "category": "security",
  "title": "SQL Injection Vulnerability",
  "description": "String concatenation in SQL query at line 42",
  "location": {
    "file_id": "file:repo:abc123:src:auth.py",
    "line": 42,
    "column": 5
  },
  "evidence": "query = \"SELECT * FROM users WHERE name = '\" + username",
  "recommendation": "Use parameterized queries",
  "status": "open"
}
```

**ID format:** `finding:{repo_id}:{short-description}-{sequence}`

### Pattern 4: Decision Logging

Every significant decision should be logged for future reference:

```json
{
  "id": "decision:session:xyz789:upgrade-flask",
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
```

**When to use:** When an agent makes a choice that affects future work.

### Pattern 5: Task Tracking

Tasks represent units of work assigned to agents:

```json
{
  "id": "task:session:xyz789:fix-auth",
  "type": "Task",
  "objective": "Fix SQL injection vulnerability in auth.py",
  "status": "in_progress",
  "priority": "high",
  "assigned_agent": "implementer",
  "requested_by": "orchestrator",
  "artifacts": ["patch:auth.py"],
  "dependencies": ["task:session:xyz789:audit-auth"]
}
```

**When to use:** When coordinating multi-step work across agents.

## Relationship Patterns

### Pattern 1: Containment Hierarchy

```
Repository ->contains-> File
Repository ->contains-> Dataset
File ->contains-> Function
File ->contains-> Class
```

**Query example:** Get all Python files in a repository
```
GET entities WHERE type=File AND repo_id=repo:abc123 AND language=python
```

### Pattern 2: Dependency Graph

```
File ->depends_on-> Library
File ->depends_on-> File
Repository ->depends_on-> Service
```

**Query example:** Get all files that depend on a library
```
GET relationships WHERE type=depends_on AND target_id=lib:requests
```

### Pattern 3: Finding Relationships

```
File ->has_finding-> Finding
Repository ->has_finding-> Finding
Finding ->related_to-> Finding
```

**Query example:** Get all findings for a repository
```
GET entities WHERE type=Finding AND repo_id=repo:abc123
```

### Pattern 4: Resolution Tracking

```
Task ->resolves-> Finding
Decision ->addresses-> Finding
Agent ->produces-> Task
```

**Query example:** Get all tasks that resolve security findings
```
GET relationships WHERE type=resolves AND target.type=Finding AND target.severity IN [HIGH, CRITICAL]
```

### Pattern 5: Provenance Chain

```
Entity ->created_by-> Agent
Entity ->source_session-> Session
Finding ->discovered_by-> Agent
```

**Query example:** Get all findings from a specific agent
```
GET entities WHERE type=Finding AND provenance.source=tour-sentry
```

## Query Patterns

### Pattern 1: Repository Context

Get all context for working on a repository:

```
# Get repo info
GET entities WHERE type=Repository AND id=repo:abc123

# Get all files
GET entities WHERE type=File AND repo_id=repo:abc123

# Get all findings
GET entities WHERE type=Finding AND repo_id=repo:abc123

# Get recent sessions
GET entities WHERE type=Session AND metadata.repo_id=repo:abc123
```

### Pattern 2: Impact Analysis

Find all files affected by a change:

```
# Get files that depend on a changed file
GET relationships WHERE type=depends_on AND target_id=file:repo:abc123:src:auth.py

# Get findings in those files
GET entities WHERE type=Finding AND location.file_id IN [file-id-1, file-id-2, ...]
```

### Pattern 3: Security Audit Follow-up

Get all open security findings:

```
GET entities WHERE type=Finding AND severity IN [HIGH, CRITICAL] AND status=open
```

### Pattern 4: Session Continuation

Resume work from a previous session:

```
# Get session context
GET entities WHERE type=Session AND id=session:xyz789

# Get decisions made
GET entities WHERE type=Decision AND session_id=session:xyz789

# Get tasks completed
GET entities WHERE type=Task AND provenance.source=session:xyz789
```

### Pattern 5: Cross-Repository Analysis

Find similar issues across repositories:

```
# Get all SQL injection findings
GET entities WHERE type=Finding AND category=security AND subtype=sql-injection

# Group by repository
GROUP BY repo_id
```

## Context Optimization Patterns

### Pattern 1: Token Budgeting

Always specify a token budget:

```yaml
context:
  query: "GET entities WHERE type=Finding AND repo_id=repo:abc123"
  max_tokens: 2000
  summarize: standard
```

### Pattern 2: Type Filtering

Only request the entity types you need:

```yaml
context:
  query: "GET entities WHERE type IN [Finding, File] AND repo_id=repo:abc123"
  include_types: [Finding, File]
```

### Pattern 3: Severity Filtering

Filter by importance:

```yaml
context:
  query: "GET entities WHERE type=Finding AND severity IN [HIGH, CRITICAL]"
```

### Pattern 4: Temporal Filtering

Get recent data:

```yaml
context:
  query: "GET entities WHERE type=Finding AND created_at > '2024-01-01'"
```

### Pattern 5: Lazy Loading

Request minimal data first, then ask for more if needed:

```yaml
# First request - brief overview
context:
  query: "GET entities WHERE type=Repository"
  max_tokens: 500
  summarize: brief

# If needed, follow-up with more detail
context:
  query: "GET entities WHERE type=File AND repo_id=repo:abc123"
  max_tokens: 2000
  summarize: standard
```

## Best Practices

### 1. Always Use IDs

When referencing entities, use their full ID, not just names or paths:
- ✅ `repo:abc123` (good - unique identifier)
- ❌ `my-project` (bad - ambiguous)

### 2. Store Before Reference

Always store an entity before creating relationships to it:
```python
# Store the file first
store_entity(file_data)

# Then create relationships
store_relationship({
    "type": "has_finding",
    "source_id": file_id,
    "target_id": finding_id
})
```

### 3. Use Standard Types

Use the standard entity types from SCHEMA.md:
- Agent, Repository, File, Finding, Decision, Dataset, Task, Session

Only create custom types when absolutely necessary.

### 4. Include Provenance

Always include provenance information:
```json
{
  "id": "...",
  "type": "Finding",
  "provenance": {
    "source": "tour-sentry",
    "confidence": 0.95,
    "session_id": "session:xyz789",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### 5. Deduplicate

Before storing, check if an entity already exists:
```python
# Check if repo exists
existing = find_entity(repo_id)
if existing:
    # Update existing
    existing.update(new_data)
    store_entity(existing)
else:
    # Store new
    store_entity(new_data)
```

### 6. Version Your Entities

Use semantic versioning for entities that change:
```json
{
  "id": "repo:abc123",
  "version": "1.0.0",
  "...": "..."
}
```

When updating, increment the version:
- **PATCH** - Minor updates (metadata, description)
- **MINOR** - Backward-compatible changes (new fields)
- **MAJOR** - Breaking changes (schema changes)

### 7. Handle Conflicts

If two agents try to update the same entity:
- Latest write wins (by timestamp)
- Higher confidence wins
- Manual resolution if conflicting

## Performance Patterns

### Pattern 1: Batch Operations

Store multiple entities in a batch:
```python
# Instead of individual stores
for entity in entities:
    store_entity(entity)

# Use batch store (when available)
store_entities(entities)
```

### Pattern 2: Indexed Queries

Query using indexed fields:
- ✅ `WHERE type=Finding` (indexed)
- ✅ `WHERE repo_id=repo:abc123` (indexed)
- ❌ `WHERE description CONTAINS 'vulnerability'` (not indexed)

### Pattern 3: Caching

Cache frequently accessed data:
```python
# Check cache first
cached = get_cached_data(cache_key)
if cached:
    return cached

# Query and cache
result = query_knowledge(query)
cache_data(cache_key, result, ttl_seconds=3600)
```

### Pattern 4: Pagination

For large result sets, use pagination:
```yaml
context:
  query: "GET entities WHERE type=File"
  limit: 100
  offset: 0
```

### Pattern 5: Streaming

For very large datasets, stream results:
```python
# Process entities one at a time
def process_entities():
    for entity in query_knowledge_stream(query):
        process(entity)
```

## Security Patterns

### Pattern 1: No Secrets

Never store secrets in the knowledge graph:
- API keys
- Passwords
- Tokens
- Private keys
- Credentials

If you must reference a secret, use a hash or reference:
```json
{
  "id": "config:api-key",
  "type": "Configuration",
  "name": "API_KEY",
  "value_hash": "sha256:abc123...",
  "description": "API key for external service"
}
```

### Pattern 2: No PII

Never store personally identifiable information:
- Names
- Email addresses
- Phone numbers
- Addresses
- IDs (unless anonymized)

### Pattern 3: Access Control

Scope knowledge access by:
- Session
- Repository
- Agent capabilities

```python
# Only allow access to current session's data
def get_session_context(session_id):
    # Verify current session
    if current_session_id != session_id:
        raise AccessDenied()
    return query_knowledge(f"WHERE session_id={session_id}")
```

### Pattern 4: Data Retention

Define retention policies:
- Session data: 30 days (default)
- Repository data: Until deleted
- Findings: Until resolved
- Decisions: Permanent

```python
# Clean up old sessions
def cleanup_old_sessions(max_age_days=30):
    for session in list_sessions():
        if session.is_older_than(max_age_days):
            delete_session(session.id)
```

### Pattern 5: Audit Trail

Track all changes to the knowledge graph:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "action": "store_entity",
  "entity_id": "finding:repo:abc123:auth-sql-inj-001",
  "entity_type": "Finding",
  "session_id": "session:xyz789",
  "agent": "tour-sentry"
}
```

## Integration with Existing Patterns

### With ETL Pattern

Knowledge graph data can be treated as an ETL source:
- **Extract**: Query the knowledge graph
- **Transform**: Filter, enrich, aggregate
- **Load**: Create reports, dashboards, or new entities

### With Testing Practice

Store test results in the knowledge graph:
```json
{
  "id": "test-result:repo:abc123:test-auth-001",
  "type": "TestResult",
  "test_file": "tests/auth_test.py",
  "status": "passed",
  "duration_ms": 120,
  "coverage": 0.85
}
```

### With Security Practice

Store security findings with full provenance:
```json
{
  "id": "finding:repo:abc123:cve-2024-1234",
  "type": "Finding",
  "severity": "CRITICAL",
  "category": "security",
  "cve": "CVE-2024-1234",
  "description": "Vulnerability in dependency",
  "affected_file": "requirements.txt",
  "recommendation": "Upgrade to version 2.0.0"
}
```

## Migration Patterns

### From File-Based Context

If you have existing file-based context:

```python
# Convert file references to entity references
def migrate_file_context(file_path: str, repo_id: str) -> str:
    # Create file entity ID
    file_id = create_file_id(repo_id, file_path)
    return file_id
```

### From In-Memory State

If agents currently use in-memory state:

```python
# Store session state at end of session
def store_session_state(session_id: str, state: dict):
    # Store as session entity
    store_entity({
        "id": session_id,
        "type": "Session",
        "state": state,
        "end_time": datetime.utcnow().isoformat()
    })
```

### From Manual Context Passing

Replace manual context with knowledge graph queries:

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
  query: "GET entities WHERE type IN [File, Finding] AND repo_id=repo:abc123 AND path LIKE '%auth%'"
  max_tokens: 2000
```

## Summary

The knowledge graph pattern provides:
- **Persistence**: Data survives across sessions
- **Queryability**: Find exactly what you need
- **Efficiency**: Token-optimized context
- **Provenance**: Track where knowledge came from
- **Relationships**: Understand connections between entities

**Rule of thumb:** If you're manually curating context, you should be using the knowledge graph instead.
