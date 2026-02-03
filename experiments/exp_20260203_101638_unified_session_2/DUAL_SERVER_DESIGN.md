# DUAL-SERVER ARCHITECTURE DESIGN

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        LAPTOP (Host Machine)                    │
│                                                                 │
│  ┌─────────────────────┐        ┌─────────────────────────────┐ │
│  │   ADMIN SERVER      │        │        LAN SERVER           │ │
│  │   127.0.0.1:8080    │        │      0.0.0.0:8081          │ │
│  │   ┌─────────────┐   │        │   ┌─────────────────────┐   │ │
│  │   │ Full Control│   │        │   │ Restricted Access   │   │ │
│  │   │ Dashboard   │   │        │   │ Read-only Dashboard │   │ │
│  │   │ Config Mgmt │   │        │   │ Status Viewer       │   │ │
│  │   │ System Ops  │   │        │   │ Public Metrics      │   │ │
│  │   └─────────────┘   │        │   └─────────────────────┘   │ │
│  └─────────────────────┘        └─────────────────────────────┘ │
│           │                                     │               │
│           │                                     │               │
└───────────┼─────────────────────────────────────┼───────────────┘
            │                                     │
            │ Admin Only                          │ LAN Access
            ▼                                     ▼
    ┌─────────────┐                      ┌─────────────────┐
    │   Laptop    │                      │  WiFi Devices   │
    │  Browser    │                      │  (Phones/etc)   │
    │ localhost:  │                      │  192.168.x.x:   │
    │    8080     │                      │     8081        │
    └─────────────┘                      └─────────────────┘
```

## Security Model

### Admin Server (127.0.0.1:8080)
- **Binding**: localhost only (127.0.0.1)
- **Access**: Direct laptop access only
- **Authentication**: None required (localhost trust)
- **Capabilities**: Full system control

### LAN Server (0.0.0.0:8081)
- **Binding**: All interfaces (accessible via WiFi)
- **Access**: Network devices on same LAN
- **Authentication**: IP-based allowlist + session tokens
- **Capabilities**: Read-only + limited interactions

## API Endpoints

### Admin Server Endpoints (Port 8080)

#### System Control
- `GET /admin/dashboard` - Full control dashboard
- `POST /admin/config/update` - Update system configuration
- `POST /admin/system/restart` - Restart services
- `POST /admin/system/shutdown` - Shutdown system
- `DELETE /admin/logs/clear` - Clear system logs
- `POST /admin/swarm/control` - Start/stop swarm operations

#### Data Management
- `GET /admin/data/export` - Export all system data
- `POST /admin/data/import` - Import system data
- `DELETE /admin/data/reset` - Factory reset
- `GET /admin/experiments/manage` - Manage experiments

#### Configuration
- `GET /admin/config` - View full configuration
- `PUT /admin/config` - Update configuration
- `POST /admin/users/manage` - Manage user access

### LAN Server Endpoints (Port 8081)

#### Public Dashboard
- `GET /` - Read-only dashboard view
- `GET /status` - System status (sanitized)
- `GET /metrics` - Public performance metrics
- `GET /health` - Health check endpoint

#### Limited Interactions
- `GET /logs/recent` - Recent logs (filtered)
- `GET /experiments/list` - List public experiments
- `GET /experiments/{id}/status` - Experiment status
- `POST /feedback/submit` - Submit feedback/observations

#### Session Management
- `POST /session/create` - Create session token
- `GET /session/info` - Get session information
- `DELETE /session/destroy` - Destroy session

## Session Management Design

### Session Architecture
```
┌─────────────────────┐
│   Session Store     │
│  ┌───────────────┐  │
│  │ Device: iPad  │  │
│  │ IP: 192.168.1.5│ │
│  │ Token: abc123 │  │
│  │ Created: time │  │
│  │ LastSeen: time│  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │ Device: Phone │  │
│  │ IP: 192.168.1.8│ │
│  │ Token: def456 │  │
│  │ Expires: time │  │
│  └───────────────┘  │
└─────────────────────┘
```

### Session Flow
1. **Device Connection**: Device connects to LAN server
2. **IP Validation**: Check if IP is in allowed range
3. **Token Generation**: Generate unique session token
4. **Device Fingerprinting**: Store device characteristics
5. **Session Tracking**: Track activity and last seen time
6. **Auto-Expiry**: Sessions expire after inactivity

### Session Data Structure
```python
{
    "session_id": "uuid4-string",
    "device_ip": "192.168.1.x",
    "device_fingerprint": {
        "user_agent": "...",
        "screen_resolution": "...",
        "timezone": "..."
    },
    "created_at": "timestamp",
    "last_activity": "timestamp",
    "expires_at": "timestamp",
    "permissions": ["read_status", "view_logs", "submit_feedback"],
    "rate_limit": {
        "requests_per_minute": 60,
        "current_count": 0,
        "reset_time": "timestamp"
    }
}
```

## Security Restrictions

### IP-Based Access Control
- **Allowed Ranges**: 192.168.x.x, 10.x.x.x, 172.16-31.x.x
- **Blocked IPs**: External/public IPs automatically rejected
- **Rate Limiting**: Per-IP request limits to prevent abuse

### Data Sanitization
- **Logs**: Remove sensitive information before serving
- **Metrics**: Only aggregate, non-sensitive data
- **Errors**: Generic error messages, no stack traces

### Capability Restrictions
- **No System Control**: Cannot restart, shutdown, or modify config
- **No Data Export**: Cannot download sensitive data
- **No Experiment Control**: Cannot start/stop experiments
- **Read-Only Access**: Most endpoints are GET only

## Implementation Strategy

### Server Separation
```python
# admin_server.py - Bound to 127.0.0.1:8080
app_admin = Flask(__name__)
app_admin.run(host='127.0.0.1', port=8080)

# lan_server.py - Bound to 0.0.0.0:8081
app_lan = Flask(__name__)
app_lan.run(host='0.0.0.0', port=8081)
```

### Shared Components
- **Data Layer**: Both servers access same data sources
- **Business Logic**: Shared core functionality
- **Authentication**: Common session management
- **Logging**: Unified logging system

### Deployment
- **Process Separation**: Two separate Python processes
- **Health Monitoring**: Each server monitors the other
- **Graceful Shutdown**: Coordinated shutdown sequence
- **Startup Order**: Admin server starts first, then LAN server

## Benefits

1. **Security**: Clear privilege separation
2. **Accessibility**: Mobile device access without compromising security
3. **Isolation**: Network issues don't affect local admin access
4. **Scalability**: Can handle multiple concurrent LAN connections
5. **Monitoring**: Clear audit trail of external access

## Future Enhancements

- **HTTPS Support**: SSL/TLS for LAN server
- **Authentication**: Optional password protection for LAN access
- **Mobile App**: Dedicated mobile application
- **Push Notifications**: Real-time updates to connected devices
- **WebSocket Support**: Real-time dashboard updates