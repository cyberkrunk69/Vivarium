# LAN User Session Isolation Design

## Architecture Overview

Multi-user LAN access with complete session isolation while maintaining swarm visibility.

## Core Components

### 1. Session Manager (`lan_session_manager.py`)
```python
class LANSessionManager:
    def __init__(self):
        self.sessions = {}  # ip -> session_id
        self.user_workspaces = {}  # session_id -> workspace_path
        self.activity_tags = {}  # task_id -> session_id

    def create_session(self, client_ip):
        session_id = f"lan_{client_ip}_{timestamp()}"
        workspace_path = f"experiments/lan_users/{session_id}/"

        self.sessions[client_ip] = session_id
        self.user_workspaces[session_id] = workspace_path

        os.makedirs(workspace_path, exist_ok=True)
        return session_id

    def tag_activity(self, task_id, session_id):
        self.activity_tags[task_id] = session_id

    def is_user_activity(self, task_id, session_id):
        return self.activity_tags.get(task_id) == session_id
```

### 2. Isolated Web Gateway (`lan_web_gateway.py`)
```python
class LANWebGateway:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.app = Flask(__name__)

    def setup_routes(self):
        @self.app.route('/dashboard/<session_id>')
        def user_dashboard(session_id):
            # User-specific dashboard with isolation
            user_tasks = self.get_user_tasks(session_id)
            swarm_activity = self.get_swarm_activity(exclude_session=session_id)

            return render_template('user_dashboard.html',
                                 user_tasks=user_tasks,
                                 swarm_activity=swarm_activity,
                                 session_id=session_id)

        @self.app.route('/api/execute', methods=['POST'])
        def execute_task():
            client_ip = request.remote_addr
            session_id = self.session_manager.get_session(client_ip)

            # Sandbox task execution to user workspace
            task_data = request.json
            task_data['workspace'] = self.session_manager.get_workspace(session_id)
            task_data['session_id'] = session_id

            return self.execute_isolated_task(task_data)
```

### 3. Activity Segregation

#### User Activity Types
- **USER_TRIGGERED**: Tasks initiated by this specific user
- **SWARM_BACKGROUND**: Network-wide swarm operations
- **OTHER_USER**: Tasks from other LAN users (anonymized)

#### Real-time Status Display
```javascript
// Client-side dashboard updates
class UserActivityMonitor {
    constructor(sessionId) {
        this.sessionId = sessionId;
        this.eventSource = new EventSource(`/stream/${sessionId}`);

        this.eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.updateActivityDisplay(data);
        };
    }

    updateActivityDisplay(data) {
        if (data.session_id === this.sessionId) {
            this.addToUserTasks(data);
        } else if (data.type === 'swarm_activity') {
            this.addToSwarmActivity(data);
        }
    }
}
```

### 4. Workspace Isolation

#### Directory Structure
```
experiments/lan_users/
├── lan_192.168.1.100_1738584000/
│   ├── workspace/           # User's isolated working directory
│   ├── outputs/            # Task outputs
│   ├── session.json        # Session metadata
│   └── activity_log.json   # User activity history
├── lan_192.168.1.101_1738584100/
│   └── ...
```

#### Workspace Sandboxing
```python
class WorkspaceSandbox:
    def __init__(self, workspace_path):
        self.workspace_path = workspace_path
        self.allowed_paths = [workspace_path, '/tmp/claude/']

    def validate_file_access(self, file_path):
        abs_path = os.path.abspath(file_path)
        return any(abs_path.startswith(allowed) for allowed in self.allowed_paths)

    def execute_with_sandbox(self, command, session_id):
        # Wrap command execution with workspace restrictions
        if not self.validate_workspace_access(command):
            raise SecurityError(f"Command restricted for session {session_id}")

        return subprocess.run(command, cwd=self.workspace_path)
```

### 5. Network Security

#### IP-based Session Binding
```python
class SessionSecurity:
    def __init__(self):
        self.ip_sessions = {}
        self.session_timeouts = {}

    def validate_session(self, client_ip, session_id):
        current_session = self.ip_sessions.get(client_ip)

        if current_session != session_id:
            raise AuthError("Session mismatch for IP")

        if self.is_session_expired(session_id):
            self.cleanup_session(session_id)
            raise AuthError("Session expired")

        return True
```

### 6. Dashboard UI Components

#### User Dashboard Template
```html
<!-- user_dashboard.html -->
<div class="dashboard-container">
    <div class="user-section">
        <h2>Your Tasks</h2>
        <div id="user-tasks" class="task-list">
            <!-- User's tasks with full control -->
        </div>
    </div>

    <div class="swarm-section">
        <h2>Network Activity</h2>
        <div id="swarm-activity" class="activity-feed">
            <!-- Read-only swarm activity display -->
        </div>
    </div>

    <div class="session-info">
        Session: {{ session_id }}
        Workspace: {{ workspace_path }}
    </div>
</div>
```

### 7. API Endpoints

#### Session Management
- `GET /api/session/create` - Initialize new session for client IP
- `GET /api/session/status` - Get current session info
- `POST /api/session/cleanup` - Clean up expired sessions

#### Task Execution
- `POST /api/tasks/execute` - Execute task in isolated workspace
- `GET /api/tasks/user` - Get user's tasks
- `GET /api/tasks/swarm` - Get swarm activity (read-only)

#### Real-time Updates
- `GET /stream/{session_id}` - SSE stream for user activity
- `GET /stream/swarm` - SSE stream for network-wide activity

### 8. Safety Constraints

#### User Limitations
```python
USER_RESTRICTIONS = {
    'max_concurrent_tasks': 5,
    'max_workspace_size': '1GB',
    'allowed_commands': ['python', 'node', 'git'],
    'blocked_commands': ['rm -rf', 'sudo', 'chmod +x'],
    'network_access': False,  # No external network calls
    'file_system_access': 'workspace_only'
}
```

#### Host Protection
```python
class HostProtection:
    FORBIDDEN_PATHS = [
        '/etc/', '/usr/', '/var/', '/sys/', '/proc/',
        '/home/', '/root/', os.path.expanduser('~')
    ]

    FORBIDDEN_OPERATIONS = [
        'system_shutdown', 'network_config', 'user_management',
        'service_control', 'firewall_modification'
    ]
```

## Implementation Flow

1. **User Connection**: Client connects via WiFi, gets assigned session_id based on IP
2. **Workspace Creation**: Isolated directory structure created for user
3. **Dashboard Access**: User accesses personalized dashboard at `/dashboard/{session_id}`
4. **Task Execution**: All tasks run in sandboxed workspace with activity tagging
5. **Real-time Updates**: Dual-stream updates (user tasks + swarm activity)
6. **Session Cleanup**: Automatic cleanup of expired sessions and workspaces

## Security Model

- **Network Isolation**: Users cannot access host machine or other user workspaces
- **Process Isolation**: All user tasks run with restricted permissions
- **File System Isolation**: Read/write access limited to user workspace
- **Command Restrictions**: Whitelist of allowed commands and operations
- **Resource Limits**: CPU, memory, and disk usage caps per session

## User Experience

Users see:
- **Green indicators** for their own tasks and outputs
- **Blue indicators** for background swarm activity
- **Gray indicators** for anonymized other user activity
- **Clear workspace path** showing their isolated environment
- **Real-time updates** without affecting other users

This design provides complete isolation while maintaining transparency into the swarm's collective intelligence.