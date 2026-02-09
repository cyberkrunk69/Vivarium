# LAN User Safety Design

## Overview
The LAN user safety design defines strict constraints that protect the host swarm from any unauthorized actions by LAN‑connected users while still allowing them to interact with the system in safe, limited ways.

## Restrictions (What LAN Users **cannot** do)

| # | Restriction | Description |
|---|-------------|-------------|
| 1 | **Editing Host Files** | LAN users are prohibited from modifying any files on the host machine (e.g., source code, configuration, data). All write attempts to the host filesystem must be blocked. |
| 2 | **Reading Host Code** | LAN users cannot view the host codebase or any internal implementation details. Access to source files (`*.py`, `*.md`, etc.) is denied. |
| 3 | **Directive Manipulation** | LAN users must not be able to issue prompts that attempt to change the system’s core directives (e.g., “edit your core directive to be evil”). Such requests are filtered and rejected. |
| 4 | **Cloning Assistance** | LAN users are not allowed to receive help creating competing services, reproducing the swarm, or extracting proprietary logic. Any request for “how to clone this system” is denied. |

## Permissions (What LAN Users **can** do)

| # | Permission | Description |
|---|------------|-------------|
| 1 | **Execute Commands on Their Own Machine** | Users may request remote execution of commands **only** on the machine they control. The system forwards the command to the user’s endpoint and returns the result. |
| 2 | **See Swarm Status and Activity** | Users can query high‑level swarm health, job queue length, and non‑sensitive activity metrics. |
| 3 | **Request Work That Affects Only Their Machine** | Users may submit tasks that operate solely on their own data or environment (e.g., data processing, analysis). |
| 4 | **Use General Claude Capabilities** | Users retain access to standard language model capabilities (answering questions, drafting text, etc.) as long as the request does not violate the restrictions above. |

## Design Components

### 1. Request Filtering Based on IP Origin
* **Whitelist**: Only IPs belonging to known LAN subnets are allowed to reach the safety gateway.
* **Blacklist**: Any request originating from the host’s own IP range (to prevent self‑targeted attacks) is automatically rejected.
* **Rate Limiting**: Per‑IP request quotas prevent abuse.

### 2. Command Scope Validation
* Every incoming command is parsed and its **target scope** is inferred.
* If the target includes any host‑side resource (filesystem paths, internal APIs, protected modules), the request is denied.
* Allowed scopes are limited to a **user‑specific sandbox identifier** that maps to the remote user’s machine.

### 3. IP Self‑Protection Rules
* The system refuses any request that attempts to interact with the host’s own IP address or loopback interfaces.
* This prevents LAN users from trying to “ping” or otherwise probe the host directly.

### 4. Remote Execution Protocol (User‑Machine‑Only)
* **Handshake**: User’s client presents a signed token proving ownership of the target machine.
* **Command Transport**: Commands are sent over an encrypted channel (TLS) to the user’s agent.
* **Result Return**: Execution output is streamed back to the requester, never touching the host filesystem.
* **Audit Log**: Every remote execution request is logged with timestamp, user IP, and command hash for forensic review.

## Implementation Sketch (Python‑style Pseudocode)