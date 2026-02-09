# MULTI-USER LAN ARCHITECTURE DESIGN

## Architecture Diagram

The architecture diagram will consist of the following components:
- A central server that manages user sessions and routes file operations
- A network load visibility module that displays anonymized network activity
- A session isolation module that tracks each user's work separately
- A remote file editing module that allows users to edit files seamlessly

## Recommended Remote File Access Approach

After investigating the options, I recommend using **Option A: Browser File System Access API**. This approach allows for zero-install and provides a seamless experience for users. Although it has limitations such as requiring a user gesture and only working on Chrome and Edge, it provides the best balance between usability and security.

## Session Management Design

To track which user is which, the server will use a combination of IP addresses and session tokens. Each user will be assigned a unique session token when they connect to the server, and this token will be used to identify their session.

## Network Load Surfacing UI Mockup

The network load surfacing UI will display the following information:
- 'X other sessions active'
- 'Y tasks running network-wide (not yours)'

This information will be displayed in a non-intrusive manner, such as a small overlay in the corner of the screen.

## Security Considerations

To ensure security, the server will use encryption to protect user data and authentication to verify user identities. The server will also use access controls to restrict user access to sensitive data and operations.

## Architecture Questions and Answers

### How does the server track which user is which?

The server uses a combination of IP addresses and session tokens to track which user is which.

### How do we route file operations to the correct machine?

The server uses the session token to identify the user's machine and routes file operations accordingly.

### What happens if a user disconnects mid-task?

If a user disconnects mid-task, the server will pause the task and resume it when the user reconnects.

### How do we handle conflicting edits (same file, different users)?

The server will use a version control system to handle conflicting edits. If two users try to edit the same file at the same time, the server will create a new version of the file and notify the users of the conflict.
# Multi‑User LAN Design for Claude Parasite Brain‑Suck

---

## 1. High‑Level Architecture Diagram  

```mermaid
flowchart LR
    subgraph LAN[Local Network]
        direction TB
        Server[LAN Server (Node.js / FastAPI)] 
        subgraph Users
            A[User A<br/>Browser] 
            B[User B<br/>Browser] 
            C[User C<br/>Browser] 
        end
    end

    A -- WS / HTTP --> Server
    B -- WS / HTTP --> Server
    C -- WS / HTTP --> Server

    Server -- Broadcast Load Info --> A
    Server -- Broadcast Load Info --> B
    Server -- Broadcast Load Info --> C

    %% Remote file access paths
    A -- File System Access API --> LocalFS_A[Local FS (Browser)] 
    B -- File System Access API --> LocalFS_B[Local FS (Browser)] 
    C -- File System Access API --> LocalFS_C[Local FS (Browser)] 

    Server -- Command Relay (WebSocket) --> A
    Server -- Command Relay (WebSocket) --> B
    Server -- Command Relay (WebSocket) --> C
```

*The server is a lightweight, stateless HTTP/WebSocket service that maintains per‑session state in memory (or Redis for persistence). All user‑specific data is indexed by a **session token + client IP**.*

---

## 2. Recommended Remote File Access Approach  

### Chosen Solution: **Option A – Browser File System Access API**  

| Aspect | Reason |
|--------|--------|
| **Zero‑install** | Users only need a modern Chromium‑based browser (Chrome, Edge, Brave). |
| **Security** | Access is granted explicitly by the user per‑folder, scoped to the origin. No background processes run. |
| **Performance** | Direct read/write via native browser APIs, no extra network hop. |
| **UX Simplicity** | One‑time “Grant Folder Access” dialog; subsequent sessions can reuse the persisted permission (via the Origin‑Scoped File System). |
| **Fallback** | If the browser does not support the API, gracefully degrade to **Option D – lightweight Python agent** (download‑once, run‑once). |

**Implementation Sketch**  

```js
// client.js (served by LAN server)
async function initFolderAccess() {
  const dirHandle = await window.showDirectoryPicker();
  // store handle in IndexedDB for later sessions
  await navigator.storage.getDirectory(); // optional persistent storage
  // expose read/write functions to the server via WebSocket
}
```

The server sends JSON‑encoded file‑operation commands (`READ`, `WRITE`, `STAT`, `DELETE`) over the WebSocket; the client executes them against the granted folder handle and returns results.

---

## 3. Session Management Design  

| Component | Description |
|-----------|-------------|
| **Session Token** | Random UUID generated on first HTTP request, stored in a secure HttpOnly cookie. |
| **Client IP** | Captured from the request (trusted inside LAN). Combined with token to form a unique **session key**. |
| **In‑Memory Store** | `Map<sessionKey, { token, ip, ws, activeTasks, folderHandle }>`. |
| **Redis (optional)** | Persisted store for graceful server restarts; TTL = 30 min of inactivity. |
| **Task Tracker** | Each file operation is wrapped in a `Task` object with status (`queued`, `running`, `finished`, `error`). |
| **Isolation** | All tasks are scoped to the originating session key; the server never mixes file handles between sessions. |

**Lifecycle**

1. **Connect** – Browser opens WebSocket, sends `{type: "HELLO", token}`. Server creates/updates session entry.  
2. **Authorize** – Client runs `initFolderAccess()`; the resulting `folderHandle` is stored in the session entry (not on the server).  
3. **Operate** – Client sends `{type:"OP", op:"READ", path:"/notes.txt", taskId:"xyz"}`. Server records task under the session and broadcasts anonymized load info to all users.  
4. **Disconnect** – On `ws.close` or network loss, server marks the session as *disconnected* but retains pending tasks for a configurable grace period (e.g., 2 min). If the client reconnects with the same token, tasks resume; otherwise they are cancelled.

---

## 4. Network Load Surfacing UI Mock‑up  

```
+--------------------------------------------------------------+
|  Network Overview                                            |
|--------------------------------------------------------------|
|  You have 3 active sessions on this LAN.                     |
|  • 2 other sessions active                                   |
|  • 7 tasks running network‑wide (not yours)                 |
|--------------------------------------------------------------|
|  Your Tasks                                                  |
|  • Editing: notes.txt (0.3 s)                                 |
|  • Compiling: script.py (1.2 s)                               |
|--------------------------------------------------------------|
|  Network Activity (anonymous)                                |
|  • User #2: 3 tasks (2 s avg)                                 |
|  • User #3: 2 tasks (1.5 s avg)                               |
+--------------------------------------------------------------+
```

*All numbers are refreshed every 2 seconds via a lightweight `/load` endpoint or WebSocket broadcast. No user‑identifying information is ever displayed.*

---

## 5. Handling Edge Cases  

### a) User Disconnects Mid‑Task  
* **Grace Period** – Server keeps the task in a *paused* state for **N** seconds (configurable).  
* **Auto‑Cancel** – If the client does not reconnect, the server sends a `CANCEL` command; any partially written files are rolled back using a temporary‑file‑swap strategy.  

### b) Conflicting Edits (same file, different users)  
* **Optimistic Locking** – Each file operation includes a **version hash** (e.g., SHA‑256 of the last known content).  
* **Conflict Detection** – If the server receives a write where the version hash differs from the current server‑side version, it rejects the operation with `CONFLICT`.  
* **Resolution UI** – Client shows a modal: “File has changed since you opened it. Choose: (1) Overwrite, (2) Merge (diff view), (3) Cancel.”  

*Because actual file writes happen on the client’s local folder, the server only mediates the version metadata; the client can perform a three‑way merge locally.*

---

## 6. Security Considerations  

| Threat | Mitigation |
|--------|------------|
| **Unauthorized File Access** | Browser File System Access API requires explicit user gesture; no path outside the granted folder can be accessed. |
| **Man‑in‑the‑Middle (LAN) Attacks** | All WebSocket/HTTP traffic is protected with **TLS** (self‑signed certs acceptable within a trusted LAN). |
| **Session Hijacking** | Session token stored in HttpOnly, SameSite=Strict cookie; token is UUID‑v4 (128‑bit). |
| **DoS via Flooded Tasks** | Rate‑limit per‑session (max 10 concurrent tasks). Global task queue size capped; excess requests receive `429 Too Many Requests`. |
| **Data Leakage in Load UI** | Load info is aggregated and anonymized; no file names or user IDs are transmitted. |
| **Persisted Folder Handles** | Stored only in the client’s IndexedDB; server never receives raw handles. |
| **Agent Fallback (Option D)** | Agent runs as a non‑privileged user, communicates over mutually‑authenticated TLS, and self‑terminates after inactivity. |

---

## 7. Summary  

* Use **Browser File System Access API** as the primary, zero‑install method.  
* Track users by **session token + IP**; keep all per‑session state isolated.  
* Broadcast anonymized load statistics to give users context without exposing details.  
* Implement optimistic locking and a graceful disconnect strategy to keep the collaborative environment stable.  

This design satisfies the requirements for multi‑user visibility, session isolation, seamless remote file editing, and robust security while keeping the user experience frictionless.  

---  

*Document generated on 2026‑02‑03.*
# MULTI‑USER LAN DESIGN

## 1. Overview Diagram
```
+-------------------+          WebSocket          +-------------------+
|   User Browser   | <-------------------------> |   LAN Server      |
| (Chrome/Edge)    |   (HTTPS + WS)               | (Node/Go/Python)  |
|  +------------+  |                               |  +------------+   |
|  | UI Layer   |  |                               |  | Session   |   |
|  +------------+  |                               |  | Manager   |   |
|  | FS Access  |  |                               |  +------------+   |
|  +------------+  |                               |  | Task Queue|   |
+-------------------+                               +------------+---+
        ^  |                                            ^   |
        |  | File System Access API (Option A)        |   |
        |  +--------------------------------------------+   |
        |                                                   |
        |   (fallback) Lightweight Agent (Option D)        |
        +---------------------------------------------------+

```

## 2. Recommended Remote File Access Approach
**Primary:** **Option A – Browser File System Access API**  
- Zero‑install for Chrome/Edge (and other Chromium‑based browsers).  
- Users grant folder access once per session via a UI button.  
- All file reads/writes happen locally in the browser; the server only sends *commands* (e.g., “open file X”, “save changes”).  
- Provides the best UX: no extra tabs, no background pages, no OS‑level share configuration.

**Fallback:** **Option D – Lightweight Python Agent**  
- If the user’s browser does not support the File System Access API, they can run a single‑file Python script (`connect_to_swarm.py`).  
- The agent opens a persistent WebSocket to the LAN server and executes file operations locally.  
- This fallback still requires a manual step but covers Firefox, Safari, and older browsers.

*Options B & C are not recommended as primary solutions because they either force the user to keep a page open (B) or require OS‑level sharing configuration (C), which adds friction and security concerns.*

## 3. Session Management Design
| Component | Responsibility |
|-----------|----------------|
| **Session Token** | Random UUID generated on first connection, stored in a secure, HttpOnly cookie. |
| **IP Binding** | Server logs the originating IP; token is considered valid only when the request originates from the same /24 subnet. |
| **Session Store** | In‑memory map (`token → {ip, userName, folderHandle, taskList}`) with TTL = 15 min of inactivity. |
| **Heartbeat** | Browser sends a lightweight ping every 5 s via WS; resets TTL. |
| **Disconnect Handling** | On missed heartbeats (≥3), server marks session *offline*: pending tasks are paused, UI shows “User disconnected”. When the user reconnects with the same token, the session is restored. |

### Routing File Operations
1. **Client → Server**: `{action: "read", path: "relative/to/granted/folder", token}`  
2. **Server** looks up the token, retrieves the stored `folderHandle` (or forwards to the Python agent if fallback).  
3. **Server** validates that the requested path is inside the granted folder (prevent path‑traversal).  
4. **Server** sends the command back to the client (or agent) which performs the actual FS operation and returns the result.

## 4. Conflict & Edit Management
- **Optimistic Concurrency**: Each file edit includes a SHA‑256 hash of the file content the client *last* saw.  
- **Server Check**: When a write arrives, the server (or agent) compares the hash with the current file hash.  
  - **Match** → Accept write.  
  - **Mismatch** → Reject and return a *conflict* response with the latest content. UI prompts user to merge.  
- **Lock‑less Collaboration**: No hard file locks; users see “X other sessions active” and “Y tasks running network‑wide” to understand potential contention.

## 5. UI Mock‑up (Textual)

```
+-----------------------------------------------------------+
| LAN Workspace                                              |
+-----------------------------------------------------------+
| Your Tasks (3)                                            |
|  • Compile projectA                                        |
|  • Run tests                                               |
|                                                             |
| Network Activity (5 other sessions)                       |
|  • 2 users editing /shared/docs/                           |
|  • 1 user running heavy data import                        |
|                                                             |
| --------------------------------------------------------   |
| File Explorer (Your Granted Folder)                        |
|  ▶ src/                                                    |
|     main.py          (edited 2 min ago)                    |
|     utils.py         (conflict! – 1 other user)            |
|  ▶ assets/                                                |
|                                                             |
| [Grant Folder Access]   [Refresh]   [Help]                |
+-----------------------------------------------------------+
```

- The **“Network Activity”** line shows anonymized counts only.  
- Conflicted files are highlighted with a warning icon; clicking opens a merge dialog.

## 6. Security Considerations
| Area | Mitigation |
|------|------------|
| **Authentication** | Stateless token in HttpOnly cookie; token tied to client IP/subnet. |
| **Authorization** | Folder handle is scoped to the exact folder the user granted; all paths are validated to stay inside that folder. |
| **Transport** | All HTTP and WebSocket traffic enforced over TLS (self‑signed LAN certs acceptable). |
| **CSRF/XSS** | No cross‑origin requests; CORS set to `null` or specific LAN origins only. |
| **Data Leakage** | Server never stores raw file contents beyond the duration of the request; logs contain only hashes and metadata. |
| **Agent Binary** | Single‑file Python script signed with SHA‑256; checksum displayed on download page. |
| **Denial‑of‑Service** | Rate‑limit per‑token (max 10 ops/sec); disconnect idle sessions after TTL. |
| **Audit** | Every file operation logged with timestamp, token, IP, and operation type. |

--- 

*End of design document.*