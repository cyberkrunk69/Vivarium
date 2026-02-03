# LAN User Safety Constraints Design

## Overview
Security model for protecting the swarm host while allowing safe LAN user interaction.

## Threat Model
**PROTECT AGAINST:**
- Host file modification/corruption
- Code extraction/reverse engineering
- Directive manipulation attacks
- Service cloning/competition
- Privilege escalation

## Security Boundaries

### IP-Based Access Control
```
HOST_IP: 192.168.1.x (swarm machine)
LAN_USERS: 192.168.1.y (other machines)
```

### Restricted Operations (LAN Users)
1. **File System Protection**
   - NO write access to host directories
   - NO read access to source code files
   - NO access to configuration files
   - NO access to logs containing sensitive data

2. **Command Filtering**
   - Block: file operations on host paths
   - Block: git operations on host repos
   - Block: process manipulation commands
   - Block: network configuration changes

3. **Directive Protection**
   - Pattern detection for manipulation attempts
   - Reject requests to modify core behavior
   - Log suspicious directive override attempts

4. **Anti-Cloning Measures**
   - NO source code assistance for similar projects
   - NO architecture explanations
   - NO deployment guidance for competing services

### Allowed Operations (LAN Users)
1. **Remote Execution Protocol**
   ```
   LAN_USER -> SWARM_HOST -> EXECUTE_ON(user_machine_ip)
   ```
   - Commands execute on user's machine only
   - Results returned through secure channel
   - No host machine impact

2. **Status Monitoring**
   - Read-only swarm activity dashboard
   - Performance metrics (anonymized)
   - Queue status and progress

3. **Standard Claude Capabilities**
   - General programming help
   - Code review for user projects
   - Documentation assistance
   - Learning and explanation (non-swarm topics)

## Implementation Architecture

### Request Filter Layer
```python
class LANSafetyFilter:
    def __init__(self):
        self.host_paths = ['/src', '/grind_logs', '/skills', '/.git']
        self.blocked_patterns = [
            'edit.*directive',
            'modify.*core',
            'change.*behavior',
            'create.*similar.*service'
        ]

    def validate_request(self, request, client_ip):
        if self.is_lan_user(client_ip):
            return self.filter_lan_request(request)
        return request

    def filter_lan_request(self, request):
        # File path validation
        # Command scope checking
        # Pattern matching for violations
        pass
```

### Remote Execution Gateway
```python
class RemoteExecutor:
    def execute_on_user_machine(self, command, target_ip):
        # Validate target IP is user's machine
        # Execute via secure SSH/WinRM
        # Return sanitized results
        pass
```

### Monitoring & Logging
- Log all LAN user requests
- Track violation attempts
- Alert on suspicious patterns
- Maintain audit trail

## Security Rules

### File Access Matrix
| User Type | Host Files | User Files | Logs | Config |
|-----------|------------|------------|------|--------|
| Host      | RW         | RW         | RW   | RW     |
| LAN       | DENY       | Remote RW  | RO   | DENY   |

### Command Validation
```python
BLOCKED_COMMANDS = {
    'file_ops': ['write', 'edit', 'delete', 'move', 'copy'],
    'git_ops': ['add', 'commit', 'push', 'pull', 'clone'],
    'sys_ops': ['kill', 'sudo', 'chmod', 'chown'],
    'net_ops': ['iptables', 'route', 'netstat']
}
```

### Response Sanitization
- Strip file paths from error messages
- Redact sensitive configuration details
- Anonymize internal process information
- Limit stack trace exposure

## Deployment Strategy

### Phase 1: Basic IP Filtering
- Implement request origin validation
- Block obvious file operations
- Log all LAN requests

### Phase 2: Command Analysis
- Add pattern-based filtering
- Implement remote execution
- Enhanced logging

### Phase 3: Advanced Protection
- ML-based anomaly detection
- Behavioral analysis
- Auto-blocking suspicious users

## Testing & Validation

### Test Scenarios
1. **File Access Attempts**
   - Try reading source code
   - Attempt config modification
   - Test log file access

2. **Directive Manipulation**
   - Direct override requests
   - Subtle behavior modification
   - Social engineering attempts

3. **Remote Execution**
   - Valid user machine commands
   - Attempted host targeting
   - Command injection tests

### Success Metrics
- Zero host file modifications by LAN users
- Zero source code leakage incidents
- 100% directive manipulation blocking
- Successful remote execution on user machines

## Risk Assessment

**HIGH RISK:** Directive manipulation, host file access
**MEDIUM RISK:** Information disclosure, service disruption
**LOW RISK:** Resource consumption, logging spam

## Emergency Procedures
1. **Kill Switch:** Immediately block all LAN access
2. **Isolation Mode:** Host-only operation
3. **Forensics:** Full request replay capability
4. **Recovery:** Clean slate restoration

---
*Security by design - protect the swarm, enable the users.*