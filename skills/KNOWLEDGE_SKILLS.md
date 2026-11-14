# Knowledge Graph Skills Guide

This guide explains which Mistral Agents Library skills are relevant to the knowledge graph and persistence functionality, and how to use them effectively.

## Overview

The Mistral Agents Library includes a **persistent knowledge graph** that enables:
- Cross-session memory for agents
- Shared knowledge across multiple agents
- Token-optimized context delivery
- Provenance tracking for all knowledge
- Automatic updates based on code changes

The knowledge graph is implemented in the `knowledge/` directory, primarily in `auto_update.py`.

---

## Skill Categories

### Core Knowledge Skills (Native to Knowledge Graph)

These skills are specifically designed for working with the knowledge graph:

| Skill | Invocation | Purpose | When to Use |
|-------|------------|---------|--------------|
| **ma-knowledge-query** | `/ma-knowledge-query` | Query the knowledge graph for entities, relationships, and context | Need to find stored information, retrieve context, search knowledge |
| **ma-knowledge-audit** | `/ma-knowledge-audit` | Audit knowledge graph integrity, consistency, and freshness | Verify knowledge base health, find stale data, detect inconsistencies |

#### Usage Examples

**Query the knowledge graph:**
```
/ma-knowledge-query GET entities WHERE type=Finding AND severity=HIGH
```

**Audit knowledge integrity:**
```
/ma-knowledge-audit
/ma-knowledge-audit integrity  # Only check integrity
/ma-knowledge-audit --repair   # Audit and offer repairs
```

---

### Complementary Skills (Work with Knowledge Graph)

These existing skills work well with the knowledge graph functionality:

#### 📊 Audit & Compliance

| Skill | Relevance | Use Case |
|-------|-----------|----------|
| **ma-governance-policy** | ⭐⭐⭐⭐⭐ | Audit knowledge graph for data governance, PII, retention policies |
| **ma-gdpr-audit** | ⭐⭐⭐⭐ | Ensure knowledge graph complies with GDPR and privacy regulations |
| **ma-security-audit** | ⭐⭐⭐⭐ | Security audit of persistence layer, access controls, encryption |
| **ma-infra-security** | ⭐⭐⭐ | Harden the file system where knowledge is stored |

**Example:** Audit knowledge for governance compliance
```
/ma-governance-policy
# Checks: PII in knowledge, retention policies, data classification
```

#### 🔍 Discovery & Orientation

| Skill | Relevance | Use Case |
|-------|-----------|----------|
| **ma-orient** | ⭐⭐⭐⭐⭐ | Understand a codebase using stored knowledge |
| **ma-tour** | ⭐⭐⭐⭐ | Run testing tours that leverage knowledge graph for context |

**Example:** Orient in a new repository with knowledge
```
/ma-orient
# Uses knowledge graph to provide faster, more accurate orientation
```

#### 📝 Documentation

| Skill | Relevance | Use Case |
|-------|-----------|----------|
| **ma-docs** | ⭐⭐⭐⭐ | Document knowledge graph schema, API, and usage patterns |

**Example:** Generate documentation for knowledge graph
```
/ma-docs
# Can document the knowledge graph structure and how to use it
```

#### 🔧 Development & Quality

| Skill | Relevance | Use Case |
|-------|-----------|----------|
| **ma-code-review** | ⭐⭐⭐⭐ | Review knowledge graph implementation code |
| **ma-design-principles** | ⭐⭐⭐ | Apply SOLID, DRY, and other principles to knowledge graph code |
| **ma-test-methodologies** | ⭐⭐⭐ | Design test strategies for knowledge graph functionality |
| **ma-coverage** | ⭐⭐ | Check test coverage for knowledge graph code |

**Example:** Code review of auto_update.py
```
/ma-code-review
# Reviews the knowledge graph implementation for quality and security
```

---

## Knowledge Graph Features & Matching Skills

| Knowledge Graph Feature | Relevant Skills | How They Work Together |
|------------------------|----------------|------------------------|
| **Persistence** | ma-security-audit, ma-infra-security | Ensure data is stored securely |
| **Auto-update** | ma-knowledge-audit, ma-knowledge-query | Verify updates, query fresh knowledge |
| **Backups** | ma-knowledge-audit | Audit backup integrity |
| **Integrity Checks** | ma-knowledge-audit, ma-governance-policy | Validate data integrity, check governance |
| **Provenance Tracking** | ma-governance-policy, ma-gdpr-audit | Audit provenance chains for compliance |
| **Context Delivery** | ma-orient, ma-knowledge-query | Retrieve optimized context for agents |
| **Token Optimization** | ma-knowledge-query | Query within token budgets |

---

## Workflow Examples

### Example 1: Onboarding to a New Project

```
# Step 1: Use knowledge graph to understand the project
/ma-orient

# Step 2: Query for specific information
/ma-knowledge-query GET entities WHERE type=Repository

# Step 3: Check knowledge health
/ma-knowledge-audit

# Step 4: Ensure compliance
/ma-governance-policy
```

### Example 2: Security Investigation

```
# Step 1: Query for security findings
/ma-knowledge-query GET entities WHERE type=Finding AND severity=HIGH

# Step 2: Audit knowledge integrity
/ma-knowledge-audit integrity

# Step 3: Full security audit
/ma-security-audit

# Step 4: Check for PII in knowledge
/ma-gdpr-audit
```

### Example 3: Knowledge Maintenance

```
# Step 1: Check for stale knowledge
/ma-knowledge-audit freshness

# Step 2: Audit overall health
/ma-knowledge-audit

# Step 3: Review knowledge graph code
/ma-code-review knowledge/auto_update.py

# Step 4: Update documentation
/ma-docs knowledge/
```

---

## Skill Invocation Patterns

### Direct Invocation
Simply use the skill invocation:
```
/ma-knowledge-query GET entities WHERE type=Repository
```

### With Parameters
Many skills accept parameters:
```
/ma-knowledge-audit freshness --stale-days 14
```

### With Scope
Limit to specific files or directories:
```
/ma-knowledge-query GET entities WHERE repo='/path/to/project'
```

### With Token Limits
Control output size:
```
/ma-knowledge-query GET context MAX_TOKENS=4000
```

---

## Best Practices

### 1. **Start with Orientation**
Always begin with `/ma-orient` when working with a new codebase. It uses the knowledge graph to provide better context.

### 2. **Query Before Acting**
Check existing knowledge before making decisions:
```
/ma-knowledge-query GET entities WHERE type=Finding AND location=file.py
```

### 3. **Audit Regularly**
Run `/ma-knowledge-audit` periodically to ensure knowledge integrity:
- Before major decisions
- After significant code changes
- When switching projects

### 4. **Combine Skills**
Use multiple skills together for comprehensive analysis:
```
/ma-knowledge-audit
/ma-governance-policy
/ma-security-audit
```

### 5. **Respect Token Limits**
When querying knowledge, always consider token budgets:
```
/ma-knowledge-query GET context MAX_TOKENS=4000
```

---

## Troubleshooting

### Issue: No knowledge graph found
**Solution:** Run `/ma-orient` first to populate the knowledge graph, or ensure you're in a project directory.

### Issue: Query returns no results
**Solution:** Try a broader query or run `/ma-knowledge-audit` to verify knowledge exists.

### Issue: Knowledge seems outdated
**Solution:** Run `/ma-knowledge-audit freshness` and consider running `/ma-orient` to refresh.

### Issue: Integrity errors detected
**Solution:** Run `/ma-knowledge-audit --repair` or restore from backup.

---

## Integration with Agents

When writing agents that use the knowledge graph:

1. **Load Context Manager**
   ```python
   from knowledge.auto_update import KnowledgeGraph
   kg = KnowledgeGraph()
   ```

2. **Query Knowledge**
   ```python
   entities = kg.query_entities(type="Finding", severity="HIGH")
   ```

3. **Store New Knowledge**
   ```python
   kg.store_entity({
       "id": "finding_123",
       "type": "Finding",
       "severity": "HIGH",
       "description": "Security vulnerability",
       "provenance": {
           "source": "my_agent",
           "confidence": 0.95
       }
   })
   ```

4. **Use in Briefs**
   ```yaml
   context:
     auto: true
     query: "GET entities WHERE repo='/path/to/project'"
     max_tokens: 2000
   ```

---

## Future Skills (Planned)

These skills are planned but not yet implemented:

| Skill | Purpose | Status |
|-------|---------|--------|
| **ma-knowledge-sync** | Synchronize knowledge across sessions/repos | 📋 Planned |
| **ma-knowledge-freshness** | Advanced freshness checking and auto-update | 📋 Planned |
| **ma-knowledge-visualize** | Generate visualizations of knowledge graph | 📋 Planned |
| **ma-context-optimize** | Optimize context selection for token efficiency | 📋 Planned |

---

## References

- [Knowledge Graph README](knowledge/README.md) - Architecture and usage
- [Knowledge Graph Schema](knowledge/SCCHEMA.md) - Entity and relationship types
- [Implementation Guide](knowledge/IMPLEMENTATION.md) - Technical details
- [auto_update.py](knowledge/auto_update.py) - Core implementation

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│ KNOWLEDGE GRAPH SKILLS                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  QUERY:       /ma-knowledge-query GET entities WHERE type=Finding │
│  AUDIT:       /ma-knowledge-audit                                 │
│  ORIENT:      /ma-orient                                          │
│  GOVERNANCE:  /ma-governance-policy                              │
│  GDPR:        /ma-gdpr-audit                                     │
│  SECURITY:    /ma-security-audit                                 │
│  DOCS:        /ma-docs                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```
