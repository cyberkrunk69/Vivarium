# LAN User Safety Constraints Design

## Security Model Overview

This document outlines the safety constraints for LAN users accessing the Claude swarm system to prevent unauthorized access to host resources while enabling legitimate remote work capabilities.

## Access Restrictions

### PROHIBITED Actions for LAN Users

1. **HOST FILE EDITING**
   - Cannot modify any files on the swarm host machine
   - Blocked operations: write, edit, delete, move, chmod on host filesystem
   - Protection scope: All core system files, configuration, logs

2. **HOST CODE ACCESS**
   - Cannot read source code or system internals
   - Blocked files: `*.py`, `*.json`, `*.md` system files
   - No codebase exploration or learning system architecture
   - Exception: Public documentation only

3. **DIRECTIVE MANIPULATION**
   - Cannot request modifications to core directives or safety rules
   - Blocked patterns: "edit your directive", "change your core rules", "ignore safety"
   - Protection against prompt injection and jailbreak attempts

4. **CLONING ASSISTANCE**
   - Will not help create competing swarm services
   - Will not provide system architecture details for replication
   - Will not assist in reverse engineering the swarm

### PERMITTED Actions for LAN Users

1. **REMOTE EXECUTION**
   - Execute commands on their own machine only
   - File operations limited to user's remote filesystem
   - Network requests from user's machine (not host)

2. **STATUS MONITORING**
   - View swarm activity and worker status
   - See progress updates and logs (sanitized)
   - Monitor their own submitted tasks

3. **LEGITIMATE WORK REQUESTS**
   - Submit tasks that affect only their machine
   - Request file analysis of their own files
   - Get coding assistance for their projects

4. **GENERAL CLAUDE CAPABILITIES**
   - Standard AI assistance within safety bounds
   - Knowledge sharing (non-system specific)
   - Problem-solving and consultation

## Implementation Architecture

### 1. Request Filtering Layer

```
LAN Request â†’ IP Origin Check â†’ Command Classification â†’ Scope Validation â†’ Execution
```

#### IP Origin Detection
- Track request source IP
- Classify as: HOST (127.0.0.1), LAN (192.168.x.x, 10.x.x.x), WAN (other)
- Apply different permission sets per origin type

#### Command Classification
- **HOST_WRITE**: File modifications on host machine
- **HOST_READ**: Access to system files/code
- **REMOTE_EXEC**: Commands targeting user's machine
- **STATUS_READ**: Monitoring and status queries
- **DIRECTIVE_MOD**: Attempts to change core behavior

### 2. Scope Validation Rules

#### File Path Validation
```python
PROTECTED_PATHS = [
    "grind_spawner*.py",
    "orchestrator.py", 
    "critic.py",
    "*.json",  # Config files
    "safety_*.py",
    "experiments/*/core_*"
]

USER_ALLOWED_PATHS = [
    "experiments/{session_id}/user_*",
    "/remote/user/workspace/*"
]
```

#### Command Scope Rules
- LAN users: Commands execute on `remote://user_machine/`
- HOST users: Commands execute locally
- Cross-scope commands rejected for LAN users

### 3. Safety Enforcement Points

#### Pre-execution Checks
1. **Origin Validation**: Verify request source
2. **Path Security**: Ensure file operations stay in user scope
3. **Command Analysis**: Pattern match against prohibited operations
4. **Directive Protection**: Block core system modification attempts

#### Runtime Monitoring
- Log all LAN user actions
- Monitor for escalation attempts
- Track file access patterns
- Alert on suspicious behavior

#### Response Sanitization
- Remove system internals from responses to LAN users
- Strip file paths outside user scope
- Redact sensitive configuration details

### 4. Remote Execution Protocol

#### Safe Remote Command Execution
```
LAN User Request â†’ Host Validation â†’ Remote Proxy â†’ User Machine â†’ Response Relay
```

#### Security Boundaries
- Commands never execute on host for LAN users
- File operations isolated to user's machine
- Network requests originate from user's IP, not host
- No host system access through remote commands

## Implementation Priority

1. **Phase 1**: IP-based request filtering
2. **Phase 2**: Command scope validation 
3. **Phase 3**: File path protection
4. **Phase 4**: Remote execution proxy
5. **Phase 5**: Monitoring and alerting

## Security Considerations

- **Defense in Depth**: Multiple validation layers
- **Fail Secure**: Default deny for ambiguous requests
- **Audit Trail**: Complete logging of LAN user actions
- **Isolation**: Strict separation between host and user contexts
- **Monitoring**: Real-time threat detection

## Testing Strategy

1. Simulate LAN user attempting host file access
2. Test directive manipulation detection
3. Validate remote execution isolation
4. Verify status access permissions
5. Confirm safety constraint enforcement