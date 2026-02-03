# DUAL-SERVER ARCHITECTURE DESIGN

## Overview
The system implements a dual-server architecture with clear privilege separation:
- **Admin Server**: Full control interface (localhost only)
- **LAN Server**: Restricted interface for WiFi users

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    LAPTOP (127.0.0.1)                      │
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │  ADMIN SERVER   │    │        CORE SYSTEM              │ │
│  │  Port: 8080     │◄──►│  - grind_spawner.py             │ │
│  │  Bind: 127.0.0.1│    │  - orchestrator.py              │ │
│  │                 │    │  - progress_server.py           │ │
│  │  FULL ACCESS:   │    │  - All experiments/logs         │ │
│  │  • Start/Stop   │    └─────────────────────────────────┘ │
│  │  • Config Edit  │                     ▲                 │
│  │  • Log Access   │                     │                 │
│  │  • Kill Switch  │                     │                 │
│  └─────────────────┘                     │                 │
└───────────────────────────────────────────┼─────────────────┘
                                            │
┌───────────────────────────────────────────┼─────────────────┐
│                    WiFi Network           │                 │
│  ┌─────────────────┐                     │                 │
│  │   LAN SERVER    │                     │                 │
│  │   Port: 8081    │◄────────────────────┘                 │
│  │   Bind: 0.0.0.0 │                                       │
│  │                 │    ┌─────────────────────────────────┐ │
│  │  LIMITED ACCESS:│    │      SAFETY GATEWAY             │ │
│  │  • View Status  │◄──►│  - Input sanitization          │ │
│  │  • Read Logs    │    │  - Rate limiting                │ │
│  │  • Basic Stats  │    │  - IP whitelist/blacklist       │ │
│  │  • Emergency    │    │  - Session tracking             │ │
│  │    Stop Only    │    │  - Command validation           │ │
│  └─────────────────┘    └─────────────────────────────────┘ │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ WiFi Device │  │ WiFi Device │  │ WiFi Device │        │
│  │ (Phone)     │  │ (Tablet)    │  │ (Laptop)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Security Model

### Admin Server (127.0.0.1:8080)
- **Access**: Local machine only
- **Authentication**: None required (localhost trust)
- **Privileges**: FULL SYSTEM CONTROL
- **Binding**: Explicitly bound to 127.0.0.1

### LAN Server (0.0.0.0:8081)
- **Access**: WiFi network devices
- **Authentication**: Session-based tokens
- **Privileges**: READ-ONLY + Emergency stop
- **Binding**: All interfaces with safety gateway

### Security Layers
1. **Network Isolation**: Admin server unreachable from network
2. **API Filtering**: LAN server blocks dangerous endpoints
3. **Input Validation**: All LAN inputs sanitized
4. **Rate Limiting**: Prevent DoS attacks
5. **Session Tracking**: Monitor connected devices

## API Endpoints

### Admin Server Endpoints
```
GET  /admin/status           - Full system status
GET  /admin/logs             - All log files
GET  /admin/experiments      - Experiment management
POST /admin/start            - Start workers
POST /admin/stop             - Stop workers
POST /admin/config           - Modify configuration
POST /admin/kill-all         - Emergency kill switch
GET  /admin/performance      - Detailed metrics
POST /admin/backup           - Create backups
```

### LAN Server Endpoints
```
GET  /lan/status             - Basic system status (sanitized)
GET  /lan/logs/recent        - Recent logs only (filtered)
GET  /lan/experiments/list   - Experiment names only
GET  /lan/metrics/basic      - Basic performance metrics
POST /lan/emergency-stop     - Emergency stop only
GET  /lan/health             - Simple health check
POST /lan/session/create     - Create session token
GET  /lan/session/validate   - Validate session
```

## Session Management Design

### Session Structure
```json
{
  "session_id": "uuid-v4",
  "device_ip": "192.168.1.xxx",
  "device_info": "User-Agent string",
  "created_at": "2026-02-03T10:22:25Z",
  "last_access": "2026-02-03T10:22:25Z",
  "permissions": ["view_status", "view_logs", "emergency_stop"],
  "rate_limit": {
    "requests_per_minute": 30,
    "current_count": 0,
    "window_start": "2026-02-03T10:22:25Z"
  }
}
```

### Session Lifecycle
1. **Creation**: Device connects → Session created with IP tracking
2. **Validation**: Each request validates session + IP match
3. **Rate Limiting**: Track requests per session per minute
4. **Expiration**: Sessions expire after 1 hour of inactivity
5. **Cleanup**: Periodic cleanup of expired sessions

### Device Tracking
- IP address logging
- User-Agent fingerprinting
- Connection timestamp tracking
- Request pattern analysis
- Automatic session termination for suspicious activity

## Implementation Notes

### Server Binding
- Admin: `app.run(host='127.0.0.1', port=8080)`
- LAN: `app.run(host='0.0.0.0', port=8081)`

### Safety Gateway Middleware
- Input sanitization for all LAN requests
- Command validation against whitelist
- Automatic request blocking for dangerous patterns
- IP-based access control

### Emergency Protocols
- LAN users can trigger emergency stop only
- Admin server has full kill switch capabilities
- Both servers log all security events
- Automatic lockdown on security violations