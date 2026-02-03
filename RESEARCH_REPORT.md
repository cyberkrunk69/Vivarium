# Pre-Execution Research Report: Multi-Server Architecture & LAN Access Control

**Date:** 2026-02-03
**Research Scope:** Dual-server architecture, LAN user session isolation, remote execution protocol, task dependency scheduling, engine/model visibility, adaptive engine selection
**Status:** Research Complete - Ready for Swarm Execution

---

## Executive Summary

This research report provides comprehensive analysis of the existing codebase to inform the swarm's implementation of:
1. **Dual-server architecture** - Admin (localhost) + User (LAN-accessible)
2. **LAN user session isolation** - Safety constraints for WiFi users
3. **Remote execution protocol** - Execute tasks on user's machine, not host
4. **Task dependency scheduling** - Proper task ordering with prerequisites
5. **Engine/model visibility** - Dashboard UI showing which engine/model per worker
6. **Adaptive engine selection** - Claude vs Groq based on task complexity

---

## 1. Current State Analysis

### 1.1 Server Architecture (`progress_server.py`)

**Current Implementation:**
```python
# Line 1581: Host binding logic
host = "0.0.0.0" if args.lan else "127.0.0.1"
```

**Key Findings:**
- **Single server design**: Only one HTTP server instance
- **Conditional binding**: `--lan` flag switches between localhost and all interfaces
- **Port**: Fixed at 8080 (configurable via `--port`)
- **No authentication**: All requests treated equally regardless of source
- **SSE for real-time updates**: Uses Server-Sent Events via `/events` endpoint
- **File-based state**: Monitors `wave_status.json`, `SUMMARY.md`, `learned_lessons.json`

**Endpoints (lines 1504-1551):**
| Endpoint | Purpose |
|----------|---------|
| `/`, `/index.html`, `/command`, `/dashboard` | Main dashboard HTML |
| `/events` | SSE stream for real-time updates |
| `/api/status` | JSON status API |

### 1.2 Dashboard Server (`dashboard_server.py`)

**Current Implementation:**
```python
# Line 260: Binds to all interfaces
socketio.run(app, host='0.0.0.0', port=8420, debug=True)
```

**Key Findings:**
- **Socket.IO based**: Uses Flask-SocketIO for WebSocket communication
- **Always binds 0.0.0.0**: No localhost-only option
- **Port 8420**: Different from progress_server (8080)
- **More endpoints**: `/status`, `/experiments`, `/pending-changes`, `/approve/<id>`, `/cost-tracking`

### 1.3 Session Management (`grind_spawner.py`)

**Current Session Tracking:**
```python
class GrindSession:
    def __init__(self, session_id: int, model: str, budget: float, ...):
        self.session_id = session_id
        self.model = model
        # No user/origin tracking
        # No remote execution support
```

**Key Findings:**
- **Local-only execution**: Sessions run on host machine via subprocess
- **No user attribution**: No tracking of who initiated a session
- **No origin tracking**: Cannot distinguish localhost vs LAN requests
- **Engine info available**: `self.model` tracks which model is used
- **Unified spawner exists**: `grind_spawner_unified.py` has engine selection logic

### 1.4 Unified Engine System (`grind_spawner_unified.py`, `inference_engine.py`)

**Engine Selection Logic:**
```python
class EngineSelector:
    def select_engine(self, task_text: str, budget: float, force_engine: Optional[EngineType] = None):
        # 1. Forced override
        # 2. Explicit preference in task ("use groq", "use claude")
        # 3. Complexity analysis (score 0.0-1.0)
        # 4. Budget consideration (<$0.10 -> Groq)
        # 5. Environment variable INFERENCE_ENGINE
        # 6. Default: Claude
```

**Key Findings:**
- **Auto-selection implemented**: Based on complexity score, budget, explicit keywords
- **Two engines**: Claude (CLI subprocess) and Groq (API)
- **Cost tracking per engine**: Both engines track cost, tokens, calls
- **Model mapping**: `haiku`, `sonnet`, `opus` aliases for Claude; `llama-3.1-8b-instant`, `llama-3.3-70b-versatile` for Groq

### 1.5 Safety Infrastructure

**Existing Safety Modules:**
| File | Purpose | Key Features |
|------|---------|--------------|
| `safety_gateway.py` | Unified pre-execution checks | Constitutional, workspace, network, prompt checks |
| `safety_sandbox.py` | Workspace isolation | Path validation, sensitive file protection |
| `safety_killswitch.py` | Emergency stop | Global halt, pause/resume, file-based flags |
| `safety_network.py` | Network isolation | Blocks external URLs, whitelists localhost |
| `safety_constitutional.py` | AI safety constraints | Semantic intent detection, malicious pattern blocking |
| `safety_sanitize.py` | Input sanitization | Injection detection |
| `safety_audit.py` | Audit logging | Operation logging |

**Current Network Whitelist:**
```python
self.whitelist: Set[str] = {
    '127.0.0.1',
    'localhost',
    '::1',
    '0.0.0.0'
}
```

---

## 2. Architecture Recommendations

### 2.1 Dual-Server Architecture

**Recommended Design:**
```
+-------------------+     +---------------------+
|   ADMIN SERVER    |     |    USER SERVER      |
|   localhost:8080  |     |    0.0.0.0:8081     |
+-------------------+     +---------------------+
         |                         |
         v                         v
  Full Control Panel         Read-Only Dashboard
  - Execute tasks            - View progress
  - Approve changes          - Monitor workers
  - Kill switch              - View logs
  - Direct file access       - Submit tasks (queued)
                             - NO direct execution
```

**Implementation Approach:**
1. **Modify `progress_server.py`** to spawn two server instances
2. **Create new handler classes**: `AdminHandler` vs `UserHandler`
3. **IP-based routing**: Check `self.client_address[0]` in request handler
4. **Separate SSE streams**: Different data for admin vs user

### 2.2 LAN User Session Isolation

**Safety Constraints for LAN Users:**
```python
class LANUserConstraints:
    # What LAN users CAN do:
    - View dashboard (read-only wave_status, SUMMARY, logs)
    - View worker status
    - Submit tasks to queue (NOT direct execution)
    - View their own submitted tasks

    # What LAN users CANNOT do:
    - Execute tasks directly on host
    - Access admin endpoints (/approve, kill switch)
    - Modify files on host
    - Access sensitive paths
    - View other users' sessions (without permission)
```

**Session Isolation Design:**
```python
class UserSession:
    user_id: str          # UUID or IP-based
    origin_ip: str        # Source IP address
    is_local: bool        # localhost detection
    permissions: List[str] # ['view', 'submit_task', 'view_own_sessions']
    tasks_submitted: List[str]
    created_at: datetime
```

### 2.3 Remote Execution Protocol

**Current Problem:**
- Tasks execute on host machine
- LAN users submitting tasks = potential security risk
- No way to execute on the user's machine

**Recommended Protocol:**
```
User Machine                    Host Server
+-------------+                +-------------+
| Claude CLI  |   WebSocket    | Task Queue  |
| or Agent    | <----------->  | Server      |
+-------------+                +-------------+
       |                              |
       v                              v
  Local Sandbox                  Orchestrator
  (experiments/)                 (dispatch only)
```

**Protocol Messages:**
```json
// Host -> User: Task Assignment
{
    "type": "TASK_ASSIGNED",
    "task_id": "task_123",
    "task": "Implement feature X",
    "budget": 0.10,
    "engine": "claude|groq|auto",
    "workspace": "user_local_path"
}

// User -> Host: Task Progress
{
    "type": "TASK_PROGRESS",
    "task_id": "task_123",
    "status": "running|completed|failed",
    "output": "...",
    "cost": 0.05,
    "engine_used": "claude",
    "model_used": "sonnet"
}
```

### 2.4 Task Dependency Scheduling

**Current State:**
- `orchestrator.py` has `depends_on` field in task schema
- No actual dependency resolution implemented

**Recommended Implementation:**
```python
class TaskScheduler:
    def __init__(self):
        self.task_graph = {}  # task_id -> TaskNode
        self.completed = set()
        self.in_progress = set()

    def can_execute(self, task_id: str) -> bool:
        task = self.task_graph[task_id]
        return all(dep in self.completed for dep in task.depends_on)

    def get_ready_tasks(self) -> List[Task]:
        return [t for t_id, t in self.task_graph.items()
                if t_id not in self.completed
                and t_id not in self.in_progress
                and self.can_execute(t_id)]

    def topological_sort(self) -> List[str]:
        # Kahn's algorithm for execution order
        pass
```

### 2.5 Engine/Model Visibility in Dashboard

**Required UI Changes:**

**Current Worker Card (dashboard.html line 647-653):**
```html
<div class="worker-card">
    <div class="worker-id">Worker ${worker.id}</div>
    <div class="worker-status">${worker.status}</div>
    <div class="worker-task">${worker.current_task}</div>
</div>
```

**Enhanced Worker Card:**
```html
<div class="worker-card">
    <div class="worker-id">Worker ${worker.id}</div>
    <div class="worker-engine">${worker.engine} / ${worker.model}</div>
    <div class="worker-status">${worker.status}</div>
    <div class="worker-task">${worker.current_task}</div>
    <div class="worker-cost">$${worker.session_cost.toFixed(4)}</div>
</div>
```

**Data Requirements:**
```json
{
    "workers": [{
        "id": 1,
        "engine": "claude",        // NEW
        "model": "sonnet",         // NEW
        "status": "running",
        "current_task": "Fix bug",
        "session_cost": 0.0234,    // NEW
        "tokens_used": 1500,       // NEW
        "origin_ip": "192.168.1.5" // NEW (for multi-user)
    }]
}
```

### 2.6 Adaptive Engine Selection

**Enhancement to `EngineSelector`:**
```python
def select_engine_adaptive(
    self,
    task: str,
    budget: float,
    history: List[TaskResult] = None
) -> Tuple[EngineType, str]:
    # 1. Check task patterns (existing)
    # 2. Analyze recent history for similar tasks
    # 3. If Groq failed recently on similar task -> use Claude
    # 4. If Claude was overkill (high cost, simple task) -> use Groq
    # 5. Time-of-day consideration (Groq faster during peak)
    pass
```

---

## 3. Task Dependency Graph

```
+----------------------------------+
|    INITIATIVE DEPENDENCIES       |
+----------------------------------+

1. Dual-Server Architecture
   |
   +---> 2. LAN User Session Isolation
   |         |
   |         +---> 3. Remote Execution Protocol
   |
   +---> 5. Engine/Model Visibility (UI)

4. Task Dependency Scheduling (INDEPENDENT)

6. Adaptive Engine Selection (INDEPENDENT, but benefits from 5)

EXECUTION ORDER:
  Phase 1 (Parallel):
    - Task 4: Dependency Scheduling
    - Task 6: Adaptive Engine Selection

  Phase 2:
    - Task 1: Dual-Server Architecture

  Phase 3:
    - Task 2: LAN Session Isolation
    - Task 5: Dashboard UI (engine visibility)

  Phase 4:
    - Task 3: Remote Execution Protocol
```

---

## 4. Critical Files to Modify

### High Priority (Core Changes)
| File | Changes Required |
|------|------------------|
| `progress_server.py` | Dual-server binding, IP-based access control, admin vs user handlers |
| `dashboard.html` | Engine/model display, user session view, permissions UI |
| `grind_spawner.py` | Session origin tracking, user attribution |
| `grind_spawner_unified.py` | Enhanced engine selection, remote execution hooks |
| `orchestrator.py` | Task dependency resolution, topological sort |

### Medium Priority (Supporting Changes)
| File | Changes Required |
|------|------------------|
| `safety_gateway.py` | User-level permission checks |
| `safety_network.py` | LAN IP whitelisting for allowed operations |
| `wave_status.json` | Add engine/model per worker |
| `inference_engine.py` | Statistics per user session |

### New Files Required
| File | Purpose |
|------|---------|
| `session_manager.py` | User session tracking, isolation |
| `task_scheduler.py` | Dependency resolution, topological sort |
| `remote_protocol.py` | WebSocket protocol for remote execution |
| `access_control.py` | IP-based permission system |

---

## 5. Risks and Mitigations

### Risk 1: Security Exposure via LAN
**Severity:** HIGH
**Description:** Opening server to LAN exposes attack surface
**Mitigation:**
- Strict IP-based access control
- Read-only default for non-localhost
- Task queue instead of direct execution
- Rate limiting per IP
- Audit logging all LAN requests

### Risk 2: Session Data Leakage
**Severity:** MEDIUM
**Description:** Users seeing other users' session data
**Mitigation:**
- Session isolation by user_id
- Permission checks on all data access
- Separate SSE streams per user

### Risk 3: Remote Execution Trust
**Severity:** HIGH
**Description:** Host trusting remote execution results
**Mitigation:**
- Cryptographic task signing
- Result verification on host
- Sandboxed execution on remote
- Cost tracking and budget enforcement on both ends

### Risk 4: Task Dependency Cycles
**Severity:** LOW
**Description:** Circular dependencies causing deadlock
**Mitigation:**
- Cycle detection during task addition
- Timeout for waiting tasks
- Admin override capability

### Risk 5: Engine Selection Failures
**Severity:** MEDIUM
**Description:** Wrong engine selected causing task failure
**Mitigation:**
- Fallback to Claude on Groq failure
- Retry with different engine
- User override capability
- Learning from historical performance

---

## 6. Implementation Checklist

### Phase 1: Foundation (Parallel Tasks)
- [ ] Implement `task_scheduler.py` with dependency resolution
- [ ] Enhance `EngineSelector` with adaptive learning
- [ ] Add engine/model tracking to worker state

### Phase 2: Server Architecture
- [ ] Refactor `progress_server.py` for dual-server
- [ ] Implement `access_control.py` with IP-based permissions
- [ ] Add admin-only endpoints protection

### Phase 3: Session & UI
- [ ] Implement `session_manager.py`
- [ ] Update dashboard.html with engine/model visibility
- [ ] Add user session isolation

### Phase 4: Remote Execution
- [ ] Design WebSocket protocol
- [ ] Implement `remote_protocol.py`
- [ ] Create remote execution client
- [ ] Add result verification

---

## 7. API Design

### Admin Endpoints (localhost only)
```
POST /admin/execute       - Direct task execution
POST /admin/approve/{id}  - Approve pending change
POST /admin/kill          - Trigger kill switch
POST /admin/pause         - Pause all workers
POST /admin/resume        - Resume workers
GET  /admin/sessions      - All sessions (full access)
GET  /admin/audit         - Safety audit log
```

### User Endpoints (LAN accessible)
```
GET  /dashboard           - Read-only dashboard
GET  /api/status          - System status
GET  /api/workers         - Worker status (filtered)
POST /api/submit-task     - Submit task to queue
GET  /api/my-sessions     - User's own sessions
WS   /ws/progress         - Real-time progress (filtered)
```

### Remote Execution Protocol (WebSocket)
```
/ws/remote-exec
  <- TASK_ASSIGNED
  -> TASK_ACCEPTED / TASK_REJECTED
  -> TASK_PROGRESS (periodic)
  -> TASK_COMPLETED / TASK_FAILED
  <- TASK_CANCELLED (from host)
```

---

## 8. Conclusion

The existing codebase provides solid foundations:
- **Safety infrastructure is comprehensive** (7 safety modules)
- **Engine abstraction exists** (inference_engine.py)
- **Real-time updates work** (SSE in progress_server.py)
- **Task dependency schema exists** (orchestrator.py `depends_on`)

Key gaps to fill:
1. **No IP-based access control** - must implement
2. **No user session tracking** - must implement
3. **No remote execution** - must implement
4. **Dependency resolution not implemented** - must implement
5. **Engine visibility not in UI** - must implement

The swarm should proceed with the phased approach outlined above, prioritizing security and the dual-server architecture first.

---

*Research conducted by: Opus 4.5 Pre-Execution Research Agent*
*Files analyzed: 15+ Python modules, 2 HTML templates, multiple JSON configs*
