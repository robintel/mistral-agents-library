#!/usr/bin/env python3
"""
Unit tests for the auto-update mechanism.

Tests cover:
- Change detection (modified, added, deleted files)
- Auto-update functionality
- Reconciliation strategies
- Freshness tracking
- Integration scenarios
"""

import unittest
import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from auto_update import (
    ChangeType,
    EntityChange,
    DriftReport,
    FreshnessPolicy,
    FreshnessStatus,
    ChangeDetector,
    AutoUpdater,
    Reconciler,
    FreshnessManager,
    FileSystemKnowledgeGraph,
    compute_file_hash,
    compute_repo_fingerprint,
    get_timestamp,
    is_expired
)


class TestUtilities(unittest.TestCase):
    """Test utility functions."""
    
    def test_compute_file_hash(self):
        """Test file hash computation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f:
            f.write("test content")
            f.flush()
            
            hash1 = compute_file_hash(f.name)
            hash2 = compute_file_hash(f.name)
            
            # Same file should produce same hash
            self.assertEqual(hash1, hash2)
            self.assertEqual(len(hash1), 64)  # SHA-256 hex length
    
    def test_compute_file_hash_different_content(self):
        """Test that different content produces different hashes."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f1:
            f1.write("content 1")
            f1.flush()
            hash1 = compute_file_hash(f1.name)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f2:
            f2.write("content 2")
            f2.flush()
            hash2 = compute_file_hash(f2.name)
        
        self.assertNotEqual(hash1, hash2)
    
    def test_compute_file_hash_nonexistent(self):
        """Test hash computation for nonexistent file."""
        hash = compute_file_hash("/nonexistent/file.py")
        self.assertEqual(hash, "")
    
    def test_compute_repo_fingerprint(self):
        """Test repository fingerprint computation."""
        path1 = "/path/to/repo1"
        path2 = "/path/to/repo2"
        
        fp1 = compute_repo_fingerprint(path1)
        fp2 = compute_repo_fingerprint(path2)
        
        # Different paths should produce different fingerprints
        self.assertNotEqual(fp1, fp2)
        
        # Same path should produce same fingerprint
        fp1_again = compute_repo_fingerprint(path1)
        self.assertEqual(fp1, fp1_again)
        
        # Fingerprint should be short (16 chars)
        self.assertEqual(len(fp1), 16)
    
    def test_get_timestamp(self):
        """Test timestamp generation."""
        ts = get_timestamp()
        
        # Should be a valid ISO 8601 timestamp
        self.assertIn('T', ts)
        self.assertIn(':', ts)
        self.assertIn('+', ts)
    
    def test_is_expired(self):
        """Test expiration check."""
        # Current timestamp
        now = get_timestamp()
        
        # Should not be expired with 0 TTL
        self.assertFalse(is_expired(now, 0))
        
        # Should not be expired with large TTL
        self.assertFalse(is_expired(now, 86400))  # 1 day
        
        # Past timestamp should be expired
        past = datetime.now(timezone.utc) - timedelta(days=2)
        past_str = past.isoformat()
        self.assertTrue(is_expired(past_str, 86400))


class TestDataClasses(unittest.TestCase):
    """Test data classes."""
    
    def test_entity_change_creation(self):
        """Test EntityChange creation."""
        change = EntityChange(
            change_type=ChangeType.FILE_MODIFIED,
            entity_id="file:repo:abc:test.py",
            entity_type="File"
        )
        
        self.assertEqual(change.change_type, ChangeType.FILE_MODIFIED)
        self.assertEqual(change.entity_id, "file:repo:abc:test.py")
        self.assertEqual(change.entity_type, "File")
        self.assertIn("T", change.timestamp)  # ISO timestamp
        self.assertEqual(change.severity, "medium")  # Default
    
    def test_entity_change_to_dict(self):
        """Test EntityChange to_dict method."""
        change = EntityChange(
            change_type=ChangeType.FILE_ADDED,
            entity_id="file:123",
            entity_type="File",
            new_value={"path": "test.py"}
        )
        
        d = change.to_dict()
        
        self.assertEqual(d["change_type"], "file_added")
        self.assertEqual(d["entity_id"], "file:123")
        self.assertEqual(d["entity_type"], "File")
        self.assertEqual(d["new_value"], {"path": "test.py"})
    
    def test_drift_report_creation(self):
        """Test DriftReport creation."""
        report = DriftReport(
            repo_id="repo:abc123",
            repo_path="/path/to/repo"
        )
        
        self.assertEqual(report.repo_id, "repo:abc123")
        self.assertEqual(report.repo_path, "/path/to/repo")
        self.assertEqual(len(report.changes), 0)
        self.assertTrue(report.has_changes() is False)
        self.assertEqual(report.freshness_score, 1.0)
    
    def test_drift_report_add_change(self):
        """Test adding changes to DriftReport."""
        report = DriftReport(
            repo_id="repo:abc123",
            repo_path="/path/to/repo"
        )
        
        change = EntityChange(
            change_type=ChangeType.FILE_MODIFIED,
            entity_id="file:1",
            entity_type="File"
        )
        
        report.add_change(change)
        
        self.assertEqual(len(report.changes), 1)
        self.assertTrue(report.has_changes())
        self.assertEqual(report.stats["modified_files"], 1)
        self.assertEqual(report.stats["total_files"], 1)
    
    def test_drift_report_multiple_changes(self):
        """Test adding multiple changes to DriftReport."""
        report = DriftReport(
            repo_id="repo:abc123",
            repo_path="/path/to/repo"
        )
        
        # Add different types of changes
        report.add_change(EntityChange(
            change_type=ChangeType.FILE_MODIFIED,
            entity_id="file:1",
            entity_type="File"
        ))
        report.add_change(EntityChange(
            change_type=ChangeType.FILE_ADDED,
            entity_id="file:2",
            entity_type="File"
        ))
        report.add_change(EntityChange(
            change_type=ChangeType.FILE_DELETED,
            entity_id="file:3",
            entity_type="File"
        ))
        report.add_change(EntityChange(
            change_type=ChangeType.FINDING_STALE,
            entity_id="finding:1",
            entity_type="Finding"
        ))
        
        self.assertEqual(len(report.changes), 4)
        self.assertEqual(report.stats["modified_files"], 1)
        self.assertEqual(report.stats["added_files"], 1)
        self.assertEqual(report.stats["deleted_files"], 1)
        self.assertEqual(report.stats["stale_findings"], 1)
    
    def test_drift_report_getters(self):
        """Test DriftReport getter methods."""
        report = DriftReport(
            repo_id="repo:abc123",
            repo_path="/path/to/repo"
        )
        
        # Add file changes
        report.add_change(EntityChange(
            change_type=ChangeType.FILE_MODIFIED,
            entity_id="file:1",
            entity_type="File"
        ))
        report.add_change(EntityChange(
            change_type=ChangeType.FILE_ADDED,
            entity_id="file:2",
            entity_type="File"
        ))
        
        # Add finding changes
        report.add_change(EntityChange(
            change_type=ChangeType.FINDING_STALE,
            entity_id="finding:1",
            entity_type="Finding"
        ))
        
        changed_files = report.get_changed_file_ids()
        self.assertEqual(len(changed_files), 2)
        self.assertIn("file:1", changed_files)
        self.assertIn("file:2", changed_files)
        
        stale_findings = report.get_stale_finding_ids()
        self.assertEqual(len(stale_findings), 1)
        self.assertIn("finding:1", stale_findings)
    
    def test_drift_report_to_dict(self):
        """Test DriftReport to_dict method."""
        report = DriftReport(
            repo_id="repo:abc123",
            repo_path="/path/to/repo"
        )
        
        report.add_change(EntityChange(
            change_type=ChangeType.FILE_MODIFIED,
            entity_id="file:1",
            entity_type="File"
        ))
        
        d = report.to_dict()
        
        self.assertEqual(d["repo_id"], "repo:abc123")
        self.assertEqual(d["repo_path"], "/path/to/repo")
        self.assertEqual(len(d["changes"]), 1)
        self.assertTrue(d["has_changes"])
    
    def test_freshness_policy_defaults(self):
        """Test default freshness policies."""
        policies = FreshnessPolicy.default_policies()
        
        # Should have policies for all main entity types
        entity_types = [p.entity_type for p in policies]
        self.assertIn("Repository", entity_types)
        self.assertIn("File", entity_types)
        self.assertIn("Finding", entity_types)
        self.assertIn("Decision", entity_types)
        self.assertIn("Task", entity_types)
    
    def test_freshness_policy_get(self):
        """Test getting policy for specific entity type."""
        policy = FreshnessPolicy.get_policy("File")
        
        self.assertIsNotNone(policy)
        self.assertEqual(policy.entity_type, "File")
        self.assertGreater(policy.ttl_seconds, 0)
    
    def test_freshness_policy_nonexistent(self):
        """Test getting policy for non-existent entity type."""
        policy = FreshnessPolicy.get_policy("NonExistent")
        self.assertIsNone(policy)
    
    def test_freshness_status_creation(self):
        """Test FreshnessStatus creation."""
        status = FreshnessStatus(
            repo_id="repo:abc123",
            score=0.95,
            last_updated=get_timestamp()
        )
        
        self.assertEqual(status.repo_id, "repo:abc123")
        self.assertEqual(status.score, 0.95)
        self.assertTrue(status.is_fresh(0.9))
        self.assertFalse(status.is_stale(0.9))
        self.assertFalse(status.is_critical(0.9))
    
    def test_freshness_status_thresholds(self):
        """Test FreshnessStatus threshold methods."""
        # Fresh status
        fresh = FreshnessStatus(
            repo_id="repo:1",
            score=0.98,
            last_updated=get_timestamp()
        )
        self.assertTrue(fresh.is_fresh())
        self.assertFalse(fresh.is_stale())
        self.assertFalse(fresh.is_critical())
        
        # Stale status
        stale = FreshnessStatus(
            repo_id="repo:2",
            score=0.75,
            last_updated=get_timestamp()
        )
        self.assertFalse(stale.is_fresh())
        self.assertTrue(stale.is_stale())
        self.assertFalse(stale.is_critical())
        
        # Critical status
        critical = FreshnessStatus(
            repo_id="repo:3",
            score=0.3,
            last_updated=get_timestamp()
        )
        self.assertFalse(critical.is_fresh())
        self.assertFalse(critical.is_stale())
        self.assertTrue(critical.is_critical())


class TestFileSystemKnowledgeGraph(unittest.TestCase):
    """Test FileSystemKnowledgeGraph implementation."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_dir = tempfile.mkdtemp(prefix="kg_test_")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Set up for each test."""
        self.kg_dir = Path(self.test_dir) / "knowledge"
        self.kg_dir.mkdir(exist_ok=True)
        
        self.kg = FileSystemKnowledgeGraph(str(self.kg_dir))
        
        # Clear any existing data
        (self.kg.graph_dir / "entities.jsonl").write_text("")
        (self.kg.graph_dir / "relationships.jsonl").write_text("")
    
    def test_store_and_query_entity(self):
        """Test storing and querying an entity."""
        entity = {
            "id": "test:entity:001",
            "type": "TestEntity",
            "name": "Test"
        }
        
        self.kg.store_entity(entity)
        
        results = self.kg.query_entities({"id": "test:entity:001"})
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "test:entity:001")
        self.assertEqual(results[0]["type"], "TestEntity")
    
    def test_store_multiple_entities(self):
        """Test storing multiple entities."""
        entities = [
            {"id": "e1", "type": "Entity1"},
            {"id": "e2", "type": "Entity2"},
            {"id": "e3", "type": "Entity3"}
        ]
        
        for entity in entities:
            self.kg.store_entity(entity)
        
        results = self.kg.query_entities()
        self.assertEqual(len(results), 3)
    
    def test_query_by_type(self):
        """Test querying entities by type."""
        self.kg.store_entity({"id": "r1", "type": "Repository"})
        self.kg.store_entity({"id": "f1", "type": "File"})
        self.kg.store_entity({"id": "f2", "type": "File"})
        
        files = self.kg.query_entities({"type": "File"})
        self.assertEqual(len(files), 2)
        
        repos = self.kg.query_entities({"type": "Repository"})
        self.assertEqual(len(repos), 1)
    
    def test_query_by_repo_id(self):
        """Test querying entities by repo_id."""
        self.kg.store_entity({
            "id": "f1",
            "type": "File",
            "repo_id": "repo:abc"
        })
        self.kg.store_entity({
            "id": "f2",
            "type": "File",
            "repo_id": "repo:def"
        })
        
        repo_abc_files = self.kg.query_entities({"type": "File", "repo_id": "repo:abc"})
        self.assertEqual(len(repo_abc_files), 1)
        self.assertEqual(repo_abc_files[0]["id"], "f1")
    
    def test_store_and_query_relationship(self):
        """Test storing and querying a relationship."""
        relationship = {
            "id": "rel:001",
            "type": "contains",
            "source_id": "repo:abc",
            "target_id": "file:001"
        }
        
        self.kg.store_relationship(relationship)
        
        results = self.kg.query_relationships({"id": "rel:001"})
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["type"], "contains")
    
    def test_delete_entity(self):
        """Test deleting an entity."""
        self.kg.store_entity({"id": "e1", "type": "Entity"})
        self.kg.store_entity({"id": "e2", "type": "Entity"})
        
        deleted = self.kg.delete_entity("e1")
        self.assertTrue(deleted)
        
        results = self.kg.query_entities()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "e2")
    
    def test_delete_nonexistent_entity(self):
        """Test deleting a non-existent entity."""
        deleted = self.kg.delete_entity("nonexistent")
        self.assertFalse(deleted)


class TestChangeDetector(unittest.TestCase):
    """Test ChangeDetector functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_dir = tempfile.mkdtemp(prefix="detector_test_")
        cls.repo_dir = Path(cls.test_dir) / "test_repo"
        cls.repo_dir.mkdir()
        
        # Create test files
        (cls.repo_dir / "file1.py").write_text("# File 1")
        (cls.repo_dir / "file2.py").write_text("# File 2")
        (cls.repo_dir / "subdir").mkdir()
        (cls.repo_dir / "subdir" / "file3.py").write_text("# File 3")
        
        # Store original file contents for restoration
        cls.original_files = {
            "file1.py": "# File 1",
            "file2.py": "# File 2",
            "subdir/file3.py": "# File 3"
        }
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Set up for each test."""
        self.kg_dir = Path(self.test_dir) / "knowledge"
        self.kg_dir.mkdir(exist_ok=True)
        
        self.kg = FileSystemKnowledgeGraph(str(self.kg_dir))
        self.detector = ChangeDetector(self.kg)
        
        # Clear knowledge graph
        (self.kg.graph_dir / "entities.jsonl").write_text("")
        (self.kg.graph_dir / "relationships.jsonl").write_text("")
        
        # Restore original file contents
        for file_path, content in self.original_files.items():
            (self.repo_dir / file_path).write_text(content)
    
    def test_detect_new_repository(self):
        """Test detecting a new repository."""
        # First run - repository doesn't exist
        report = self.detector.detect_drift(str(self.repo_dir))
        
        # Should detect repository as modified (new)
        self.assertTrue(report.has_changes())
        self.assertTrue(any(
            c.change_type == ChangeType.REPO_MODIFIED 
            for c in report.changes
        ))
    
    def test_detect_new_files(self):
        """Test detecting new files."""
        # First, register the repository
        repo_fingerprint = compute_repo_fingerprint(str(self.repo_dir))
        repo_id = f"repo:{repo_fingerprint}"
        
        self.kg.store_entity({
            "id": repo_id,
            "type": "Repository",
            "path": str(self.repo_dir),
            "fingerprint": repo_fingerprint
        })
        
        # Now detect drift - should find new files
        report = self.detector.detect_drift(str(self.repo_dir))
        
        self.assertTrue(report.has_changes())
        
        # Should detect added files
        added_files = [
            c for c in report.changes 
            if c.change_type == ChangeType.FILE_ADDED
        ]
        self.assertGreater(len(added_files), 0)
    
    def test_detect_modified_file(self):
        """Test detecting a modified file."""
        # First, create initial state
        repo_fingerprint = compute_repo_fingerprint(str(self.repo_dir))
        repo_id = f"repo:{repo_fingerprint}"
        
        # Store repository
        self.kg.store_entity({
            "id": repo_id,
            "type": "Repository",
            "path": str(self.repo_dir),
            "fingerprint": repo_fingerprint
        })
        
        # Store initial files
        for file_path in ["file1.py", "file2.py", "subdir/file3.py"]:
            abs_path = self.repo_dir / file_path
            file_hash = compute_file_hash(str(abs_path))
            file_id = f"file:{repo_fingerprint}:{file_path}"
            
            self.kg.store_entity({
                "id": file_id,
                "type": "File",
                "path": file_path,
                "repo_id": repo_id,
                "content_hash": file_hash
            })
        
        # Now modify a file
        (self.repo_dir / "file1.py").write_text("# Modified File 1")
        
        # Detect drift
        report = self.detector.detect_drift(str(self.repo_dir))
        
        self.assertTrue(report.has_changes())
        
        # Should detect modified file
        modified_files = [
            c for c in report.changes 
            if c.change_type == ChangeType.FILE_MODIFIED
        ]
        self.assertEqual(len(modified_files), 1)
    
    def test_detect_deleted_file(self):
        """Test detecting a deleted file."""
        # First, create initial state with files
        repo_fingerprint = compute_repo_fingerprint(str(self.repo_dir))
        repo_id = f"repo:{repo_fingerprint}"
        
        self.kg.store_entity({
            "id": repo_id,
            "type": "Repository",
            "path": str(self.repo_dir),
            "fingerprint": repo_fingerprint
        })
        
        # Store initial files
        for file_path in ["file1.py", "file2.py"]:
            abs_path = self.repo_dir / file_path
            file_hash = compute_file_hash(str(abs_path))
            file_id = f"file:{repo_fingerprint}:{file_path}"
            
            self.kg.store_entity({
                "id": file_id,
                "type": "File",
                "path": file_path,
                "repo_id": repo_id,
                "content_hash": file_hash
            })
        
        # Now delete a file
        (self.repo_dir / "file2.py").unlink()
        
        # Detect drift
        report = self.detector.detect_drift(str(self.repo_dir))
        
        self.assertTrue(report.has_changes())
        
        # Should detect deleted file
        deleted_files = [
            c for c in report.changes 
            if c.change_type == ChangeType.FILE_DELETED
        ]
        self.assertEqual(len(deleted_files), 1)
    
    def test_freshness_score(self):
        """Test freshness score calculation."""
        # Create a repository with some files
        repo_fingerprint = compute_repo_fingerprint(str(self.repo_dir))
        repo_id = f"repo:{repo_fingerprint}"
        
        self.kg.store_entity({
            "id": repo_id,
            "type": "Repository",
            "path": str(self.repo_dir),
            "fingerprint": repo_fingerprint
        })
        
        # Store files
        for file_path in ["file1.py", "file2.py", "subdir/file3.py"]:
            abs_path = self.repo_dir / file_path
            file_hash = compute_file_hash(str(abs_path))
            file_id = f"file:{repo_fingerprint}:{file_path}"
            
            self.kg.store_entity({
                "id": file_id,
                "type": "File",
                "path": file_path,
                "repo_id": repo_id,
                "content_hash": file_hash
            })
        
        # No changes - freshness should be 1.0
        report = self.detector.detect_drift(str(self.repo_dir))
        self.assertEqual(report.freshness_score, 1.0)
        
        # Modify a file
        (self.repo_dir / "file1.py").write_text("# Modified")
        
        # Now freshness should be less than 1.0
        report = self.detector.detect_drift(str(self.repo_dir))
        self.assertLess(report.freshness_score, 1.0)


class TestReconciler(unittest.TestCase):
    """Test Reconciler functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_dir = tempfile.mkdtemp(prefix="reconciler_test_")
        cls.repo_dir = Path(cls.test_dir) / "test_repo"
        cls.repo_dir.mkdir()
        
        # Create test files
        (cls.repo_dir / "file1.py").write_text("# File 1")
        (cls.repo_dir / "file2.py").write_text("# File 2")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Set up for each test."""
        self.kg_dir = Path(self.test_dir) / "knowledge"
        self.kg_dir.mkdir(exist_ok=True)
        
        self.kg = FileSystemKnowledgeGraph(str(self.kg_dir))
        self.reconciler = Reconciler(self.kg)
        
        # Clear knowledge graph
        (self.kg.graph_dir / "entities.jsonl").write_text("")
        (self.kg.graph_dir / "relationships.jsonl").write_text("")
    
    def test_reconcile_file_added(self):
        """Test reconciling a new file."""
        repo_fingerprint = compute_repo_fingerprint(str(self.repo_dir))
        repo_id = f"repo:{repo_fingerprint}"
        
        # Create repository entity
        self.kg.store_entity({
            "id": repo_id,
            "type": "Repository",
            "path": str(self.repo_dir),
            "fingerprint": repo_fingerprint
        })
        
        # Create drift report with new file
        report = DriftReport(
            repo_id=repo_id,
            repo_path=str(self.repo_dir)
        )
        
        report.add_change(EntityChange(
            change_type=ChangeType.FILE_ADDED,
            entity_id=f"file:{repo_fingerprint}:file1.py",
            entity_type="File",
            new_value={
                "path": "file1.py",
                "hash": compute_file_hash(str(self.repo_dir / "file1.py"))
            }
        ))
        
        # Reconcile
        self.reconciler.reconcile(report)
        
        # Check that file was added
        files = self.kg.query_entities({"type": "File"})
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]["path"], "file1.py")
        
        # Check that relationship was created
        relationships = self.kg.query_relationships({"type": "contains"})
        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0]["source_id"], repo_id)
        self.assertEqual(relationships[0]["target_id"], files[0]["id"])
    
    def test_reconcile_file_modified(self):
        """Test reconciling a modified file."""
        repo_fingerprint = compute_repo_fingerprint(str(self.repo_dir))
        repo_id = f"repo:{repo_fingerprint}"
        file_id = f"file:{repo_fingerprint}:file1.py"
        
        # Create initial file entity
        self.kg.store_entity({
            "id": file_id,
            "type": "File",
            "path": "file1.py",
            "repo_id": repo_id,
            "content_hash": "old_hash",
            "version": "1"
        })
        
        # Create drift report with modified file
        report = DriftReport(
            repo_id=repo_id,
            repo_path=str(self.repo_dir)
        )
        
        report.add_change(EntityChange(
            change_type=ChangeType.FILE_MODIFIED,
            entity_id=file_id,
            entity_type="File",
            new_value={"hash": "new_hash"}
        ))
        
        # Reconcile
        self.reconciler.reconcile(report)
        
        # Check that file was updated
        files = self.kg.query_entities({"id": file_id})
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]["content_hash"], "new_hash")
        self.assertEqual(files[0]["version"], "2")  # Version incremented
    
    def test_reconcile_file_deleted(self):
        """Test reconciling a deleted file."""
        repo_fingerprint = compute_repo_fingerprint(str(self.repo_dir))
        repo_id = f"repo:{repo_fingerprint}"
        file_id = f"file:{repo_fingerprint}:file1.py"
        
        # Create file entity and relationship
        self.kg.store_entity({
            "id": file_id,
            "type": "File",
            "path": "file1.py",
            "repo_id": repo_id
        })
        
        self.kg.store_relationship({
            "id": f"rel:{repo_id}:contains:{file_id}",
            "type": "contains",
            "source_id": repo_id,
            "target_id": file_id
        })
        
        # Create drift report with deleted file
        report = DriftReport(
            repo_id=repo_id,
            repo_path=str(self.repo_dir)
        )
        
        report.add_change(EntityChange(
            change_type=ChangeType.FILE_DELETED,
            entity_id=file_id,
            entity_type="File"
        ))
        
        # Reconcile
        self.reconciler.reconcile(report)
        
        # Check that file was deleted
        files = self.kg.query_entities({"id": file_id})
        self.assertEqual(len(files), 0)
        
        # Check that relationships were deleted
        relationships = self.kg.query_relationships({
            "source_id": file_id
        })
        self.assertEqual(len(relationships), 0)


class TestFreshnessManager(unittest.TestCase):
    """Test FreshnessManager functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_dir = tempfile.mkdtemp(prefix="freshness_test_")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Set up for each test."""
        self.kg_dir = Path(self.test_dir) / "knowledge"
        self.kg_dir.mkdir(exist_ok=True)
        
        self.kg = FileSystemKnowledgeGraph(str(self.kg_dir))
        self.manager = FreshnessManager(self.kg)
        
        # Clear knowledge graph
        (self.kg.graph_dir / "entities.jsonl").write_text("")
        (self.kg.graph_dir / "relationships.jsonl").write_text("")
    
    def test_check_freshness_empty(self):
        """Test freshness check with empty repository."""
        status = self.manager.check_freshness("repo:nonexistent")
        
        self.assertEqual(status.score, 1.0)
        self.assertEqual(status.total_entities, 0)
        self.assertEqual(status.stale_entities, 0)
        self.assertTrue(status.is_fresh())
    
    def test_check_freshness_all_fresh(self):
        """Test freshness check with all fresh entities."""
        repo_id = "repo:test"
        
        # Store some entities
        for i in range(5):
            self.kg.store_entity({
                "id": f"file:{repo_id}:{i}",
                "type": "File",
                "repo_id": repo_id,
                "updated_at": get_timestamp()
            })
        
        status = self.manager.check_freshness(repo_id)
        
        self.assertEqual(status.score, 1.0)
        self.assertEqual(status.total_entities, 5)
        self.assertEqual(status.stale_entities, 0)
        self.assertTrue(status.is_fresh())
    
    def test_check_freshness_with_stale(self):
        """Test freshness check with some stale entities."""
        repo_id = "repo:test"
        
        # Store entities with old timestamps
        old_time = datetime.now(timezone.utc) - timedelta(days=2)
        old_ts = old_time.isoformat()
        
        for i in range(5):
            self.kg.store_entity({
                "id": f"file:{repo_id}:{i}",
                "type": "File",
                "repo_id": repo_id,
                "updated_at": old_ts,
                "needs_refresh": True
            })
        
        status = self.manager.check_freshness(repo_id)
        
        self.assertLess(status.score, 1.0)
        self.assertEqual(status.total_entities, 5)
        self.assertEqual(status.stale_entities, 5)
        self.assertTrue(status.is_stale() or status.is_critical())
    
    def test_get_stale_entities(self):
        """Test getting stale entities."""
        repo_id = "repo:test"
        
        # Store some fresh entities
        self.kg.store_entity({
            "id": "file:1",
            "type": "File",
            "repo_id": repo_id
        })
        
        # Store some stale entities
        self.kg.store_entity({
            "id": "file:2",
            "type": "File",
            "repo_id": repo_id,
            "needs_refresh": True
        })
        self.kg.store_entity({
            "id": "file:3",
            "type": "File",
            "repo_id": repo_id,
            "needs_refresh": True
        })
        
        stale = self.manager.get_stale_entities(repo_id)
        
        self.assertEqual(len(stale), 2)
        self.assertIn("file:2", [e["id"] for e in stale])
        self.assertIn("file:3", [e["id"] for e in stale])
    
    def test_refresh_entity(self):
        """Test refreshing an entity."""
        entity_id = "file:test"
        
        # Store an entity that needs refresh
        self.kg.store_entity({
            "id": entity_id,
            "type": "File",
            "needs_refresh": True,
            "version": "1"
        })
        
        # Refresh it
        refreshed = self.manager.refresh_entity(entity_id)
        
        self.assertTrue(refreshed)
        
        # Check that it was updated
        entities = self.kg.query_entities({"id": entity_id})
        self.assertEqual(len(entities), 1)
        self.assertFalse(entities[0].get("needs_refresh"))
        self.assertEqual(entities[0]["version"], "2")


class TestAutoUpdater(unittest.TestCase):
    """Test AutoUpdater functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_dir = tempfile.mkdtemp(prefix="updater_test_")
        cls.repo_dir = Path(cls.test_dir) / "test_repo"
        cls.repo_dir.mkdir()
        
        # Create test files
        (cls.repo_dir / "file1.py").write_text("# File 1")
        (cls.repo_dir / "file2.py").write_text("# File 2")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Set up for each test."""
        self.kg_dir = Path(self.test_dir) / "knowledge"
        self.kg_dir.mkdir(exist_ok=True)
        
        self.kg = FileSystemKnowledgeGraph(str(self.kg_dir))
        self.updater = AutoUpdater(self.kg)
        
        # Clear knowledge graph
        (self.kg.graph_dir / "entities.jsonl").write_text("")
        (self.kg.graph_dir / "relationships.jsonl").write_text("")
    
    def test_update_new_repository(self):
        """Test updating a new repository."""
        report = self.updater.update(str(self.repo_dir), session_id="session:test")
        
        # Should detect changes for new repository
        self.assertTrue(report.has_changes())
        
        # Should have created repository entity
        repos = self.kg.query_entities({"type": "Repository"})
        self.assertEqual(len(repos), 1)
    
    def test_update_existing_repository(self):
        """Test updating an existing repository."""
        repo_fingerprint = compute_repo_fingerprint(str(self.repo_dir))
        repo_id = f"repo:{repo_fingerprint}"
        
        # First, create initial state
        self.kg.store_entity({
            "id": repo_id,
            "type": "Repository",
            "path": str(self.repo_dir),
            "fingerprint": repo_fingerprint
        })
        
        # Add a file
        file_path = "file1.py"
        file_id = f"file:{repo_fingerprint}:{file_path}"
        file_hash = compute_file_hash(str(self.repo_dir / file_path))
        
        self.kg.store_entity({
            "id": file_id,
            "type": "File",
            "path": file_path,
            "repo_id": repo_id,
            "content_hash": file_hash
        })
        
        # Now modify the file
        (self.repo_dir / file_path).write_text("# Modified File 1")
        
        # Update
        report = self.updater.update(str(self.repo_dir), session_id="session:test")
        
        # Should detect the modification
        self.assertTrue(report.has_changes())
        
        modified_files = [
            c for c in report.changes 
            if c.change_type == ChangeType.FILE_MODIFIED
        ]
        self.assertEqual(len(modified_files), 1)


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    # Configure test runner
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestDataClasses))
    suite.addTests(loader.loadTestsFromTestCase(TestFileSystemKnowledgeGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestChangeDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestReconciler))
    suite.addTests(loader.loadTestsFromTestCase(TestFreshnessManager))
    suite.addTests(loader.loadTestsFromTestCase(TestAutoUpdater))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("AUTO-UPDATE MECHANISM TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"Success: {result.wasSuccessful()}")
    print("=" * 80)
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
