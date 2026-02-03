#!/usr/bin/env python3
"""
LAN Session Manager - Per-IP session isolation with real-time activity tracking
"""

import time
import json
import os
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import websockets
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SessionContext:
    """Individual user session context"""
    session_id: str
    client_ip: str
    workspace_path: str
    created_at: float
    user_id: str
    last_activity: float = None
    active_tasks: List[str] = None
    is_admin: bool = False

    def __post_init__(self):
        if self.last_activity is None:
            self.last_activity = time.time()
        if self.active_tasks is None:
            self.active_tasks = []

@dataclass
class ActivityTag:
    """Activity tagging for task attribution"""
    task_id: str
    source_ip: str
    activity_type: str  # user_triggered|background_swarm|admin_task
    timestamp: float
    user_session: str
    description: str
    status: str = "pending"  # pending|running|completed|failed

class SessionManager:
    """Core session management with per-IP isolation"""

    def __init__(self, config_path: str = "lan_config.json"):
        self.active_sessions: Dict[str, SessionContext] = {}
        self.user_workspaces: Dict[str, str] = {}
        self.activity_log: List[ActivityTag] = []
        self.websocket_clients: Dict[str, set] = {}  # IP -> set of websockets
        self.config = self._load_config(config_path)

        # Create base directories
        self.sessions_dir = Path("user_sessions")
        self.sessions_dir.mkdir(exist_ok=True)

        # Start cleanup task
        asyncio.create_task(self._cleanup_expired_sessions())

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load LAN configuration"""
        default_config = {
            "session_timeout": 3600,
            "max_concurrent_sessions": 10,
            "user_workspace_quota": "10GB",
            "resource_limits": {
                "cpu_cores": 2,
                "memory_mb": 4096,
                "execution_timeout": 300
            },
            "admin_ips": ["192.168.1.1"],
            "allowed_subnets": ["192.168.1.0/24"]
        }

        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                return {**default_config, **config}
        except Exception as e:
            logger.warning(f"Could not load config {config_path}: {e}")

        return default_config

    def create_session(self, client_ip: str, user_id: Optional[str] = None) -> SessionContext:
        """Create new user session with isolated workspace"""

        # Check session limits
        if len(self.active_sessions) >= self.config["max_concurrent_sessions"]:
            raise Exception("Maximum concurrent sessions reached")

        # Generate session ID and workspace
        session_id = f"lan_{client_ip}_{int(time.time())}"
        safe_ip = client_ip.replace('.', '_').replace(':', '_')
        workspace_path = f"user_sessions/{safe_ip}"

        # Check if admin
        is_admin = client_ip in self.config["admin_ips"]

        session = SessionContext(
            session_id=session_id,
            client_ip=client_ip,
            workspace_path=workspace_path,
            created_at=time.time(),
            user_id=user_id or f"user_{safe_ip}",
            is_admin=is_admin
        )

        # Create isolated workspace
        self._create_user_workspace(workspace_path)

        # Store session
        self.active_sessions[client_ip] = session
        self.user_workspaces[client_ip] = workspace_path

        # Initialize WebSocket client set
        self.websocket_clients[client_ip] = set()

        # Log session creation
        self._log_activity(
            task_id=f"session_create_{session_id}",
            source_ip=client_ip,
            activity_type="admin_task",
            description=f"Session created for {user_id or client_ip}",
            status="completed"
        )

        logger.info(f"Created session {session_id} for {client_ip}")
        return session

    def _create_user_workspace(self, workspace_path: str):
        """Create isolated user workspace directory"""
        workspace_dir = Path(workspace_path)
        workspace_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        (workspace_dir / "tasks").mkdir(exist_ok=True)
        (workspace_dir / "outputs").mkdir(exist_ok=True)
        (workspace_dir / "temp").mkdir(exist_ok=True)

        # Create README
        readme_content = """# User Workspace

This is your isolated workspace for this session.
- tasks/: Your task outputs and results
- outputs/: Generated files and artifacts
- temp/: Temporary files (cleared on session end)

Your session is isolated from other users.
"""
        (workspace_dir / "README.md").write_text(readme_content)

        logger.info(f"Created workspace: {workspace_path}")

    def get_session(self, client_ip: str) -> Optional[SessionContext]:
        """Get existing session for IP"""
        return self.active_sessions.get(client_ip)

    def update_session_activity(self, client_ip: str):
        """Update last activity timestamp"""
        if client_ip in self.active_sessions:
            self.active_sessions[client_ip].last_activity = time.time()

    def destroy_session(self, client_ip: str):
        """Clean up and destroy user session"""
        session = self.active_sessions.get(client_ip)
        if not session:
            return

        # Close all WebSocket connections
        if client_ip in self.websocket_clients:
            for ws in self.websocket_clients[client_ip].copy():
                asyncio.create_task(ws.close())
            del self.websocket_clients[client_ip]

        # Clean up workspace (temp files only)
        workspace_path = Path(session.workspace_path)
        temp_dir = workspace_path / "temp"
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)

        # Remove from active sessions
        del self.active_sessions[client_ip]
        if client_ip in self.user_workspaces:
            del self.user_workspaces[client_ip]

        # Log session destruction
        self._log_activity(
            task_id=f"session_destroy_{session.session_id}",
            source_ip=client_ip,
            activity_type="admin_task",
            description=f"Session destroyed for {session.user_id}",
            status="completed"
        )

        logger.info(f"Destroyed session {session.session_id} for {client_ip}")

    async def _cleanup_expired_sessions(self):
        """Background task to clean up expired sessions"""
        while True:
            try:
                current_time = time.time()
                timeout = self.config["session_timeout"]

                expired_ips = []
                for ip, session in self.active_sessions.items():
                    if current_time - session.last_activity > timeout:
                        expired_ips.append(ip)

                for ip in expired_ips:
                    logger.info(f"Session expired for {ip}")
                    self.destroy_session(ip)

                # Sleep for 60 seconds before next cleanup
                await asyncio.sleep(60)

            except Exception as e:
                logger.error(f"Error in session cleanup: {e}")
                await asyncio.sleep(60)


class ActivityTracker:
    """Track and categorize all system activity"""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    def tag_activity(self, task_id: str, source_ip: str, activity_type: str,
                    description: str, status: str = "pending") -> ActivityTag:
        """Tag activity with source attribution"""
        session = self.session_manager.get_session(source_ip)
        user_session = session.session_id if session else "unknown"

        tag = ActivityTag(
            task_id=task_id,
            source_ip=source_ip,
            activity_type=activity_type,
            timestamp=time.time(),
            user_session=user_session,
            description=description,
            status=status
        )

        return tag

    def get_user_activities(self, client_ip: str) -> List[ActivityTag]:
        """Get activities for specific user"""
        return [
            activity for activity in self.session_manager.activity_log
            if activity.source_ip == client_ip
        ]

    def get_network_activities(self, client_ip: str, include_own: bool = False) -> List[ActivityTag]:
        """Get network-wide activities (excluding user's own unless specified)"""
        activities = []
        for activity in self.session_manager.activity_log:
            if include_own or activity.source_ip != client_ip:
                # Anonymize other users' IPs
                display_activity = ActivityTag(
                    task_id=activity.task_id,
                    source_ip="system" if activity.activity_type == "background_swarm"
                             else "another_user" if activity.source_ip != client_ip
                             else activity.source_ip,
                    activity_type=activity.activity_type,
                    timestamp=activity.timestamp,
                    user_session="anonymous" if activity.source_ip != client_ip
                                else activity.user_session,
                    description=activity.description,
                    status=activity.status
                )
                activities.append(display_activity)

        return activities


class WebSocketServer:
    """Real-time WebSocket updates for session status"""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.activity_tracker = ActivityTracker(session_manager)

    async def register_client(self, websocket, client_ip: str):
        """Register WebSocket client for real-time updates"""
        if client_ip not in self.session_manager.websocket_clients:
            self.session_manager.websocket_clients[client_ip] = set()

        self.session_manager.websocket_clients[client_ip].add(websocket)
        logger.info(f"WebSocket client registered for {client_ip}")

        # Send initial status
        await self.send_status_update(client_ip)

    async def unregister_client(self, websocket, client_ip: str):
        """Unregister WebSocket client"""
        if client_ip in self.session_manager.websocket_clients:
            self.session_manager.websocket_clients[client_ip].discard(websocket)
            if not self.session_manager.websocket_clients[client_ip]:
                del self.session_manager.websocket_clients[client_ip]

        logger.info(f"WebSocket client unregistered for {client_ip}")

    async def send_status_update(self, client_ip: str):
        """Send status update to specific client"""
        if client_ip not in self.session_manager.websocket_clients:
            return

        user_activities = self.activity_tracker.get_user_activities(client_ip)
        network_activities = self.activity_tracker.get_network_activities(client_ip)

        # Format for dashboard
        status_data = {
            "user_tasks": [
                {
                    "task_id": activity.task_id,
                    "status": activity.status,
                    "description": activity.description,
                    "started_by": "you",
                    "timestamp": activity.timestamp
                }
                for activity in user_activities[-10:]  # Last 10 activities
            ],
            "network_activity": [
                {
                    "task_id": activity.task_id,
                    "status": activity.status,
                    "description": activity.description,
                    "started_by": activity.source_ip,
                    "timestamp": activity.timestamp
                }
                for activity in network_activities[-20:]  # Last 20 activities
            ]
        }

        message = json.dumps(status_data)

        # Send to all WebSocket clients for this IP
        disconnected_clients = set()
        for websocket in self.session_manager.websocket_clients[client_ip]:
            try:
                await websocket.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(websocket)
            except Exception as e:
                logger.error(f"Error sending WebSocket message: {e}")
                disconnected_clients.add(websocket)

        # Clean up disconnected clients
        for websocket in disconnected_clients:
            await self.unregister_client(websocket, client_ip)

    async def broadcast_activity(self, activity: ActivityTag):
        """Broadcast new activity to all connected clients"""
        # Add to session manager's activity log
        self.session_manager.activity_log.append(activity)

        # Keep only last 1000 activities
        if len(self.session_manager.activity_log) > 1000:
            self.session_manager.activity_log = self.session_manager.activity_log[-1000:]

        # Send updates to all connected clients
        for client_ip in self.session_manager.websocket_clients:
            await self.send_status_update(client_ip)


# Extension to SessionManager for activity logging
def _log_activity_method(self, task_id: str, source_ip: str, activity_type: str,
                        description: str, status: str = "pending"):
    """Add activity to log and broadcast to WebSocket clients"""
    activity = ActivityTag(
        task_id=task_id,
        source_ip=source_ip,
        activity_type=activity_type,
        timestamp=time.time(),
        user_session=self.get_session(source_ip).session_id if self.get_session(source_ip) else "unknown",
        description=description,
        status=status
    )

    self.activity_log.append(activity)

    # Keep only last 1000 activities
    if len(self.activity_log) > 1000:
        self.activity_log = self.activity_log[-1000:]

    logger.info(f"Activity logged: {task_id} ({activity_type}) from {source_ip}")

# Monkey patch the method
SessionManager._log_activity = _log_activity_method


# Demo usage
async def main():
    """Demo the session manager"""
    session_manager = SessionManager()
    websocket_server = WebSocketServer(session_manager)

    # Create some demo sessions
    session1 = session_manager.create_session("192.168.1.100", "user_alice")
    session2 = session_manager.create_session("192.168.1.101", "user_bob")

    # Log some activities
    session_manager._log_activity(
        "task_001", "192.168.1.100", "user_triggered",
        "Processing data analysis request", "running"
    )

    session_manager._log_activity(
        "swarm_bg_001", "system", "background_swarm",
        "Background optimization running", "running"
    )

    session_manager._log_activity(
        "task_002", "192.168.1.101", "user_triggered",
        "Generating report", "completed"
    )

    print("Session Manager Demo:")
    print(f"Active sessions: {len(session_manager.active_sessions)}")
    print(f"Activity log: {len(session_manager.activity_log)} entries")

    # Show user-specific activities
    alice_activities = ActivityTracker(session_manager).get_user_activities("192.168.1.100")
    print(f"Alice's activities: {len(alice_activities)}")

    network_activities = ActivityTracker(session_manager).get_network_activities("192.168.1.100")
    print(f"Network activities (Alice's view): {len(network_activities)}")

if __name__ == "__main__":
    asyncio.run(main())