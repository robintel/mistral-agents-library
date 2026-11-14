"""
Query Engine for Knowledge Graph

Provides fast, token-aware querying of the persistent knowledge graph.
Supports the query DSL defined in knowledge/SCCHEMA.md
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


# Data: clean - no credentials, PII, or sensitive data
# Provenance: mistral-agents-library


@dataclass
class QueryResult:
    """Result of a knowledge graph query."""
    entities: List[Dict[str, Any]] = field(default_factory=list)
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    total_count: int = 0
    token_count: int = 0
    truncated: bool = False
    query: str = ""
    execution_time_ms: float = 0.0


@dataclass
class QueryError:
    """Error from query execution."""
    error_type: str
    message: str
    suggestion: Optional[str] = None


class QueryEngine:
    """
    Executes queries against the knowledge graph.
    
    Supports:
    - GET entities WHERE conditions
    - GET relationships WHERE conditions
    - JOIN-like queries via subqueries
    - Token-aware result summarization
    """
    
    def __init__(self, knowledge_path: Optional[Path] = None):
        """
        Initialize query engine.
        
        Args:
            knowledge_path: Path to knowledge directory (default: ~/.mistral-agents/knowledge)
        """
        if knowledge_path is None:
            knowledge_path = Path.home() / ".mistral-agents" / "knowledge"
        self.knowledge_path = Path(knowledge_path)
        self.entities_path = self.knowledge_path / "graph" / "entities.jsonl"
        self.relationships_path = self.knowledge_path / "graph" / "relationships.jsonl"
        self.index_path = self.knowledge_path / "graph" / "index.json"
        
        # Load index
        self._index = self._load_index()
        self._entities = None  # Lazy loaded
        self._relationships = None  # Lazy loaded
    
    def _load_index(self) -> Dict[str, Any]:
        """Load the index from disk."""
        if not self.index_path.exists():
            return {"version": "1", "entities": {}, "relationships": {}}
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"version": "1", "entities": {}, "relationships": {}}
    
    def _load_entities(self) -> List[Dict[str, Any]]:
        """Load all entities from disk."""
        if self._entities is not None:
            return self._entities
        
        if not self.entities_path.exists():
            self._entities = []
            return self._entities
        
        entities = []
        try:
            with open(self.entities_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entities.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except IOError:
            pass
        
        self._entities = entities
        return self._entities
    
    def _load_relationships(self) -> List[Dict[str, Any]]:
        """Load all relationships from disk."""
        if self._relationships is not None:
            return self._relationships
        
        if not self.relationships_path.exists():
            self._relationships = []
            return self._relationships
        
        relationships = []
        try:
            with open(self.relationships_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            relationships.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except IOError:
            pass
        
        self._relationships = relationships
        return self._relationships
    
    def query(self, query: str, max_tokens: Optional[int] = None, 
              session_id: Optional[str] = None) -> Tuple[Optional[QueryResult], Optional[QueryError]]:
        """
        Execute a query against the knowledge graph.
        
        Args:
            query: Query string in DSL format
            max_tokens: Maximum tokens for response (enables summarization)
            session_id: Current session ID (for scoping and logging)
        
        Returns:
            Tuple of (QueryResult or None, QueryError or None)
        """
        import time
        start_time = time.time()
        
        try:
            parsed = self._parse_query(query)
            if parsed is None:
                return None, QueryError(
                    error_type="syntax_error",
                    message=f"Could not parse query: {query}",
                    suggestion="Check query syntax. Use: GET entities WHERE conditions"
                )
            
            entity_type_filter = parsed.get("entity_type")
            if entity_type_filter == "entities":
                result = self._query_entities(parsed, max_tokens)
            elif entity_type_filter == "relationships":
                result = self._query_relationships(parsed, max_tokens)
            else:
                return None, QueryError(
                    error_type="invalid_query",
                    message=f"Unknown query type: {entity_type_filter}"
                )
            
            result.query = query
            result.execution_time_ms = (time.time() - start_time) * 1000
            return result, None
            
        except Exception as e:
            return None, QueryError(
                error_type="execution_error",
                message=str(e),
                suggestion="Try a simpler query"
            )
    
    def _parse_query(self, query: str) -> Optional[Any]:
        """Parse query string into structured query object."""
        # Simple parser for basic queries
        # Pattern: GET <type> WHERE <conditions>
        
        # Normalize whitespace but preserve case for values
        query = query.strip()
        
        # Check if it's a GET query (case-insensitive)
        if not query.upper().startswith("GET "):
            return None
        
        # Extract entity type
        parts = query[4:].split(" WHERE ", 1)
        if len(parts) < 2:
            # Simple GET without WHERE
            entity_type = parts[0].strip()
            return {"entity_type": entity_type, "conditions": []}
        
        entity_type = parts[0].strip()
        conditions_str = parts[1].strip()
        
        # Parse conditions (simple AND-only for now)
        conditions = []
        for cond in conditions_str.split(" AND "):
            cond = cond.strip()
            if "=" in cond:
                field, value = cond.split("=", 1)
                conditions.append({"field": field.strip(), "op": "=", "value": value.strip()})
            elif " IN (" in cond.upper():
                # Handle IN clause
                field_part, in_part = cond.split(" IN (", 1)
                field = field_part.strip()
                values_str = in_part.rstrip(")")
                values = [v.strip().strip("'\"") for v in values_str.split(",")]
                conditions.append({"field": field, "op": "IN", "value": values})
            elif " LIKE " in cond.upper():
                field, pattern = cond.split(" LIKE ", 1)
                conditions.append({"field": field.strip(), "op": "LIKE", "value": pattern.strip().strip("'\"")})
        
        return {"entity_type": entity_type, "conditions": conditions}
    
    def _query_entities(self, parsed: Dict[str, Any], max_tokens: Optional[int] = None) -> QueryResult:
        """Query entities based on parsed query."""
        entities = self._load_entities()
        
        # Filter by type if specified
        entity_type_filter = parsed.get("entity_type")
        if entity_type_filter and entity_type_filter != "entities":
            filtered = [e for e in entities if e.get("type") == entity_type_filter]
        else:
            filtered = entities[:]
        
        # Apply conditions
        conditions = parsed.get("conditions", [])
        for cond in conditions:
            filtered = self._apply_condition(filtered, cond)
        
        # Sort by recency (newest first) by default
        filtered.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # Token-aware summarization
        if max_tokens:
            result_entities, truncated = self._summarize_entities(filtered, max_tokens)
        else:
            result_entities = filtered
            truncated = False
        
        # Calculate token count
        token_count = self._estimate_tokens(result_entities)
        
        return QueryResult(
            entities=result_entities,
            total_count=len(filtered),
            token_count=token_count,
            truncated=truncated
        )
    
    def _query_relationships(self, parsed: Dict[str, Any], max_tokens: Optional[int] = None) -> QueryResult:
        """Query relationships based on parsed query."""
        relationships = self._load_relationships()
        
        # Filter by type if specified
        rel_type_filter = parsed.get("entity_type")
        if rel_type_filter and rel_type_filter != "relationships":
            filtered = [r for r in relationships if r.get("type") == rel_type_filter]
        else:
            filtered = relationships[:]
        
        # Apply conditions
        conditions = parsed.get("conditions", [])
        for cond in conditions:
            filtered = self._apply_condition(filtered, cond, is_relationship=True)
        
        # Sort by recency
        filtered.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # Token-aware summarization
        if max_tokens:
            result_rels, truncated = self._summarize_relationships(filtered, max_tokens)
        else:
            result_rels = filtered
            truncated = False
        
        token_count = self._estimate_tokens(result_rels)
        
        return QueryResult(
            relationships=result_rels,
            total_count=len(filtered),
            token_count=token_count,
            truncated=truncated
        )
    
    def _apply_condition(self, items: List[Dict[str, Any]], condition: Dict[str, Any], 
                         is_relationship: bool = False) -> List[Dict[str, Any]]:
        """Apply a single condition to filter items."""
        field = condition.get("field", "")
        op = condition.get("op", "=")
        value = condition.get("value")
        
        if op == "=" or op == "==":
            if isinstance(value, list) and len(value) == 1:
                value = value[0]
            return [item for item in items if self._get_nested(item, field) == value]
        elif op == "IN":
            return [item for item in items if self._get_nested(item, field) in value]
        elif op == "LIKE":
            pattern = value.replace("%", ".*").replace("_", ".")
            import re as re_module
            try:
                regex = re_module.compile(pattern, re_module.IGNORECASE)
                return [item for item in items 
                        if regex.search(str(self._get_nested(item, field)))]
            except:
                return items
        else:
            return items
    
    def _get_nested(self, obj: Dict[str, Any], path: str) -> Any:
        """Get nested value from object using dot notation."""
        parts = path.split(".")
        current = obj
        for part in parts:
            if current is None:
                return None
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return current
    
    def _summarize_entities(self, entities: List[Dict[str, Any]], max_tokens: int) -> Tuple[List[Dict[str, Any]], bool]:
        """Summarize entities to fit token budget."""
        # Simple summarization: include key fields only
        summarized = []
        token_count = 0
        
        # Estimate tokens per entity (rough estimate)
        avg_tokens_per_entity = 100  # Conservative estimate
        max_entities = max_tokens // avg_tokens_per_entity
        
        for entity in entities[:max_entities]:
            # Create summary with essential fields
            summary = {
                "id": entity.get("id"),
                "type": entity.get("type"),
                "summary": self._create_summary(entity)
            }
            # Add a few key properties
            if entity.get("type") == "Finding":
                summary["severity"] = entity.get("severity")
                summary["title"] = entity.get("title")
            elif entity.get("type") == "File":
                summary["path"] = entity.get("path")
                summary["language"] = entity.get("language")
            
            summarized.append(summary)
        
        truncated = len(entities) > max_entities
        return summarized, truncated
    
    def _create_summary(self, entity: Dict[str, Any]) -> str:
        """Create a brief text summary of an entity."""
        entity_type = entity.get("type", "Unknown")
        
        if entity_type == "Finding":
            severity = entity.get("severity", "UNKNOWN")
            title = entity.get("title", "Untitled finding")
            return f"{severity}: {title}"
        elif entity_type == "File":
            path = entity.get("path", "unknown")
            language = entity.get("language", "unknown")
            return f"{language} file: {path}"
        elif entity_type == "Repository":
            name = entity.get("name", entity.get("path", "unknown"))
            language = entity.get("language", "unknown")
            return f"{language} repo: {name}"
        elif entity_type == "Agent":
            name = entity.get("name", "unknown")
            domain = entity.get("domain", "unknown")
            return f"{domain} agent: {name}"
        else:
            return f"{entity_type}: {entity.get('id', 'unknown')}"
    
    def _summarize_relationships(self, relationships: List[Dict[str, Any]], max_tokens: int) -> Tuple[List[Dict[str, Any]], bool]:
        """Summarize relationships to fit token budget."""
        # For relationships, we typically want to keep the structure
        # but limit the number
        avg_tokens_per_rel = 50
        max_rels = max_tokens // avg_tokens_per_rel
        
        summarized = relationships[:max_rels]
        truncated = len(relationships) > max_rels
        return summarized, truncated
    
    def _estimate_tokens(self, data: Any) -> int:
        """Estimate token count for data (rough estimate)."""
        json_str = json.dumps(data)
        # Rough estimate: 4 characters per token (conservative)
        return len(json_str) // 4


# Singleton instance for easy use
_default_query_engine = None


def get_query_engine(knowledge_path: Optional[Path] = None) -> QueryEngine:
    """Get or create the default query engine."""
    global _default_query_engine
    if _default_query_engine is None or knowledge_path:
        _default_query_engine = QueryEngine(knowledge_path)
    return _default_query_engine
