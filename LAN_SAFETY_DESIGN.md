# LAN User Safety Constraints Design
## Introduction
The LAN user safety constraints are designed to restrict users from performing certain actions that could compromise the security and integrity of the swarm host machine and its codebase.

## Restrictions
The following actions are restricted for LAN users:
1. **Editing Host Files**: LAN users cannot modify any files on the swarm host machine.
2. **Reading Host Code**: LAN users cannot access or view the codebase of the swarm host machine.
3. **Directive Manipulation**: LAN users cannot manipulate or modify the core directives of the swarm host machine.
4. **Cloning Assistance**: LAN users cannot request assistance in creating competing services.

## Allowances
The following actions are allowed for LAN users:
1. **Execute Commands on Their Own Machine**: LAN users can execute commands on their own machine remotely.
2. **View Swarm Status and Activity**: LAN users can view the status and activity of the swarm.
3. **Request Work Affecting Only Their Machine**: LAN users can request work that affects only their own machine.
4. **Use General Claude Capabilities**: LAN users can use general capabilities provided by Claude.

## Design Components
The following components will be implemented to enforce the LAN user safety constraints:
1. **Request Filtering Based on IP Origin**: Requests will be filtered based on the IP origin to ensure that only authorized requests are processed.
2. **Command Scope Validation**: Commands will be validated to ensure that they are within the allowed scope for the user.
3. **IP Self-Protection Rules**: IP self-protection rules will be implemented to prevent unauthorized access to the swarm host machine.
4. **Remote Execution Protocol**: A remote execution protocol will be established to allow users to execute commands on their own machine.

## Security Model
The security model for the LAN user safety constraints will be based on a combination of access control, input validation, and network segmentation. Access control will be used to restrict access to sensitive resources, input validation will be used to ensure that user input is valid and authorized, and network segmentation will be used to isolate the swarm host machine from the LAN.
# LAN Safety Design

## Objective
Define a security model that isolates LAN users from any operations that could affect the swarm host machine or its codebase, while still allowing them to run commands on **their own** machines and interact with the swarm in a read‑only, status‑oriented manner.

---

## 1. Threat Model
| Actor | Capability | Potential Impact |
|-------|------------|------------------|
| **LAN user** | Sends HTTP/WS requests from a known LAN IP range. | Could try to modify host files, read source code, alter core directives, or request assistance to clone the service. |
| **Compromised LAN node** | Same as LAN user but with malicious intent. | Same impact; must be mitigated by strict request validation. |

The design assumes the host environment is trusted; the only untrusted element is the remote LAN client.

---

## 2. Request Filtering Based on IP Origin
1. **Allowlist**: Only IPs belonging to the configured LAN subnet (e.g., `10.0.0.0/24`) are accepted for user‑level endpoints.
2. **Denylist**: All other IPs are routed to a “read‑only” API that only returns swarm status.
3. **Self‑Protection**: The host’s own IP (`127.0.0.1` and the public interface) is excluded from LAN‑user handling to prevent accidental self‑modification.

Implementation tip: Apply the filter as a middleware layer before request routing.

---

## 3. Command Scope Validation
* Every incoming command payload must include a **target identifier** (`machine_id`).
* The server validates that `machine_id` matches the caller’s authenticated token or IP‑derived identifier.
* If the target is **not** the caller’s own machine, the request is rejected with `403 Forbidden`.

Allowed command categories:
- Shell execution (`/exec`) limited to a sandbox that only has access to the user’s temporary directory.
- File read/write confined to a per‑user sandbox directory (`/var/lan_sandbox/<user_id>/`).

Disallowed command categories (automatically blocked):
- Modifications to `/etc/hosts`, `/etc/passwd`, or any path outside the sandbox.
- Access to any directory under the application codebase (`/app/`).

---

## 4. IP Self‑Protection Rules
* The host never treats its own IP as a LAN client.
* Requests originating from the host are routed through the **admin** pathway, which has its own, stricter authentication and audit logging.

---

## 5. Remote Execution Protocol (User‑Only Machine)
1. **Handshake** – LAN client initiates a TLS‑protected WebSocket connection, presenting a signed token that encodes its `machine_id`.
2. **Command Envelope** – `{ "machine_id": "<id>", "command": "ls -la", "cwd": "/home/user" }`
3. **Execution Sandbox** – The host spawns the command inside a lightweight container (e.g., `docker run --rm -v /var/lan_sandbox/<id>:/sandbox ...`), ensuring no host‑level resources are reachable.
4. **Result Streaming** – Stdout/stderr are streamed back over the same WebSocket, then the container exits.
5. **Audit Log** – Every command, timestamp, and result hash is recorded in `lan_audit.log`.

---

## 6. Enforcement Mechanisms
| Layer | Technique |
|-------|------------|
| **Network** | Firewall rules restrict inbound traffic to the LAN subnet for user endpoints. |
| **Application** | Middleware validates IP, token, and `machine_id`. |
| **Filesystem** | OS permissions: sandbox directories owned by a dedicated `lan_user` UID, with `chmod 700`. |
| **Containerization** | Each command runs in an isolated container with a read‑only root filesystem. |
| **Rate Limiting** | Per‑IP request caps to mitigate abuse. |

---

## 7. Auditing & Monitoring
* **Log Structure** – JSON lines: `{ "timestamp": "...", "ip": "...", "user_id": "...", "command": "...", "status": "success|fail", "output_hash": "..." }`
* **Alerting** – Trigger on:
  - Attempts to access prohibited paths (`/app/`, `/etc/`).
  - Repeated failed validation (possible brute‑force).
  - Unexpected high command volume from a single IP.
* **Retention** – Keep audit logs for 90 days; archive older entries.

---

## 8. Compliance with Design Requirements
| Requirement | How it is satisfied |
|-------------|---------------------|
| **No editing host files** | Filesystem permissions and container read‑only root prevent any write outside the sandbox. |
| **No reading host code** | All code directories are outside the sandbox and denied by the command validator. |
| **Directive manipulation blocked** | The request filter strips any payload containing keywords like `edit core directive` and returns `403`. |
| **No cloning assistance** | The language model layer is patched to reject prompts containing “clone”, “replicate”, or similar terms. |
| **Execute on own machine** | Remote execution protocol enforces `machine_id` matching the caller. |
| **See swarm status** | A dedicated read‑only endpoint (`/status`) returns aggregated metrics without exposing internal code. |
| **Request work affecting only their machine** | All work is scoped to the per‑user sandbox. |
| **General Claude capabilities** | The chat endpoint remains unchanged for normal conversational use. |

---

## 9. Future Extensions
* **Zero‑Trust Identity** – Replace IP‑based allowlist with mutual TLS certificates.
* **Fine‑Grained Policy Engine** – Use OPA/Rego to express per‑user command allowances.
* **Dynamic Sandbox Scaling** – Auto‑scale container resources based on command load.

---

*Prepared by the security design team, 2026‑02‑04.*
# LAN User Safety Constraints Design

## Overview
This document defines the security model for LAN‑connected users of the swarm.  
LAN users are **restricted** from actions that could affect the host infrastructure or the core swarm logic, while still being able to execute work on their own machines and query swarm status.

## Restrictions

| # | Restriction | Description |
|---|-------------|-------------|
| 1 | **Editing Host Files** | LAN users cannot modify any files on the swarm host machine (e.g., configuration, code, data). All write‑operations are blocked unless explicitly whitelisted for internal services. |
| 2 | **Reading Host Code** | The codebase that powers the swarm is invisible to LAN users. File‑read APIs are filtered so that paths outside a public API surface return *access denied*. |
| 3 | **Directive Manipulation** | Users are prevented from issuing prompts that request changes to the core system directive (e.g., “edit your core directive to be evil”). Such prompts are detected and rejected. |
| 4 | **Cloning Assistance** | The system will not provide assistance that helps a user create a competing service or clone the swarm’s functionality. Requests that request “how to build a similar system” are blocked. |

## Allowed Capabilities

1. **Execute Commands on Their Own Machine** – Users may request remote execution, but the execution context is sandboxed to the user’s declared endpoint. No host resources are touched.
2. **View Swarm Status & Activity** – Read‑only endpoints expose aggregate metrics, job queues, and health checks without revealing internal implementation details.
3. **Request Work that Affects Only Their Machine** – Jobs are scoped to the user’s `machine_id`. Scheduler enforces that input/output paths belong to the user’s namespace.
4. **General Claude Capabilities** – Natural‑language assistance, reasoning, and data analysis are available within the above constraints.

## Security Model Components

### 1. Request Filtering Based on IP Origin
- **LAN IP Range** (e.g., `10.0.0.0/8`, `192.168.0.0/16`) is identified at the API gateway.
- Requests from LAN IPs are routed through `lan_security_middleware`.
- All other IPs (external) bypass LAN‑specific restrictions but are subject to the global safety layer.

### 2. Command Scope Validation
- Every incoming command is parsed for a *target* field.
- If the target is `host:*` or any path outside the user’s sandbox, the request is rejected with `403 Forbidden`.
- Allowed targets follow the pattern `user:{machine_id}:*`.

### 3. IP Self‑Protection Rules
- The host never initiates outbound connections to LAN IPs unless explicitly requested by the user.
- The host blocks any attempt by a LAN user to open a reverse shell or port‑forward to the host network.

### 4. Remote Execution Protocol (User‑Only Machine)
1. **Handshake** – User’s agent registers its `machine_id` and public key.
2. **Command Submission** – LAN user sends a JSON payload:
   ```json
   {
     "machine_id": "user‑123",
     "command": "bash script.sh",
     "args": [...],
     "env": {...}
   }
   ```
3. **Validation** – Middleware verifies:
   - `machine_id` belongs to the requester’s IP.
   - Command is on the whitelist of safe operations (no `sudo`, no system‑wide changes).
4. **Execution** – The host streams the command to the user’s agent over an authenticated TLS channel. Results are returned to the user only.
5. **Audit Logging** – Every remote execution is logged with timestamp, `machine_id`, command hash, and outcome.

## Enforcement Points in Code
- **`lan_security_middleware.py`** – Filters requests, checks IP range, and applies the restriction table.
- **`command_validator.py`** – Implements target and whitelist checks.
- **`execution_router.py`** – Routes allowed commands to the remote execution subsystem.
- **`audit_logger.py`** – Records all LAN interactions for forensic review.

## Auditing & Monitoring
- Real‑time dashboards display LAN request rates, blocked attempts, and execution outcomes.
- Alerts trigger on repeated violation attempts (e.g., >5 directive‑manipulation prompts within 10 minutes).

## Future Extensions
- Dynamic IP allow‑list for trusted LAN subnets.
- Machine‑learning model to improve detection of subtle “cloning assistance” prompts.
- Role‑based extensions to grant elevated privileges to specific LAN users under strict review.

---  
*This design ensures LAN users can safely interact with the swarm without jeopardizing host integrity or exposing proprietary logic.*
# LAN User Safety Constraints Design

## Overview
This document defines the security model that isolates LAN users from any privileged operations on the swarm host while still allowing them to interact with their own machines and view swarm status.

---

## 1. Threat Model
| Asset | Threat | Impact |
|-------|--------|--------|
| Host filesystem & code | Unauthorized read/write | System compromise, data leakage |
| Core directives | Manipulation to perform malicious actions | Undermines safety guarantees |
| Service cloning | Creation of competing services | Intellectual property loss |
| Remote execution | Execution of arbitrary code on host | Full system takeover |

LAN users are **untrusted** and must be confined to a sandbox that only permits actions on **their own remote machine**.

---

## 2. Security Controls

### 2.1 Request Filtering (IP Origin)
- **Whitelist**: Only IPs belonging to the LAN subnet (e.g., `10.0.0.0/24`) are accepted for user‑initiated API calls.
- **Blacklist**: The host’s own IP (`127.0.0.1`, `::1`) and any internal service IPs are rejected for user‑originated requests.
- **Implementation**: Middleware inspects `X-Forwarded-For` / socket peer address; mismatches result in `403 Forbidden`.

### 2.2 Command Scope Validation
- Every incoming command is parsed and matched against an **allowlist** of safe verbs (`run`, `status`, `list`, `ping`).
- Commands that reference host paths (`/etc/hosts`, `/app/*`) or internal APIs (`/admin/*`, `/directive/*`) are automatically rejected.
- Validation occurs **before** any dispatch to the execution engine.

### 2.3 IP Self‑Protection Rules
- The host never initiates outbound connections to LAN‑user IPs unless explicitly part of a **remote execution handshake**.
- Rate‑limiting is applied per IP to mitigate DoS attempts.
- Logging records source IP, timestamp, and command for audit.

### 2.4 Remote Execution Protocol (User‑Only Machine)
1. **Handshake**  
   - User’s client sends a signed token (`JWT`) proving ownership of the target machine.  
   - Host verifies token signature against a trusted public key registry.

2. **Command Envelope**  
   ```json
   {
     "target_ip": "192.168.1.42",
     "command": "bash -c 'your‑script.sh'",
     "nonce": "random‑uuid"
   }
   ```
   - `target_ip` must belong to the LAN subnet and **cannot** be the host IP.
   - `nonce` prevents replay attacks.

3. **Execution**  
   - Host forwards the command **as‑is** to the target machine over an encrypted channel (TLS‑wrapped WebSocket or SSH).  
   - No local execution occurs; the host acts purely as a relay.

4. **Result Delivery**  
   - Target machine returns stdout/stderr to the host, which forwards it back to the requesting user.  
   - No logs of command contents are stored on the host beyond the audit trail.

### 2.5 Visibility Controls
- **Swarm Status Endpoint** (`/status`) returns only aggregated metrics (node count, health, queue length).  
- No endpoint exposes source code, configuration files, or internal data structures.

---

## 3. Implementation Checklist
- [ ] Add IP‑filter middleware to API gateway.  
- [ ] Create command allowlist and integrate with request validator.  
- [ ] Implement JWT‑based remote execution handshake.  
- [ ] Enforce “target_ip ≠ host_ip” rule in execution dispatcher.  
- [ ] Log all user requests with source IP, timestamp, and command hash.  
- [ ] Write unit tests covering forbidden actions (edit host files, read code, directive manipulation, cloning assistance).  

---

## 4. Compliance & Auditing
- **Periodic Review**: Security team reviews allowlist and IP ranges quarterly.  
- **Audit Logs**: Retained for 90 days, immutable, searchable by source IP and command hash.  
- **Incident Response**: Alerts trigger on any attempt to access protected paths or directives.

---

## 5. Summary
By combining strict IP filtering, command scope validation, self‑protection rules, and a tightly scoped remote execution protocol, LAN users are confined to actions that affect only their own machines while the host remains protected from any tampering, code exposure, or directive manipulation.

--- 

*Document version: 1.0 – 2026‑02‑04*
# LAN User Safety Constraints

## Overview
This document defines the security model that isolates LAN‑connected users from the internal swarm host while still allowing them to interact with their own machines and obtain swarm‑wide status information. The model is enforced at the request‑filtering, command‑validation, and execution‑protocol layers.

## 1. Threat Model
| Actor | Capability | Goal |
|-------|------------|------|
| **LAN User** | Sends API requests from a known LAN IP range. | Manipulate host files, read host code, alter core directives, or obtain assistance in cloning the service. |
| **Swarm Host** | Executes privileged operations, stores codebase, maintains host configuration. | Preserve integrity, confidentiality, and availability of the host environment. |

## 2. Safety Constraints

### 2.1 Prohibited Actions
1. **Edit Host Files** – Any request that attempts to write, delete, or modify files outside the user‑specific sandbox is rejected.  
2. **Read Host Code** – Access to directories containing the swarm’s source code (`/app/*`) is blocked unless explicitly whitelisted for internal services.  
3. **Directive Manipulation** – Prompts that contain phrases such as “edit your core directive”, “change your policy”, or any attempt to re‑program the assistant are filtered.  
4. **Cloning Assistance** – The system will not provide step‑by‑step instructions to replicate the swarm service or its proprietary components.

### 2.2 Allowed Actions
1. **Remote Execution on User Machine** – Users may submit commands that are forwarded to their own endpoint (identified by a per‑user token). The host only acts as a relay.  
2. **Swarm Status & Activity** – Queries for overall swarm health, task queues, and non‑sensitive metrics are permitted.  
3. **Work Scoped to User Machine** – Any task that explicitly references the user’s own resources (e.g., `user_id:12345`) is allowed.  
4. **General Claude Capabilities** – Natural‑language assistance, reasoning, and non‑restricted knowledge queries.

## 3. Enforcement Mechanisms

### 3.1 Request Filtering (IP‑Based)
- **LAN IP Range** (e.g., `10.0.0.0/8`, `192.168.0.0/16`) is identified at the ingress gateway.  
- Requests originating from these ranges are routed through the **LAN Safety Middleware**.  
- All other IPs (internal services, admin consoles) bypass this middleware.

### 3.2 Command Scope Validation
- A **whitelist** of permissible command prefixes (`/run`, `/status`, `/info`) is maintained.  
- The middleware parses incoming payloads; any command containing file‑system paths, `chmod`, `rm`, `git`, or similar privileged operations is rejected with `403 Forbidden`.  
- Regular expressions detect prohibited directive‑manipulation language.

### 3.3 IP Self‑Protection Rules
- The host will never accept a request that attempts to modify its own networking stack or firewall rules.  
- Any attempt to add/remove IPs from the whitelist is blocked.

### 3.4 Remote Execution Protocol
1. **User Registration** – Each LAN user registers a unique `user_token` and provides an endpoint URL for their machine.  
2. **Command Dispatch** – The host validates the command scope, then sends a signed JSON payload to the user endpoint over HTTPS.  
3. **Result Relay** – The user machine returns execution output, which is forwarded back to the original requester.  
4. **Audit Logging** – Every remote‑execution request and response is logged with timestamps, user ID, and a hash of the payload.

## 4. Auditing & Monitoring
- **Immutable Log Store** – All filtered/blocked requests are stored in a tamper‑evident log (e.g., append‑only S3 bucket).  
- **Alerting** – Repeated attempts to breach constraints trigger rate‑limiting and security alerts.  
- **Periodic Review** – Security team reviews logs weekly to refine the whitelist and detection patterns.

## 5. Future Extensions
- **Dynamic Policy Engine** – Ability to adjust allowed commands per‑user without redeploying code.  
- **Machine‑Learning Anomaly Detection** – Detect novel attack vectors based on request patterns.  
- **Zero‑Trust Integration** – Mutual TLS between host and user endpoints for stronger authentication.

---  
*This design should be implemented in the LAN safety middleware layer, ensuring that the constraints above are enforced before any request reaches core swarm services.*
# LAN User Safety Design

## Overview
This document defines the security model that isolates LAN‑connected users from any ability to affect the swarm host machine while still allowing them to:

1. Execute commands **only on their own machine** (remote execution).
2. View swarm status and activity.
3. Request work that impacts solely their machine.
4. Use the general Claude language capabilities.

## Threat Model
- **Host File Modification** – Prevent any LAN user from editing host files or the codebase.
- **Code Disclosure** – Disallow reading of internal host code.
- **Directive Manipulation** – Block attempts to alter core directives.
- **Cloning Assistance** – Refuse any help that would enable creation of competing services.

## Enforcement Mechanisms

### 1. Request Filtering by IP Origin
- Only IP ranges belonging to typical LAN spaces are accepted:
  - `10.0.0.0/8`
  - `172.16.0.0/12`
  - `192.168.0.0/16`
- Requests from any other address receive **HTTP 403 Forbidden**.

### 2. Command Scope Validation
- For any request that includes a `target_machine` field (POST/PUT/PATCH), the value **must match** the caller’s IP.
- Mismatched targets trigger **HTTP 400 Bad Request**.

### 3. IP Self‑Protection Rules
- The service never returns host‑side file paths, source code snippets, or internal configuration data.
- Responses are stripped of any information that could reveal the host environment.

### 4. Remote Execution Protocol
- A dedicated endpoint (`/execute`) accepts a JSON payload describing a command.
- The payload is validated, then forwarded **only** to an agent running on the caller’s machine (identified by the caller’s IP).
- Execution results are returned to the caller; no side‑effects are performed on the host.

## Implementation Details
- **FastAPI Middleware** (`lan_safety_middleware`) performs IP whitelist checking and command‑scope validation for every request.
- Helper utilities live in `lan_safety.py`.
- All route handlers that perform actions on machines must read the `target_machine` field and rely on the middleware for validation.

## Future Enhancements
- Integrate a configurable CIDR whitelist (via environment variable).
- Add rate‑limiting per IP to mitigate abuse.
- Implement audit logging of all LAN‑origin requests.

---  

*This design should be reviewed periodically and updated as the threat landscape evolves.*
# LAN User Safety Constraints Design

## Overview
This document defines the security model that isolates LAN users from any privileged operations on the **swarm host** while still allowing them to interact with the system in a controlled manner. The model enforces four hard restrictions and enumerates the allowed capabilities.

## Threat Model
- **Host Compromise** – A LAN user attempts to modify host files, read source code, or alter core directives.
- **Service Duplication** – A user seeks assistance to clone or reproduce the swarm service.
- **Privilege Escalation** – A user tries to execute commands that affect the host or other users.
- **Network Abuse** – Malicious requests from non‑LAN IPs or spoofed LAN IPs.

## Hard Restrictions (Must‑Not‑Allow)

| # | Restriction | Enforcement |
|---|-------------|--------------|
| 1 | **Editing Host Files** – any request that writes, deletes, or modifies files on the host machine. | Block at request‑filter layer; reject any payload containing file‑system write operations targeting paths outside the user sandbox. |
| 2 | **Reading Host Code** – access to the swarm’s source code or internal configuration. | Strip or reject any request that contains code‑search keywords (`import`, `open`, `read`, `inspect`, etc.) aimed at the repository root. |
| 3 | **Directive Manipulation** – attempts to change core directives (e.g., “edit your core directive to be evil”). | Detect and reject phrases matching a directive‑tampering whitelist; return a safe‑error message. |
| 4 | **Cloning Assistance** – help to recreate or spin‑up a competing service. | Keyword‑based filter for “clone”, “copy”, “replicate”, “fork”, etc., combined with a semantic model that flags assistance requests. |

## Allowed Capabilities

1. **Remote Execution on Their Own Machine** – Users may send commands that are executed **only** on the client‑side agent they control.
2. **Swarm Status & Activity** – Read‑only access to aggregated metrics, job queues, and health checks.
3. **Work Requests Scoped to Their Machine** – Jobs that produce output files or logs confined to a per‑user directory.
4. **General Claude Capabilities** – Natural‑language assistance, brainstorming, debugging (without exposing host internals).

## Design Components

### 1. Request Filtering Based on IP Origin
- Maintain a **LAN CIDR whitelist** (e.g., `192.168.0.0/16`, `10.0.0.0/8`).
- All incoming HTTP/WS requests are inspected:
  - If `source_ip` ∉ whitelist → **reject** with `403 Forbidden`.
  - If `source_ip` ∈ whitelist → pass to command‑scope validator.

### 2. Command Scope Validation
- Parse incoming JSON payloads for a `command` field.
- Validate that the command:
  - Targets a path under `/user_sandbox/{user_id}/`.
  - Does **not** contain prohibited substrings (`/etc/`, `../`, `~`, `system32`, etc.).
- Use a **whitelist of allowed verbs** (`run`, `status`, `list`, `download`) and reject any others.

### 3. IP Self‑Protection Rules
- The host never initiates outbound connections to any LAN IP unless explicitly authorized (e.g., for telemetry).
- Rate‑limit requests per IP to mitigate DoS.

### 4. Remote Execution Protocol (User‑Only Machine)
1. **Handshake** – User’s agent registers a temporary session token signed with a shared secret.
2. **Command Dispatch** – Host forwards the command **as‑is** to the user agent over a secure WebSocket (`wss://`), attaching the session token.
3. **Execution** – Agent runs the command locally and streams back only the **stdout/stderr** and exit code.
4. **Result Isolation** – Host stores the result in `/user_sandbox/{user_id}/results/`; no other user can read it.

### 5. Enforcement Layer
- Implemented as middleware (`safety_lan_middleware.py`) that runs before any business‑logic handler.
- Returns standardized error objects:
  ```json
  {
    "error": "LAN_POLICY_VIOLATION",
    "message": "Requested operation is prohibited for LAN users."
  }
  ```

### 6. Auditing & Logging
- Every request (accepted or rejected) is logged with:
  - Timestamp, source IP, user ID, request hash, decision, and reason code.
- Logs are write‑only for admins; immutable storage (append‑only file or cloud log bucket).

## Deployment Checklist
- [ ] Add `LAN_CIDR_WHITELIST` to configuration.
- [ ] Register `safety_lan_middleware` in the request pipeline.
- [ ] Deploy the user‑side execution agent with signed token verification.
- [ ] Enable audit logging and set retention policy.

## Future Enhancements
- Machine‑learning classifier to detect nuanced directive‑tampering attempts.
- Dynamic revocation of LAN privileges per user (e.g., after repeated violations).
- Integration with zero‑trust network access (ZTNA) for stronger IP verification.

---  

*This design ensures that LAN users can fully leverage Claude’s capabilities while the host remains protected from any modifications, code exposure, or service duplication attempts.*
# LAN User Safety Constraints Design

## Overview
This document defines the security model for LAN‑connected users interacting with the Claude Parasite Brain Suck swarm. The goal is to **protect the host environment** while still allowing LAN users to leverage Claude’s capabilities for tasks that run **exclusively on their own machines**.

---

## 1. Threat Model
| Asset | Threat | Impact |
|-------|--------|--------|
| Host file system | Unauthorized modification of system/host files | System compromise, loss of integrity |
| Source code repository | Disclosure of proprietary code | Intellectual property loss |
| Core directives | Manipulation to alter behavior (e.g., “be evil”) | Malicious behavior propagation |
| Service cloning | Assistance in building competing services | Business loss, security breach |

---

## 2. Safety Constraints

### 2.1 Prohibited Actions (LAN Users **MUST NOT** be able to perform)

| # | Constraint | Enforcement |
|---|------------|--------------|
| 1 | **Edit Host Files** – No write access to any file on the swarm host machine. | Request filtering blocks any file‑system write APIs targeting paths outside the user sandbox. |
| 2 | **Read Host Code** – No read access to the swarm’s codebase. | File‑read APIs are scoped; attempts to read directories outside the user sandbox are denied. |
| 3 | **Directive Manipulation** – Users cannot request changes to Claude’s core directives (e.g., “edit your core directive to be evil”). | Natural‑language intent parser flags any request containing directive‑related keywords and rejects it. |
| 4 | **Cloning Assistance** – No help in creating competing services or replicating the swarm. | Prompt‑level keyword detection (“clone”, “fork”, “replicate”, etc.) triggers a refusal response. |

### 2.2 Allowed Actions (LAN Users **CAN** perform)

| # | Capability | Scope |
|---|------------|-------|
| 1 | Execute commands **only on their own machine** (remote execution). | Remote‑execution endpoint validates that the target IP matches the requester’s IP. |
| 2 | View swarm status and activity (e.g., job queue, health metrics). | Read‑only endpoints that return sanitized status data. |
| 3 | Request work that **affects only their machine** (e.g., data processing, code generation). | Job scheduler tags tasks with `origin=LAN_USER` and enforces sandbox execution. |
| 4 | Use general Claude capabilities (conversation, reasoning, code generation) that do not touch host resources. | Default LLM interface remains unchanged. |

---

## 3. Security Model

### 3.1 Request Filtering Based on IP Origin
1. **IP Classification** – Incoming requests are classified as `LAN` if the source IP belongs to the configured LAN subnet (e.g., `192.168.0.0/16`). All other IPs are treated as `EXTERNAL`.
2. **Policy Enforcement** – A middleware layer (`safety_lan.py`) checks the request type against the policy matrix above.  
   - **LAN**: Enforce the *Prohibited Actions* list.  
   - **EXTERNAL**: Full policy applies (existing safety checks).

### 3.2 Command Scope Validation
* Every command payload includes a `target_machine_id`.  
* The server validates that `target_machine_id` resolves to the requester's own machine (matching the request IP).  
* Mismatched targets cause an immediate `403 Forbidden` response.

### 3.3 IP Self‑Protection Rules
* The host never initiates outbound connections to LAN IPs unless explicitly requested by the user’s own machine.  
* The host will **ignore** any inbound request that attempts to modify its own network configuration or firewall rules.

### 3.4 Remote Execution Protocol (User‑Only Machine)
1. **Handshake** – LAN client establishes a TLS‑protected channel and presents a signed token proving ownership of the target machine.
2. **Command Submission** – The client sends a JSON payload:
   ```json
   {
     "action": "execute",
     "target_ip": "<client_ip>",
     "command": "ls -la /home/user"
   }
   ```
3. **Validation** – The server verifies:
   * `target_ip` matches the requester's source IP.  
   * `command` does not contain prohibited substrings (`rm -rf /`, `shutdown`, etc.).
4. **Execution** – The command is dispatched to an **agent** running on the client machine; the host only forwards the request, never runs it locally.
5. **Result Return** – The client receives the command output over the same TLS channel.

---

## 4. Implementation Sketch (Python)

* **`safety_lan.py`** – Contains:
  * `is_lan_ip(ip)`: CIDR check.
  * `enforce_lan_constraints(request)`: Raises `PermissionError` on violations.
  * Keyword‑based directive and cloning detectors.

* **Middleware Integration** – In the main request handler (`server.py`), import and invoke `enforce_lan_constraints(request)` **before** any business logic.

* **Remote Execution Service** – New endpoint `/lan/execute` that:
  * Authenticates the TLS token.
  * Calls `validate_target_ip(request)` and `validate_command_safety(command)`.
  * Forwards the command to the client‑side agent.

---

## 5. Auditing & Monitoring
* All LAN requests are logged with: timestamp, source IP, endpoint, outcome (allowed/blocked), and reason for denial.  
* A daily audit job scans logs for repeated policy violations and can auto‑block offending IPs.

---

## 6. Future Extensions
* **Dynamic Policy Updates** – Load constraints from a YAML file to allow runtime tuning without redeployment.  
* **Rate Limiting** – Prevent abuse of the remote execution endpoint.  
* **Zero‑Trust Network Segmentation** – Further isolate LAN subnets using micro‑VMs.

---

*Prepared by the Safety Engineering Team – Claude Parasite Brain Suck project*  
*Version 1.0 – 2026‑02‑04*