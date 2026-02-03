#!/usr/bin/env python3
"""
LAN Session Manager - Multi-user session isolation and activity tracking
Based on LAN_SESSION_DESIGN.md specifications
"""

import os
import json
import time
import shutil
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Set, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import websockets
import threading
from queue import Queue
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
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
    owner_ip: str
    task_type: str
    tag: str
    started_at: datetime
    status: str = "running"
    visible_to: List[str] = None

    def __post_init__(self):
        if self.visible_to is None:
            self.visible_to = [self.owner_ip]


class UserSession:
    """Individual user session context with workspace isolation"""

    def __init__(self, ip: str, workspace: str, task_namespace: str, created_at: datetime):
        self.ip = ip
        self.workspace = workspace
        self.task_namespace = task_namespace
        self.created_at = created_at
        self.active_tasks: Set[str] = set()
        self.task_history: List[str] = []
        self.permissions = UserPermissions()
        self.last_activity = datetime.now()
        self.session_timeout = timedelta(hours=2)  # 2 hour timeout

    def is_expired(self) -> bool:
        """Check if session has expired due to inactivity"""
        return datetime.now() - self.last_activity > self.session_timeout

    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()

    def add_task(self, task_id: str):
        """Add task to active tasks"""
        if len(self.active_tasks) >= self.permissions.max_concurrent_tasks:
            raise RuntimeError(f"Max concurrent tasks ({self.permissions.max_concurrent_tasks}) reached")

        self.active_tasks.add(task_id)
        self.task_history.append(task_id)
        self.update_activity()

    def remove_task(self, task_id: str):
        """Remove task from active tasks"""
        self.active_tasks.discard(task_id)
        self.update_activity()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize session to dictionary"""
        return {
            'ip': self.ip,
            'workspace': self.workspace,
            'task_namespace': self.task_namespace,
            'created_at': self.created_at.isoformat(),
            'active_tasks': list(self.active_tasks),
            'task_count': len(self.task_history),
            'last_activity': self.last_activity.isoformat(),
            'permissions': asdict(self.permissions)
        }


class WorkspaceManager:
    """Manages isolated user workspaces"""

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
        safe_ip = client_ip.replace('.', '_').replace(':', '_')
        workspace_path = self.base_path / safe_ip

        # Create workspace directories
        workspace_path.mkdir(exist_ok=True)
        (workspace_path / "inputs").mkdir(exist_ok=True)
        (workspace_path / "outputs").mkdir(exist_ok=True)
        (workspace_path / "temp").mkdir(exist_ok=True)

        # Create session metadata file
        session_file = workspace_path / "session.json"
        session_data = {
            'created': datetime.now().isoformat(),
            'ip': client_ip,
            'workspace_path': str(workspace_path)
        }

        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

        return str(workspace_path)

    def validate_file_access(self, client_ip: str, file_path: str) -> bool:
        """Validate user can access requested file path"""
        safe_ip = client_ip.replace('.', '_').replace(':', '_')
        user_workspace = self.base_path / safe_ip

        # Convert to absolute paths for comparison
        abs_file_path = Path(file_path).resolve()
        abs_workspace = user_workspace.resolve()

        # Check if file is within user workspace or shared area
        shared_path = (self.base_path / "shared").resolve()

        try:
            abs_file_path.relative_to(abs_workspace)
            return True
        except ValueError:
            try:
                abs_file_path.relative_to(shared_path)
                return True
            except ValueError:
                return False

    def get_user_workspace(self, client_ip: str) -> str:
        """Get user workspace path"""
        safe_ip = client_ip.replace('.', '_').replace(':', '_')
        return str(self.base_path / safe_ip)

    def cleanup_workspace(self, client_ip: str):
        """Clean up user workspace on session end"""
        workspace_path = Path(self.get_user_workspace(client_ip))
        if workspace_path.exists():
            shutil.rmtree(workspace_path)


class ActivityTracker:
    """Tracks and categorizes system activity"""

    TASK_TYPES = {
        'USER_TRIGGERED': "Started by user {owner_ip}",
        'SWARM_AUTO': "Background swarm activity",
        'ADMIN_TASK': "System maintenance",
        'CROSS_USER': "Multi-user collaboration"
    }

    def __init__(self):
        self.task_metadata: Dict[str, TaskMetadata] = {}
        self.activity_log: List[Dict[str, Any]] = []

    def tag_task(self, task_id: str, task_type: str, owner_ip: str = None) -> TaskMetadata:
        """Tag task with metadata and ownership"""
        tag = self.TASK_TYPES.get(task_type, "Unknown task type").format(owner_ip=owner_ip)

        metadata = TaskMetadata(
            task_id=task_id,
            owner_ip=owner_ip or "system",
            task_type=task_type,
            tag=tag,
            started_at=datetime.now(),
            visible_to=self.get_visibility_scope(task_type, owner_ip)
        )

        self.task_metadata[task_id] = metadata

        # Log activity
        self.activity_log.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'task_started',
            'task_id': task_id,
            'owner': owner_ip,
            'type': task_type
        })

        return metadata

    def get_visibility_scope(self, task_type: str, owner_ip: str = None) -> List[str]:
        """Determine who can see this task"""
        if task_type == 'USER_TRIGGERED' and owner_ip:
            return [owner_ip]  # Only owner can see details
        elif task_type == 'SWARM_AUTO':
            return ['all']  # Everyone can see it exists (but no details)
        elif task_type == 'ADMIN_TASK':
            return ['admin']
        else:
            return ['all']

    def complete_task(self, task_id: str):
        """Mark task as completed"""
        if task_id in self.task_metadata:
            self.task_metadata[task_id].status = "completed"

            self.activity_log.append({
                'timestamp': datetime.now().isoformat(),
                'event': 'task_completed',
                'task_id': task_id
            })

    def get_visible_activity(self, client_ip: str) -> Dict[str, Any]:
        """Get activity visible to specific client"""
        user_tasks = []
        network_summary = {"other_users_active": 0, "background_tasks": 0}

        for task_id, metadata in self.task_metadata.items():
            if metadata.status != "completed":
                if metadata.owner_ip == client_ip:
                    # Full details for own tasks
                    user_tasks.append({
                        'task_id': task_id,
                        'status': metadata.status,
                        'started_at': metadata.started_at.isoformat(),
                        'type': metadata.task_type,
                        'tag': metadata.tag
                    })
                elif metadata.task_type == 'SWARM_AUTO':
                    network_summary["background_tasks"] += 1
                elif metadata.task_type == 'USER_TRIGGERED':
                    network_summary["other_users_active"] += 1

        return {
            'my_tasks': user_tasks,
            'network_summary': network_summary,
            'total_active_tasks': len([t for t in self.task_metadata.values() if t.status != "completed"])
        }


class SessionSafety:
    """Security validation for session operations"""

    FORBIDDEN_PATHS = [
        'grind_spawner.py',
        'orchestrator.py',
        'core_system/',
        '../',  # No directory traversal
        '/etc/', '/system/',  # System paths
        'safety_', 'security_'  # Security modules
    ]

    @classmethod
    def validate_file_access(cls, client_ip: str, file_path: str, workspace_manager: WorkspaceManager) -> bool:
        """Validate file access is safe and within bounds"""

        # Check workspace isolation
        if not workspace_manager.validate_file_access(client_ip, file_path):
            raise SecurityError(f"Path outside user workspace: {file_path}")

        # Check forbidden paths
        normalized_path = os.path.normpath(file_path).lower()
        for forbidden in cls.FORBIDDEN_PATHS:
            if forbidden in normalized_path:
                raise SecurityError(f"Access to system files denied: {file_path}")

        return True

    @classmethod
    def validate_task_id(cls, task_id: str, client_ip: str) -> bool:
        """Validate task ID belongs to user"""
        safe_ip = client_ip.replace('.', '_').replace(':', '_')
        expected_prefix = f"user_{safe_ip}_"

        return task_id.startswith(expected_prefix)


class LANSessionManager:
    """Main session manager for multi-user LAN access"""

    def __init__(self, base_workspace_path: str = "user_sessions"):
        self.sessions: Dict[str, UserSession] = {}
        self.active_tasks: Dict[str, str] = {}  # task_id -> owner_ip
        self.activity_tracker = ActivityTracker()
        self.workspace_manager = WorkspaceManager(base_workspace_path)

        # WebSocket connections for real-time updates
        self.websocket_connections: Dict[str, Set] = {}
        self.update_queue = Queue()

        # Start background cleanup task
        self._cleanup_thread = threading.Thread(target=self._cleanup_expired_sessions, daemon=True)
        self._cleanup_thread.start()

        logger.info("LAN Session Manager initialized")

    def create_session(self, client_ip: str, user_id: str = None) -> UserSession:
        """Create new user session with isolated workspace"""

        # Clean up any existing expired session
        if client_ip in self.sessions and self.sessions[client_ip].is_expired():
            self.cleanup_session(client_ip)

        # Create workspace
        workspace_path = self.workspace_manager.create_user_workspace(client_ip)

        # Generate task namespace
        safe_ip = client_ip.replace('.', '_').replace(':', '_')
        task_namespace = f"user_{safe_ip}"

        # Create session
        session = UserSession(
            ip=client_ip,
            workspace=workspace_path,
            task_namespace=task_namespace,
            created_at=datetime.now()
        )

        self.sessions[client_ip] = session

        logger.info(f"Created session for {client_ip} with workspace {workspace_path}")

        return session

    def get_session(self, client_ip: str) -> Optional[UserSession]:
        """Get existing session for client IP"""
        session = self.sessions.get(client_ip)

        if session and session.is_expired():
            self.cleanup_session(client_ip)
            return None

        return session

    def get_or_create_session(self, client_ip: str) -> UserSession:
        """Get existing session or create new one"""
        session = self.get_session(client_ip)
        if not session:
            session = self.create_session(client_ip)
        return session

    def start_user_task(self, client_ip: str, task_description: str) -> str:
        """Start a new task for user"""
        session = self.get_or_create_session(client_ip)

        # Generate task ID
        task_counter = len(session.task_history) + 1
        task_id = f"{session.task_namespace}_task_{task_counter:03d}"

        # Validate task limits
        session.add_task(task_id)

        # Track task
        self.active_tasks[task_id] = client_ip
        self.activity_tracker.tag_task(task_id, 'USER_TRIGGERED', client_ip)

        # Notify via WebSocket
        self._broadcast_update(client_ip, {
            'type': 'task_started',
            'task_id': task_id,
            'description': task_description
        })

        logger.info(f"Started task {task_id} for user {client_ip}")

        return task_id

    def complete_user_task(self, task_id: str, client_ip: str):
        """Complete a user task"""
        if task_id not in self.active_tasks:
            raise ValueError(f"Task {task_id} not found")

        if self.active_tasks[task_id] != client_ip:
            raise SecurityError(f"Task {task_id} does not belong to user {client_ip}")

        # Update tracking
        session = self.get_session(client_ip)
        if session:
            session.remove_task(task_id)

        self.activity_tracker.complete_task(task_id)
        del self.active_tasks[task_id]

        # Notify via WebSocket
        self._broadcast_update(client_ip, {
            'type': 'task_completed',
            'task_id': task_id
        })

        logger.info(f"Completed task {task_id} for user {client_ip}")

    def get_user_dashboard_data(self, client_ip: str) -> Dict[str, Any]:
        """Get dashboard data for specific user"""
        session = self.get_or_create_session(client_ip)
        activity = self.activity_tracker.get_visible_activity(client_ip)

        return {
            'session': session.to_dict(),
            'activity': activity,
            'workspace_path': session.workspace,
            'system_status': {
                'total_users': len(self.sessions),
                'total_tasks': len(self.active_tasks),
                'system_health': 'healthy'
            }
        }

    def cleanup_session(self, client_ip: str):
        """Clean up user session and workspace"""
        if client_ip in self.sessions:
            session = self.sessions[client_ip]

            # Complete any remaining tasks
            for task_id in list(session.active_tasks):
                if task_id in self.active_tasks:
                    self.activity_tracker.complete_task(task_id)
                    del self.active_tasks[task_id]

            # Clean workspace
            self.workspace_manager.cleanup_workspace(client_ip)

            # Remove session
            del self.sessions[client_ip]

            logger.info(f"Cleaned up session for {client_ip}")

    def _cleanup_expired_sessions(self):
        """Background thread to clean up expired sessions"""
        while True:
            try:
                expired_ips = [
                    ip for ip, session in self.sessions.items()
                    if session.is_expired()
                ]

                for ip in expired_ips:
                    self.cleanup_session(ip)

                time.sleep(300)  # Check every 5 minutes

            except Exception as e:
                logger.error(f"Error in session cleanup: {e}")
                time.sleep(60)

    def _broadcast_update(self, client_ip: str, update: Dict[str, Any]):
        """Send update to client via WebSocket"""
        if client_ip in self.websocket_connections:
            self.update_queue.put((client_ip, update))

    def register_websocket(self, client_ip: str, websocket):
        """Register WebSocket connection for real-time updates"""
        if client_ip not in self.websocket_connections:
            self.websocket_connections[client_ip] = set()
        self.websocket_connections[client_ip].add(websocket)

    def unregister_websocket(self, client_ip: str, websocket):
        """Unregister WebSocket connection"""
        if client_ip in self.websocket_connections:
            self.websocket_connections[client_ip].discard(websocket)
            if not self.websocket_connections[client_ip]:
                del self.websocket_connections[client_ip]


class SecurityError(Exception):
    """Security-related errors"""
    pass


# WebSocket handler for real-time updates
async def websocket_handler(websocket, path, session_manager: LANSessionManager):
    """Handle WebSocket connections for real-time updates"""
    client_ip = websocket.remote_address[0]
    session_manager.register_websocket(client_ip, websocket)

    try:
        async for message in websocket:
            # Handle incoming messages if needed
            pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        session_manager.unregister_websocket(client_ip, websocket)


def create_session_dashboard_template() -> str:
    """Create HTML template for session dashboard"""
    return """<!DOCTYPE html>
<html>
<head>
    <title>LAN Session Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .dashboard { max-width: 1200px; margin: 0 auto; }
        .section { background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .section h2 { margin-top: 0; color: #333; border-bottom: 2px solid #007acc; padding-bottom: 10px; }
        .task-list { list-style: none; padding: 0; }
        .task-item { background: #f8f9fa; margin: 10px 0; padding: 15px; border-radius: 4px; border-left: 4px solid #007acc; }
        .task-id { font-weight: bold; color: #007acc; }
        .task-status { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .status-running { background: #ffeaa7; color: #2d3436; }
        .status-completed { background: #00b894; color: white; }
        .network-stats { display: flex; justify-content: space-around; text-align: center; }
        .stat-box { background: #f1c40f; color: #2d3436; padding: 20px; border-radius: 8px; min-width: 120px; }
        .stat-number { font-size: 2em; font-weight: bold; display: block; }
        .workspace-info { background: #e8f4fd; padding: 15px; border-radius: 4px; }
        #status { position: fixed; top: 10px; right: 10px; padding: 10px; border-radius: 4px; }
        .connected { background: #00b894; color: white; }
        .disconnected { background: #e74c3c; color: white; }
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>LAN Session Dashboard</h1>
        <div id="status" class="disconnected">Connecting...</div>

        <div class="section">
            <h2>My Tasks</h2>
            <div id="my-tasks">
                <p>No active tasks</p>
            </div>
        </div>

        <div class="section">
            <h2>Network Activity</h2>
            <div class="network-stats" id="network-stats">
                <div class="stat-box">
                    <span class="stat-number" id="other-users">-</span>
                    <span>Other Users</span>
                </div>
                <div class="stat-box">
                    <span class="stat-number" id="background-tasks">-</span>
                    <span>Background Tasks</span>
                </div>
                <div class="stat-box">
                    <span class="stat-number" id="total-tasks">-</span>
                    <span>Total Active</span>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>My Workspace</h2>
            <div class="workspace-info" id="workspace-info">
                <p><strong>Workspace Path:</strong> <span id="workspace-path">-</span></p>
                <p><strong>Session Created:</strong> <span id="session-created">-</span></p>
                <p><strong>Task Namespace:</strong> <span id="task-namespace">-</span></p>
            </div>
        </div>
    </div>

    <script>
        // WebSocket connection for real-time updates
        let ws;
        let clientIP = location.hostname;

        function connect() {
            ws = new WebSocket(`ws://${location.host}/ws/${clientIP}`);

            ws.onopen = function() {
                document.getElementById('status').className = 'connected';
                document.getElementById('status').textContent = 'Connected';
                updateDashboard();
            };

            ws.onclose = function() {
                document.getElementById('status').className = 'disconnected';
                document.getElementById('status').textContent = 'Disconnected';
                setTimeout(connect, 3000); // Reconnect after 3 seconds
            };

            ws.onmessage = function(event) {
                const update = JSON.parse(event.data);
                handleUpdate(update);
            };
        }

        function handleUpdate(update) {
            if (update.type === 'dashboard_data') {
                renderDashboard(update.data);
            } else if (update.type === 'task_started' || update.type === 'task_completed') {
                updateDashboard(); // Refresh full dashboard
            }
        }

        function updateDashboard() {
            fetch(`/api/dashboard/${clientIP}`)
                .then(response => response.json())
                .then(data => renderDashboard(data))
                .catch(console.error);
        }

        function renderDashboard(data) {
            // Render my tasks
            const myTasksDiv = document.getElementById('my-tasks');
            if (data.activity.my_tasks.length > 0) {
                const tasksList = data.activity.my_tasks.map(task => `
                    <div class="task-item">
                        <span class="task-id">${task.task_id}</span>
                        <span class="task-status status-${task.status}">${task.status.toUpperCase()}</span>
                        <p>${task.tag}</p>
                        <small>Started: ${new Date(task.started_at).toLocaleString()}</small>
                    </div>
                `).join('');
                myTasksDiv.innerHTML = tasksList;
            } else {
                myTasksDiv.innerHTML = '<p>No active tasks</p>';
            }

            // Render network stats
            const networkSummary = data.activity.network_summary;
            document.getElementById('other-users').textContent = networkSummary.other_users_active || 0;
            document.getElementById('background-tasks').textContent = networkSummary.background_tasks || 0;
            document.getElementById('total-tasks').textContent = data.activity.total_active_tasks || 0;

            // Render workspace info
            document.getElementById('workspace-path').textContent = data.session.workspace;
            document.getElementById('session-created').textContent = new Date(data.session.created_at).toLocaleString();
            document.getElementById('task-namespace').textContent = data.session.task_namespace;
        }

        // Start connection and initial update
        connect();
        setInterval(updateDashboard, 30000); // Update every 30 seconds
    </script>
</body>
</html>"""


if __name__ == "__main__":
    # Example usage
    session_manager = LANSessionManager()

    # Simulate user connections
    session1 = session_manager.create_session("192.168.1.100")
    session2 = session_manager.create_session("192.168.1.101")

    # Start tasks
    task1 = session_manager.start_user_task("192.168.1.100", "Analyze data.csv")
    task2 = session_manager.start_user_task("192.168.1.101", "Generate report")

    # Get dashboard data
    dashboard_data = session_manager.get_user_dashboard_data("192.168.1.100")
    print(json.dumps(dashboard_data, indent=2))