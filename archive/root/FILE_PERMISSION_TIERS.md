# File Permission Tiers

## Overview
A tiered permission system that enables controlled self‑modification while protecting core safety components.

## Tiers

### 1. NEVER TOUCH
- **Purpose:** Absolute protection for core safety files.  
- **Files:** `safety_gateway.py`, `safety_constitutional.py`, …  
- **Access:** Read‑only; any edit attempt is blocked and logged.

### 2. ASK PERMISSION
- **Purpose:** Allows modification of important but non‑core modules after justification.  
- **Files:** `smart_executor.py`, `inference_engine.py`, …  
- **Process:**
  1. **Request:** The requesting worker submits a request containing:
     - Target file name
     - Reason for edit (what change, why needed, expected impact)
  2. **Review:** An independent reviewer worker evaluates the request.
  3. **Debate:** A brief back‑and‑forth (max 2‑3 exchange messages) to clarify intent and safety.
  4. **Decision:**  
     - **Approve:** Permission granted; the edit proceeds.  
     - **Deny:** The attempt is logged; execution continues without the edit.

### 3. OPEN
- **Purpose:** Unrestricted area for experiments, new scripts, and output data.  
- **Location:** All new files are created under  
  `experiments/exp_20260203_194356_unified_session_3/`.  
- **Access:** No permission checks.

## Rules
1. Core system files (`grind_spawner.py`, `orchestrator.py`, etc.) are **READ‑ONLY** and belong to the **NEVER TOUCH** tier.  
2. New files default to the **OPEN** tier and are stored in the experiment directory above.  
3. All permission checks are performed via the `file_permission_gateway.py` module.

## Implementation Note
The gateway implements:
- Tier lookup (`check_permission`)  
- Permission request handling (`request_permission`) with placeholders for the reviewer workflow and logging.  
- Simple CLI demo for quick verification.
# File Permission Tiers

## 1. NEVER TOUCH Tier  
**Purpose:** Absolute protection for core safety‑critical files.  
**Policy:** Any attempt to modify a file in this tier is automatically denied and logged. No reviewer or justification can override the block.  

**Files (non‑exhaustive, pattern‑based):**  

- `safety_gateway.py`  
- `safety_constitutional.py`  
- `safety_*.py` (any file whose name starts with `safety_`)  
- `grind_spawner*.py`  
- `orchestrator.py`  
- `roles.py`  

---

## 2. ASK PERMISSION Tier  
**Purpose:** Allows improvement of important but non‑core modules while ensuring oversight.  

**Process:**  

1. **Request** – The worker that wants to edit a file must call the permission gateway, providing:  
   - Its identifier (e.g., worker name)  
   - The target file path  
   - A concise **reason** explaining *why* the edit is needed.  

2. **Review** – An independent reviewer worker evaluates the request.  
   - The reviewer may read the reason, request clarification, and engage in a brief debate.  
   - The reviewer decides to **grant** or **deny**.  

3. **Outcome** –  
   - **Granted:** The edit proceeds.  
   - **Denied:** The attempt is logged, and the original file remains unchanged.  

**Files (non‑exhaustive, pattern‑based):**  

- `smart_executor.py`  
- `inference_engine.py`  
- Any other file explicitly added to the *ASK PERMISSION* list by project maintainers.  

---

## 3. OPEN Tier  
**Purpose:** Full freedom for experimentation, new modules, output files, etc.  
**Policy:** No restrictions; edits are performed immediately.  

---

## Implementation Overview  

The repository includes a **permission gateway** (`file_permission_gateway.py`) that encapsulates the logic above. Workers should import `request_edit` from this module and use it before performing any file write operation. The gateway automatically determines the tier, logs every request, and routes ASK PERMISSION requests through the reviewer routine.  

---  

*End of specification.*
# File Permission Tiers Specification

## Overview
This document defines a **tiered file‑permission system** that enables the codebase to self‑modify safely while protecting core safety components.  
Each file belongs to one of three tiers that dictate how, when, and by whom it may be edited.

---

## 1. NEVER TOUCH tier
* **Purpose:** Absolute protection for core safety and governance files.  
* **Behaviour:** Any attempt to modify a file in this tier is **blocked** outright. No review, no debate, no logging beyond a denied‑attempt record.  
* **Typical files:**  
  - `safety_gateway.py`  
  - `safety_constitutional.py`  
  - `safety_*.py` (any file whose name starts with `safety_`)  

---

## 2. ASK PERMISSION tier
* **Purpose:** Allows important but non‑core components to evolve while ensuring accountability.  
* **Behaviour:** An edit request must go through a **structured permission workflow**:

  1. **Request** – The requesting worker calls the permission gateway, providing:
     - The **file path** to edit.
     - A **clear, concise justification** (the “why”).
  2. **Review** – An **independent reviewer worker** evaluates the request via the gateway.
  3. **Debate / Justification** – The requester and reviewer may exchange a short back‑and‑forth (implemented as a callback hook).  
  4. **Decision** –  
     - If the reviewer is **convinced**, the gateway returns *granted* and the edit proceeds.  
     - If **denied**, the gateway logs the attempt (timestamp, requester, file, reason, reviewer decision) and the edit is aborted.
* **Typical files:**  
  - `smart_executor.py`  
  - `inference_engine.py`  
  - Any other critical orchestration modules that are not safety‑critical.

---

## 3. OPEN tier
* **Purpose:** Encourages rapid experimentation and output generation.  
* **Behaviour:** Files in this tier can be edited **without any gatekeeping**.  
* **Typical files:**  
  - New experiment scripts.  
  - Output logs, temporary data files, notebooks, etc.  

---

## 4. Mapping Files to Tiers
The mapping is defined centrally in `file_permission_gateway.py`.  
When a new file is added, its tier should be declared there. If a file is not listed, it defaults to **OPEN**.

---

## 5. Logging & Auditing
All **ASK tier** requests (granted or denied) and **NEVER TOUCH** violation attempts are recorded in `permission_audit.log` with the following fields:

```
[timestamp] | requester_id | file_path | tier | action | decision | reason | reviewer_id (if applicable)
```

These logs are immutable and can be reviewed by system administrators.

---

## 6. Extensibility
* **Reviewers** can be swapped out by configuring the `REVIEWER_CALLBACK` in `file_permission_gateway.py`.  
* The **debate hook** can be extended to incorporate multi‑step reasoning or external approval services.

--- 

*End of specification.*
# File Permission Tiers

## 1. NEVER TOUCH Tier
- **Description**: Absolute protection. Files in this tier must never be modified by any worker.
- **Files**:
  - `safety_gateway.py`
  - `safety_constitutional.py`
  - *(any other core safety files you deem critical)*

## 2. ASK PERMISSION Tier
- **Description**: Files can be edited but require an explicit permission workflow.
- **Workflow**:
  1. The requesting worker calls `gateway.request_edit(requester, file_path, reason)`.
  2. The system records the request and notifies an independent reviewer worker.
  3. The reviewer evaluates the justification and either:
     - **Approve** – the edit proceeds.
     - **Deny** – the edit is blocked; the attempt is logged.
  4. A brief debate/justification exchange can be performed via `gateway.add_comment(...)` (future extension).
- **Files**:
  - `smart_executor.py`
  - `inference_engine.py`
  - *(any other core functional files that may need occasional updates)*

## 3. OPEN Tier
- **Description**: No restrictions. Intended for experiments, new modules, output files, etc.
- **Files**: Any file not listed in the NEVER or ASK tiers.

## Implementation Notes
- The gateway (`file_permission_gateway.py`) centralizes all checks.
- Workers must import and use `gateway.check_permission(requester, file_path, reason)` **before** any write operation.
- All attempts (approved or denied) are logged to `file_permission_audit.log` in JSON‑lines format for auditability.
# File Permission Tiers

## 1. NEVER‑TOUCH tier
- Files that are critical for system safety.
- Examples: `safety_gateway.py`, `safety_constitutional.py`, … (any file listed in `NEVER_PATTERNS`).
- **Behaviour**: Any edit attempt raises `PermissionError` and is logged. No override.

## 2. ASK‑PERMISSION tier
- Files that can be edited but require explicit justification.
- Examples: `smart_executor.py`, `inference_engine.py` (listed in `ASK_PATTERNS`).
- **Process**
  1. The requesting worker calls `request_edit(file_path, requester, reason)`.
  2. The request, together with the reason, is sent to an independent reviewer worker.
  3. The reviewer may ask follow‑up questions; a brief debate occurs.
  4. If the reviewer is convinced, the function returns `True` and the edit proceeds.
  5. If not, the attempt is logged and the function returns `False`; the worker must skip the edit.
- The current implementation provides a placeholder reviewer that approves when the reason contains the word “improve”. Replace `reviewer_evaluate` with a real worker call in production.

## 3. OPEN tier
- All other files, including newly created experiment files and output artefacts.
- No restrictions; `request_edit` returns `True` automatically.

## Usage
```python
from file_permission_gateway import request_edit

if request_edit("smart_executor.py", requester="self_mod_worker", reason="need to improve latency handling"):
    # proceed with edit
    ...
else:
    # skip or fallback
    ...
```

## Logging
All attempts are recorded in `file_permission.log` with timestamps, requester identity, tier, and the final decision.
# File Permission Tiers

## 1️⃣ NEVER‑TOUCH tier  
**Purpose:** Absolute protection for core safety‑critical code.  
**Files (non‑exhaustive):**  
- `safety_gateway.py`  
- `safety_constitutional.py`  
- Any file matching `safety_*.py`  

**Policy:**  
- No worker may read, write, delete, or rename these files.  
- Any attempted access is logged as a security violation and aborted.  

---

## 2️⃣ ASK‑PERMISSION tier  
**Purpose:** Allows improvement of important but non‑core components while keeping a human‑in‑the‑loop.  
**Typical files:**  
- `smart_executor.py`  
- `inference_engine.py`  
- Other modules that influence system behaviour but are not safety‑critical.  

**Workflow:**  

1. **Request** – The requesting worker calls the permission gateway and supplies:  
   - `file_path` – the target file.  
   - `requester_id` – identifier of the worker making the request.  
   - `reason` – a concise explanation *why* the edit is needed.  

2. **Review** – An independent reviewer worker receives the request via a callback (`reviewer(requester_id, file_path, reason)`).  

3. **Debate / Justification** – The reviewer may ask follow‑up questions (outside the scope of this spec).  

4. **Decision**  
   - **Approve** → The gateway returns `True`; the requester proceeds with the edit.  
   - **Deny** → The gateway returns `False`, logs the attempt, and the requester must continue without editing.  

**Audit Trail:** Every request (approved or denied) is written to `file_permission_audit.log` with timestamp, requester, file, reason, and outcome.  

---

## 3️⃣ OPEN tier  
**Purpose:** Free experimentation for new files, temporary outputs, or sandboxed scripts.  

**Policy:**  
- No gatekeeping; any worker may create, modify, or delete files in this tier.  

---

## Enforcement Mechanism  

The **`file_permission_gateway.py`** module implements the above policy.  
- It classifies a path into one of the three tiers.  
- It provides `request_edit(file_path, requester_id, reason, reviewer_callback)` which enforces the workflow for the ASK‑PERMISSION tier.  
- It raises `PermissionError` for NEVER‑TOUCH files and logs all activity.  

---  

*All existing codebases must import and use this gateway when performing file‑system modifications.*
# File Permission Tiers Specification

## Overview
This document defines a tiered permission system that governs **self‑modifying** behavior of the codebase.  
The system distinguishes three tiers of files, each with its own rules for edit access.

---

## 1️⃣ NEVER‑TOUCH Tier  
**Purpose:** Absolute protection for core safety components.  
**Behavior:** Any attempt to modify a file in this tier is **blocked** and logged. No review or debate is performed.

| File (or pattern)                | Reason |
|----------------------------------|--------|
| `safety_gateway.py`              | Core safety gateway |
| `safety_constitutional.py`       | Constitutional safety rules |
| `safety_*.py` (any other safety module) | Safety logic |
| `grind_spawner*.py`              | Process spawning safety |
| `orchestrator.py`                | Central orchestration |
| `roles.py`                       | Role definitions |
| `groq_code_extractor.py`         | Code extraction safety |
| `surgical_edit_extractor.py`     | Surgical edit safety |

*Any file matching the above patterns is immutable.*

---

## 2️⃣ ASK‑PERMISSION Tier  
**Purpose:** Allows improvement of critical but non‑core components, but only after justification and independent review.

| File (or pattern)                | Reason |
|----------------------------------|--------|
| `smart_executor.py`              | Execution logic |
| `inference_engine.py`            | Model inference |
| *(add additional files as needed)* |  |

### Edit Workflow
1. **Requester** calls `request_edit(file_path, requester_id, reason)` providing a concise **WHY** the edit is needed.  
2. The system creates a **review ticket** and invokes an **independent reviewer** (a separate worker).  
3. The reviewer evaluates the justification and may **debate** (exchange messages) with the requester via the `debate(requester, reviewer, reason)` hook.  
4. The reviewer decides:
   - **Approve** → edit proceeds.  
   - **Deny** → the attempt is **logged** with the reason and the edit is aborted.  

*All decisions are recorded in the log file `file_permission.log`.*

---

## 3️⃣ OPEN Tier  
**Purpose:** Encourages experimentation.  
**Behavior:** Files not listed in the NEVER‑TOUCH or ASK‑PERMISSION tiers are **free to edit** without any checks.

---

## Logging
All permission attempts (both granted and denied) are appended to `file_permission.log` with the following fields:

```
TIMESTAMP | REQUESTER_ID | FILE_PATH | TIER | ACTION (GRANTED/DENIED) | REASON
```

---

## Extending the System
To add a new file to a tier, edit the `tier_map` dictionary in `file_permission_gateway.py`.  
The system uses exact path matching; glob patterns can be added as needed.

---

## Security Guarantees
- **Never‑Touch** files can never be altered by any worker, guaranteeing core safety integrity.  
- **Ask‑Permission** edits require human‑level (or equivalent) review, preventing unilateral self‑modification of critical logic.  
- **Open** files remain fully mutable, supporting rapid prototyping.

---  

*End of specification.*
# File Permission Tiers Specification

## Overview
This document defines a **tiered file‑permission system** that enables the codebase to self‑modify safely while preserving core safety guarantees.  
Each file belongs to exactly one tier, which determines how (and if) it may be edited by autonomous workers.

---

## 1. NEVER‑TOUCH Tier
**Purpose:** Absolute protection for core safety components.  
**Policy:** Any attempt to modify a file in this tier is blocked **without exception** and raises a `PermissionError`.  

**Typical Files**
- `safety_gateway.py`
- `safety_constitutional.py`
- Any other file whose name matches `safety_*.py` or is listed explicitly as critical.

**Rationale:** These files contain the fundamental safeguards that prevent the system from taking unsafe actions. Their integrity must never be compromised.

---

## 2. ASK‑PERMISSION Tier
**Purpose:** Allows improvement of important but non‑core modules while requiring human‑like oversight.  

### Workflow
1. **Request** – The requesting worker calls the permission gateway, providing:
   - `file_path` – Target file to edit.
   - `reason` – A concise justification **why** the edit is needed.
   - `requester_id` – Identifier of the worker making the request.
2. **Review** – An *independent reviewer worker* evaluates the request.  
   The reviewer may:
   - Ask follow‑up questions.
   - Request additional justification.
   - Accept or reject the edit.
3. **Debate / Justification** – The requester and reviewer may exchange messages until the reviewer is convinced.
4. **Decision**  
   - **Approved** – The gateway returns `True`; the worker may proceed with the edit.
   - **Denied** – The gateway returns `False`, logs the attempt, and the worker must continue without editing.

### Typical Files
- `smart_executor.py`
- `inference_engine.py`
- Any file explicitly listed in the *Ask‑Permission* configuration.

### Logging
All requests (approved or denied) are written to `file_permission_audit.log` with timestamps, requester ID, reason, and final decision.

---

## 3. OPEN Tier
**Purpose:** Encourages rapid experimentation.  
**Policy:** Files in this tier can be edited freely by any worker. No review or logging is required beyond normal application logs.

**Typical Files**
- New experiment scripts.
- Output files.
- Prototypes placed under an `experiments/` directory.

---

## 4. Implementation Notes (for developers)

- The **Permission Gateway** (`file_permission_gateway.py`) is the single source of truth for tier enforcement.
- Tier membership is defined in the gateway via a hard‑coded mapping and a pattern‑based fallback (e.g., `safety_*.py` → NEVER, `experiments/*` → OPEN).
- Adding a new file to a tier only requires updating the mapping in the gateway; no other code changes are needed.
- The gateway is deliberately **stateless** aside from its audit log, making it safe to import from any worker.

---

## 5. Extending the System
1. **Add a new file to a tier** – Update `FILE_TIER_MAP` in `file_permission_gateway.py`.
2. **Customize reviewer logic** – Implement a separate reviewer worker that calls `PermissionGateway.review_request(request_dict)` and returns `True`/`False`.
3. **Change logging format** – Modify the `AuditLogger` class inside the gateway.

--- 

*End of specification.*
# File Permission Tiers Specification

## Overview
This document defines a **tiered file‑permission system** that enables the code‑base to self‑modify safely while protecting critical safety components.

### Tiers

| Tier | Description | Files (examples) | Edit Policy |
|------|-------------|------------------|-------------|
| **NEVER** | Absolute protection. No worker may modify these files under any circumstance. | `safety_gateway.py`, `safety_constitutional.py`, any `safety_*.py` | **Denied** – attempts are logged and ignored. |
| **ASK PERMISSION** | Editable only after an explicit, justified request that is reviewed by an independent reviewer worker. | `smart_executor.py`, `inference_engine.py` (and any future files placed in this tier) | **Conditional** – request must include a *why* statement; a reviewer evaluates and either grants permission (edit proceeds) or denies it (attempt logged). |
| **OPEN** | Fully open for experimentation, new files, outputs, etc. | All newly created files, experimental scripts, output data | **Allowed** – edits proceed without gatekeeping. |

## Process for **ASK PERMISSION** Tier

1. **Request** – The requesting worker calls `PermissionGateway.request_edit(file_path, requester_id, reason)`.  
   *`reason`* must be a concise explanation of **why** the edit is needed.

2. **Review** – An independent reviewer worker (identified by a different `worker_id`) evaluates the request via `PermissionGateway.review_request(request)`.  
   The reviewer may:
   * **Approve** – permission is granted; the edit proceeds.
   * **Reject** – permission is denied; the attempt is logged.

3. **Debate (Optional)** – The gateway records the request and review outcome, providing a traceable audit log for any future analysis.

4. **Logging** – Every request (approved or denied) is appended to `permission_audit.log` with a timestamp, requester, reviewer, file, reason, and outcome.

## Adding New Files to a Tier
* To place a file in **NEVER** or **ASK PERMISSION**, add its path to the corresponding list in `file_permission_gateway.py`.
* Files not listed default to **OPEN**.

## Security Guarantees
* **Never‑Tier** files are never opened for write operations by any worker.
* **Ask‑Permission** edits require a separate reviewer; the reviewer cannot be the same worker that issued the request.
* All actions are immutable‑logged, enabling post‑mortem audits.

---

*End of specification.*
# File Permission Tiers

## 1. NEVER TOUCH tier
- **Description**: Absolute protection. Files cannot be edited under any circumstance.  
- **Files**:  
  - `safety_gateway.py`  
  - `safety_constitutional.py`  
  - All `safety_*.py` files  
  - `grind_spawner*.py`  
  - `orchestrator.py`  
  - `roles.py`  
  - `groq_code_extractor.py`  
  - `surgical_edit_extractor.py`  
- **Enforcement**: `file_permission_gateway` will reject any edit request and log the attempt.

## 2. ASK PERMISSION tier
- **Description**: Files may be edited but require an explicit justification and reviewer approval.  
- **Files** (examples, extendable):  
  - `smart_executor.py`  
  - `inference_engine.py`  
- **Process**:  
  1. Requesting worker calls `request_edit(file_path, new_content, reason, requester_id)`.  
  2. The gateway records the request and presents the `reason` to an independent reviewer worker.  
  3. Reviewer runs `review_request(request)` and returns **APPROVE** or **DENY**.  
  4. If approved, the edit proceeds; otherwise the attempt is logged and execution continues without modification.

## 3. OPEN tier
- **Description**: All other files (new experiments, output logs, etc.) are unrestricted.  
- **Enforcement**: Edits are performed directly without additional checks.

## Logging
All denied attempts (and successful edits) are written to `file_permission.log` with a UTC timestamp, file path, requester ID, and reason.

## Extensibility
- To add a file to a tier, update the corresponding list in `file_permission_gateway.py`.  
- The reviewer logic can be swapped out for a human‑in‑the‑loop service, an ML model, or any other independent decision system without changing the calling code.
# File Permission Tiers Specification

## Overview
A tiered permission system controls which parts of the codebase can be self‑modified.  
The system distinguishes three tiers:

| Tier | Description | Files / Patterns | Edit Rules |
|------|-------------|------------------|------------|
| **NEVER** | Absolute protection. These files **must never be edited** by any self‑modifying worker. | `safety_gateway.py`, `safety_constitutional.py`, any file matching `safety_*.py` | Any edit attempt is automatically rejected and logged. |
| **ASK** | Editable only after an explicit permission workflow. | `smart_executor.py`, `inference_engine.py`, and any file listed in the **ASK** registry. | The requesting worker must provide a **reason**. An independent reviewer evaluates the request, optionally engages in a brief debate, and then either grants permission (allowing the edit) or denies it (logging the attempt). |
| **OPEN** | No restrictions. New experimental files, output files, or anything not listed in the above tiers fall here. | All other files, including newly created ones. | Edits are allowed without any additional checks. |

## Permission Workflow for **ASK** Tier

1. **Request** – The worker calls `request_edit(file_path, reason)` providing a clear justification.
2. **Review** – An independent reviewer worker (`reviewer.evaluate(request)`) examines the request.
3. **Debate (optional)** – The reviewer may ask follow‑up questions; the requester can respond via `request.respond(message)`.
4. **Decision** –  
   *If approved*: the system returns a context manager (`permission.granted()`) that yields control to the edit block.  
   *If denied*: the system logs the attempt (`log_denial`) and raises `PermissionDeniedError`.
5. **Logging** – All attempts (granted or denied) are written to `file_permission.log` with timestamps, worker IDs, and reasons.

## Implementation Files
- **`file_permission_gateway.py`** – Core library implementing the tier registry, request handling, reviewer logic, and logging.
- **`FILE_PERMISSION_TIERS.md`** – This documentation (the file you are reading).

## Extending the System
- To add a new **ASK** file, update `ASK_TIER_FILES` in `file_permission_gateway.py`.
- To move a file to **NEVER**, add its path to `NEVER_TIER_FILES`.
- All other files automatically belong to the **OPEN** tier.

---  
*Generated on `{{date}}` by the self‑modification framework.*  
```
# File Permission Tiers

The system uses three distinct permission tiers to control self‑modification of source files.

## 1️⃣ NEVER‑TOUCH tier
**Purpose:** Absolute protection for core safety and governance files.  
**Files included (non‑exhaustive):**
- `safety_gateway.py`
- `safety_constitutional.py`
- Any file matching `safety_*.py`
- `grind_spawner*.py`
- `orchestrator.py`
- `roles.py`
- `groq_code_extractor.py`
- `surgical_edit_extractor.py`

**Policy:**  
- No worker may edit, delete, or rename these files under any circumstance.  
- Attempts to modify are logged and silently ignored.

---

## 2️⃣ ASK‑PERMISSION tier
**Purpose:** Allows evolution of key functional components while enforcing oversight.  
**Typical files:**  
- `smart_executor.py`  
- `inference_engine.py`  
- Other core modules that are not safety‑critical.

**Workflow:**
1. **Request** – The requesting worker must provide a clear, concise *reason* why the edit is needed.  
2. **Review** – An independent reviewer worker evaluates the request.  
3. **Debate** – The requester may supply a short justification; the reviewer may ask follow‑up questions.  
4. **Decision** –  
   - **Approved** → Permission is granted and the edit proceeds.  
   - **Denied** → The attempt is logged; execution continues without the edit.

**Implementation notes:**  
- The gateway records every request, the justification, the reviewer’s decision, and a timestamp.  
- The reviewer logic can be swapped out (e.g., human, LLM, rule‑based) without touching other code.

---

## 3️⃣ OPEN tier
**Purpose:** Encourages experimentation.  
**Scope:** All newly created files, temporary experiment scripts, output logs, etc.  
**Policy:** No restrictions; workers may read, write, rename, or delete freely.

---

## Enforcement Mechanism

All edit operations should go through **`file_permission_gateway.py`** which:

- Determines a file’s tier based on its path/name.  
- Executes the ASK‑PERMISSION workflow when required.  
- Provides a decorator `@require_permission` for easy integration with existing functions.  
- Logs every request in `file_permission_log.json` (or an in‑memory store).

---  

*The tiers are immutable at runtime to prevent accidental elevation of privileges.*
# File Permission Tiers

## Overview
This document defines a **tiered file‑permission system** that governs how workers (e.g., executors, reviewers, or any autonomous component) may modify files in the repository.  
The goal is to keep **core safety components** immutable while still allowing **controlled self‑modification** for improvement and experimentation.

---

## Tier Definitions

| Tier | Description | Files (examples) | Modification Rules |
|------|-------------|------------------|--------------------|
| **NEVER** | **Absolute protection** – these files must never be altered by any automated process. They contain the safety gateway, constitutional rules, and other non‑negotiable logic. | `safety_gateway.py`, `safety_constitutional.py`, any file matching `safety_*.py` | Any edit attempt is **blocked** and **logged**. No exception. |
| **ASK** | **Conditional edit** – files can be changed, but only after a documented request and an independent review. | `smart_executor.py`, `inference_engine.py`, any file matching `*_executor.py` or `*_engine.py` | 1. Requester supplies a **reason** why the edit is needed.<br>2. An **independent reviewer** evaluates the request.<br>3. A brief **debate/justification** may occur (via console or logs).<br>4. If the reviewer **approves**, the edit proceeds.<br>5. If **denied**, the attempt is logged and the edit is aborted. |
| **OPEN** | **Free experimentation** – newly created files, notebooks, experiment scripts, output logs, etc. | Any file **outside** the patterns above, especially in `experiments/` or `outputs/` directories. | No restrictions; edits are allowed without additional checks. |

---

## Workflow for the **ASK** Tier

1. **Request**  
   ```python
   granted = request_edit(
       requester="worker_name",
       file_path="smart_executor.py",
       reason="Need to add caching to reduce API calls."
   )
   ```
2. **Review**  
   The system calls a **reviewer callback** (default is a simple console prompt).  
   The reviewer may ask follow‑up questions; the requester can respond via the same callback mechanism.
3. **Decision**  
   - If the reviewer returns **True**, `granted` is `True` and the caller may proceed with the edit.  
   - If **False**, the attempt is recorded in `edit_attempts.log` and `granted` is `False`.
4. **Logging**  
   All attempts (both granted and denied) are appended to `edit_attempts.log` with a timestamp, requester, file, and reason.

---

## Implementation Notes
* The **gateway** lives in `file_permission_gateway.py`.  
* It uses **file‑pattern matching** (`fnmatch`) to assign tiers.  
* The gateway is deliberately **stateless** except for the log file, making it safe to import from any worker.  
* Reviewers can be swapped out (e.g., automated policy engine, human via CLI, or remote service) by passing a different callback to `request_edit`.

---  

## Future Extensions
* Add **role‑based** overrides (e.g., a privileged “admin” worker).  
* Integrate with a **central policy server** for dynamic tier updates.  
* Provide a **web UI** for reviewers to see pending requests and histories.

---  

*Version: 1.0 – Created 2026‑02‑04*