# Knowledge Graph Schema

## Overview

The knowledge graph uses a simple, extensible schema based on JSON-LD principles. Every entity is a JSON object with standard fields plus type-specific properties.

## Standard Fields (All Entities)

```json
{
  "id": "unique-identifier",
  "type": "EntityType",
  "version": "semantic-version",
  "created_at": "ISO-8601-timestamp",
  "updated_at": "ISO-8601-timestamp",
  "provenance": {
    "source": "agent-or-session-id",
    "confidence": 0.0-1.0,
    "method": "how-it-was-created"
  },
  "metadata": {
    "tags": ["string-tags"],
    "description": "brief-description",
    "related": ["entity-ids"]
  }
}
```

## Entity Types

### 1. Agent

Represents an AI agent in the system.

```json
{
  "id": "orchestrator",
  "type": "Agent",
  "name": "Orchestrator",
  "domain": "core",
  "tier": "t1",
  "escalate": "t4",
  "accepts": ["triage", "synthesis"],
  "capabilities": ["routing", "integration", "dispatch"],
  "description": "Single source of truth for agent coordination"
}
```

**Required fields:** `id`, `type`, `name`, `domain`
**Optional fields:** `tier`, `escalate`, `accepts`, `capabilities`, `description`

### 2. Repository

Represents a code repository.

```json
{
  "id": "repo:2f1adf2",
  "type": "Repository",
  "path": "/home/user/project",
  "fingerprint": "sha256:abc123...",
  "name": "my-project",
  "description": "Project description",
  "language": "python",
  "framework": "flask",
  "dependencies": {
    "flask": "2.0.0",
    "requests": "2.25.0"
  },
  "size_bytes": 1024000,
  "file_count": 42,
  "last_commit": "2024-01-15T10:30:00Z"
}
```

**Required fields:** `id`, `type`, `path`, `fingerprint`
**Optional fields:** `name`, `description`, `language`, `framework`, `dependencies`, `size_bytes`, `file_count`, `last_commit`

### 3. File

Represents a source file.

```json
{
  "id": "file:2f1adf2:src/auth.py",
  "type": "File",
  "path": "src/auth.py",
  "repo_id": "repo:2f1adf2",
  "hash": "sha256:def456...",
  "language": "python",
  "lines_of_code": 150,
  "complexity": 5.2,
  "functions": ["login", "logout", "validate_token"],
  "classes": ["AuthService"],
  "imports": ["flask", "jwt"],
  "last_modified": "2024-01-15T10:30:00Z"
}
```

**Required fields:** `id`, `type`, `path`, `repo_id`, `hash`
**Optional fields:** `language`, `lines_of_code`, `complexity`, `functions`, `classes`, `imports`, `last_modified`

### 4. Finding

Represents a discovery, issue, or insight.

```json
{
  "id": "finding:2f1adf2:auth-sql-injection",
  "type": "Finding",
  "severity": "HIGH",
  "category": "security",
  "subtype": "sql-injection",
  "title": "SQL Injection Vulnerability in auth.py",
  "description": "The login function uses string concatenation for SQL queries.",
  "location": {
    "file_id": "file:2f1adf2:src/auth.py",
    "line": 42,
    "column": 5
  },
  "evidence": "query = \"SELECT * FROM users WHERE name = '\" + username",
  "recommendation": "Use parameterized queries",
  "status": "open",
  "related": ["finding:2f1adf2:user-input-validation"]
}
```

**Required fields:** `id`, `type`, `severity`, `title`, `description`
**Optional fields:** `category`, `subtype`, `location`, `evidence`, `recommendation`, `status`, `related`

**Severity values:** `INFO`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`

### 5. Decision

Represents a choice or conclusion.

```json
{
  "id": "decision:2f1adf2:upgrade-flask",
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

**Required fields:** `id`, `type`, `question`, `answer`
**Optional fields:** `context`, `rationale`, `alternatives_considered`, `impact`, `owner`, `status`

### 6. Dataset

Represents a data collection or resource.

```json
{
  "id": "dataset:users",
  "type": "Dataset",
  "name": "users",
  "description": "User account data",
  "schema": {
    "id": "integer",
    "name": "string",
    "email": "string",
    "created_at": "datetime"
  },
  "size": 10000,
  "location": "postgres://localhost:5432/mydb",
  "classification": "internal",
  "pii": true,
  "owner": "data-team",
  "retention": "7 years"
}
```

**Required fields:** `id`, `type`, `name`
**Optional fields:** `description`, `schema`, `size`, `location`, `classification`, `pii`, `owner`, `retention`

**Classification values:** `public`, `internal`, `confidential`, `restricted`

### 7. Task

Represents a unit of work.

```json
{
  "id": "task:2f1adf2:fix-auth",
  "type": "Task",
  "objective": "Fix SQL injection vulnerability in auth.py",
  "status": "in_progress",
  "priority": "high",
  "assigned_agent": "implementer",
  "requested_by": "orchestrator",
  "artifacts": ["patch:auth.py"],
  "dependencies": ["task:2f1adf2:audit-auth"],
  "start_time": "2024-01-15T10:30:00Z",
  "end_time": null,
  "outcome": null
}
```

**Required fields:** `id`, `type`, `objective`, `status`
**Optional fields:** `priority`, `assigned_agent`, `requested_by`, `artifacts`, `dependencies`, `start_time`, `end_time`, `outcome`

**Status values:** `pending`, `in_progress`, `completed`, `failed`, `cancelled`
**Priority values:** `low`, `medium`, `high`, `critical`

### 8. Session

Represents an agent session.

```json
{
  "id": "session:abc123",
  "type": "Session",
  "start_time": "2024-01-15T10:30:00Z",
  "end_time": "2024-01-15T11:45:00Z",
  "user_intent": "Audit security of my-project",
  "agents_used": ["orchestrator", "app-cartographer", "tour-sentry"],
  "tasks_completed": ["task:2f1adf2:audit-auth"],
  "findings_count": 15,
  "decisions_count": 3,
  "token_usage": {
    "input": 15000,
    "output": 8000
  }
}
```

**Required fields:** `id`, `type`, `start_time`
**Optional fields:** `end_time`, `user_intent`, `agents_used`, `tasks_completed`, `findings_count`, `decisions_count`, `token_usage`

## Relationship Types

Relationships are stored separately from entities to enable flexible querying.

### Relationship Schema

```json
{
  "id": "rel:2f1adf2:auth-has-vulnerability",
  "type": "has_vulnerability",
  "source_id": "file:2f1adf2:src/auth.py",
  "target_id": "finding:2f1adf2:auth-sql-injection",
  "created_at": "2024-01-15T10:30:00Z",
  "provenance": {
    "source": "tour-sentry",
    "confidence": 0.95
  },
  "properties": {
    "line": 42,
    "severity": "HIGH"
  }
}
```

**Required fields:** `id`, `type`, `source_id`, `target_id`
**Optional fields:** `created_at`, `provenance`, `properties`

### Standard Relationship Types

| Type | Description | Direction | Example |
|------|-------------|-----------|---------|
| `contains` | Containment | Parent -> Child | Repo -> File |
| `depends_on` | Dependency | Dependent -> Dependency | File -> Library |
| `references` | Reference/citation | Source -> Target | Finding -> File |
| `produces` | Production | Agent -> Artifact | Implementer -> File |
| `consumes` | Consumption | Agent -> Input | Agent -> File |
| `validates` | Validation | Validator -> Validated | Agent -> Finding |
| `resolves` | Resolution | Solution -> Problem | Task -> Finding |
| `owns` | Ownership | Owner -> Owned | Team -> Dataset |
| `uses` | Usage | User -> Used | Agent -> Tool |
| `has_finding` | Finding relationship | Container -> Finding | Repo -> Finding |
| `has_task` | Task relationship | Parent -> Task | Session -> Task |
| `part_of` | Membership | Part -> Whole | File -> Module |
| `calls` | Function call | Caller -> Callee | Function -> Function |
| `reads` | Read access | Reader -> Read | Agent -> File |
| `writes` | Write access | Writer -> Written | Agent -> File |

### Custom Relationships

Agents can define custom relationship types as needed. Use descriptive names and document them.

## Index Structure

The index enables fast querying without scanning all entities.

```json
{
  "version": "1",
  "entities": {
    "by_type": {
      "Agent": ["orchestrator", "implementer", ...],
      "Repository": ["repo:abc123", ...],
      "File": ["file:abc123:path/to/file", ...]
    },
    "by_property": {
      "repo_id": {
        "repo:abc123": ["file:abc123:file1", "file:abc123:file2"]
      },
      "language": {
        "python": ["file:abc123:script.py", ...]
      }
    }
  },
  "relationships": {
    "by_type": {
      "contains": ["rel:1", "rel:2", ...],
      "depends_on": ["rel:3", ...]
    },
    "by_source": {
      "file:abc123:file1": ["rel:1", "rel:2"]
    },
    "by_target": {
      "file:abc123:file2": ["rel:3"]
    }
  },
  "last_updated": "2024-01-15T10:30:00Z"
}
```

## Query Language

The knowledge graph supports a simple query DSL:

### Basic Queries

```
GET entities WHERE type=File AND language=python
GET entities WHERE repo_id=repo:abc123
GET relationships WHERE type=contains AND source_id=repo:abc123
```

### Advanced Queries

```
# Find all Python files in a repo
GET entities WHERE type=File AND repo_id=repo:abc123 AND language=python

# Find all findings related to a file
GET entities WHERE type=Finding AND location.file_id=file:abc123:path

# Find all dependencies of a repo
GET relationships WHERE type=depends_on AND source_id=repo:abc123

# Find all files that depend on a library
GET entities WHERE id IN (
  SELECT target_id FROM relationships 
  WHERE type=depends_on AND source_id=lib:requests
)
```

### Query Parameters

- `LIMIT n` - Limit results to n entities
- `OFFSET n` - Skip first n results
- `ORDER BY field [ASC|DESC]` - Sort results
- `MAX_TOKENS n` - Limit response to n tokens (requires summarization)

## Serialization

### Storage Format

Entities and relationships are stored as JSON Lines (`.jsonl`) files:
- One JSON object per line
- Easy to append
- Easy to stream
- Easy to parse

### File Structure

```
knowledge/graph/
├── entities.jsonl          # All entities
├── relationships.jsonl      # All relationships
├── index.json              # Index for fast queries
└── schema_version.txt      # Current schema version
```

## Versioning

The schema uses semantic versioning:
- **MAJOR** - Breaking changes (entities must be migrated)
- **MINOR** - Backward-compatible additions
- **PATCH** - Bug fixes and clarifications

When the schema changes:
1. Increment the version in `schema_version.txt`
2. Create a migration script if needed
3. Update all documentation

## Validation

All entities and relationships should be validated against the schema before storage. Validation includes:
- Required fields present
- Field types correct
- Enum values valid
- No circular references (for relationships)

## Performance Considerations

1. **Indexing** - Maintain indexes for frequently queried fields
2. **Caching** - Cache common queries
3. **Lazy loading** - Only load entity details when needed
4. **Batching** - Batch writes for performance
5. **Compression** - Consider compression for large text fields
