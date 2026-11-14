"""
Storage Engine for Knowledge Graph

Handles persistent storage of entities and relationships.
Provides deduplication, validation, and indexing.
"""

import json
import hashlib
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


# Data: clean - no credentials, PII, or sensitive data
# Provenance: mistral-agents-library


@dataclass
class StoreResult:
    """Result of a storage operation."""
    entity_id: str
    stored: bool
    updated: bool
    message: str
    warnings: List[str] = field(default_factory=list)


@dataclass
class ValidationError:
    """Validation error for an entity."""
    field: str
    message: str
    severity: str = "error"  # error, warning, info


class StorageEngine:
    """
    Stores and retrieves entities and relationships.
    
    Features:
    - JSON Lines storage for append-only writes
    - Automatic deduplication by ID
    - Schema validation
    - Index maintenance
    - Session scoping
    """
    
    # Entity type definitions (from SCHEMA.md)
    ENTITY_TYPES = {
        "Agent", "Repository", "File", "Finding", 
        "Decision", "Dataset", "Task", "Session"
    }
    
    # Required fields per entity type
    REQUIRED_FIELDS = {
        "Agent": ["id", "type", "name", "domain"],
        "Repository": ["id", "type", "path", "fingerprint"],
        "File": ["id", "type", "path", "repo_id", "hash"],
        "Finding": ["id", "type", "severity", "title", "description"],
        "Decision": ["id", "type", "question", "answer"],
        "Dataset": ["id", "type", "name"],
        "Task": ["id", "type", "objective", "status"],
        "Session": ["id", "type", "start_time"]
    }
    
    # Valid enum values
    VALID_ENUMS = {
        "severity": ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"],
        "classification": ["public", "internal", "confidential", "restricted"],
        "status": ["pending", "in_progress", "completed", "failed", "cancelled", "open"],
        "priority": ["low", "medium", "high", "critical"]
    }
    
    def __init__(self, knowledge_path: Optional[Path] = None):
        """
        Initialize storage engine.
        
        Args:
            knowledge_path: Path to knowledge directory
        """
        if knowledge_path is None:
            knowledge_path = Path.home() / ".mistral-agents" / "knowledge"
        self.knowledge_path = Path(knowledge_path)
        self.entities_path = self.knowledge_path / "graph" / "entities.jsonl"
        self.relationships_path = self.knowledge_path / "graph" / "relationships.jsonl"
        self.index_path = self.knowledge_path / "graph" / "index.json"
        self.sessions_path = self.knowledge_path / "sessions"
        self.cache_path = self.knowledge_path / "cache"
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Load existing data
        self._index = self._load_index()
        self._entities = self._load_all(self.entities_path)
        self._relationships = self._load_all(self.relationships_path)
    
    def _ensure_directories(self):
        """Create necessary directories."""
        self.knowledge_path.mkdir(parents=True, exist_ok=True)
        (self.knowledge_path / "graph").mkdir(parents=True, exist_ok=True)
        self.sessions_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
    
    def _load_all(self, path: Path) -> List[Dict[str, Any]]:
        """Load all JSON objects from a JSONL file."""
        if not path.exists():
            return []
        
        items = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            items.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except IOError:
            pass
        return items
    
    def _load_index(self) -> Dict[str, Any]:
        """Load the index from disk."""
        if not self.index_path.exists():
            return {
                "version": "1",
                "entities": {
                    "by_type": {},
                    "by_property": {}
                },
                "relationships": {
                    "by_type": {},
                    "by_source": {},
                    "by_target": {}
                },
                "last_updated": None
            }
        
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If index is corrupted, rebuild it
            return self._rebuild_index()
    
    def _save_index(self):
        """Save the index to disk."""
        self._index["last_updated"] = datetime.utcnow().isoformat()
        try:
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(self._index, f, indent=2)
        except IOError:
            pass
    
    def _rebuild_index(self) -> Dict[str, Any]:
        """Rebuild index from entities and relationships."""
        index = {
            "version": "1",
            "entities": {
                "by_type": {},
                "by_property": {}
            },
            "relationships": {
                "by_type": {},
                "by_source": {},
                "by_target": {}
            },
            "last_updated": datetime.utcnow().isoformat()
        }
        
        # Index entities
        for entity in self._entities:
            entity_type = entity.get("type")
            if entity_type not in index["entities"]["by_type"]:
                index["entities"]["by_type"][entity_type] = []
            index["entities"]["by_type"][entity_type].append(entity["id"])
            
            # Index by properties
            for key, value in entity.items():
                if key in ["id", "type", "created_at", "updated_at", "provenance"]:
                    continue
                if key not in index["entities"]["by_property"]:
                    index["entities"]["by_property"][key] = {}
                if str(value) not in index["entities"]["by_property"][key]:
                    index["entities"]["by_property"][key][str(value)] = []
                index["entities"]["by_property"][key][str(value)].append(entity["id"])
        
        # Index relationships
        for rel in self._relationships:
            rel_type = rel.get("type")
            if rel_type not in index["relationships"]["by_type"]:
                index["relationships"]["by_type"][rel_type] = []
            index["relationships"]["by_type"][rel_type].append(rel["id"])
            
            source_id = rel.get("source_id")
            if source_id not in index["relationships"]["by_source"]:
                index["relationships"]["by_source"][source_id] = []
            index["relationships"]["by_source"][source_id].append(rel["id"])
            
            target_id = rel.get("target_id")
            if target_id not in index["relationships"]["by_target"]:
                index["relationships"]["by_target"][target_id] = []
            index["relationships"]["by_target"][target_id].append(rel["id"])
        
        return index
    
    def store_entity(self, entity: Dict[str, Any], 
                     session_id: Optional[str] = None) -> Tuple[StoreResult, List[ValidationError]]:
        """
        Store an entity in the knowledge graph.
        
        Args:
            entity: Entity to store
            session_id: Current session ID (for provenance)
        
        Returns:
            Tuple of (StoreResult, List[ValidationError])
        """
        # Validate
        errors = self._validate_entity(entity)
        if errors:
            return StoreResult(
                entity_id=entity.get("id", "unknown"),
                stored=False,
                updated=False,
                message="Validation failed"
            ), errors
        
        # Check if entity already exists
        existing = self._find_entity(entity["id"])
        
        if existing:
            # Update existing entity
            if entity.get("version") and existing.get("version"):
                # Version check
                existing_version = self._parse_version(existing.get("version", "1.0.0"))
                new_version = self._parse_version(entity.get("version", "1.0.0"))
                if new_version <= existing_version:
                    return StoreResult(
                        entity_id=entity["id"],
                        stored=False,
                        updated=False,
                        message="Version conflict"
                    ), []
            
            # Merge updates
            existing.update(entity)
            existing["updated_at"] = datetime.utcnow().isoformat()
            
            # Write to file
            self._append_to_file(self.entities_path, existing)
            
            # Update in memory
            self._update_entity_in_memory(existing)
            
            return StoreResult(
                entity_id=entity["id"],
                stored=False,
                updated=True,
                message="Entity updated"
            ), []
        else:
            # New entity
            entity["created_at"] = datetime.utcnow().isoformat()
            entity["updated_at"] = entity["created_at"]
            
            # Set provenance
            if "provenance" not in entity:
                entity["provenance"] = {}
            if session_id:
                entity["provenance"]["source"] = session_id
            
            # Write to file
            self._append_to_file(self.entities_path, entity)
            
            # Add to memory
            self._entities.append(entity)
            
            # Update index
            self._index_entity(entity)
            
            return StoreResult(
                entity_id=entity["id"],
                stored=True,
                updated=False,
                message="Entity stored"
            ), []
    
    def store_relationship(self, relationship: Dict[str, Any],
                           session_id: Optional[str] = None) -> Tuple[StoreResult, List[ValidationError]]:
        """
        Store a relationship in the knowledge graph.
        
        Args:
            relationship: Relationship to store
            session_id: Current session ID (for provenance)
        
        Returns:
            Tuple of (StoreResult, List[ValidationError])
        """
        # Validate
        errors = self._validate_relationship(relationship)
        if errors:
            return StoreResult(
                entity_id=relationship.get("id", "unknown"),
                stored=False,
                updated=False,
                message="Validation failed"
            ), errors
        
        # Check if relationship already exists
        existing = self._find_relationship(relationship["id"])
        
        if existing:
            # Update existing relationship
            existing.update(relationship)
            existing["updated_at"] = datetime.utcnow().isoformat()
            
            # Write to file
            self._append_to_file(self.relationships_path, existing)
            
            # Update in memory
            self._update_relationship_in_memory(existing)
            
            return StoreResult(
                entity_id=relationship["id"],
                stored=False,
                updated=True,
                message="Relationship updated"
            ), []
        else:
            # New relationship
            relationship["created_at"] = datetime.utcnow().isoformat()
            relationship["updated_at"] = relationship["created_at"]
            
            # Set provenance
            if "provenance" not in relationship:
                relationship["provenance"] = {}
            if session_id:
                relationship["provenance"]["source"] = session_id
            
            # Write to file
            self._append_to_file(self.relationships_path, relationship)
            
            # Add to memory
            self._relationships.append(relationship)
            
            # Update index
            self._index_relationship(relationship)
            
            return StoreResult(
                entity_id=relationship["id"],
                stored=True,
                updated=False,
                message="Relationship stored"
            ), []
    
    def store_session_context(self, session_id: str, context: Dict[str, Any]) -> bool:
        """
        Store complete session context.
        
        Args:
            session_id: Session identifier
            context: Session context to store
        
        Returns:
            True if successful
        """
        session_dir = self.sessions_path / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Store context
        context_path = session_dir / "context.json"
        try:
            with open(context_path, 'w', encoding='utf-8') as f:
                json.dump(context, f, indent=2)
            return True
        except IOError:
            return False
    
    def load_session_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load session context.
        
        Args:
            session_id: Session identifier
        
        Returns:
            Session context or None if not found
        """
        session_dir = self.sessions_path / session_id
        context_path = session_dir / "context.json"
        
        if not context_path.exists():
            return None
        
        try:
            with open(context_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def cache_data(self, key: str, data: Any, ttl_seconds: Optional[int] = None) -> bool:
        """
        Cache external data.
        
        Args:
            key: Cache key (should be hashable)
            data: Data to cache
            ttl_seconds: Time to live in seconds (None = no expiry)
        
        Returns:
            True if successful
        """
        # Create cache key hash
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        cache_file = self.cache_path / f"{key_hash}.json"
        
        # Add metadata
        cache_data = {
            "key": key,
            "data": data,
            "cached_at": datetime.utcnow().isoformat()
        }
        
        if ttl_seconds:
            cache_data["expires_at"] = datetime.fromtimestamp(
                datetime.utcnow().timestamp() + ttl_seconds
            ).isoformat()
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f)
            return True
        except IOError:
            return False
    
    def get_cached_data(self, key: str) -> Optional[Any]:
        """
        Get cached data.
        
        Args:
            key: Cache key
        
        Returns:
            Cached data or None if not found or expired
        """
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        cache_file = self.cache_path / f"{key_hash}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check expiry
            if "expires_at" in cache_data:
                expiry = datetime.fromisoformat(cache_data["expires_at"])
                if datetime.utcnow() > expiry:
                    # Expired, remove
                    cache_file.unlink()
                    return None
            
            return cache_data.get("data")
        except (json.JSONDecodeError, IOError):
            return None
    
    def _append_to_file(self, path: Path, data: Dict[str, Any]):
        """Append a JSON object to a JSONL file."""
        try:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        except IOError:
            pass
    
    def _find_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Find an entity by ID."""
        for entity in self._entities:
            if entity.get("id") == entity_id:
                return entity
        return None
    
    def _find_relationship(self, rel_id: str) -> Optional[Dict[str, Any]]:
        """Find a relationship by ID."""
        for rel in self._relationships:
            if rel.get("id") == rel_id:
                return rel
        return None
    
    def _update_entity_in_memory(self, entity: Dict[str, Any]):
        """Update entity in memory storage."""
        for i, e in enumerate(self._entities):
            if e.get("id") == entity.get("id"):
                self._entities[i] = entity
                self._index_entity(entity)
                self._save_index()
                return
    
    def _update_relationship_in_memory(self, relationship: Dict[str, Any]):
        """Update relationship in memory storage."""
        for i, r in enumerate(self._relationships):
            if r.get("id") == relationship.get("id"):
                self._relationships[i] = relationship
                self._index_relationship(relationship)
                self._save_index()
                return
    
    def _index_entity(self, entity: Dict[str, Any]):
        """Index a single entity."""
        entity_type = entity.get("type")
        entity_id = entity["id"]
        
        # Index by type
        if entity_type not in self._index["entities"]["by_type"]:
            self._index["entities"]["by_type"][entity_type] = []
        if entity_id not in self._index["entities"]["by_type"][entity_type]:
            self._index["entities"]["by_type"][entity_type].append(entity_id)
        
        # Index by properties
        for key, value in entity.items():
            if key in ["id", "type", "created_at", "updated_at", "provenance", "metadata"]:
                continue
            if key not in self._index["entities"]["by_property"]:
                self._index["entities"]["by_property"][key] = {}
            str_value = str(value)
            if str_value not in self._index["entities"]["by_property"][key]:
                self._index["entities"]["by_property"][key][str_value] = []
            if entity_id not in self._index["entities"]["by_property"][key][str_value]:
                self._index["entities"]["by_property"][key][str_value].append(entity_id)
    
    def _index_relationship(self, relationship: Dict[str, Any]):
        """Index a single relationship."""
        rel_type = relationship.get("type")
        rel_id = relationship["id"]
        source_id = relationship.get("source_id")
        target_id = relationship.get("target_id")
        
        # Index by type
        if rel_type not in self._index["relationships"]["by_type"]:
            self._index["relationships"]["by_type"][rel_type] = []
        if rel_id not in self._index["relationships"]["by_type"][rel_type]:
            self._index["relationships"]["by_type"][rel_type].append(rel_id)
        
        # Index by source
        if source_id not in self._index["relationships"]["by_source"]:
            self._index["relationships"]["by_source"][source_id] = []
        if rel_id not in self._index["relationships"]["by_source"][source_id]:
            self._index["relationships"]["by_source"][source_id].append(rel_id)
        
        # Index by target
        if target_id not in self._index["relationships"]["by_target"]:
            self._index["relationships"]["by_target"][target_id] = []
        if rel_id not in self._index["relationships"]["by_target"][target_id]:
            self._index["relationships"]["by_target"][target_id].append(rel_id)
    
    def _validate_entity(self, entity: Dict[str, Any]) -> List[ValidationError]:
        """Validate an entity against schema."""
        errors = []
        entity_type = entity.get("type")
        
        # Check type is valid
        if entity_type not in self.ENTITY_TYPES:
            errors.append(ValidationError(
                field="type",
                message=f"Invalid entity type: {entity_type}"
            ))
            return errors
        
        # Check required fields
        required = self.REQUIRED_FIELDS.get(entity_type, [])
        for field in required:
            if field not in entity:
                errors.append(ValidationError(
                    field=field,
                    message=f"Missing required field: {field}"
                ))
        
        # Check ID format
        if "id" in entity:
            if not entity["id"] or not isinstance(entity["id"], str):
                errors.append(ValidationError(
                    field="id",
                    message="ID must be a non-empty string"
                ))
        
        # Check enum values
        for field, valid_values in self.VALID_ENUMS.items():
            if field in entity:
                value = entity[field]
                if value not in valid_values:
                    errors.append(ValidationError(
                        field=field,
                        message=f"Invalid value: {value}. Must be one of: {valid_values}"
                    ))
        
        # Check for sensitive data
        sensitive_fields = ["password", "secret", "token", "api_key", "apikey", "credential"]
        for field in entity:
            field_lower = field.lower()
            if any(sensitive in field_lower for sensitive in sensitive_fields):
                errors.append(ValidationError(
                    field=field,
                    message=f"Potential sensitive field: {field}",
                    severity="error"
                ))
        
        return errors
    
    def _validate_relationship(self, relationship: Dict[str, Any]) -> List[ValidationError]:
        """Validate a relationship."""
        errors = []
        
        # Check required fields
        required = ["id", "type", "source_id", "target_id"]
        for field in required:
            if field not in relationship:
                errors.append(ValidationError(
                    field=field,
                    message=f"Missing required field: {field}"
                ))
        
        # Check ID format
        if "id" in relationship:
            if not relationship["id"] or not isinstance(relationship["id"], str):
                errors.append(ValidationError(
                    field="id",
                    message="ID must be a non-empty string"
                ))
        
        return errors
    
    def _parse_version(self, version: str) -> Tuple[int, ...]:
        """Parse version string into tuple of ints."""
        try:
            parts = version.split(".")
            return tuple(int(p) for p in parts)
        except:
            return (0,)
    
    def flush(self):
        """Flush all changes to disk."""
        self._save_index()


# Singleton instance
_default_storage_engine = None


def get_storage_engine(knowledge_path: Optional[Path] = None) -> StorageEngine:
    """Get or create the default storage engine."""
    global _default_storage_engine
    if _default_storage_engine is None or knowledge_path:
        _default_storage_engine = StorageEngine(knowledge_path)
    return _default_storage_engine
