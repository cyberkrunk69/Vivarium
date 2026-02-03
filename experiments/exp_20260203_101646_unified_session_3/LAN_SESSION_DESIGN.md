# LAN User Session Isolation Architecture

## Overview
Multi-user LAN access requires strict session isolation while maintaining visibility into swarm operations. Each connecting IP gets isolated workspace with tagged activity monitoring.

## Core Architecture

### Session Management
```
├── SessionManager
│   ├── ip_sessions: Dict[str, UserSession]
│   ├── create_session(ip: str) → UserSession
│   ├── get_session(ip: str) → UserSession
│   └── cleanup_expired_sessions()
│
└── UserSession
    ├── session_id: str (uuid)
    ├── client_ip: str
    ├── workspace_path: str
    ├── active_tasks: List[TaskInfo]
    ├── created_at: datetime
    └── last_activity: datetime
```

### Workspace Isolation
- **Per-IP Workspace**: `/workspaces/session_{session_id}/`
- **Sandboxed Execution**: All user tasks run in isolated containers
- **Resource Limits**: CPU/memory quotas per session
- **File Access**: Read-only to core system, full access to user workspace

### Activity Tagging System
```python
class ActivityTag:
    source_type: Literal["user", "swarm", "system"]
    session_id: Optional[str]  # None for swarm/system
    task_id: str
    description: str
    timestamp: datetime
```

### Real-Time Status API
```
GET /api/session/{session_id}/status
{
    "user_tasks": [
        {"id": "task_123", "status": "running", "description": "Data analysis"}
    ],
    "network_activity": [
        {"id": "swarm_456", "status": "active", "description": "Background optimization"}
    ],
    "system_status": {
        "swarm_workers": 10,
        "active_sessions": 3,
        "cpu_usage": 65
    }
}
```

## Security Boundaries

### Network Isolation
- User tasks cannot access host network interfaces
- No direct file system access outside workspace
- API rate limiting per session
- WebSocket connections scoped to session

### Process Isolation
- Docker containers per user session
- Non-privileged execution
- Resource quotas enforced
- Process cleanup on session end

### Data Isolation
- Session workspaces auto-created
- No cross-session file access
- Temporary data cleaned on disconnect
- User cannot modify core system files

## Implementation Components

### 1. Session Router (session_router.py)
```python
class SessionRouter:
    def route_request(self, ip: str, request) → Response:
        session = self.session_manager.get_session(ip)
        return self.execute_in_session(session, request)
```

### 2. Activity Monitor (activity_monitor.py)
```python
class ActivityMonitor:
    def tag_activity(self, activity: Activity, source: ActivityTag):
        # Tag and route to appropriate session viewers

    def get_session_view(self, session_id: str) → SessionView:
        # Filter activities relevant to this session
```

### 3. Workspace Manager (workspace_manager.py)
```python
class WorkspaceManager:
    def create_workspace(self, session_id: str) → str:
        # Create isolated workspace directory

    def cleanup_workspace(self, session_id: str):
        # Clean up on session end
```

## User Experience Flow

### Connection Flow
1. User connects via LAN (IP detected)
2. SessionManager creates new UserSession
3. Isolated workspace created at `/workspaces/session_{id}/`
4. WebSocket connection established for real-time updates
5. User sees dashboard with "Your Tasks" vs "Network Activity"

### Task Execution Flow
1. User submits task via web interface
2. Task tagged with session_id and source_type="user"
3. Execution happens in isolated container
4. Real-time status updates sent to user's WebSocket
5. Results saved to user's workspace

### Activity Visibility
- **Your Tasks**: Tasks initiated by this session
- **Network Activity**: Background swarm operations, other users
- **System Status**: Overall swarm health, worker count

## Configuration

### Session Settings
```json
{
    "session_timeout_minutes": 60,
    "max_sessions_per_ip": 1,
    "workspace_size_limit_mb": 1024,
    "task_timeout_minutes": 30,
    "rate_limit_requests_per_minute": 100
}
```

### Security Settings
```json
{
    "allow_file_uploads": true,
    "max_upload_size_mb": 50,
    "allowed_file_types": [".py", ".json", ".txt", ".md"],
    "network_access": false,
    "docker_security_opts": ["no-new-privileges", "apparmor=default"]
}
```

## Monitoring & Cleanup

### Health Checks
- Session heartbeat every 30 seconds
- Workspace disk usage monitoring
- Container resource usage tracking
- Failed task cleanup

### Automatic Cleanup
- Sessions expire after 60 minutes of inactivity
- Workspaces cleaned on session end
- Failed containers automatically removed
- Temporary files purged daily

## Integration Points

### With Existing System
- **orchestrator.py**: Routes tasks through SessionRouter
- **progress_server.py**: Enhanced with session-aware endpoints
- **grind_spawner.py**: Remains unchanged (system-level)
- **safety_*.py**: Session-aware safety checks

### New Components Required
1. `session_manager.py` - Core session management
2. `activity_monitor.py` - Activity tagging and routing
3. `workspace_manager.py` - Workspace isolation
4. `session_router.py` - Request routing by session
5. Enhanced web dashboard with session views

## Deployment Strategy

### Phase 1: Core Infrastructure
- Implement SessionManager and WorkspaceManager
- Add session-aware routing to existing endpoints

### Phase 2: Activity Monitoring
- Deploy ActivityMonitor
- Enhance dashboard with "Your Tasks" vs "Network Activity"

### Phase 3: Security Hardening
- Container isolation
- Resource quotas
- Rate limiting

This architecture ensures complete user isolation while maintaining transparency into swarm operations.