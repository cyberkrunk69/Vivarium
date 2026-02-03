#!/usr/bin/env python3
"""
LAN Session Manager - Multi-user session isolation and activity tracking
"""

import os
import json
import time
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Set, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import threading
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class UserPermissions:
    """User permission settings"""
    can_read_core_system: bool = False
    can_modify_core_system: bool = False
    can_see_other_workspaces: bool = False
    can_trigger_swarm_tasks: bool = True
    can_view_network_activity: bool = True
    workspace_quota_mb: int = 1024
    max_concurrent_tasks: int = 5
    role: str = "standard_user"

@dataclass
class TaskMetadata:
    """Task tracking metadata"""
    task_id: str
    source_type: str
    owner_ip: str
    tag: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str = "running"
    visible_to: List[str] = None
    workspace_path: str = ""

    def __post_init__(self):
        if self.visible_to is None:
            self.visible_to = []

class UserSession:
    """Individual user session context"""

    def __init__(self, ip: str, workspace: str, task_namespace: str, created_at: datetime):
        self.ip = ip
        self.workspace = workspace
        self.task_namespace = task_namespace
        self.created_at = created_at
        self.active_tasks: Set[str] = set()
        self.task_history: List[TaskMetadata] = []
        self.permissions = UserPermissions()
        self.last_activity = datetime.now()
        self.session_id = self._generate_session_id()

    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        data = f"{self.ip}_{self.created_at.isoformat()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]

    def add_task(self, task_id: str, task_metadata: TaskMetadata):
        """Add task to session"""
        self.active_tasks.add(task_id)
        self.task_history.append(task_metadata)
        self.last_activity = datetime.now()

    def complete_task(self, task_id: str, status: str = "completed"):
        """Mark task as completed"""
        self.active_tasks.discard(task_id)

        # Update task history
        for task in self.task_history:
            if task.task_id == task_id:
                task.status = status
                task.completed_at = datetime.now()
                break

        self.last_activity = datetime.now()

    def is_expired(self, timeout_minutes: int = 60) -> bool:
        """Check if session has expired"""
        timeout = timedelta(minutes=timeout_minutes)
        return datetime.now() - self.last_activity > timeout

    def get_session_info(self) -> dict:
        """Get session information for dashboard"""
        return {
            'session_id': self.session_id,
            'ip': self.ip,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'active_tasks': len(self.active_tasks),
            'total_tasks': len(self.task_history),
            'workspace': self.workspace,
            'permissions': asdict(self.permissions)
        }

class WorkspaceManager:
    """Manages user workspace isolation"""

    def __init__(self, base_path: str = "user_sessions"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

        # Create shared resources directory
        shared_path = self.base_path / "shared"
        shared_path.mkdir(exist_ok=True)
        (shared_path / "templates").mkdir(exist_ok=True)
        (shared_path / "references").mkdir(exist_ok=True)

    def create_user_workspace(self, client_ip: str) -> str:
        """Create isolated workspace for user"""
        workspace_name = client_ip.replace('.', '_').replace(':', '_')
        workspace_path = self.base_path / workspace_name

        # Create workspace directories
        workspace_path.mkdir(exist_ok=True)
        (workspace_path / "inputs").mkdir(exist_ok=True)
        (workspace_path / "outputs").mkdir(exist_ok=True)
        (workspace_path / "temp").mkdir(exist_ok=True)

        # Create session metadata file
        session_file = workspace_path / "session.json"
        if not session_file.exists():
            session_data = {
                'ip': client_ip,
                'created_at': datetime.now().isoformat(),
                'workspace_path': str(workspace_path)
            }
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)

        return str(workspace_path)

    def validate_file_access(self, client_ip: str, file_path: str) -> bool:
        """Validate user can access requested file path"""
        workspace_name = client_ip.replace('.', '_').replace(':', '_')
        user_workspace = self.base_path / workspace_name

        # Forbidden paths
        forbidden_paths = [
            'grind_spawner.py',
            'orchestrator.py',
            'core_system',
            '../',
            '/etc/',
            '/system/',
            '/home/',
            'C:/',
            'D:/'
        ]

        try:
            # Resolve absolute paths
            requested_path = Path(file_path).resolve()
            workspace_abs = user_workspace.resolve()

            # Must be within user workspace or shared resources
            shared_path = (self.base_path / "shared").resolve()

            if not (str(requested_path).startswith(str(workspace_abs)) or
                   str(requested_path).startswith(str(shared_path))):
                logger.warning(f"Path outside workspace: {file_path} for IP {client_ip}")
                return False

            # Check forbidden paths
            for forbidden in forbidden_paths:
                if forbidden in str(file_path):
                    logger.warning(f"Forbidden path access attempt: {file_path} for IP {client_ip}")
                    return False

            return True

        except Exception as e:
            logger.error(f"Path validation error: {e}")
            return False

    def get_workspace_usage(self, client_ip: str) -> dict:
        """Get workspace usage statistics"""
        workspace_name = client_ip.replace('.', '_').replace(':', '_')
        workspace_path = self.base_path / workspace_name

        if not workspace_path.exists():
            return {'size_mb': 0, 'file_count': 0}

        total_size = 0
        file_count = 0

        for root, dirs, files in os.walk(workspace_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    total_size += file_path.stat().st_size
                    file_count += 1
                except:
                    pass

        return {
            'size_mb': round(total_size / (1024 * 1024), 2),
            'file_count': file_count
        }

class ActivityTracker:
    """Track and categorize system activity"""

    def __init__(self):
        self.task_metadata: Dict[str, TaskMetadata] = {}
        self.activity_log: List[dict] = []
        self.lock = threading.Lock()

    def tag_task(self, task_id: str, source_type: str, owner_ip: str = None) -> TaskMetadata:
        """Tag and track a task"""
        tags = {
            'USER_TRIGGERED': f"Started by user {owner_ip}",
            'SWARM_AUTO': "Background swarm activity",
            'ADMIN_TASK': "System maintenance",
            'CROSS_USER': "Multi-user collaboration"
        }

        visibility_scope = self._get_visibility_scope(source_type, owner_ip)

        metadata = TaskMetadata(
            task_id=task_id,
            source_type=source_type,
            owner_ip=owner_ip or "system",
            tag=tags.get(source_type, "Unknown task type"),
            started_at=datetime.now(),
            visible_to=visibility_scope
        )

        with self.lock:
            self.task_metadata[task_id] = metadata
            self.activity_log.append({
                'timestamp': datetime.now().isoformat(),
                'event': 'task_started',
                'task_id': task_id,
                'source': source_type,
                'owner': owner_ip
            })

        logger.info(f"Task tagged: {task_id} as {source_type} by {owner_ip}")
        return metadata

    def complete_task(self, task_id: str, status: str = "completed"):
        """Mark task as completed"""
        with self.lock:
            if task_id in self.task_metadata:
                self.task_metadata[task_id].status = status
                self.task_metadata[task_id].completed_at = datetime.now()

                self.activity_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'event': 'task_completed',
                    'task_id': task_id,
                    'status': status
                })

    def get_visible_activity(self, client_ip: str) -> dict:
        """Get activity visible to specific user"""
        with self.lock:
            user_tasks = []
            network_stats = {'active_users': 0, 'background_tasks': 0}

            unique_ips = set()

            for task_id, metadata in self.task_metadata.items():
                if metadata.status == "running":
                    if metadata.owner_ip == client_ip:
                        # User's own tasks - full details
                        user_tasks.append({
                            'task_id': task_id,
                            'tag': metadata.tag,
                            'started_at': metadata.started_at.isoformat(),
                            'source_type': metadata.source_type
                        })
                    elif metadata.source_type == 'USER_TRIGGERED':
                        # Other users - count only
                        unique_ips.add(metadata.owner_ip)
                    elif metadata.source_type == 'SWARM_AUTO':
                        network_stats['background_tasks'] += 1

            network_stats['active_users'] = len(unique_ips)

            return {
                'my_tasks': user_tasks,
                'network_activity': network_stats
            }

    def _get_visibility_scope(self, source_type: str, owner_ip: str = None) -> List[str]:
        """Determine who can see this task"""
        if source_type == 'USER_TRIGGERED':
            return [owner_ip] if owner_ip else []
        elif source_type in ['SWARM_AUTO', 'ADMIN_TASK']:
            return ['public_stats']  # Only counts, not details
        else:
            return []

class LANSessionManager:
    """Main session manager for LAN multi-user access"""

    def __init__(self, base_workspace_path: str = "user_sessions"):
        self.sessions: Dict[str, UserSession] = {}
        self.active_tasks: Dict[str, str] = {}  # task_id -> owner_ip
        self.workspace_manager = WorkspaceManager(base_workspace_path)
        self.activity_tracker = ActivityTracker()
        self.websocket_clients: Dict[str, List] = defaultdict(list)  # ip -> [websockets]
        self.session_timeout_minutes = 60
        self.lock = threading.Lock()

        # Start cleanup thread
        self._start_cleanup_thread()

    def create_session(self, client_ip: str, user_id: str = None) -> UserSession:
        """Create new user session"""
        with self.lock:
            if client_ip in self.sessions:
                # Refresh existing session
                self.sessions[client_ip].last_activity = datetime.now()
                logger.info(f"Refreshed existing session for {client_ip}")
                return self.sessions[client_ip]

            # Create workspace
            workspace_path = self.workspace_manager.create_user_workspace(client_ip)

            # Create task namespace
            task_namespace = f"user_{client_ip.replace('.', '_').replace(':', '_')}"

            # Create session
            session = UserSession(
                ip=client_ip,
                workspace=workspace_path,
                task_namespace=task_namespace,
                created_at=datetime.now()
            )

            self.sessions[client_ip] = session

            logger.info(f"Created new session for {client_ip}: {session.session_id}")

            return session

    def get_session(self, client_ip: str) -> Optional[UserSession]:
        """Get existing session"""
        return self.sessions.get(client_ip)

    def submit_task(self, client_ip: str, task_description: str, task_type: str = "USER_TRIGGERED") -> str:
        """Submit task for user"""
        session = self.sessions.get(client_ip)
        if not session:
            raise ValueError(f"No session found for {client_ip}")

        # Generate task ID
        task_counter = len(session.task_history) + 1
        task_id = f"{session.task_namespace}_task_{task_counter:03d}"

        # Track task
        metadata = self.activity_tracker.tag_task(task_id, task_type, client_ip)
        session.add_task(task_id, metadata)
        self.active_tasks[task_id] = client_ip

        # Set workspace path in metadata
        metadata.workspace_path = session.workspace

        logger.info(f"Task submitted: {task_id} by {client_ip}")

        # Notify WebSocket clients
        self._notify_websocket_clients(client_ip, {
            'event': 'task_started',
            'task_id': task_id,
            'description': task_description
        })

        return task_id

    def complete_task(self, task_id: str, status: str = "completed"):
        """Complete a task"""
        if task_id in self.active_tasks:
            owner_ip = self.active_tasks[task_id]
            session = self.sessions.get(owner_ip)

            if session:
                session.complete_task(task_id, status)

            self.activity_tracker.complete_task(task_id, status)
            del self.active_tasks[task_id]

            # Notify WebSocket clients
            self._notify_websocket_clients(owner_ip, {
                'event': 'task_completed',
                'task_id': task_id,
                'status': status
            })

            logger.info(f"Task completed: {task_id} with status {status}")

    def get_user_dashboard_data(self, client_ip: str) -> dict:
        """Get dashboard data for specific user"""
        session = self.sessions.get(client_ip)
        if not session:
            return {'error': 'No session found'}

        # Get user's activity
        activity = self.activity_tracker.get_visible_activity(client_ip)

        # Get workspace usage
        workspace_usage = self.workspace_manager.get_workspace_usage(client_ip)

        # Get system health
        swarm_health = self._get_public_system_metrics()

        return {
            'session': session.get_session_info(),
            'my_tasks': activity['my_tasks'],
            'network_activity': activity['network_activity'],
            'swarm_health': swarm_health,
            'workspace_usage': workspace_usage,
            'permissions': asdict(session.permissions)
        }

    def validate_file_access(self, client_ip: str, file_path: str) -> bool:
        """Validate user file access"""
        session = self.sessions.get(client_ip)
        if not session:
            return False

        return self.workspace_manager.validate_file_access(client_ip, file_path)

    def register_websocket(self, client_ip: str, websocket):
        """Register WebSocket client for real-time updates"""
        self.websocket_clients[client_ip].append(websocket)
        logger.info(f"WebSocket registered for {client_ip}")

    def unregister_websocket(self, client_ip: str, websocket):
        """Unregister WebSocket client"""
        if client_ip in self.websocket_clients:
            try:
                self.websocket_clients[client_ip].remove(websocket)
            except ValueError:
                pass

    def _notify_websocket_clients(self, client_ip: str, message: dict):
        """Send real-time update to WebSocket clients"""
        if client_ip in self.websocket_clients:
            disconnected = []
            for websocket in self.websocket_clients[client_ip]:
                try:
                    asyncio.create_task(websocket.send(json.dumps(message)))
                except:
                    disconnected.append(websocket)

            # Clean up disconnected clients
            for ws in disconnected:
                self.websocket_clients[client_ip].remove(ws)

    def _get_public_system_metrics(self) -> dict:
        """Get public system health metrics"""
        active_sessions = len([s for s in self.sessions.values() if not s.is_expired()])
        total_active_tasks = len(self.active_tasks)

        return {
            'status': 'healthy',
            'active_sessions': active_sessions,
            'total_active_tasks': total_active_tasks,
            'timestamp': datetime.now().isoformat()
        }

    def _cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        expired = []

        with self.lock:
            for ip, session in self.sessions.items():
                if session.is_expired(self.session_timeout_minutes):
                    expired.append(ip)

            for ip in expired:
                logger.info(f"Cleaning up expired session: {ip}")
                del self.sessions[ip]

                # Clean up any remaining tasks
                expired_tasks = [tid for tid, owner in self.active_tasks.items() if owner == ip]
                for tid in expired_tasks:
                    self.complete_task(tid, "session_expired")

    def _start_cleanup_thread(self):
        """Start background cleanup thread"""
        def cleanup_loop():
            while True:
                time.sleep(300)  # Check every 5 minutes
                self._cleanup_expired_sessions()

        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        cleanup_thread.start()

    def get_all_sessions_info(self) -> dict:
        """Get information about all active sessions (admin view)"""
        with self.lock:
            return {
                'total_sessions': len(self.sessions),
                'active_tasks': len(self.active_tasks),
                'sessions': {
                    ip: session.get_session_info()
                    for ip, session in self.sessions.items()
                }
            }

# Global session manager instance
session_manager = LANSessionManager()

def get_session_manager() -> LANSessionManager:
    """Get global session manager instance"""
    return session_manager