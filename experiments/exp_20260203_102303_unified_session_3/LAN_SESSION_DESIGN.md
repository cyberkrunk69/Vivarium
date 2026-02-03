# LAN User Session Isolation Architecture

## Overview
Multi-user LAN access to the swarm system with complete session isolation, activity visibility, and workspace separation.

## Core Components

### 1. Session Manager (`lan_session_manager.py`)
```python
class LANSessionManager:
    def __init__(self):
        self.sessions = {}  # ip -> SessionContext
        self.active_tasks = {}  # task_id -> owner_ip
        self.shared_visibility = SharedActivityTracker()

    def create_session(self, client_ip, user_id=None):
        session = UserSession(
            ip=client_ip,
            workspace=f"user_sessions/{client_ip}",
            task_namespace=f"user_{client_ip.replace('.', '_')}",
            created_at=datetime.now()
        )
        self.sessions[client_ip] = session
        return session
```

### 2. User Session Context
```python
class UserSession:
    def __init__(self, ip, workspace, task_namespace, created_at):
        self.ip = ip
        self.workspace = workspace  # Isolated file workspace
        self.task_namespace = task_namespace  # Task ID prefix
        self.created_at = created_at
        self.active_tasks = set()
        self.task_history = []
        self.permissions = UserPermissions()
```

### 3. Workspace Isolation

#### Directory Structure
```
user_sessions/
├── 192_168_1_100/           # User workspace (IP-based)
│   ├── inputs/              # User input files
│   ├── outputs/             # Generated files
│   ├── temp/                # Temporary files
│   └── session.json         # Session metadata
├── 192_168_1_101/
│   └── ...
└── shared/                  # Read-only shared resources
    ├── templates/
    └── references/
```

#### Workspace Manager
```python
class WorkspaceManager:
    def create_user_workspace(self, client_ip):
        workspace_path = f"user_sessions/{client_ip.replace('.', '_')}"
        os.makedirs(workspace_path, exist_ok=True)

        # Set permissions - user can only access their workspace
        self.set_workspace_permissions(workspace_path, client_ip)

        return workspace_path

    def isolate_file_operations(self, client_ip, requested_path):
        user_workspace = self.get_user_workspace(client_ip)
        if not requested_path.startswith(user_workspace):
            raise PermissionError(f"Access denied: {requested_path}")
```

### 4. Activity Tagging System

#### Task Classification
```python
class ActivityTracker:
    def tag_task(self, task_id, source_type, owner_ip=None):
        tags = {
            'USER_TRIGGERED': f"Started by user {owner_ip}",
            'SWARM_AUTO': "Background swarm activity",
            'ADMIN_TASK': "System maintenance",
            'CROSS_USER': "Multi-user collaboration"
        }

        self.task_metadata[task_id] = {
            'type': source_type,
            'owner': owner_ip,
            'tag': tags[source_type],
            'started_at': datetime.now(),
            'visible_to': self.get_visibility_scope(source_type)
        }
```

### 5. Real-time Status Dashboard

#### User View Components
```javascript
// Client-side dashboard sections
const UserDashboard = {
    myTasks: [],          // Tasks I triggered
    networkActivity: [],   // What others are doing (filtered)
    swarmStatus: {},      // Overall system health
    myWorkspace: {}       // My files and outputs
}

// SSE endpoint per user
app.get('/status/:client_ip', (req, res) => {
    const userSession = sessionManager.getSession(req.params.client_ip);
    const userView = {
        myTasks: userSession.getActiveTasks(),
        networkActivity: activityTracker.getVisibleActivity(req.params.client_ip),
        swarmHealth: systemMonitor.getPublicMetrics()
    };
    res.json(userView);
});
```

### 6. Permission System

#### User Permissions
```python
class UserPermissions:
    def __init__(self, role="standard_user"):
        self.can_read_core_system = False
        self.can_modify_core_system = False
        self.can_see_other_workspaces = False
        self.can_trigger_swarm_tasks = True
        self.can_view_network_activity = True  # Read-only
        self.workspace_quota_mb = 1024
        self.max_concurrent_tasks = 5
```

#### Safety Boundaries
```python
class SessionSafety:
    FORBIDDEN_PATHS = [
        'grind_spawner.py',
        'orchestrator.py',
        'core_system/',
        '../',  # No directory traversal
        '/etc/', '/system/',  # System paths
    ]

    def validate_file_access(self, client_ip, file_path):
        user_workspace = f"user_sessions/{client_ip.replace('.', '_')}"

        # Must be within user workspace
        if not os.path.abspath(file_path).startswith(user_workspace):
            raise SecurityError("Path outside user workspace")

        # Check forbidden paths
        if any(forbidden in file_path for forbidden in self.FORBIDDEN_PATHS):
            raise SecurityError("Access to system files denied")
```

## Implementation Flow

### 1. User Connection
1. Client connects via LAN (IP detected)
2. SessionManager creates isolated session
3. WorkspaceManager sets up user directory
4. Dashboard shows personalized view

### 2. Task Execution
1. User submits task → Tagged as 'USER_TRIGGERED'
2. Task runs in user's namespace: `user_192_168_1_100_task_001`
3. File operations restricted to user workspace
4. Status updates sent to user's SSE stream

### 3. Activity Visibility
1. User sees their own tasks in detail
2. Network activity shows: "3 other users active, 12 background tasks"
3. Swarm status shows overall system health
4. No access to other users' task details

### 4. File Management
```python
# Example: User uploads file
def handle_file_upload(client_ip, file_data, filename):
    session = session_manager.get_session(client_ip)
    safe_path = os.path.join(session.workspace, 'inputs', filename)

    # Validate and save to user workspace only
    workspace_manager.save_file(safe_path, file_data, client_ip)

    return {'path': safe_path, 'accessible_to': client_ip}
```

## Security Features

1. **Path Traversal Prevention**: All file paths validated against user workspace
2. **Resource Limits**: CPU/memory quotas per user session
3. **Network Isolation**: Users cannot access host network or other machines
4. **Task Namespace**: All user tasks prefixed with IP identifier
5. **Read-Only Core**: System files completely protected

## User Experience

### What Users See
- **My Tasks**: Tasks I started, with full details and logs
- **Network Activity**: "5 users active, 23 swarm tasks running" (no details)
- **My Workspace**: My files, inputs, outputs (isolated)
- **System Status**: Overall health, no admin controls

### What Users Cannot See
- Other users' task details or logs
- System configuration or core files
- Other users' workspaces or files
- Administrative functions or controls

## Example Session Flow

```
User 192.168.1.100 connects:
1. Session created: user_192_168_1_100
2. Workspace: user_sessions/192_168_1_100/
3. Dashboard loads showing:
   - My Tasks: (empty)
   - Network: "2 other users active"
   - Swarm: "Healthy, 15 background tasks"

User submits task "Analyze my data.csv":
1. File saved to user_sessions/192_168_1_100/inputs/data.csv
2. Task tagged: USER_TRIGGERED, owner=192.168.1.100
3. Task ID: user_192_168_1_100_task_001
4. Runs isolated in user workspace
5. Updates appear in user's "My Tasks" section only
```

This architecture provides complete isolation while maintaining useful visibility into swarm activity.