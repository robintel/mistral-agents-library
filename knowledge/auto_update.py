#!/usr/bin/env python3
"""
Auto-Update Mechanism for Knowledge Graph

This module provides automatic detection and resolution of knowledge drift
between the persisted knowledge graph and the current state of repositories.

Features:
- Change detection: Identify modified, added, and deleted files
- Auto-update: Automatically refresh stale knowledge
- Reconciliation: Handle different types of changes appropriately
- Freshness tracking: Monitor and report knowledge freshness
"""

import os
import json
import hashlib
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum


# ============================================================================
# Data Classes
# ============================================================================

class ChangeType(Enum):
    """Types of changes that can be detected."""
    FILE_MODIFIED = "file_modified"
    FILE_ADDED = "file_added"
    FILE_DELETED = "file_deleted"
    FILE_RENAMED = "file_renamed"
    REPO_MODIFIED = "repo_modified"
    FINDING_STALE = "finding_stale"
    ENTITY_STALE = "entity_stale"


@dataclass
class EntityChange:
    """Represents a single change to an entity."""
    change_type: ChangeType
    entity_id: str
    entity_type: str
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    severity: str = "medium"  # low, medium, high, critical
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "change_type": self.change_type.value,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "timestamp": self.timestamp,
            "severity": self.severity
        }


@dataclass
class DriftReport:
    """Report of all detected changes between persisted and current state."""
    repo_id: str
    repo_path: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    changes: List[EntityChange] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)
    freshness_score: float = 1.0
    
    def __post_init__(self):
        if not self.stats:
            self.stats = {
                "total_files": 0,
                "modified_files": 0,
                "added_files": 0,
                "deleted_files": 0,
                "stale_findings": 0,
                "stale_entities": 0
            }
    
    def add_change(self, change: EntityChange):
        """Add a change to the report."""
        self.changes.append(change)
        
        # Update stats
        if change.change_type == ChangeType.FILE_MODIFIED:
            self.stats["modified_files"] += 1
            self.severity = max(self.severity, change.severity) if hasattr(self, 'severity') else change.severity
        elif change.change_type == ChangeType.FILE_ADDED:
            self.stats["added_files"] += 1
        elif change.change_type == ChangeType.FILE_DELETED:
            self.stats["deleted_files"] += 1
        elif change.change_type == ChangeType.FINDING_STALE:
            self.stats["stale_findings"] += 1
        elif change.change_type == ChangeType.ENTITY_STALE:
            self.stats["stale_entities"] += 1
        
        self.stats["total_files"] += 1
    
    def has_changes(self) -> bool:
        """Check if any changes were detected."""
        return len(self.changes) > 0
    
    def has_critical_changes(self) -> bool:
        """Check if there are critical changes."""
        return any(c.severity == "critical" for c in self.changes)
    
    def has_high_severity_changes(self) -> bool:
        """Check if there are high severity changes."""
        return any(c.severity in ["critical", "high"] for c in self.changes)
    
    def get_changed_file_ids(self) -> Set[str]:
        """Get all file IDs that have changed."""
        return {
            c.entity_id for c in self.changes 
            if c.change_type in [ChangeType.FILE_MODIFIED, ChangeType.FILE_ADDED, ChangeType.FILE_DELETED]
        }
    
    def get_stale_finding_ids(self) -> Set[str]:
        """Get all finding IDs that are stale."""
        return {
            c.entity_id for c in self.changes 
            if c.change_type == ChangeType.FINDING_STALE
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "repo_id": self.repo_id,
            "repo_path": self.repo_path,
            "timestamp": self.timestamp,
            "changes": [c.to_dict() for c in self.changes],
            "stats": self.stats,
            "freshness_score": self.freshness_score,
            "has_changes": self.has_changes(),
            "has_critical_changes": self.has_critical_changes()
        }


@dataclass
class FreshnessPolicy:
    """Defines freshness policy for entity types."""
    entity_type: str
    ttl_seconds: int  # Time-to-live in seconds
    auto_refresh: bool = True
    refresh_trigger: str = "access"  # access, schedule, manual
    refresh_priority: int = 0  # 0 = low, 1 = medium, 2 = high
    
    @classmethod
    def default_policies(cls) -> List["FreshnessPolicy"]:
        """Get default freshness policies for all entity types."""
        return [
            FreshnessPolicy("Repository", 3600, True, "access", 1),  # 1 hour
            FreshnessPolicy("File", 3600, True, "access", 1),  # 1 hour
            FreshnessPolicy("Finding", 86400, True, "re_audit", 2),  # 24 hours
            FreshnessPolicy("Decision", 2592000, False, "manual", 0),  # 30 days (manual)
            FreshnessPolicy("Task", 604800, True, "status_change", 1),  # 7 days
            FreshnessPolicy("Session", 86400, True, "end", 0),  # 24 hours
            FreshnessPolicy("Dataset", 86400, True, "access", 1),  # 24 hours
        ]
    
    @classmethod
    def get_policy(cls, entity_type: str) -> Optional["FreshnessPolicy"]:
        """Get freshness policy for a specific entity type."""
        for policy in cls.default_policies():
            if policy.entity_type == entity_type:
                return policy
        return None


@dataclass
class FreshnessStatus:
    """Freshness status for a repository or entity."""
    repo_id: str
    score: float  # 0-1, where 1 = fully fresh
    last_updated: str
    stale_entities: int = 0
    total_entities: int = 0
    next_refresh: Optional[str] = None
    status: str = "fresh"  # fresh, stale, critical
    
    def is_fresh(self, threshold: float = 0.95) -> bool:
        """Check if knowledge is fresh."""
        return self.score >= threshold
    
    def is_stale(self, threshold: float = 0.8) -> bool:
        """Check if knowledge is stale."""
        return self.score < threshold and self.score >= 0.5
    
    def is_critical(self, threshold: float = 0.5) -> bool:
        """Check if knowledge is critically stale."""
        return self.score < threshold


# ============================================================================
# Utility Functions
# ============================================================================

def compute_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Compute hash of a file's content."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            if algorithm == "sha256":
                return hashlib.sha256(content).hexdigest()
            elif algorithm == "md5":
                return hashlib.md5(content).hexdigest()
            else:
                return hashlib.sha256(content).hexdigest()
    except (FileNotFoundError, PermissionError, OSError):
        return ""


def compute_repo_fingerprint(repo_path: str) -> str:
    """Compute fingerprint for a repository based on its path."""
    return hashlib.sha256(repo_path.encode()).hexdigest()[:16]


def get_timestamp() -> str:
    """Get current timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def is_expired(timestamp: str, ttl_seconds: int) -> bool:
    """Check if a timestamp is expired based on TTL."""
    if ttl_seconds == 0:
        return False
    try:
        ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return (datetime.now(timezone.utc) - ts) > timedelta(seconds=ttl_seconds)
    except (ValueError, TypeError):
        return True


# ============================================================================
# Knowledge Graph Interface (Abstract)
# ============================================================================

class KnowledgeGraphInterface:
    """Abstract interface for knowledge graph operations."""
    
    def query_entities(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query entities from the knowledge graph."""
        raise NotImplementedError
    
    def query_relationships(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query relationships from the knowledge graph."""
        raise NotImplementedError
    
    def store_entity(self, entity: Dict[str, Any], session_id: Optional[str] = None) -> Dict[str, Any]:
        """Store an entity in the knowledge graph."""
        raise NotImplementedError
    
    def store_relationship(self, relationship: Dict[str, Any], session_id: Optional[str] = None) -> Dict[str, Any]:
        """Store a relationship in the knowledge graph."""
        raise NotImplementedError
    
    def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity from the knowledge graph."""
        raise NotImplementedError
    
    def delete_relationship(self, relationship_id: str) -> bool:
        """Delete a relationship from the knowledge graph."""
        raise NotImplementedError


# ============================================================================
# File System Knowledge Graph (Default Implementation)
# ============================================================================

# Import file locking if available (POSIX systems)
try:
    import fcntl
    HAS_FLOCK = True
except ImportError:
    HAS_FLOCK = False
    fcntl = None


class FileSystemKnowledgeGraph(KnowledgeGraphInterface):
    """Knowledge graph implementation using the file system."""
    
    def __init__(self, knowledge_dir: Optional[str] = None):
        """Initialize the knowledge graph."""
        if knowledge_dir is None:
            knowledge_dir = os.path.expanduser("~/.mistral-agents/knowledge")
        self.knowledge_dir = Path(knowledge_dir)
        self.graph_dir = self.knowledge_dir / "graph"
        self.sessions_dir = self.knowledge_dir / "sessions"
        self.cache_dir = self.knowledge_dir / "cache"
        
        # File lock for concurrent access protection
        self._lock_file = self.knowledge_dir / ".knowledge_lock"
        self._lock_fd = None
        
        # Ensure directories exist
        self.graph_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _acquire_lock(self):
        """Acquire file lock for atomic operations."""
        if not HAS_FLOCK:
            return  # No locking on Windows
        
        if self._lock_fd is None:
            self._lock_fd = open(self._lock_file, 'w')
        
        fcntl.flock(self._lock_fd, fcntl.LOCK_EX)
    
    def _release_lock(self):
        """Release file lock."""
        if not HAS_FLOCK or self._lock_fd is None:
            return
        
        try:
            fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
        except Exception:
            pass
    
    def __enter__(self):
        """Context manager entry - acquire lock."""
        self._acquire_lock()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - release lock."""
        self._release_lock()
        return False
    
    def __del__(self):
        """Clean up lock file descriptor."""
        if self._lock_fd is not None:
            try:
                self._lock_fd.close()
            except Exception:
                pass
            self._lock_fd = None
    
    def query_entities(self, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query entities from the knowledge graph."""
        self._acquire_lock()
        try:
            entities_file = self.graph_dir / "entities.jsonl"
            entities = []
            
            if not entities_file.exists():
                return []
            
            with open(entities_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            entity = json.loads(line)
                            entities.append(entity)
                        except json.JSONDecodeError:
                            continue
            
            # Apply filters
            if query:
                filtered = []
                for entity in entities:
                    match = True
                    for key, value in query.items():
                        if key == "type":
                            if entity.get("type") != value:
                                match = False
                                break
                        elif key == "repo_id":
                            if entity.get("repo_id") != value:
                                match = False
                                break
                        elif key == "id":
                            if entity.get("id") != value:
                                match = False
                                break
                        elif key == "status":
                            if entity.get("status") != value:
                                match = False
                                break
                        elif key.startswith("metadata."):
                            field = key.split(".")[1]
                            if entity.get("metadata", {}).get(field) != value:
                                match = False
                                break
                        elif key.startswith("location."):
                            field = key.split(".")[1]
                            if entity.get("location", {}).get(field) != value:
                                match = False
                                break
                        else:
                            # Generic field match
                            if entity.get(key) != value:
                                match = False
                                break
                    if match:
                        filtered.append(entity)
                return filtered
            
            return entities
        finally:
            self._release_lock()
    
    def query_relationships(self, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query relationships from the knowledge graph."""
        self._acquire_lock()
        try:
            relationships_file = self.graph_dir / "relationships.jsonl"
            relationships = []
            
            if not relationships_file.exists():
                return []
            
            with open(relationships_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            rel = json.loads(line)
                            relationships.append(rel)
                        except json.JSONDecodeError:
                            continue
            
            if query:
                filtered = []
                for rel in relationships:
                    match = True
                    for key, value in query.items():
                        if rel.get(key) != value:
                            match = False
                            break
                    if match:
                        filtered.append(rel)
                return filtered
            
            return relationships
        finally:
            self._release_lock()
    
    def store_entity(self, entity: Dict[str, Any], session_id: Optional[str] = None) -> Dict[str, Any]:
        """Store an entity in the knowledge graph."""
        if "id" not in entity:
            raise ValueError("Entity must have an 'id' field")
        if "type" not in entity:
            raise ValueError("Entity must have a 'type' field")
        
        # Add timestamps if not present
        entity.setdefault("created_at", get_timestamp())
        entity.setdefault("updated_at", get_timestamp())
        
        # Add provenance if not present
        if "provenance" not in entity:
            entity["provenance"] = {
                "source": "auto_update",
                "confidence": 0.95,
                "method": "auto_detection"
            }
        
        if session_id:
            entity.setdefault("metadata", {})["session_id"] = session_id
        
        self._acquire_lock()
        try:
            entities_file = self.graph_dir / "entities.jsonl"
            
            # Atomic write: write to temp file, then rename
            temp_file = entities_file.with_suffix('.tmp')
            try:
                # Read existing entities
                existing_lines = []
                if entities_file.exists():
                    with open(entities_file, 'r') as f:
                        existing_lines = f.readlines()
                
                # Write all existing + new entity to temp file
                with open(temp_file, 'w') as f:
                    f.writelines(existing_lines)
                    json.dump(entity, f)
                    f.write('\n')
                
                # Atomic rename (POSIX guarantees this is atomic)
                temp_file.rename(entities_file)
            finally:
                # Clean up temp file if rename failed
                if temp_file.exists():
                    temp_file.unlink(missing_ok=True)
        finally:
            self._release_lock()
        
        return entity
    
    def store_relationship(self, relationship: Dict[str, Any], session_id: Optional[str] = None) -> Dict[str, Any]:
        """Store a relationship in the knowledge graph."""
        if "id" not in relationship:
            raise ValueError("Relationship must have an 'id' field")
        if "type" not in relationship:
            raise ValueError("Relationship must have a 'type' field")
        if "source_id" not in relationship:
            raise ValueError("Relationship must have a 'source_id' field")
        if "target_id" not in relationship:
            raise ValueError("Relationship must have a 'target_id' field")
        
        relationship.setdefault("created_at", get_timestamp())
        
        if "provenance" not in relationship:
            relationship["provenance"] = {
                "source": "auto_update",
                "confidence": 0.95
            }
        
        self._acquire_lock()
        try:
            relationships_file = self.graph_dir / "relationships.jsonl"
            
            # Atomic write: write to temp file, then rename
            temp_file = relationships_file.with_suffix('.tmp')
            try:
                # Read existing relationships
                existing_lines = []
                if relationships_file.exists():
                    with open(relationships_file, 'r') as f:
                        existing_lines = f.readlines()
                
                # Write all existing + new relationship to temp file
                with open(temp_file, 'w') as f:
                    f.writelines(existing_lines)
                    json.dump(relationship, f)
                    f.write('\n')
                
                # Atomic rename (POSIX guarantees this is atomic)
                temp_file.rename(relationships_file)
            finally:
                # Clean up temp file if rename failed
                if temp_file.exists():
                    temp_file.unlink(missing_ok=True)
        finally:
            self._release_lock()
        
        return relationship
    
    def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity from the knowledge graph."""
        self._acquire_lock()
        try:
            entities_file = self.graph_dir / "entities.jsonl"
            
            if not entities_file.exists():
                return False
            
            # Read all entities
            with open(entities_file, 'r') as f:
                lines = f.readlines()
            
            # Filter out the entity to delete
            new_lines = []
            deleted = False
            for line in lines:
                if line.strip():
                    try:
                        entity = json.loads(line)
                        if entity.get("id") == entity_id:
                            deleted = True
                            continue
                        new_lines.append(line)
                    except json.JSONDecodeError:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            # Atomic write: write to temp file, then rename
            temp_file = entities_file.with_suffix('.tmp')
            try:
                with open(temp_file, 'w') as f:
                    f.writelines(new_lines)
                
                # Atomic rename (POSIX guarantees this is atomic)
                temp_file.rename(entities_file)
            finally:
                # Clean up temp file if rename failed
                if temp_file.exists():
                    temp_file.unlink(missing_ok=True)
        finally:
            self._release_lock()
        
        return deleted
    
    def delete_relationship(self, relationship_id: str) -> bool:
        """Delete a relationship from the knowledge graph."""
        self._acquire_lock()
        try:
            relationships_file = self.graph_dir / "relationships.jsonl"
            
            if not relationships_file.exists():
                return False
            
            with open(relationships_file, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            deleted = False
            for line in lines:
                if line.strip():
                    try:
                        rel = json.loads(line)
                        if rel.get("id") == relationship_id:
                            deleted = True
                            continue
                        new_lines.append(line)
                    except json.JSONDecodeError:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            # Atomic write: write to temp file, then rename
            temp_file = relationships_file.with_suffix('.tmp')
            try:
                with open(temp_file, 'w') as f:
                    f.writelines(new_lines)
                
                # Atomic rename (POSIX guarantees this is atomic)
                temp_file.rename(relationships_file)
            finally:
                # Clean up temp file if rename failed
                if temp_file.exists():
                    temp_file.unlink(missing_ok=True)
        finally:
            self._release_lock()
        
        return deleted


# ============================================================================
# Change Detector
# ============================================================================

class ChangeDetector:
    """Detects changes between persisted state and current state."""
    
    def __init__(self, kg: KnowledgeGraphInterface = None):
        """Initialize the change detector."""
        self.kg = kg or FileSystemKnowledgeGraph()
    
    def detect_drift(self, repo_path: str, session_id: Optional[str] = None) -> DriftReport:
        """
        Detect all changes between persisted knowledge and current state.
        
        Args:
            repo_path: Path to the repository
            session_id: Optional session ID for tracking
            
        Returns:
            DriftReport containing all detected changes
        """
        repo_fingerprint = compute_repo_fingerprint(repo_path)
        repo_id = f"repo:{repo_fingerprint}"
        
        report = DriftReport(
            repo_id=repo_id,
            repo_path=repo_path
        )
        
        # Get persisted repository entity
        repos = self.kg.query_entities({"type": "Repository", "path": repo_path})
        
        if not repos:
            # New repository - create entity and continue scanning
            repo_entity = {
                "id": repo_id,
                "type": "Repository",
                "path": repo_path,
                "fingerprint": repo_fingerprint,
                "created_at": get_timestamp()
            }
            self.kg.store_entity(repo_entity)
            # Add change to report
            report.add_change(EntityChange(
                change_type=ChangeType.REPO_MODIFIED,
                entity_id=repo_id,
                entity_type="Repository",
                severity="high"
            ))
            repo = repo_entity
        else:
            repo = repos[0]
        
        # Get all persisted files for this repo
        persisted_files = self.kg.query_entities({"type": "File", "repo_id": repo_id})
        
        # Get all current files in the repository
        current_files = self._scan_repository_files(repo_path)
        
        # Build map of persisted files by path
        persisted_by_path = {f["path"]: f for f in persisted_files}
        
        # Detect added, modified, and deleted files
        for file_path, file_info in current_files.items():
            full_path = os.path.join(repo_path, file_path)
            current_hash = compute_file_hash(full_path)
            
            if file_path in persisted_by_path:
                # File exists in both - check if modified
                persisted_file = persisted_by_path[file_path]
                if persisted_file.get("content_hash") != current_hash:
                    report.add_change(EntityChange(
                        change_type=ChangeType.FILE_MODIFIED,
                        entity_id=persisted_file["id"],
                        entity_type="File",
                        old_value={"hash": persisted_file.get("content_hash")},
                        new_value={"hash": current_hash},
                        severity="high"
                    ))
                    # Mark related findings as stale
                    self._mark_related_findings_stale(report, persisted_file["id"])
            else:
                # New file - added
                report.add_change(EntityChange(
                    change_type=ChangeType.FILE_ADDED,
                    entity_id=f"file:{repo_fingerprint}:{file_path}",
                    entity_type="File",
                    new_value={"path": file_path, "hash": current_hash},
                    severity="medium"
                ))
        
        # Check for deleted files
        for file_path, persisted_file in persisted_by_path.items():
            if file_path not in current_files:
                report.add_change(EntityChange(
                    change_type=ChangeType.FILE_DELETED,
                    entity_id=persisted_file["id"],
                    entity_type="File",
                    old_value={"path": file_path, "hash": persisted_file.get("content_hash")},
                    severity="high"
                ))
                # Delete relationships for this file
                self._mark_related_findings_stale(report, persisted_file["id"])
        
        # Check for stale entities (based on TTL)
        self._check_stale_entities(report, repo_id)
        
        # Calculate freshness score
        report.freshness_score = self._calculate_freshness_score(report, repo_id)
        
        return report
    
    def _scan_repository_files(self, repo_path: str) -> Dict[str, Dict[str, Any]]:
        """Scan repository and return file information."""
        files = {}
        
        for root, dirs, filenames in os.walk(repo_path):
            # Skip .git, node_modules, dist, etc.
            dirs[:] = [d for d in dirs if d not in [".git", "node_modules", "dist", "build", "__pycache__", ".vscode", ".idea"]]
            
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, repo_path)
                
                # Skip binary files, logs, etc.
                if self._should_skip_file(filename):
                    continue
                
                file_hash = compute_file_hash(file_path)
                if file_hash:  # Only include if we could read the file
                    files[rel_path] = {
                        "path": rel_path,
                        "hash": file_hash,
                        "size": os.path.getsize(file_path),
                        "mtime": os.path.getmtime(file_path)
                    }
        
        return files
    
    def _should_skip_file(self, filename: str) -> bool:
        """Check if a file should be skipped."""
        skip_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp',
            '.mp3', '.mp4', '.avi', '.mov', '.wav', '.ogg',
            '.zip', '.tar', '.gz', '.rar', '.7z',
            '.exe', '.dll', '.so', '.o', '.bin',
            '.log', '.tmp', '.swp', '.bak', '.cache',
            '.lock', '.json.lock', '.pid'
        }
        
        skip_files = {
            'package-lock.json',
            'yarn.lock',
            'pnpm-lock.yaml',
            '.DS_Store',
            'Thumbs.db'
        }
        
        if filename.lower() in skip_files:
            return True
        
        if any(filename.lower().endswith(ext) for ext in skip_extensions):
            return True
        
        return False
    
    def _mark_related_findings_stale(self, report: DriftReport, file_id: str):
        """Mark findings related to a file as stale."""
        # Find relationships where this file has findings
        relationships = self.kg.query_relationships({
            "type": "has_finding",
            "source_id": file_id
        })
        
        for rel in relationships:
            finding_id = rel["target_id"]
            report.add_change(EntityChange(
                change_type=ChangeType.FINDING_STALE,
                entity_id=finding_id,
                entity_type="Finding",
                severity="high"
            ))
    
    def _check_stale_entities(self, report: DriftReport, repo_id: str):
        """Check for stale entities based on TTL."""
        policies = FreshnessPolicy.default_policies()
        
        for policy in policies:
            if not policy.auto_refresh:
                continue
            
            entities = self.kg.query_entities({
                "type": policy.entity_type,
                "repo_id": repo_id
            })
            
            for entity in entities:
                if is_expired(entity.get("updated_at", ""), policy.ttl_seconds):
                    report.add_change(EntityChange(
                        change_type=ChangeType.ENTITY_STALE,
                        entity_id=entity["id"],
                        entity_type=policy.entity_type,
                        severity="medium"
                    ))
    
    def _calculate_freshness_score(self, report: DriftReport, repo_id: str) -> float:
        """Calculate freshness score for the repository."""
        total_entities = self.kg.query_entities({"repo_id": repo_id})
        if not total_entities:
            return 1.0
        
        stale_count = len(report.get_stale_finding_ids())
        
        # Also count modified files as stale
        modified_files = report.stats.get("modified_files", 0)
        deleted_files = report.stats.get("deleted_files", 0)
        added_files = report.stats.get("added_files", 0)
        
        total_issues = stale_count + modified_files + deleted_files + added_files
        
        if total_issues == 0:
            return 1.0
        
        # Weight issues by severity
        critical_issues = sum(1 for c in report.changes if c.severity == "critical")
        high_issues = sum(1 for c in report.changes if c.severity == "high")
        
        weight = (critical_issues * 3 + high_issues * 2 + (total_issues - critical_issues - high_issues) * 1)
        
        return max(0.0, 1.0 - (weight / len(total_entities)))


# ============================================================================
# Auto Updater
# ============================================================================

class AutoUpdater:
    """Automatically updates the knowledge graph when changes are detected."""
    
    def __init__(self, kg: KnowledgeGraphInterface = None):
        """Initialize the auto updater."""
        self.kg = kg or FileSystemKnowledgeGraph()
        self.detector = ChangeDetector(kg)
        self.reconciler = Reconciler(kg)
    
    def update(self, repo_path: str, session_id: Optional[str] = None) -> DriftReport:
        """
        Check for changes and update the knowledge graph.
        
        Args:
            repo_path: Path to the repository
            session_id: Optional session ID for tracking
            
        Returns:
            DriftReport with all changes detected and applied
        """
        repo_fingerprint = compute_repo_fingerprint(repo_path)
        repo_id = f"repo:{repo_fingerprint}"
        
        # Ensure repository entity exists
        repos = self.kg.query_entities({"type": "Repository", "id": repo_id})
        if not repos:
            # Create repository entity
            repo_entity = {
                "id": repo_id,
                "type": "Repository",
                "path": repo_path,
                "fingerprint": repo_fingerprint,
                "created_at": get_timestamp(),
                "updated_at": get_timestamp(),
                "version": "1"
            }
            self.kg.store_entity(repo_entity, session_id)
        
        # Detect drift
        report = self.detector.detect_drift(repo_path, session_id)
        
        if not report.has_changes():
            return report
        
        # Apply updates
        self.reconciler.reconcile(report, session_id)
        
        # Store update metadata
        self._store_update_metadata(report, session_id)
        
        return report
    
    def on_session_start(self, repo_path: str, session_id: str) -> DriftReport:
        """
        Check for changes when a session starts.
        
        Args:
            repo_path: Path to the repository
            session_id: Current session ID
            
        Returns:
            DriftReport with any changes detected
        """
        return self.update(repo_path, session_id)
    
    def on_agent_dispatch(self, repo_path: str, agent_type: str, session_id: str) -> DriftReport:
        """
        Check for changes before dispatching an agent.
        
        Args:
            repo_path: Path to the repository
            agent_type: Type of agent being dispatched
            session_id: Current session ID
            
        Returns:
            DriftReport with any changes detected
        """
        # Only check for certain agent types
        agents_requiring_refresh = [
            "tour-sentry", "tour-siren", "tour-supper-model",
            "implementer", "code-reviewer", "debugger"
        ]
        
        if agent_type in agents_requiring_refresh:
            return self.update(repo_path, session_id)
        
        return DriftReport(
            repo_id=compute_repo_fingerprint(repo_path),
            repo_path=repo_path
        )
    
    def full_refresh(self, repo_path: str, session_id: Optional[str] = None) -> DriftReport:
        """
        Perform a full refresh of the repository knowledge.
        
        Args:
            repo_path: Path to the repository
            session_id: Optional session ID for tracking
            
        Returns:
            DriftReport with all changes
        """
        # For now, just call update (can be enhanced for full refresh)
        return self.update(repo_path, session_id)
    
    def _store_update_metadata(self, report: DriftReport, session_id: Optional[str]):
        """Store metadata about the update."""
        # This could be enhanced to store more detailed metadata
        pass


# ============================================================================
# Reconciler
# ============================================================================

class Reconciler:
    """Reconciles detected changes with the knowledge graph."""
    
    def __init__(self, kg: KnowledgeGraphInterface = None):
        """Initialize the reconciler."""
        self.kg = kg or FileSystemKnowledgeGraph()
    
    def reconcile(self, report: DriftReport, session_id: Optional[str] = None):
        """
        Apply reconciliation strategies to detected changes.
        
        Args:
            report: DriftReport with detected changes
            session_id: Optional session ID for tracking
        """
        for change in report.changes:
            self._handle_change(change, session_id)
    
    def _handle_change(self, change: EntityChange, session_id: Optional[str]):
        """Handle a single change."""
        if change.change_type == ChangeType.FILE_MODIFIED:
            self._handle_file_modified(change, session_id)
        elif change.change_type == ChangeType.FILE_ADDED:
            self._handle_file_added(change, session_id)
        elif change.change_type == ChangeType.FILE_DELETED:
            self._handle_file_deleted(change, session_id)
        elif change.change_type == ChangeType.FILE_RENAMED:
            self._handle_file_renamed(change, session_id)
        elif change.change_type == ChangeType.FINDING_STALE:
            self._handle_finding_stale(change, session_id)
        elif change.change_type == ChangeType.ENTITY_STALE:
            self._handle_entity_stale(change, session_id)
        elif change.change_type == ChangeType.REPO_MODIFIED:
            self._handle_repo_modified(change, session_id)
    
    def _handle_file_modified(self, change: EntityChange, session_id: Optional[str]):
        """Handle a modified file."""
        # Update the file entity with new hash
        file_id = change.entity_id
        files = self.kg.query_entities({"type": "File", "id": file_id})
        
        if files:
            file_entity = files[0]
            if change.new_value and "hash" in change.new_value:
                # Delete old entity to avoid duplicates
                self.kg.delete_entity(file_id)
                
                file_entity["content_hash"] = change.new_value["hash"]
                file_entity["updated_at"] = get_timestamp()
                
                # Increment version
                file_entity["version"] = str(int(file_entity.get("version", "1")) + 1)
                
                self.kg.store_entity(file_entity, session_id)
                
                # Update the change to reflect the update
                change.severity = "low"  # Now handled
    
    def _handle_file_added(self, change: EntityChange, session_id: Optional[str]):
        """Handle a new file."""
        # Check if file already exists (to avoid duplicates)
        files = self.kg.query_entities({"type": "File", "id": change.entity_id})
        if files:
            # File already exists, skip
            return
        
        # Extract repo_id from entity_id (format: file:{repo_fingerprint}:{path})
        parts = change.entity_id.split(":", 2)
        if len(parts) >= 2:
            repo_id = f"repo:{parts[1]}"
        else:
            repo_id = "unknown"
        file_path = change.new_value.get("path", "") if change.new_value else ""
        file_hash = change.new_value.get("hash", "") if change.new_value else ""
        
        # Create new file entity
        file_entity = {
            "id": change.entity_id,
            "type": "File",
            "path": file_path,
            "repo_id": repo_id,
            "hash": file_hash,
            "content_hash": file_hash,
            "language": self._detect_language(file_path),
            "lines_of_code": 0,  # Can be updated later
            "created_at": get_timestamp(),
            "updated_at": get_timestamp(),
            "version": "1"
        }
        
        self.kg.store_entity(file_entity, session_id)
        
        # Create relationship from repo to file
        repo = self.kg.query_entities({"type": "Repository", "id": repo_id})
        if repo:
            relationship = {
                "id": f"rel:{repo_id}:contains:{change.entity_id}",
                "type": "contains",
                "source_id": repo_id,
                "target_id": change.entity_id
            }
            self.kg.store_relationship(relationship, session_id)
    
    def _handle_file_deleted(self, change: EntityChange, session_id: Optional[str]):
        """Handle a deleted file."""
        # Delete the file entity
        self.kg.delete_entity(change.entity_id)
        
        # Delete relationships involving this file
        relationships = self.kg.query_relationships({
            "source_id": change.entity_id
        })
        for rel in relationships:
            self.kg.delete_relationship(rel["id"])
        
        relationships = self.kg.query_relationships({
            "target_id": change.entity_id
        })
        for rel in relationships:
            self.kg.delete_relationship(rel["id"])
    
    def _handle_file_renamed(self, change: EntityChange, session_id: Optional[str]):
        """Handle a renamed file."""
        # This would require tracking old and new paths
        # For now, treat as delete + add
        if change.old_value and "path" in change.old_value:
            old_file_id = change.entity_id  # Assuming this is the old ID
            # Delete old entity
            self.kg.delete_entity(old_file_id)
        
        if change.new_value and "path" in change.new_value:
            # Add new entity (handled by _handle_file_added)
            new_change = EntityChange(
                change_type=ChangeType.FILE_ADDED,
                entity_id=change.entity_id,
                entity_type="File",
                new_value=change.new_value
            )
            self._handle_file_added(new_change, session_id)
    
    def _handle_finding_stale(self, change: EntityChange, session_id: Optional[str]):
        """Handle a stale finding."""
        findings = self.kg.query_entities({"type": "Finding", "id": change.entity_id})
        
        if findings:
            finding = findings[0]
            if finding.get("status") != "stale":
                self.kg.delete_entity(change.entity_id)
                finding["status"] = "stale"
                finding["needs_refresh"] = True
                finding["last_refreshed"] = get_timestamp()
                finding["refresh_attempts"] = finding.get("refresh_attempts", 0) + 1
                
                self.kg.store_entity(finding, session_id)
    
    def _handle_entity_stale(self, change: EntityChange, session_id: Optional[str]):
        """Handle a stale entity."""
        entities = self.kg.query_entities({"id": change.entity_id})
        
        if entities:
            entity = entities[0]
            if not entity.get("needs_refresh"):
                self.kg.delete_entity(change.entity_id)
                entity["needs_refresh"] = True
                entity["last_refreshed"] = get_timestamp()
                
                self.kg.store_entity(entity, session_id)
    
    def _handle_repo_modified(self, change: EntityChange, session_id: Optional[str]):
        """Handle repository modification."""
        # For now, just mark as needing refresh
        repos = self.kg.query_entities({"type": "Repository", "id": change.entity_id})
        
        if repos:
            repo = repos[0]
            self.kg.delete_entity(change.entity_id)
            repo["needs_full_resync"] = True
            repo["updated_at"] = get_timestamp()
            
            self.kg.store_entity(repo, session_id)
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension."""
        extension = os.path.splitext(file_path)[1].lower()
        
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.xml': 'XML',
            '.sql': 'SQL',
            '.sh': 'Shell',
            '.bash': 'Shell',
            '.ps1': 'PowerShell',
            '.md': 'Markdown',
            '.txt': 'Text'
        }
        
        return language_map.get(extension, 'Unknown')


# ============================================================================
# Freshness Manager
# ============================================================================

class FreshnessManager:
    """Manages freshness policies and tracking."""
    
    def __init__(self, kg: KnowledgeGraphInterface = None):
        """Initialize the freshness manager."""
        self.kg = kg or FileSystemKnowledgeGraph()
    
    def check_freshness(self, repo_id: str) -> FreshnessStatus:
        """
        Check the freshness status of a repository.
        
        Args:
            repo_id: Repository ID
            
        Returns:
            FreshnessStatus with score and details
        """
        entities = self.kg.query_entities({"repo_id": repo_id})
        stale_entities = self.kg.query_entities({
            "repo_id": repo_id,
            "needs_refresh": True
        })
        
        if not entities:
            return FreshnessStatus(
                repo_id=repo_id,
                score=1.0,
                last_updated=get_timestamp(),
                stale_entities=0,
                total_entities=0,
                status="fresh"
            )
        
        score = max(0.0, 1.0 - (len(stale_entities) / len(entities)))
        
        # Determine status
        if score >= 0.95:
            status = "fresh"
        elif score >= 0.8:
            status = "stale"
        else:
            status = "critical"
        
        # Calculate next refresh
        policies = FreshnessPolicy.default_policies()
        min_ttl = min(p.ttl_seconds for p in policies if p.auto_refresh)
        next_refresh = datetime.now(timezone.utc) + timedelta(seconds=min_ttl)
        
        return FreshnessStatus(
            repo_id=repo_id,
            score=score,
            last_updated=get_timestamp(),
            stale_entities=len(stale_entities),
            total_entities=len(entities),
            next_refresh=next_refresh.isoformat(),
            status=status
        )
    
    def get_stale_entities(self, repo_id: str) -> List[Dict[str, Any]]:
        """
        Get all stale entities for a repository.
        
        Args:
            repo_id: Repository ID
            
        Returns:
            List of stale entities
        """
        return self.kg.query_entities({
            "repo_id": repo_id,
            "needs_refresh": True
        })
    
    def get_expiring_entities(self, repo_id: str, within_seconds: int = 86400) -> List[Dict[str, Any]]:
        """
        Get entities that will expire soon.
        
        Args:
            repo_id: Repository ID
            within_seconds: Time window in seconds
            
        Returns:
            List of entities that will expire soon
        """
        policies = FreshnessPolicy.default_policies()
        expiring = []
        
        for policy in policies:
            if not policy.auto_refresh:
                continue
            
            entities = self.kg.query_entities({
                "type": policy.entity_type,
                "repo_id": repo_id
            })
            
            for entity in entities:
                updated_at = entity.get("updated_at", "")
                if updated_at:
                    expires_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00')) + \
                                  timedelta(seconds=policy.ttl_seconds)
                    time_until_expiry = (expires_at - datetime.now(timezone.utc)).total_seconds()
                    
                    if 0 < time_until_expiry <= within_seconds:
                        entity["expires_in_seconds"] = time_until_expiry
                        expiring.append(entity)
        
        return expiring
    
    def refresh_entity(self, entity_id: str, session_id: Optional[str] = None) -> bool:
        """
        Refresh a single entity.
        
        Args:
            entity_id: Entity ID to refresh
            session_id: Optional session ID for tracking
            
        Returns:
            True if refreshed successfully
        """
        entities = self.kg.query_entities({"id": entity_id})
        
        if not entities:
            return False
        
        entity = entities[0]
        
        # Delete old entity to avoid duplicates
        self.kg.delete_entity(entity_id)
        
        # Update timestamp
        entity["updated_at"] = get_timestamp()
        entity["last_refreshed"] = get_timestamp()
        entity["needs_refresh"] = False
        entity["refresh_attempts"] = 0
        
        # Increment version
        entity["version"] = str(int(entity.get("version", "1")) + 1)
        
        self.kg.store_entity(entity, session_id)
        return True


# ============================================================================
# Convenience Functions
# ============================================================================

def get_default_kg() -> FileSystemKnowledgeGraph:
    """Get the default knowledge graph instance."""
    return FileSystemKnowledgeGraph()


def check_and_update(repo_path: str, session_id: str = None) -> DriftReport:
    """
    Convenience function to check for changes and update.
    
    Args:
        repo_path: Path to the repository
        session_id: Optional session ID for tracking
        
    Returns:
        DriftReport with changes
    """
    updater = AutoUpdater()
    return updater.update(repo_path, session_id)


def get_freshness_status(repo_id: str) -> FreshnessStatus:
    """
    Convenience function to get freshness status.
    
    Args:
        repo_id: Repository ID
        
    Returns:
        FreshnessStatus
    """
    manager = FreshnessManager()
    return manager.check_freshness(repo_id)


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    # Example usage
    print("=" * 80)
    print("Knowledge Graph Auto-Update Mechanism - Example Usage")
    print("=" * 80)
    print()
    
    # Initialize components
    # Use context manager for atomic operations and proper lock cleanup
    kg = get_default_kg()
    detector = ChangeDetector(kg)
    updater = AutoUpdater(kg)
    manager = FreshnessManager(kg)
    
    # For concurrent access, use the knowledge graph as a context manager:
    # with kg:
    #     # All operations within this block are atomic and thread-safe
    #     detector.detect_drift(repo_path)
    #     # ... other operations ...
    
    # Example: Check a repository for changes
    repo_path = "/path/to/real application code"
    
    print(f"Checking for changes in: {repo_path}")
    print()
    
    # Detect drift
    report = detector.detect_drift(repo_path)
    
    print(f"Drift Report for {repo_path}:")
    print(f"  Changes detected: {len(report.changes)}")
    print(f"  Freshness score: {report.freshness_score:.2%}")
    print(f"  Stats: {report.stats}")
    print()
    
    if report.has_changes():
        print("Changes:")
        for change in report.changes[:5]:  # Show first 5
            print(f"  - {change.change_type.value}: {change.entity_id}")
        if len(report.changes) > 5:
            print(f"  ... and {len(report.changes) - 5} more")
        print()
        
        # Apply updates
        print("Applying updates...")
        updater.reconcile(report)
        print("✓ Updates applied")
        print()
    else:
        print("✓ No changes detected - knowledge is up to date")
        print()
    
    # Check freshness
    repo_fingerprint = compute_repo_fingerprint(repo_path)
    repo_id = f"repo:{repo_fingerprint}"
    
    status = manager.check_freshness(repo_id)
    print(f"Freshness Status:")
    print(f"  Score: {status.score:.2%}")
    print(f"  Status: {status.status}")
    print(f"  Stale entities: {status.stale_entities} / {status.total_entities}")
    print()
    
    print("=" * 80)
    print("Example complete!")
    print("=" * 80)
