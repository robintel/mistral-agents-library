"""
Session Manager for Knowledge Graph

Manages session lifecycle, context snapshots, and state persistence.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


# Data: clean - no credentials, PII, or sensitive data
# Provenance: mistral-agents-library


@dataclass
class Session:
    """Represents an agent session."""
    id: str
    start_time: str
    end_time: Optional[str] = None
    user_intent: Optional[str] = None
    agents_used: List[str] = field(default_factory=list)
    tasks_completed: List[str] = field(default_factory=list)
    findings_count: int = 0
    decisions_count: int = 0
    token_usage: Dict[str, int] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class SessionManager:
    """
    Manages agent sessions and their context.
    
    Features:
    - Session creation and lifecycle management
    - Context snapshots
    - Decision tracking
    - Session history
    """
    
    def __init__(self, knowledge_path: Optional[Path] = None):
        """
        Initialize session manager.
        
        Args:
            knowledge_path: Path to knowledge directory
        """
        if knowledge_path is None:
            knowledge_path = Path.home() / ".mistral-agents" / "knowledge"
        self.knowledge_path = Path(knowledge_path)
        self.sessions_path = self.knowledge_path / "sessions"
        self.sessions_path.mkdir(parents=True, exist_ok=True)
        
        self._current_session: Optional[Session] = None
    
    def create_session(self, user_intent: Optional[str] = None) -> Session:
        """
        Create a new session.
        
        Args:
            user_intent: Description of user's intent for this session
        
        Returns:
            New session object
        """
        session_id = self._generate_session_id()
        
        session = Session(
            id=session_id,
            start_time=datetime.utcnow().isoformat(),
            user_intent=user_intent
        )
        
        self._current_session = session
        self._save_session(session)
        
        return session
    
    def end_session(self) -> Optional[Session]:
        """
        End the current session.
        
        Returns:
            The ended session or None if no session was active
        """
        if self._current_session is None:
            return None
        
        self._current_session.end_time = datetime.utcnow().isoformat()
        self._save_session(self._current_session)
        
        session = self._current_session
        self._current_session = None
        
        return session
    
    def get_current_session(self) -> Optional[Session]:
        """Get the current active session."""
        return self._current_session
    
    def add_agent_used(self, agent_name: str):
        """Record that an agent was used in the current session."""
        if self._current_session is None:
            return
        if agent_name not in self._current_session.agents_used:
            self._current_session.agents_used.append(agent_name)
            self._save_session(self._current_session)
    
    def add_task_completed(self, task_id: str):
        """Record that a task was completed in the current session."""
        if self._current_session is None:
            return
        if task_id not in self._current_session.tasks_completed:
            self._current_session.tasks_completed.append(task_id)
            self._save_session(self._current_session)
    
    def increment_finding_count(self, count: int = 1):
        """Increment the finding count for the current session."""
        if self._current_session is None:
            return
        self._current_session.findings_count += count
        self._save_session(self._current_session)
    
    def increment_decision_count(self, count: int = 1):
        """Increment the decision count for the current session."""
        if self._current_session is None:
            return
        self._current_session.decisions_count += count
        self._save_session(self._current_session)
    
    def update_token_usage(self, input_tokens: int, output_tokens: int):
        """Update token usage for the current session."""
        if self._current_session is None:
            return
        self._current_session.token_usage["input"] = \
            self._current_session.token_usage.get("input", 0) + input_tokens
        self._current_session.token_usage["output"] = \
            self._current_session.token_usage.get("output", 0) + output_tokens
        self._save_session(self._current_session)
    
    def store_context_snapshot(self, context: Dict[str, Any]):
        """
        Store a snapshot of the current context.
        
        Args:
            context: Context to snapshot
        """
        if self._current_session is None:
            return False
        
        session_dir = self.sessions_path / self._current_session.id
        context_path = session_dir / "context.json"
        
        try:
            with open(context_path, 'w', encoding='utf-8') as f:
                json.dump(context, f, indent=2)
            return True
        except IOError:
            return False
    
    def load_context_snapshot(self, session_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Load a context snapshot.
        
        Args:
            session_id: Session ID (defaults to current session)
        
        Returns:
            Context snapshot or None
        """
        if session_id is None and self._current_session is None:
            return None
        
        target_session_id = session_id or self._current_session.id
        session_dir = self.sessions_path / target_session_id
        context_path = session_dir / "context.json"
        
        if not context_path.exists():
            return None
        
        try:
            with open(context_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def store_decision(self, decision: Dict[str, Any]):
        """
        Store a decision in the current session.
        
        Args:
            decision: Decision to store
        """
        if self._current_session is None:
            return False
        
        session_dir = self.sessions_path / self._current_session.id
        decisions_path = session_dir / "decisions.jsonl"
        
        # Ensure decision has metadata
        decision["session_id"] = self._current_session.id
        decision["timestamp"] = datetime.utcnow().isoformat()
        
        try:
            with open(decisions_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(decision, ensure_ascii=False) + '\n')
            self.increment_decision_count()
            return True
        except IOError:
            return False
    
    def load_decisions(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load all decisions for a session.
        
        Args:
            session_id: Session ID (defaults to current session)
        
        Returns:
            List of decisions
        """
        if session_id is None and self._current_session is None:
            return []
        
        target_session_id = session_id or self._current_session.id
        session_dir = self.sessions_path / target_session_id
        decisions_path = session_dir / "decisions.jsonl"
        
        if not decisions_path.exists():
            return []
        
        decisions = []
        try:
            with open(decisions_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            decisions.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except IOError:
            pass
        
        return decisions
    
    def store_metadata(self, metadata: Dict[str, Any]):
        """
        Store session metadata.
        
        Args:
            metadata: Metadata to store
        """
        if self._current_session is None:
            return False
        
        self._current_session.metadata.update(metadata)
        self._save_session(self._current_session)
        return True
    
    def load_session(self, session_id: str) -> Optional[Session]:
        """
        Load a session by ID.
        
        Args:
            session_id: Session ID
        
        Returns:
            Session object or None
        """
        session_dir = self.sessions_path / session_id
        metadata_path = session_dir / "metadata.json"
        
        if not metadata_path.exists():
            return None
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            session = Session(
                id=data.get("id", session_id),
                start_time=data.get("start_time"),
                end_time=data.get("end_time"),
                user_intent=data.get("user_intent"),
                agents_used=data.get("agents_used", []),
                tasks_completed=data.get("tasks_completed", []),
                findings_count=data.get("findings_count", 0),
                decisions_count=data.get("decisions_count", 0),
                token_usage=data.get("token_usage", {}),
                metadata=data.get("metadata", {})
            )
            return session
        except (json.JSONDecodeError, IOError):
            return None
    
    def list_sessions(self, limit: int = 100, offset: int = 0) -> List[Session]:
        """
        List all sessions.
        
        Args:
            limit: Maximum number of sessions to return
            offset: Number of sessions to skip
        
        Returns:
            List of sessions
        """
        sessions = []
        
        for session_dir in self.sessions_path.iterdir():
            if session_dir.is_dir():
                session = self.load_session(session_dir.name)
                if session:
                    sessions.append(session)
        
        # Sort by start time (newest first)
        sessions.sort(key=lambda s: s.start_time or "", reverse=True)
        
        return sessions[offset:offset + limit]
    
    def cleanup_old_sessions(self, max_age_days: int = 30):
        """
        Clean up old session data.
        
        Args:
            max_age_days: Maximum age in days (sessions older than this will be deleted)
        
        Returns:
            Number of sessions deleted
        """
        import time
        
        cutoff = datetime.utcnow().timestamp() - (max_age_days * 24 * 60 * 60)
        deleted = 0
        
        for session_dir in self.sessions_path.iterdir():
            if session_dir.is_dir():
                session = self.load_session(session_dir.name)
                if session and session.start_time:
                    session_time = datetime.fromisoformat(session.start_time).timestamp()
                    if session_time < cutoff:
                        # Delete session directory
                        import shutil
                        shutil.rmtree(session_dir)
                        deleted += 1
        
        return deleted
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        timestamp = datetime.utcnow().isoformat()
        # Use hash of timestamp + random for uniqueness
        import random
        random_bytes = str(random.randint(0, 999999)).encode()
        hash_input = (timestamp + str(random_bytes)).encode()
        return "session:" + hashlib.sha256(hash_input).hexdigest()[:16]
    
    def _save_session(self, session: Session):
        """Save session metadata to disk."""
        session_dir = self.sessions_path / session.id
        session_dir.mkdir(parents=True, exist_ok=True)
        metadata_path = session_dir / "metadata.json"
        
        data = {
            "id": session.id,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "user_intent": session.user_intent,
            "agents_used": session.agents_used,
            "tasks_completed": session.tasks_completed,
            "findings_count": session.findings_count,
            "decisions_count": session.decisions_count,
            "token_usage": session.token_usage,
            "metadata": session.metadata
        }
        
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass


# Singleton instance
_default_session_manager = None


def get_session_manager(knowledge_path: Optional[Path] = None) -> SessionManager:
    """Get or create the default session manager."""
    global _default_session_manager
    if _default_session_manager is None or knowledge_path:
        _default_session_manager = SessionManager(knowledge_path)
    return _default_session_manager
