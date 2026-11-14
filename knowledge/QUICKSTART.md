# Quick Start Guide: Knowledge Graph & Context Persistence

Get started with the new knowledge graph in 5 minutes.

## Step 1: Install/Update

```bash
cd mistral-agents-library
./install.py
```

This installs the updated profiles including the new `context-manager` agent.

## Step 2: Start a Session

```bash
vibe --agent orchestrator
```

## Step 3: Try It Out

Ask the orchestrator to do some work. It will automatically:
1. Create a session
2. Query the knowledge graph for relevant context
3. Persist findings and decisions
4. Store session state

### Example Session

**User:** "Run a security audit on this repository"

**What happens:**
1. Orchestrator creates a new session
2. Dispatches `app-cartographer` to map the repo
3. Dispatches `tour-sentry` for security tour
4. `tour-sentry` finds vulnerabilities
5. Findings are stored in the knowledge graph
6. Session ends, state is saved

**User (later):** "Show me the security issues from last time"

**What happens:**
1. Orchestrator creates a new session
2. Queries knowledge graph for previous findings
3. Returns the stored security issues
4. You can continue where you left off

## Step 4: Verify It's Working

Check the knowledge graph location:

```bash
ls -la ~/.mistral-agents/knowledge/
```

You should see:
```
graph/
  entities.jsonl
  relationships.jsonl
  index.json
sessions/
  {session-id}/
    context.json
    decisions.jsonl
    metadata.json
cache/
```

## Step 5: Query Directly (Optional)

If you want to query the knowledge graph directly:

```python
from tools.vetted.context.query import QueryEngine

engine = QueryEngine()

# Query for repositories
result, error = engine.query("GET entities WHERE type=Repository")
print(f"Found {result.total_count} repositories")

# Query for findings
result, error = engine.query("GET entities WHERE type=Finding AND severity=HIGH")
for finding in result.entities:
    print(f"{finding['severity']}: {finding['title']}")
```

## Step 6: Integrate with Your Agents

If you're writing custom agents, use the knowledge graph:

```python
from tools.vetted.context.store import StorageEngine
from tools.vetted.context.query import QueryEngine

# Store a finding
storage = StorageEngine()
storage.store_entity({
    'id': 'finding:my-repo:issue-001',
    'type': 'Finding',
    'severity': 'HIGH',
    'title': 'Issue found',
    'description': 'Detailed description'
})

# Query for context
engine = QueryEngine()
result, error = engine.query("GET entities WHERE type=Finding AND status=open")
```

## Key Commands

| Command | Purpose |
|---------|---------|
| `GET entities WHERE type=Repository` | List all repositories |
| `GET entities WHERE type=Finding AND severity=HIGH` | List high-severity findings |
| `GET entities WHERE repo_id=repo:abc123` | Get all entities for a repo |
| `GET relationships WHERE type=contains` | Get all containment relationships |

## Query DSL Reference

### Basic Syntax

```
GET <type> WHERE <conditions>
```

### Types

- `entities` - Query entities
- `relationships` - Query relationships
- Or a specific type like `Repository`, `Finding`, `File`, etc.

### Conditions

```
# Equality
WHERE type=Finding
WHERE severity=HIGH
WHERE repo_id=repo:abc123

# AND
WHERE type=Finding AND severity=HIGH AND status=open

# IN
WHERE severity IN (HIGH, CRITICAL)
WHERE type IN (Finding, File)

# LIKE (pattern matching)
WHERE path LIKE '%auth%'
WHERE name LIKE 'test_*'
```

### Modifiers

```
# Limit results
GET entities WHERE type=File LIMIT 10

# Skip results
GET entities WHERE type=File OFFSET 10 LIMIT 10

# Token budget
GET entities WHERE type=Finding MAX_TOKENS 2000

# Summarization
GET entities WHERE type=Finding SUMMARIZE standard
```

## Example Workflows

### Workflow 1: Security Audit

```python
# Session 1: Run audit
from tools.vetted.context.session import SessionManager
from tools.vetted.context.store import StorageEngine

manager = SessionManager()
storage = StorageEngine()

session = manager.create_session(user_intent="Security audit")

# Run audit...
findings = [...]  # From tour-sentry

for finding in findings:
    storage.store_entity(finding, session_id=session.id)

manager.end_session()

# Session 2: Review findings
session2 = manager.create_session(user_intent="Review security findings")

from tools.vetted.context.query import QueryEngine

engine = QueryEngine()
result, _ = engine.query(
    "GET entities WHERE type=Finding AND provenance.source=tour-sentry",
    max_tokens=2000
)

for finding in result.entities:
    print(f"{finding['severity']}: {finding['title']}")
```

### Workflow 2: Multi-Session Task

```python
# Session 1: Start task
session1 = manager.create_session(user_intent="Upgrade dependencies")

# Store task
task = {
    'id': 'task:upgrade-deps',
    'type': 'Task',
    'objective': 'Upgrade all dependencies',
    'status': 'in_progress'
}
storage.store_entity(task, session_id=session1.id)

# Store findings
findings = [...]  # From upgrade-planner
for finding in findings:
    storage.store_entity(finding, session_id=session1.id)

manager.end_session()

# Session 2: Continue task
session2 = manager.create_session(user_intent="Continue dependency upgrade")

# Query for incomplete tasks
result, _ = engine.query(
    "GET entities WHERE type=Task AND status=in_progress",
    max_tokens=1000
)

# Continue work on tasks...
```

## Troubleshooting

### No results from query

Check if entities exist:
```python
result, _ = engine.query("GET entities WHERE type=Repository")
print(result.total_count)
```

### Entity not stored

Check validation errors:
```python
result, errors = storage.store_entity(entity)
if errors:
    for error in errors:
        print(f"{error.field}: {error.message}")
```

### Token budget exceeded

Reduce max_tokens or use more specific queries:
```python
# Instead of this
result, _ = engine.query("GET entities WHERE type=File", max_tokens=500)

# Try this
result, _ = engine.query(
    "GET entities WHERE type=File AND repo_id=repo:abc123",
    max_tokens=500
)
```

## Best Practices

1. **Always specify token budgets** - Prevents token waste
2. **Use specific queries** - `WHERE repo_id=repo:abc123` is better than getting all entities
3. **Store findings with provenance** - Always include `source` and `session_id`
4. **Use standard types** - Use `Finding`, `File`, `Repository` etc. when possible
5. **Deduplicate** - Check if entity exists before storing
6. **End sessions properly** - Always call `end_session()` to save state

## Next Steps

1. ✅ Install and test
2. Try a multi-session workflow
3. Query the knowledge graph directly
4. Integrate with your custom agents
5. Provide feedback!

## Need Help?

- Read the full documentation in `knowledge/IMPLEMENTATION.md`
- Check the schema in `knowledge/SCCHEMA.md`
- See the patterns in `shared/dialects/patterns/knowledge.md`
- Review the agent definition in `knowledge/context-manager.md`
