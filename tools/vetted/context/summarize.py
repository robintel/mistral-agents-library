"""
Summarizer for Knowledge Graph Context

Provides token-aware summarization of entities and context.
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


# Data: clean - no credentials, PII, or sensitive data
# Provenance: mistral-agents-library


@dataclass
class SummarizationOptions:
    """Options for context summarization."""
    max_tokens: int = 4000
    summary_level: str = "standard"  # brief, standard, detailed, full
    include_types: Optional[List[str]] = None
    exclude_types: Optional[List[str]] = None
    focus_fields: Optional[List[str]] = None


class Summarizer:
    """
    Summarizes entities and context for token-efficient briefs.
    
    Features:
    - Token-aware truncation
    - Field prioritization
    - Multi-level summaries
    - Entity grouping
    - Relevance-based selection
    """
    
    # Token estimates (characters per token)
    TOKEN_PER_CHAR = 4
    
    # Field priorities by entity type
    FIELD_PRIORITIES = {
        "Finding": ["id", "severity", "title", "description", "location", "recommendation"],
        "File": ["id", "path", "language", "lines_of_code", "complexity", "functions"],
        "Repository": ["id", "path", "name", "language", "dependencies", "size_bytes"],
        "Agent": ["id", "name", "domain", "tier", "capabilities"],
        "Decision": ["id", "question", "answer", "rationale", "impact"],
        "Task": ["id", "objective", "status", "priority", "assigned_agent"],
        "Dataset": ["id", "name", "schema", "size", "classification"],
        "Session": ["id", "start_time", "user_intent", "agents_used", "findings_count"]
    }
    
    # Summary level configurations
    SUMMARY_LEVELS = {
        "brief": {
            "token_budget": 500,
            "fields": 3,
            "depth": 1
        },
        "standard": {
            "token_budget": 2000,
            "fields": 5,
            "depth": 2
        },
        "detailed": {
            "token_budget": 4000,
            "fields": 8,
            "depth": 3
        },
        "full": {
            "token_budget": None,
            "fields": None,
            "depth": None
        }
    }
    
    def summarize_entities(self, entities: List[Dict[str, Any]], 
                           options: Optional[SummarizationOptions] = None) -> Tuple[List[Dict[str, Any]], bool]:
        """
        Summarize a list of entities to fit within token budget.
        
        Args:
            entities: List of entities to summarize
            options: Summarization options
        
        Returns:
            Tuple of (summarized entities, truncated flag)
        """
        if options is None:
            options = SummarizationOptions()
        
        if options.max_tokens is None:
            return entities, False
        
        # Get summary level config
        level_config = self.SUMMARY_LEVELS.get(options.summary_level, self.SUMMARY_LEVELS["standard"])
        
        # Apply token budget
        if level_config["token_budget"]:
            max_tokens = min(options.max_tokens, level_config["token_budget"])
        else:
            max_tokens = options.max_tokens
        
        # First pass: filter by type
        if options.include_types:
            entities = [e for e in entities if e.get("type") in options.include_types]
        if options.exclude_types:
            entities = [e for e in entities if e.get("type") not in options.exclude_types]
        
        # Calculate token count and select entities
        selected_entities = []
        total_tokens = 0
        
        for entity in entities:
            entity_type = entity.get("type", "Unknown")
            
            # Get priority fields for this type
            priority_fields = self.FIELD_PRIORITIES.get(entity_type, ["id", "type"])
            
            # Create summary
            summary = self._summarize_single_entity(entity, priority_fields, options)
            
            # Estimate tokens
            entity_tokens = self._estimate_tokens(summary)
            
            # Check if we can add this entity
            if total_tokens + entity_tokens <= max_tokens:
                selected_entities.append(summary)
                total_tokens += entity_tokens
            else:
                # Try with fewer fields
                reduced_summary = self._reduce_summary(summary, max_tokens - total_tokens)
                if reduced_summary:
                    selected_entities.append(reduced_summary)
                    total_tokens += self._estimate_tokens(reduced_summary)
                else:
                    # Can't fit this entity at all
                    break
        
        truncated = len(entities) > len(selected_entities)
        return selected_entities, truncated
    
    def summarize_relationships(self, relationships: List[Dict[str, Any]],
                               options: Optional[SummarizationOptions] = None) -> Tuple[List[Dict[str, Any]], bool]:
        """
        Summarize a list of relationships.
        
        Args:
            relationships: List of relationships to summarize
            options: Summarization options
        
        Returns:
            Tuple of (summarized relationships, truncated flag)
        """
        if options is None:
            options = SummarizationOptions()
        
        if options.max_tokens is None:
            return relationships, False
        
        # Simple approach: just limit the number
        avg_tokens_per_rel = 50
        max_rels = options.max_tokens // avg_tokens_per_rel
        
        # Sort by relevance (if available) or recency
        sorted_rels = sorted(
            relationships,
            key=lambda r: (
                r.get("provenance", {}).get("confidence", 0),
                r.get("created_at", "")
            ),
            reverse=True
        )
        
        selected = sorted_rels[:max_rels]
        truncated = len(relationships) > len(selected)
        
        return selected, truncated
    
    def create_context_block(self, entities: List[Dict[str, Any]],
                            relationships: List[Dict[str, Any]],
                            options: Optional[SummarizationOptions] = None) -> Dict[str, Any]:
        """
        Create a context block for a brief.
        
        Args:
            entities: List of entities
            relationships: List of relationships
            options: Summarization options
        
        Returns:
            Context block ready for a brief
        """
        if options is None:
            options = SummarizationOptions()
        
        # Summarize entities
        summary_entities, entities_truncated = self.summarize_entities(entities, options)
        
        # Summarize relationships
        summary_rels, rels_truncated = self.summarize_relationships(relationships, options)
        
        # Calculate total tokens
        total_tokens = (
            self._estimate_tokens(summary_entities) +
            self._estimate_tokens(summary_rels)
        )
        
        return {
            "entities": summary_entities,
            "relationships": summary_rels,
            "token_count": total_tokens,
            "truncated": entities_truncated or rels_truncated,
            "summary_level": options.summary_level,
            "max_tokens": options.max_tokens
        }
    
    def _summarize_single_entity(self, entity: Dict[str, Any],
                                  priority_fields: List[str],
                                  options: SummarizationOptions) -> Dict[str, Any]:
        """Summarize a single entity."""
        summary = {}
        
        # Always include id and type
        if "id" in entity:
            summary["id"] = entity["id"]
        if "type" in entity:
            summary["type"] = entity["type"]
        
        # Add priority fields
        for field in priority_fields:
            if field in entity and field not in summary:
                summary[field] = entity[field]
        
        # Add focus fields if specified
        if options.focus_fields:
            for field in options.focus_fields:
                if field in entity and field not in summary:
                    summary[field] = entity[field]
        
        # Add provenance if available
        if "provenance" in entity:
            summary["provenance"] = entity["provenance"]
        
        # Add metadata if it exists and we have room
        if "metadata" in entity and "description" in entity.get("metadata", {}):
            summary["_description"] = entity["metadata"]["description"]
        
        return summary
    
    def _reduce_summary(self, summary: Dict[str, Any], max_tokens: int) -> Optional[Dict[str, Any]]:
        """Reduce a summary to fit within token budget."""
        if self._estimate_tokens(summary) <= max_tokens:
            return summary
        
        # Try removing fields from lowest to highest priority
        # Keep id and type
        keep_fields = ["id", "type"]
        
        # Sort other fields by priority (reverse)
        other_fields = [f for f in summary if f not in keep_fields]
        
        # Get field priorities (default to 0)
        entity_type = summary.get("type", "Unknown")
        priority_fields = self.FIELD_PRIORITIES.get(entity_type, [])
        field_priority = {f: i for i, f in enumerate(priority_fields)}
        
        # Sort by priority (ascending = lowest priority first)
        other_fields.sort(key=lambda f: field_priority.get(f, len(priority_fields)))
        
        # Try removing fields until we fit
        reduced = dict(summary)
        for field in other_fields:
            if field in reduced:
                del reduced[field]
                if self._estimate_tokens(reduced) <= max_tokens:
                    return reduced
        
        # If we still don't fit, try truncating string values
        for field in keep_fields + other_fields:
            if field in reduced and isinstance(reduced[field], str):
                # Truncate to save tokens
                reduced[field] = reduced[field][:100] + "..."
                if self._estimate_tokens(reduced) <= max_tokens:
                    return reduced
        
        return None
    
    def _estimate_tokens(self, data: Any) -> int:
        """Estimate token count for data."""
        try:
            json_str = json.dumps(data, ensure_ascii=False)
            return len(json_str) // self.TOKEN_PER_CHAR
        except:
            return 0
    
    def create_text_summary(self, entities: List[Dict[str, Any]],
                          max_lines: int = 10) -> str:
        """
        Create a human-readable text summary.
        
        Args:
            entities: List of entities
            max_lines: Maximum number of lines
        
        Returns:
            Text summary
        """
        lines = []
        
        # Group by type
        by_type = {}
        for entity in entities:
            entity_type = entity.get("type", "Unknown")
            if entity_type not in by_type:
                by_type[entity_type] = []
            by_type[entity_type].append(entity)
        
        # Add header
        lines.append(f"Context Summary ({len(entities)} entities)")
        lines.append("=" * 40)
        
        # Add each type
        for entity_type, type_entities in by_type.items():
            lines.append(f"\n{entity_type} ({len(type_entities)})")
            lines.append("-" * len(entity_type))
            
            for entity in type_entities[:3]:  # Max 3 per type
                if entity_type == "Finding":
                    severity = entity.get("severity", "UNKNOWN")
                    title = entity.get("title", "Untitled")
                    lines.append(f"  [{severity}] {title}")
                elif entity_type == "File":
                    path = entity.get("path", "unknown")
                    language = entity.get("language", "unknown")
                    lines.append(f"  {language}: {path}")
                elif entity_type == "Repository":
                    name = entity.get("name", entity.get("path", "unknown"))
                    lines.append(f"  {name}")
                else:
                    lines.append(f"  {entity.get('id', 'unknown')}")
        
        # Truncate if needed
        if len(lines) > max_lines:
            lines = lines[:max_lines - 1]
            lines.append("  ... (truncated)")
        
        return "\n".join(lines)


# Singleton instance
_default_summarizer = None


def get_summarizer() -> Summarizer:
    """Get or create the default summarizer."""
    global _default_summarizer
    if _default_summarizer is None:
        _default_summarizer = Summarizer()
    return _default_summarizer
