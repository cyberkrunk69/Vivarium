# DUAL-SERVER ARCHITECTURE DESIGN

## Architecture Overview

```ascii
┌─────────────────────────────────────────────────────────────┐
│                    LAPTOP (HOST MACHINE)                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │   ADMIN SERVER  │    │        LAN SERVER               │ │
│  │  localhost:8080 │    │      0.0.0.0:8081               │ │
│  │   FULL CONTROL  │    │   RESTRICTED ACCESS             │ │
│  └─────────────────┘    └─────────────────────────────────┘ │
│           │                           │                     │
│           │                           │                     │
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │ SESSION MANAGER │    │     SAFETY GATEWAY             │ │
│  │ - Admin tokens  │    │ - IP whitelist                  │ │
│  │ - Full perms    │    │ - Rate limiting                 │ │
│  │ - No restrictions│   │ - Command filtering             │ │
│  └─────────────────┘    └─────────────────────────────────┘ │
│                                       │                     │
└───────────────────────────────────────┼─────────────────────┘
                                        │
                            ┌───────────┼───────────┐
                            │    LOCAL NETWORK      │
                            │                       │
                    ┌───────┴─────┐       ┌─────────┴───────┐
                    │   PHONE A   │       │    PHONE B      │
                    │ 192.168.x.x │       │  192.168.x.x    │
                    └─────────────┘       └─────────────────┘
```

## Security Model

### ADMIN SERVER (localhost:8080)
- **Binding**: 127.0.0.1:8080 ONLY
- **Access**: Local laptop only, no network exposure
- **Privileges**: FULL SYSTEM CONTROL
- **Authentication**: Optional (trusted local environment)
- **Capabilities**: All API endpoints, system management, file operations

### LAN SERVER (0.0.0.0:8081)
- **Binding**: All interfaces (0.0.0.0:8081)
- **Access**: WiFi devices on local network
- **Privileges**: RESTRICTED READ-ONLY + LIMITED OPERATIONS
- **Authentication**: Session tokens + IP validation
- **Capabilities**: Dashboard viewing, limited status queries

## API Endpoints

### ADMIN SERVER ENDPOINTS (localhost:8080)

#### System Control
```
POST /admin/start-session         # Start new grind session
POST /admin/stop-session          # Stop current session
POST /admin/pause-session         # Pause current session
POST /admin/restart-worker/{id}   # Restart specific worker
POST /admin/shutdown              # Full system shutdown
```

#### File Operations
```
GET  /admin/files/list            # List all files
POST /admin/files/upload          # Upload files
PUT  /admin/files/edit            # Edit files
DELETE /admin/files/delete        # Delete files
```

#### Configuration
```
GET  /admin/config                # Get full configuration
PUT  /admin/config                # Update configuration
POST /admin/config/reset          # Reset to defaults
```

#### Logs & Debug
```
GET  /admin/logs/full             # Get all system logs
POST /admin/debug/enable          # Enable debug mode
GET  /admin/metrics/detailed      # Detailed performance metrics
```

### LAN SERVER ENDPOINTS (0.0.0.0:8081)

#### Dashboard & Status (READ-ONLY)
```
GET  /status                      # Basic system status
GET  /dashboard                   # Dashboard view
GET  /workers/status              # Worker status only
GET  /logs/recent                 # Recent logs (filtered)
```

#### Limited Interactions
```
POST /submit-feedback             # Submit feedback/suggestions
GET  /session/progress            # Current session progress
GET  /metrics/basic               # Basic performance metrics
```

#### Session Management
```
POST /auth/register-device        # Register device for access
GET  /auth/session-info           # Get current session info
POST /auth/heartbeat              # Keep session alive
```

## Session Management Design

### Device Registration Flow
```
1. Device connects to LAN server
2. Server generates unique device_id
3. Device provides basic info (name, type, IP)
4. Server creates session with restrictions
5. Session token issued with expiration
6. IP address bound to session
```

### Session Tracking Structure
```json
{
  "session_id": "sess_abc123",
  "device_id": "dev_xyz789",
  "ip_address": "192.168.1.100",
  "device_info": {
    "name": "iPhone 12",
    "type": "mobile",
    "user_agent": "..."
  },
  "created_at": "2026-02-03T10:30:42Z",
  "last_heartbeat": "2026-02-03T10:35:42Z",
  "expires_at": "2026-02-03T18:30:42Z",
  "permissions": ["read_status", "submit_feedback"],
  "rate_limits": {
    "requests_per_minute": 60,
    "requests_per_hour": 1000
  }
}
```

## Security Restrictions

### IP-Based Access Control
- **Whitelist Mode**: Only allow local network IPs (192.168.x.x, 10.x.x.x)
- **Blacklist**: Block known suspicious patterns
- **Rate Limiting**: Per-IP request limits
- **Geographic Blocking**: Block non-local requests

### Command Filtering (LAN Server)
```
ALLOWED:
- GET requests for status/dashboard
- POST for feedback submission
- Session management calls

BLOCKED:
- Any file system operations
- System control commands
- Configuration changes
- Worker management
- Debug/admin functions
```

### Data Sanitization
- Strip sensitive paths from responses
- Filter out internal system details
- Mask configuration values
- Remove debug information

## Implementation Architecture

### Server Separation
```python
# admin_server.py - Full privilege server
class AdminServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8080
        self.auth = None  # Optional local auth

    def start(self):
        # Bind ONLY to localhost
        pass

# lan_server.py - Restricted network server
class LanServer:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 8081
        self.safety_gateway = SafetyGateway()
        self.session_manager = SessionManager()

    def start(self):
        # Bind to all interfaces with restrictions
        pass
```

### Safety Gateway
```python
class SafetyGateway:
    def __init__(self):
        self.ip_whitelist = self.load_local_network_ranges()
        self.rate_limiter = RateLimiter()
        self.command_filter = CommandFilter()

    def validate_request(self, request):
        # IP validation
        # Rate limiting
        # Command filtering
        # Session validation
        pass
```

### Deployment Strategy
1. **Single Process**: Both servers in one Python process with different routes
2. **Dual Process**: Separate processes for complete isolation
3. **Docker**: Containerized deployment with network policies
4. **Reverse Proxy**: nginx/Apache frontend with routing rules

## Monitoring & Logging

### Admin Server Logging
- Full request/response logging
- System operation audit trail
- Performance metrics collection
- Error tracking and debugging

### LAN Server Logging
- Connection attempts and IP tracking
- Rate limit violations
- Suspicious activity detection
- Session lifecycle events

## Emergency Controls

### Kill Switch
- **Admin Server**: Immediate shutdown command
- **LAN Server**: Network isolation mode
- **Global**: Full system lockdown

### Safety Triggers
- Suspicious IP activity
- Repeated authentication failures
- Unusual traffic patterns
- System resource exhaustion

## Configuration Example

```json
{
  "admin_server": {
    "host": "127.0.0.1",
    "port": 8080,
    "auth_required": false,
    "log_level": "DEBUG"
  },
  "lan_server": {
    "host": "0.0.0.0",
    "port": 8081,
    "auth_required": true,
    "session_timeout": 28800,
    "rate_limits": {
      "requests_per_minute": 60,
      "requests_per_hour": 1000
    },
    "allowed_networks": ["192.168.0.0/16", "10.0.0.0/8"],
    "log_level": "INFO"
  }
}
```