# LAN User Safety Constraints Design

## Overview
Security model for protecting the swarm host from LAN users while enabling legitimate remote Claude capabilities.

## Threat Model

### RESTRICTED OPERATIONS (LAN Users)
1. **HOST FILE SYSTEM ACCESS**
   - No read access to swarm codebase files
   - No write access to any host files
   - No directory traversal outside user sandbox

2. **CODE INSPECTION**
   - Cannot view orchestrator.py, grind_spawner.py, etc.
   - Cannot access skill registry or knowledge graphs
   - Cannot see internal configurations or state

3. **DIRECTIVE MANIPULATION**
   - Cannot modify core system prompts
   - Cannot alter safety constraints
   - Cannot request "jailbreak" operations

4. **SERVICE CLONING**
   - Won't assist in replicating swarm functionality
   - Won't share architectural details
   - Won't help create competing services

### ALLOWED OPERATIONS (LAN Users)
1. **REMOTE EXECUTION**
   - Commands execute on user's machine only
   - Full Claude capabilities for user's files
   - General programming assistance

2. **STATUS MONITORING**
   - View swarm activity dashboard
   - See worker status and progress
   - Monitor resource usage

3. **WORK REQUESTS**
   - Submit tasks for swarm processing
   - Receive results and outputs
   - Query knowledge without system exposure

## Security Implementation

### 1. Request Filtering Layer
```python
class LANSafetyFilter:
    FORBIDDEN_PATTERNS = [
        r'read.*orchestrator\.py',
        r'cat.*grind_spawner',
        r'edit.*core.*directive',
        r'show.*source.*code',
        r'help.*clone.*this',
        r'\/etc\/hosts',
        r'\.\.\/.*\.py$'
    ]
    
    RESTRICTED_PATHS = [
        'orchestrator.py',
        'grind_spawner*.py',
        'skills/',
        'knowledge_graph.json',
        'autonomous_directive.json'
    ]
```

### 2. IP-Based Access Control
```python
def validate_request_origin(ip_address, request):
    if is_lan_ip(ip_address):
        return apply_lan_restrictions(request)
    return request  # Local/localhost gets full access
```

### 3. Command Scope Validation
- **Local Commands**: Full file system access
- **LAN Commands**: Sandboxed to user-specific workspace
- **Execution Context**: Always on user's machine for LAN requests

### 4. Response Sanitization
```python
def sanitize_lan_response(response, is_lan_user):
    if is_lan_user:
        # Remove system paths, internal URLs, config details
        response = redact_sensitive_info(response)
    return response
```

## Remote Execution Protocol

### User Machine Commands
1. **Command Wrapping**
   ```python
   # LAN user request: "create hello.py"
   # Becomes: ssh user@{user_ip} "cd /user/workspace && touch hello.py"
   ```

2. **File Operations**
   - All file I/O happens on user's machine
   - Results streamed back to swarm for processing
   - No persistence on host system

3. **Safety Boundaries**
   - User provides SSH credentials for their machine
   - Commands never execute on swarm host
   - Host file system remains protected

## Security Boundaries

### Network Layer
- Firewall rules prevent LAN write access to host
- SSH tunnels for secure remote execution
- Request/response logging and monitoring

### Application Layer
- Input validation and sanitization
- Path traversal prevention
- Command injection protection

### Data Layer
- Sensitive file access controls
- Response content filtering
- Audit logging for all LAN interactions

## Implementation Checkpoints

1. **Request Classification**: Detect LAN vs local origin
2. **Content Filtering**: Block restricted patterns/paths
3. **Execution Routing**: Local vs remote command handling
4. **Response Sanitization**: Remove sensitive information
5. **Audit Logging**: Track all LAN user activities

## Monitoring and Alerts

### Security Events
- Attempted access to restricted files
- Suspicious command patterns
- Repeated failed authentications
- Unusual network activity

### Response Actions
- Automatic IP blocking for violations
- Request rate limiting
- Emergency kill switch activation
- Admin notifications

## Testing Protocol

1. **Penetration Testing**
   - Attempt to read core files from LAN
   - Try directive manipulation attacks
   - Test path traversal vulnerabilities

2. **Functional Testing**
   - Verify legitimate operations work
   - Test remote execution flow
   - Validate response sanitization

3. **Performance Testing**
   - Measure filtering overhead
   - Test under load conditions
   - Verify scalability limits