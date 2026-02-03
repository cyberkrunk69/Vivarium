# Remote Execution Protocol

## Overview
Allows LAN users to execute commands on their own machines through the swarm host. When a user connects from their device and asks Claude to perform actions like "open my browser", the command executes on the user's machine, not the swarm host.

## Components

### 1. remote_execution_client.py
Runs on user's machine to:
- Connect to swarm via WebSocket
- Authenticate using machine ID + challenge-response
- Execute whitelisted commands safely
- Return results to swarm

**Security Features:**
- Command whitelist per OS (start/open/code/browser commands only)
- 30-second timeout per command
- Home directory execution context
- Machine ID based on MAC address

### 2. remote_execution_relay.py
Runs on swarm host to:
- Accept client connections
- Manage user sessions and machine associations
- Route commands to correct machines
- Handle authentication and response routing

**Key Features:**
- Session-based machine grouping
- Multi-machine command execution
- Automatic cleanup of stale connections
- WebSocket + HTTP API support

## Usage

### Start Relay (on swarm host):
```bash
python remote_execution_relay.py --host 0.0.0.0 --port 8765
```

### Start Client (on user machine):
```bash
python remote_execution_client.py --host SWARM_IP --port 8765
```

### Integration with Swarm:
1. User connects to swarm web interface
2. Swarm creates session and associates with user's machines
3. When user asks "open my browser", swarm routes command to user's machine
4. Client executes `start chrome` (Windows) or `open -a Safari` (Mac)
5. Result returns to swarm and user interface

## Security Model
- Whitelist-only command execution
- Machine identification via MAC address
- Session isolation between users
- Command timeout protection
- Home directory sandboxing