# Dashboard Code Review

## Executive Summary

Comprehensive audit of manually-introduced dashboard code reveals **1 CRITICAL security vulnerability** and **6 bugs** requiring immediate attention. The code implements a real-time task visualization system but has significant issues around security, error handling, and race conditions.

## Critical Issues (Fix Immediately)

### 🚨 CRITICAL - XSS Vulnerability in Node Titles
**File**: `dashboard_vision.js:75`
**Risk**: Code injection, session hijacking, credential theft

```javascript
// VULNERABLE CODE
el.innerHTML = `
    <div class="node-title">${title}</div>  // ⚠️ UNSAFE
`;
```

**Impact**: Malicious input like `<script>alert(document.cookie)</script>` executes JavaScript.

**Fix**:
```javascript
// SAFE VERSION
el.innerHTML = `
    <div class="node-title"></div>
`;
el.querySelector('.node-title').textContent = title; // Safe text-only
```

## High Priority Bugs

### 1. Race Condition in SSE Event Handling
**File**: `dashboard_vision.js:317-330`
**Issue**: Concurrent `task_started` events can create duplicate nodes

```javascript
// PROBLEMATIC CODE
let existingNode = state.nodes.find(n => n.id === event.nodeId);
if (!existingNode) {
    existingNode = createNode(...);  // Race condition here
}
```

**Fix**: Use a processing queue or node ID registry to prevent duplicates.

### 2. Memory Leak in Connection Lines
**File**: `dashboard_vision.js:265-267`
**Issue**: Only cleans `data-to` lines, not `data-from` lines

```javascript
// INCOMPLETE CLEANUP
const line = elements.nodesContainer.querySelector(
    `.connection-line[data-to="${node.id}"]`  // Missing data-from cleanup
);
```

**Fix**: Clean both incoming and outgoing connection lines.

### 3. Tree Layout Y-Position Bug
**File**: `dashboard_vision.js:119`
**Issue**: Incorrect centering calculation for child nodes

```javascript
// BUG: Uses siblings.length which excludes current node
y = parentY + (node.childIndex * (NODE_HEIGHT + V_GAP)) - (siblings.length * (NODE_HEIGHT + V_GAP) / 2);
```

**Fix**: Use total child count including current node for proper centering.

### 4. Missing Error Handling in /chat Endpoint
**File**: `dashboard_server.py:219-310`
**Issues**:
- No input validation or size limits (DoS risk)
- No rate limiting
- Background thread has no error handling
- No cleanup on thread failure

**Fix**: Add validation, rate limiting, and proper error handling.

### 5. Weak SSE Reconnection Logic
**File**: `dashboard_vision.js:310-313`
**Issue**: Only retries on `onerror`, misses silent disconnections

```javascript
// INCOMPLETE
eventSource.onerror = () => {
    setTimeout(connectSSE, 3000);  // Only handles explicit errors
};
```

**Fix**: Add periodic connection health checks and handle all disconnect scenarios.

### 6. Unsafe Task Processing Thread
**File**: `dashboard_server.py:250-304`
**Issue**: Background task simulation has no error handling

```python
# UNSAFE
def process_task():
    import time
    time.sleep(0.5)  # No try/catch, thread can crash
```

**Fix**: Wrap in try/catch with proper error propagation.

## Medium Priority Issues

### 7. Input Validation Missing
- No message length limits in `/chat` endpoint
- No sanitization of task titles before storage
- No validation of node types or parent IDs

### 8. Resource Management
- `active_tasks` dict grows indefinitely (memory leak)
- No cleanup of completed tasks from memory
- SSE connections not tracked or limited

### 9. Security Headers Missing
- No CSRF protection on `/chat` endpoint
- No rate limiting on any endpoints
- Missing security headers (CSP, etc.)

## Code Quality Issues

### 10. Hardcoded Values
- Magic numbers for delays and positions throughout
- No configuration management
- Inconsistent error messages

### 11. Poor Error Propagation
- Client doesn't handle server errors gracefully
- No user feedback for failed operations
- Silent failures in many code paths

## Recommended Fixes by Priority

### Phase 1 (Critical - Fix Today)
1. **Fix XSS vulnerability** - Replace innerHTML with textContent
2. **Add input validation** - Sanitize all user inputs
3. **Implement error handling** - Wrap all async operations

### Phase 2 (High - Fix This Week)
1. **Fix race conditions** - Add proper synchronization
2. **Fix memory leaks** - Complete cleanup in all code paths
3. **Add proper reconnection** - Handle all SSE disconnect scenarios

### Phase 3 (Medium - Next Sprint)
1. **Add rate limiting** - Prevent abuse
2. **Add resource limits** - Prevent memory exhaustion
3. **Add comprehensive logging** - For debugging and monitoring

## Testing Recommendations

1. **Security Testing**: Test XSS payloads in task titles
2. **Load Testing**: Rapid task submission to find race conditions
3. **Connection Testing**: Network interruption scenarios
4. **Error Testing**: Invalid inputs and server failures
5. **Memory Testing**: Long-running sessions for leak detection

## Conclusion

The dashboard implementation shows good UX design but has serious security and stability issues. The **XSS vulnerability must be fixed immediately** before any production use. The other bugs should be addressed systematically to ensure reliable operation.

**Risk Assessment**: HIGH - Critical security vulnerability present
**Recommended Action**: Fix critical issues before any further development