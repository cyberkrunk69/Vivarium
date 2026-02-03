# DUAL-SERVER ARCHITECTURE DESIGN

## Overview
Two-tier server architecture providing secure admin access and controlled LAN access for the Claude Parasite Brain Suck system.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    LAPTOP HOST SYSTEM                       │
├─────────────────────────────────────────────────────────────┤
│  ADMIN SERVER (127.0.0.1:8080)                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • Full system control                               │   │
│  │ • Worker management                                 │   │
│  │ • Configuration changes                             │   │
│  │ • Experiment control                                │   │
│  │ • Safety overrides                                  │   │
│  │ • Session termination                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                             │                               │
│                             │ Internal API                  │
│                             ▼                               │
│  LAN SERVER (0.0.0.0:8081)                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • Read-only dashboard                               │   │
│  │ • Progress monitoring                               │   │
│  │ • Log viewing (filtered)                           │   │
│  │ • Basic status info                                │   │
│  │ • Rate limited requests                            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ WiFi Network
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    LAN CLIENTS                              │
│  📱 Phone    💻 Tablet    💻 Other Laptops                 │
└─────────────────────────────────────────────────────────────┘
```

## Security Model

### Admin Server (127.0.0.1:8080)
- **Binding**: localhost only (127.0.0.1)
- **Access**: Physical laptop access required
- **Authentication**: None required (physical security)
- **Privileges**: Full system control

### LAN Server (0.0.0.0:8081)
- **Binding**: All interfaces
- **Access**: WiFi network clients
- **Authentication**: Session tokens + IP whitelist
- **Privileges**: Read-only + limited interactions

### Access Control Layers
1. **Network Layer**: IP binding restrictions
2. **Session Layer**: Token-based authentication for LAN
3. **Endpoint Layer**: Route-level privilege checks
4. **Rate Limiting**: Per-IP request throttling

## API Endpoints

### Admin Server API (127.0.0.1:8080)

#### System Control
- `POST /admin/shutdown` - Emergency system shutdown
- `POST /admin/restart` - Restart orchestrator
- `POST /admin/killswitch` - Activate safety killswitch

#### Worker Management
- `GET /admin/workers` - List all workers with full details
- `POST /admin/workers/spawn` - Spawn new worker
- `DELETE /admin/workers/{id}` - Terminate worker
- `POST /admin/workers/{id}/pause` - Pause worker
- `POST /admin/workers/{id}/resume` - Resume worker

#### Configuration
- `GET /admin/config` - Get full configuration
- `PUT /admin/config` - Update configuration
- `POST /admin/experiments/create` - Create new experiment
- `DELETE /admin/experiments/{id}` - Delete experiment

#### Monitoring
- `GET /admin/logs/full` - Unrestricted log access
- `GET /admin/metrics/detailed` - Detailed system metrics
- `GET /admin/safety/status` - Safety system status
- `POST /admin/safety/override` - Override safety constraints

### LAN Server API (0.0.0.0:8081)

#### Dashboard Access
- `GET /` - Main dashboard view
- `GET /status` - Basic system status
- `GET /progress` - Progress overview
- `GET /workers/summary` - Worker count and states

#### Monitoring (Read-Only)
- `GET /logs/filtered` - Sanitized log entries
- `GET /metrics/basic` - Basic performance metrics
- `GET /experiments/list` - Experiment list (no details)

#### Limited Interactions
- `POST /feedback` - Submit user feedback
- `GET /notifications` - Get system notifications
- `POST /alerts/acknowledge` - Acknowledge alerts

## Session Management Design

### Admin Sessions
- **Type**: Stateless (no session tracking needed)
- **Security**: Physical access assumption
- **Duration**: Unlimited
- **Storage**: None

### LAN Sessions
- **Type**: Token-based with expiry
- **Creation**: First connection generates session token
- **Duration**: 24 hours (configurable)
- **Renewal**: Automatic on activity
- **Storage**: In-memory with Redis backup option

```python
# Session Structure
{
    "session_id": "uuid4",
    "client_ip": "192.168.1.100",
    "user_agent": "browser_string",
    "created_at": "2026-02-03T10:16:49Z",
    "last_activity": "2026-02-03T10:16:49Z",
    "permissions": ["read", "feedback"],
    "rate_limit": {
        "requests_per_minute": 60,
        "current_count": 0,
        "window_start": "timestamp"
    }
}
```

### IP-Based Access Control
- **Whitelist Mode**: Only known LAN IPs allowed
- **Auto-Discovery**: New LAN IPs require admin approval
- **Blacklist**: Automatic blocking for abuse
- **Geo-Blocking**: Block non-local IP ranges

## Security Considerations

### Network Security
- Admin server NEVER binds to 0.0.0.0
- LAN server firewall rules restrict external access
- No port forwarding or external exposure

### Data Protection
- LAN clients see filtered/sanitized data only
- No sensitive configuration exposed via LAN API
- Log sanitization removes API keys, paths, etc.

### Rate Limiting
- Per-IP request limits on LAN server
- Exponential backoff for repeated violations
- Temporary IP bans for abuse patterns

### Monitoring & Alerts
- Failed authentication attempts logged
- Suspicious activity patterns detected
- Admin notifications for security events

## Implementation Notes

### Server Startup
```python
# admin_server.py - Binds to 127.0.0.1:8080
# lan_server.py - Binds to 0.0.0.0:8081
# Both share orchestrator state via internal API
```

### Communication Pattern
- LAN server queries admin server for data
- Admin server acts as data source authority
- No direct database access from LAN server
- Internal API uses localhost communication

### Failover Behavior
- If admin server down: LAN server shows cached data
- If LAN server down: Admin server continues normally
- Graceful degradation with status indicators