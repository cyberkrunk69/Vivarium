# LAN User Session Isolation Architecture

## Overview
Multi-user LAN access requires strict session isolation while maintaining visibility into swarm activity. Each WiFi-connected user gets their own workspace and clear activity attribution.

## Core Components

### 1. Session Manager (`session_manager.py`)
```python
class SessionManager:
    def __init__(self):
        self.active_sessions = {}  # IP -> SessionContext
        self.user_workspaces = {}  # IP -> workspace_path
        
    def create_session(self, client_ip, user_id=None):
        session_id = f"lan_{client_ip}_{int(time.time())}"
        workspace_path = f"user_sessions/{client_ip.replace('.', '_')}"
        
        session = SessionContext(
            session_id=session_id,
            client_ip=client_ip,
            workspace_path=workspace_path,
            created_at=time.time(),
            user_id=user_id or f"user_{client_ip}"
        )
        
        self.active_sessions[client_ip] = session
        self._create_user_workspace(workspace_path)
        return session
```

### 2. Activity Tagging System
```python
class ActivityTracker:
    def tag_activity(self, task_id, source_ip, activity_type):
        # Tag format: "user_triggered|background_swarm|admin_task"
        tag = {
            "task_id": task_id,
            "source_ip": source_ip,
            "activity_type": activity_type,
            "timestamp": time.time(),
            "user_session": self.get_session_id(source_ip)
        }
        return tag
```

### 3. Workspace Isolation
- **User Workspaces**: `user_sessions/{ip}/` for each connected IP
- **Sandboxed Execution**: All user tasks run in their workspace
- **File Boundaries**: Users cannot access parent directories or other user sessions
- **Resource Limits**: CPU/memory quotas per session

### 4. Real-time Status Dashboard
```javascript
// WebSocket message format
{
    "user_tasks": [
        {
            "task_id": "task_123",
            "status": "running",
            "description": "Processing your request...",
            "started_by": "you"
        }
    ],
    "network_activity": [
        {
            "task_id": "swarm_456", 
            "status": "running",
            "description": "Background optimization",
            "started_by": "system"
        },
        {
            "task_id": "user_789",
            "status": "completed", 
            "description": "Another user's task",
            "started_by": "192.168.1.105"
        }
    ]
}
```

## Security Boundaries

### Network Isolation
- **No Inter-User Communication**: Users cannot send messages to each other
- **Host Protection**: Users cannot execute commands on host machine
- **Admin Privilege**: Only admin IP can access core system files

### Filesystem Isolation
```
project_root/
â”œâ”€â”€ core_system/          # READ-ONLY for LAN users
â”‚   â”œâ”€â”€ orchestrator.py
â”‚   â”œâ”€â”€ grind_spawner.py
â”‚   â””â”€â”€ ...
â”œâ”€â”€ user_sessions/        # User workspaces
â”‚   â”œâ”€â”€ 192_168_1_100/   # User 1 workspace
â”‚   â”œâ”€â”€ 192_168_1_101/   # User 2 workspace
â”‚   â””â”€â”€ ...
â””â”€â”€ shared_readonly/      # Read-only shared resources
    â”œâ”€â”€ knowledge_graph.json
    â””â”€â”€ skill_registry.py
```

### Process Isolation
- **Containerization**: Each user session runs in Docker container
- **Resource Quotas**: CPU: 2 cores max, RAM: 4GB max, Disk: 10GB max
- **Network Restrictions**: No external network access except approved APIs

## Implementation Flow

### 1. User Connection
```
1. User connects to LAN interface
2. IP detected and session created
3. User workspace initialized
4. Welcome dashboard shows status
```

### 2. Task Execution
```
1. User submits task
2. Task tagged with user IP
3. Executed in user workspace
4. Status updates sent to user's WebSocket
```

### 3. Activity Monitoring
```
1. All tasks tagged by source
2. Real-time status aggregated
3. Users see "Your tasks" vs "Network activity"
4. Admin sees all activity across all users
```

## API Endpoints

### Session Management
- `POST /api/session/create` - Initialize user session
- `GET /api/session/status` - Get current session info
- `DELETE /api/session/destroy` - Clean up session

### Task Management
- `POST /api/task/submit` - Submit task to user workspace
- `GET /api/task/status/{task_id}` - Get task status
- `GET /api/task/list` - List user's tasks

### Activity Feed
- `GET /api/activity/user` - User's activity only
- `GET /api/activity/network` - Network-wide activity (anonymized)
- `WebSocket /ws/activity` - Real-time activity updates

## Configuration

### `lan_config.json`
```json
{
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
```

## Safety Features

1. **Auto-Cleanup**: Sessions expire after 1 hour of inactivity
2. **Resource Monitoring**: Kill tasks exceeding resource limits
3. **Audit Logging**: All user actions logged with IP attribution
4. **Emergency Stop**: Admin can kill all user sessions instantly
5. **Network Firewall**: Block access to sensitive network resources

This architecture ensures users have their own isolated environment while maintaining visibility into the broader swarm activity.