# LAN Session Isolation Architecture

## Overview
Design for multi-user LAN access with proper session isolation, visibility, and security boundaries.

## Core Components

### 1. Session Management Layer
```
SessionManager:
  - per_ip_sessions: Dict[str, UserSession]
  - active_connections: Dict[str, WebSocketConnection]
  - workspace_isolation: WorkspaceManager
```

**UserSession Structure:**
- `session_id`: UUID per IP
- `user_ip`: Client IP address
- `workspace_path`: Isolated workspace directory
- `task_queue`: User-specific task queue
- `permissions`: User permission level
- `created_at`: Session creation timestamp

### 2. Workspace Isolation

**Directory Structure:**
```
/workspaces/
  /{session_id}/
    /input/     # User upload area
    /output/    # Generated artifacts
    /temp/      # Temporary files
    /logs/      # Session-specific logs
```

**Isolation Rules:**
- Each user gets isolated filesystem sandbox
- No access to host system beyond workspace
- No cross-user file access
- Temporary files auto-cleanup on disconnect

### 3. Activity Classification System

**Task Tagging:**
- `USER_TRIGGERED`: Direct user commands
- `BACKGROUND_SWARM`: Autonomous swarm operations
- `SYSTEM_MAINTENANCE`: System-level operations
- `CROSS_SESSION`: Multi-user collaborative tasks

**Activity Visibility:**
```json
{
  "your_tasks": [
    {
      "id": "task_123",
      "type": "USER_TRIGGERED",
      "status": "running",
      "description": "Generate API documentation"
    }
  ],
  "network_activity": [
    {
      "id": "swarm_456",
      "type": "BACKGROUND_SWARM",
      "status": "running",
      "description": "Code optimization sweep",
      "user_session": null
    }
  ]
}
```

### 4. Real-Time Status Dashboard

**User Interface Sections:**
1. **Your Session** - Personal task queue and status
2. **Network Activity** - Swarm operations visible to all
3. **System Resources** - CPU/memory usage across network
4. **Connection Status** - Your connection health

**WebSocket Events:**
- `session.task.started`
- `session.task.completed`
- `swarm.activity.update`
- `network.status.change`

### 5. Security Boundaries

**Network Isolation:**
- Users cannot execute commands on host
- No access to other users' workspaces
- Read-only view of system status
- Sandboxed code execution only

**Permission Levels:**
- `GUEST`: View-only access
- `USER`: Can trigger tasks in own workspace
- `ADMIN`: Full system access (host machine)

### 6. Implementation Plan

**Core Files to Create:**
1. `session_manager.py` - Session lifecycle management
2. `workspace_isolator.py` - File system isolation
3. `activity_classifier.py` - Task tagging and visibility
4. `lan_gateway.py` - Network access point
5. `user_dashboard.py` - Per-session UI

**Integration Points:**
- Hook into existing `progress_server.py` for WebSocket handling
- Extend `orchestrator.py` with session awareness
- Modify task execution to respect workspace isolation

**Database Schema:**
```sql
CREATE TABLE user_sessions (
    session_id VARCHAR(36) PRIMARY KEY,
    user_ip VARCHAR(45) NOT NULL,
    workspace_path VARCHAR(255) NOT NULL,
    permission_level VARCHAR(20) DEFAULT 'USER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE session_tasks (
    task_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) REFERENCES user_sessions(session_id),
    task_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Benefits

1. **True Multi-User Support**: Multiple people can use the system simultaneously
2. **Clear Ownership**: Users see exactly what they triggered vs background activity
3. **Security**: No risk of users affecting host or each other
4. **Transparency**: Full visibility into swarm operations
5. **Scalability**: Session management supports many concurrent users

## Next Steps

1. Implement session manager with IP-based isolation
2. Create workspace sandboxing layer
3. Add activity classification to existing task system
4. Build user-specific dashboard views
5. Test with multiple concurrent LAN connections