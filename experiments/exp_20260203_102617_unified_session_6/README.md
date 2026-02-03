# LAN Session Manager

Complete multi-user session isolation system for LAN access to the swarm system.

## Components

### Core Files

- **`lan_session_manager.py`** - Main session management with workspace isolation
- **`session_web_server.py`** - Flask web server serving dashboard and REST API
- **`session_websocket_server.py`** - Real-time WebSocket updates
- **`session_dashboard.html`** - Frontend dashboard interface

### Features

#### ✅ Session Isolation
- Per-IP session tracking with unique identifiers
- Isolated workspace directories for each user
- Task namespace prefixes (e.g., `user_192_168_1_100_task_001`)
- Session timeout and cleanup

#### ✅ Security & Permissions
- Path traversal prevention
- Core system file protection
- Workspace quota limits
- File access validation

#### ✅ Activity Segregation
- **"My Tasks"** - Full details of user's own tasks
- **"Network Activity"** - Anonymous stats about other users
- **"Swarm Status"** - Overall system health metrics
- Real-time task status updates

#### ✅ WebSocket Integration
- Real-time dashboard updates
- Task submission notifications
- Connection status monitoring
- Automatic reconnection

## Quick Start

```bash
# Start the web server (includes WebSocket server)
python session_web_server.py --host 0.0.0.0 --port 5000

# Or with debug mode
python session_web_server.py --debug
```

Access dashboard: `http://your-server-ip:5000`

## API Endpoints

### Session Management
- `GET /` - Dashboard interface
- `GET /api/client-ip` - Get client IP
- `GET /api/dashboard/{client_ip}` - Get dashboard data
- `GET /api/session/{client_ip}` - Get session info

### Task Management
- `POST /api/task/submit` - Submit new task
- `POST /api/task/{task_id}/complete` - Complete task

### System Information
- `GET /api/system/health` - System health
- `GET /api/sessions/all` - All sessions (admin)
- `GET /api/activity/log` - Activity log

### File Access
- `POST /api/workspace/{client_ip}/validate` - Validate file access

## Usage Example

```python
from lan_session_manager import get_session_manager

session_manager = get_session_manager()

# Create session for user
session = session_manager.create_session("192.168.1.100")

# Submit task
task_id = session_manager.submit_task("192.168.1.100", "Analyze data.csv")

# Validate file access
is_valid = session_manager.validate_file_access("192.168.1.100", "user_sessions/192_168_1_100/inputs/data.csv")

# Get dashboard data
dashboard_data = session_manager.get_user_dashboard_data("192.168.1.100")
```

## Directory Structure

```
user_sessions/
├── 192_168_1_100/           # User workspace
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

## Security Features

1. **Path Traversal Prevention** - All file paths validated against user workspace
2. **Resource Limits** - CPU/memory quotas per user session
3. **Network Isolation** - Users cannot access host network
4. **Task Namespace** - All user tasks prefixed with IP identifier
5. **Read-Only Core** - System files completely protected

## Dashboard Features

### User View
- **My Tasks** - Tasks I started with full details and logs
- **Network Activity** - "5 users active, 23 swarm tasks running" (no details)
- **Workspace Usage** - My files, storage usage
- **System Status** - Overall health, no admin controls

### Real-time Updates
- WebSocket connection with auto-reconnect
- Live task status changes
- Network activity counters
- Connection status indicator

## Configuration

Environment variables:
- `SESSION_TIMEOUT_MINUTES` - Session timeout (default: 60)
- `WORKSPACE_QUOTA_MB` - User storage quota (default: 1024)
- `MAX_CONCURRENT_TASKS` - Max tasks per user (default: 5)

## Integration with Existing System

To integrate with the main swarm system:

```python
# In your main orchestrator
from experiments.exp_20260203_102617_unified_session_6.lan_session_manager import get_session_manager

session_manager = get_session_manager()

# When starting a task, check if it's from a LAN user
def start_task(task_id, description, source_ip=None):
    if source_ip:
        # Tag as user task
        session_manager.activity_tracker.tag_task(task_id, 'USER_TRIGGERED', source_ip)
        session = session_manager.get_session(source_ip)
        if session:
            session.add_task(task_id, metadata)
    else:
        # Tag as system task
        session_manager.activity_tracker.tag_task(task_id, 'SWARM_AUTO')
```

## Notes

- Sessions auto-expire after 60 minutes of inactivity
- WebSocket server runs on port 8765 by default
- All user data is isolated to their workspace
- Dashboard updates every 30 seconds as fallback
- Compatible with existing grind_spawner and orchestrator systems