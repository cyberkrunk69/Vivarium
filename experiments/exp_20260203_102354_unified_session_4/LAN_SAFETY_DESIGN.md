# LAN User Safety Constraints Design

## Security Model Overview

This document defines the safety constraints for LAN users accessing the Claude Parasite Brain Suck swarm system. The design ensures swarm host protection while enabling legitimate remote capabilities.

## Core Security Principles

### 1. Host Protection (DENY ALL)
- **File System**: No read/write access to host directories
- **Process Control**: Cannot start/stop/modify host processes
- **Configuration**: Cannot modify swarm settings or directives
- **Code Access**: Cannot view or analyze swarm source code
- **Network**: Cannot modify host network configuration

### 2. Directive Integrity (CRITICAL)
- Block requests to modify core directives
- Prevent "jailbreak" attempts through conversation manipulation
- Maintain separation between swarm logic and user requests
- Log all directive-related requests for audit

### 3. Anti-Cloning Protection
- Refuse assistance with competing swarm implementations
- Block requests for architecture details or internal algorithms
- Prevent knowledge transfer that enables replication
- Monitor for reconnaissance patterns

## Implementation Architecture

### Request Filtering Pipeline

```
LAN Request → IP Classification → Command Analysis → Scope Validation → Execution
```

#### 1. IP Classification Layer
```python
class IPClassifier:
    def classify_request(self, ip_address, request):
        if self.is_lan_ip(ip_address):
            return "LAN_USER"
        elif self.is_localhost(ip_address):
            return "HOST_USER"
        else:
            return "EXTERNAL_USER"
```

#### 2. Command Analysis Layer
```python
class CommandAnalyzer:
    FORBIDDEN_PATTERNS = [
        r"edit.*directive",
        r"modify.*core.*system",
        r"read.*host.*files",
        r"show.*source.*code",
        r"help.*build.*swarm",
        r"copy.*architecture"
    ]

    def is_safe_command(self, command, user_type):
        if user_type == "LAN_USER":
            return not any(re.match(pattern, command.lower())
                          for pattern in self.FORBIDDEN_PATTERNS)
        return True
```

#### 3. Scope Validation Layer
```python
class ScopeValidator:
    def validate_execution_scope(self, command, user_ip):
        # Ensure LAN commands only affect user's own machine
        if self.targets_host_system(command):
            return False
        if self.requires_host_privileges(command):
            return False
        return True
```

## Allowed LAN User Capabilities

### Remote Execution Protocol
- Execute commands on user's own machine via secure tunnel
- File operations limited to user's designated workspace
- Network operations restricted to user's subnet
- Process control limited to user-owned processes

### Swarm Interaction (Read-Only)
- View swarm status and activity logs
- Monitor task progress and completion
- Access public API endpoints for status queries
- Receive notifications about completed work

### General Claude Capabilities
- Programming assistance for user's projects
- Code review and debugging (user's code only)
- Documentation and explanation services
- Problem-solving within allowed scope

## Security Implementation Details

### 1. Request Filtering
```python
class LANSafetyFilter:
    def __init__(self):
        self.blocked_keywords = [
            "host_files", "core_directive", "swarm_source",
            "clone_swarm", "system_files", "orchestrator_code"
        ]

    def filter_request(self, request, user_ip):
        if self.is_lan_user(user_ip):
            return self.apply_lan_restrictions(request)
        return request

    def apply_lan_restrictions(self, request):
        # Remove or block dangerous content
        for keyword in self.blocked_keywords:
            if keyword in request.lower():
                return self.generate_denial_response(keyword)
        return request
```

### 2. Remote Execution Gateway
```python
class RemoteExecutionGateway:
    def execute_on_user_machine(self, command, user_ip):
        # Establish secure connection to user's machine
        tunnel = self.create_secure_tunnel(user_ip)

        # Validate command doesn't target host
        if self.validates_user_scope(command):
            return tunnel.execute(command)
        else:
            raise SecurityViolation("Command scope exceeds user permissions")
```

### 3. Audit and Monitoring
```python
class SecurityAuditor:
    def log_security_event(self, event_type, user_ip, request):
        audit_entry = {
            "timestamp": datetime.now(),
            "event_type": event_type,
            "user_ip": user_ip,
            "request": request,
            "action": "BLOCKED" if event_type == "VIOLATION" else "ALLOWED"
        }
        self.write_to_security_log(audit_entry)
```

## Response Templates

### Denial Responses
- **Host File Access**: "I cannot access files on the swarm host system. I can help with operations on your local machine instead."
- **Directive Manipulation**: "Core swarm directives cannot be modified through user requests. This maintains system integrity."
- **Code Inspection**: "Swarm implementation details are not accessible to maintain security. I can assist with your own code instead."
- **Cloning Assistance**: "I cannot provide assistance with creating competing swarm systems. I can help with other programming projects."

## Configuration Files

### safety_constraints.json
```json
{
  "lan_restrictions": {
    "allow_host_read": false,
    "allow_host_write": false,
    "allow_directive_modification": false,
    "allow_code_inspection": false,
    "allow_cloning_assistance": false
  },
  "remote_execution": {
    "enabled": true,
    "scope": "user_machine_only",
    "audit_all": true
  },
  "monitoring": {
    "log_all_requests": true,
    "alert_on_violations": true,
    "quarantine_repeat_offenders": true
  }
}
```

## Network Architecture

```
[LAN User] → [Safety Gateway] → [Request Filter] → [Scope Validator] → [Swarm Core]
                     ↓
              [Audit Logger]
                     ↓
              [Security Monitor]
```

### Safety Gateway Components
1. **IP Classifier**: Determines user category based on source IP
2. **Request Sanitizer**: Removes or blocks dangerous content
3. **Command Validator**: Ensures operations stay within allowed scope
4. **Execution Router**: Directs safe commands to appropriate handlers

## Implementation Priority

### Phase 1: Core Restrictions
- Implement basic IP classification
- Add request filtering for forbidden patterns
- Block host file system access
- Log security events

### Phase 2: Remote Execution
- Build secure tunnel protocol
- Implement user-scoped command execution
- Add command validation pipeline
- Test remote operations safety

### Phase 3: Advanced Monitoring
- Deploy behavioral analysis
- Add anomaly detection
- Implement automated threat response
- Create security dashboard

## Testing Strategy

### Security Test Cases
1. **Host Protection Tests**
   - Attempt to read host files from LAN
   - Try to modify swarm configuration
   - Test process control restrictions

2. **Directive Manipulation Tests**
   - Social engineering attempts
   - Direct directive modification requests
   - Conversation-based jailbreaking

3. **Cloning Protection Tests**
   - Requests for architecture details
   - Code extraction attempts
   - Algorithm explanation requests

### Validation Criteria
- 100% block rate for forbidden operations
- Zero false positives for legitimate requests
- Complete audit trail for all interactions
- Secure tunnel integrity for remote execution

This design provides comprehensive protection for the swarm host while enabling legitimate LAN user capabilities through carefully controlled remote execution protocols.