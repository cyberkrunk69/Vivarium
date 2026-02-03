# DUAL-SERVER ARCHITECTURE DESIGN

## Overview
Two-server architecture providing secure separation between local admin control and network-accessible monitoring.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          LOCALHOST                             │
│  ┌─────────────────┐                                           │
│  │  ADMIN SERVER   │ ← FULL CONTROL                            │
│  │  127.0.0.1:8080 │   - Start/stop workers                   │
│  │                 │   - Modify configurations                 │
│  └─────────────────┘   - View all logs                        │
│           │             - System diagnostics                  │
│           │                                                   │
│  ┌─────────────────┐                                           │
│  │   ORCHESTRATOR  │ ← CORE SYSTEM                            │
│  │   BACKEND       │   - Worker management                    │
│  │                 │   - State tracking                       │
│  └─────────────────┘   - Performance metrics                 │
│           │                                                   │
└───────────┼───────────────────────────────────────────────────┘
            │
┌───────────┼───────────────────────────────────────────────────┐
│           │                    LAN                            │
│  ┌─────────────────┐                                           │
│  │   LAN SERVER    │ ← RESTRICTED ACCESS                      │
│  │  0.0.0.0:8081   │   - Read-only monitoring                 │
│  │                 │   - Progress viewing                     │
│  └─────────────────┘   - Basic metrics                       │
│                                                               │
│  ┌─────────────────┐   ┌─────────────────┐                    │
│  │  WIFI CLIENT 1  │   │  WIFI CLIENT 2  │                    │
│  │  192.168.1.100  │   │  192.168.1.101  │                    │
│  └─────────────────┘   └─────────────────┘                    │
└───────────────────────────────────────────────────────────────┘
```

## Security Model

### Admin Server (127.0.0.1:8080)
- **Binding**: Localhost only (`127.0.0.1`)
- **Access**: Physical machine only
- **Privileges**: FULL CONTROL
- **Authentication**: None required (localhost trusted)

### LAN Server (0.0.0.0:8081)
- **Binding**: All interfaces (`0.0.0.0`)
- **Access**: Network clients (WiFi/LAN)
- **Privileges**: READ-ONLY monitoring
- **Authentication**: Session-based tracking
- **Rate Limiting**: Per-IP request limits

## API Endpoints

### Admin Server Endpoints (127.0.0.1:8080)

#### System Control
- `POST /api/workers/start` - Start worker processes
- `POST /api/workers/stop` - Stop worker processes
- `POST /api/workers/restart` - Restart worker processes
- `PUT /api/config` - Update system configuration
- `POST /api/experiments/create` - Create new experiment
- `DELETE /api/experiments/{id}` - Delete experiment

#### Full Data Access
- `GET /api/status/full` - Complete system status
- `GET /api/logs/all` - All system logs
- `GET /api/metrics/detailed` - Detailed performance metrics
- `GET /api/workers/debug` - Debug information
- `GET /api/files/edit/{path}` - Edit system files
- `PUT /api/files/save/{path}` - Save system files

#### Admin Dashboard
- `GET /` - Full admin dashboard
- `GET /admin/controls` - Worker control panel
- `GET /admin/config` - Configuration editor
- `GET /admin/logs` - Log viewer with filters

### LAN Server Endpoints (0.0.0.0:8081)

#### Read-Only Monitoring
- `GET /api/status/basic` - Basic system status (filtered)
- `GET /api/progress` - Current progress metrics
- `GET /api/workers/status` - Worker status (no debug info)
- `GET /api/experiments/list` - List experiments (metadata only)
- `GET /api/metrics/public` - Public performance metrics

#### Limited Dashboard
- `GET /` - Read-only monitoring dashboard
- `GET /monitor/progress` - Progress visualization
- `GET /monitor/stats` - Statistics view
- `GET /api/session/info` - Session information

#### WebSocket Streams
- `WS /ws/progress` - Real-time progress updates
- `WS /ws/metrics` - Real-time metrics stream

## Session Management Design

### Session Tracking Structure
```json
{
  "session_id": "uuid-v4",
  "client_ip": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "connected_at": "2026-02-03T10:19:38Z",
  "last_activity": "2026-02-03T10:25:12Z",
  "request_count": 147,
  "rate_limit_remaining": 853,
  "access_level": "lan_readonly",
  "blocked": false
}
```

### IP-Based Access Control

#### Allowed IP Ranges
- `127.0.0.1` - Admin server access
- `192.168.0.0/16` - Private network (LAN server)
- `10.0.0.0/8` - Private network (LAN server)
- `172.16.0.0/12` - Private network (LAN server)

#### Rate Limiting
- **LAN Clients**: 100 requests/minute per IP
- **WebSocket**: 1 connection per IP
- **Burst**: 10 requests/10 seconds

#### Blocked Actions for LAN
- No file modifications
- No worker control
- No configuration changes
- No experiment deletion
- No system diagnostics access

## Implementation Components

### 1. Server Factory
```python
def create_admin_server():
    # Bind to 127.0.0.1:8080 only
    # Full Flask app with all endpoints

def create_lan_server():
    # Bind to 0.0.0.0:8081
    # Filtered Flask app with read-only endpoints
```

### 2. Middleware Stack
```python
- IP Validation Middleware
- Rate Limiting Middleware
- Session Tracking Middleware
- Access Control Middleware
- Logging Middleware
```

### 3. Data Filtering
```python
def filter_for_lan(data):
    # Remove sensitive information
    # Redact debug details
    # Limit data depth
```

### 4. WebSocket Security
```python
- Origin validation
- IP-based connection limits
- Automatic disconnection on rate limit
- Heartbeat monitoring
```

## Security Considerations

### Admin Server Protection
- Only accessible from localhost
- No network exposure risk
- Full trust model
- No authentication overhead

### LAN Server Protection
- Public interface with restrictions
- Session-based tracking
- Rate limiting per IP
- Data filtering/redaction
- WebSocket connection limits
- Graceful degradation on overload

### Network Isolation
- Admin operations completely isolated
- LAN server cannot modify core system
- Clear privilege separation
- Audit logging for all LAN access

## Deployment Configuration

### Docker Compose Setup
```yaml
services:
  admin-server:
    ports:
      - "127.0.0.1:8080:8080"

  lan-server:
    ports:
      - "8081:8081"
```

### Firewall Rules
- Allow 8080 only from 127.0.0.1
- Allow 8081 from private networks
- Block external access to both ports

## Monitoring & Logging

### Admin Server Logs
- All user actions
- Configuration changes
- System modifications
- Error details

### LAN Server Logs
- Client connections
- Request patterns
- Rate limit hits
- Security events

### Metrics Collection
- Connection counts per server
- Request rates
- Error rates
- Session duration
- Resource usage per server