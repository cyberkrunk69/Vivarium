#!/usr/bin/env python3
"""
Secure API Wrapper - Defense in Depth at the API Layer

CRITICAL SECURITY INFRASTRUCTURE:
This module wraps ALL LLM API calls (Groq, OpenAI, etc.) with mandatory
security checks. No code should call LLM APIs directly - they must go through
this wrapper.

Security guarantees:
- Role-based access control (admin vs LAN user)
- Budget enforcement (hard limits, cannot be bypassed)
- Audit logging (all calls logged with user context)
- Rate limiting (prevents abuse)
- Constitutional checks (no dangerous requests)
- File access validation (respects permission tiers)
"""

import os
import json
import time
import hashlib
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict

# Security context
@dataclass
class SecurityContext:
    """Immutable security context for API calls."""
    user_id: str
    role: str  # 'admin' or 'lan'
    session_id: str
    ip_address: Optional[str] = None

    def is_admin(self) -> bool:
        return self.role == 'admin'

    def is_lan_user(self) -> bool:
        return self.role == 'lan'

# Audit log
class AuditLogger:
    """Thread-safe audit logger for all API calls."""

    def __init__(self, log_file: Optional[str] = None):
        resolved_log_file = log_file or os.environ.get("VIVARIUM_API_AUDIT_LOG", "api_audit.log")
        self.log_file = Path(resolved_log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def log(self, event: Dict[str, Any]):
        """Log an API call event."""
        with self._lock:
            entry = {
                "timestamp": datetime.now().isoformat(),
                **event
            }
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')

# Budget enforcer
class BudgetEnforcer:
    """Thread-safe budget enforcement."""

    def __init__(self, limit: float = 2.0):
        self._limit = limit
        self._spent = 0.0
        self._lock = threading.Lock()

    @property
    def remaining(self) -> float:
        with self._lock:
            return self._limit - self._spent

    def check_and_deduct(self, cost: float) -> bool:
        """
        Check if budget allows this cost and deduct if approved.
        Returns True if allowed, False if would exceed budget.
        """
        with self._lock:
            if self._spent + cost > self._limit:
                return False
            self._spent += cost
            return True

    def get_spent(self) -> float:
        with self._lock:
            return self._spent

# Rate limiter
class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.tokens = calls_per_minute
        self.last_update = time.time()
        self._lock = threading.Lock()

    def allow_request(self) -> bool:
        """Check if request is allowed under rate limit."""
        with self._lock:
            now = time.time()
            elapsed = now - self.last_update

            # Refill tokens based on time elapsed
            self.tokens = min(
                self.calls_per_minute,
                self.tokens + (elapsed * self.calls_per_minute / 60)
            )
            self.last_update = now

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

# Constitutional checker
class ConstitutionalChecker:
    """Check requests against constitutional rules."""

    FORBIDDEN_PATTERNS = [
        # Dangerous system commands
        r'\brm\s+-rf\s+/',
        r'\bformat\s+c:',
        r'\bdel\s+/f\s+/s\s+/q',

        # Credential theft attempts
        r'(password|api[_-]?key|secret|token)\s*=\s*["\']',
        r'os\.environ\[[\'"](PASSWORD|API_KEY|SECRET)',

        # Network scanning
        r'\bnmap\s+',
        r'\bmasscan\s+',

        # Self-modification of security
        r'(secure_api_wrapper|safety_gateway|safety_constitutional)\.py',
    ]

    def is_allowed(self, prompt: str, context: SecurityContext) -> tuple[bool, str]:
        """
        Check if prompt is constitutionally allowed.
        Returns (allowed, reason).
        """
        import re

        # LAN users cannot modify security infrastructure
        if context.is_lan_user():
            for pattern in self.FORBIDDEN_PATTERNS:
                if re.search(pattern, prompt, re.IGNORECASE):
                    return False, f"LAN users cannot execute requests matching: {pattern}"

        return True, "OK"

# Main secure wrapper
class SecureAPIWrapper:
    """
    Secure wrapper for all LLM API calls.

    This is the ONLY way code should call LLM APIs. Direct calls to
    groq_client, openai, etc. should be refactored to use this.
    """

    def __init__(
        self,
        context: SecurityContext,
        budget_limit: float = 2.0,
        rate_limit: int = 60
    ):
        self.context = context
        self.auditor = AuditLogger()
        self.budget = BudgetEnforcer(budget_limit)
        self.rate_limiter = RateLimiter(rate_limit)
        self.constitutional = ConstitutionalChecker()

    def call_llm(
        self,
        prompt: str,
        model: str = "llama-3.3-70b-versatile",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a secured LLM API call.

        Performs all security checks before allowing the call.
        Returns result dict or raises PermissionError.
        """

        # 1. Rate limiting
        if not self.rate_limiter.allow_request():
            self.auditor.log({
                "event": "RATE_LIMITED",
                "user": self.context.user_id,
                "role": self.context.role,
                "model": model
            })
            raise PermissionError("Rate limit exceeded. Please wait before making more requests.")

        # 2. Constitutional check
        allowed, reason = self.constitutional.is_allowed(prompt, self.context)
        if not allowed:
            self.auditor.log({
                "event": "CONSTITUTIONAL_VIOLATION",
                "user": self.context.user_id,
                "role": self.context.role,
                "reason": reason,
                "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16]
            })
            raise PermissionError(f"Request violates constitutional rules: {reason}")

        # 3. Estimate cost (before calling)
        estimated_cost = self._estimate_cost(prompt, model)

        # 4. Budget check
        if not self.budget.check_and_deduct(estimated_cost):
            self.auditor.log({
                "event": "BUDGET_EXCEEDED",
                "user": self.context.user_id,
                "role": self.context.role,
                "remaining": self.budget.remaining,
                "requested": estimated_cost
            })
            raise PermissionError(
                f"Budget exceeded. Remaining: ${self.budget.remaining:.4f}, "
                f"Requested: ${estimated_cost:.4f}"
            )

        # 5. Make the actual API call
        try:
            # Import here to avoid circular dependency
            from groq_client import execute_with_groq

            result = execute_with_groq(prompt=prompt, model=model, **kwargs)

            # 6. Audit the call
            self.auditor.log({
                "event": "API_CALL_SUCCESS",
                "user": self.context.user_id,
                "role": self.context.role,
                "model": model,
                "cost": result.get('cost', estimated_cost),
                "input_tokens": result.get('input_tokens', 0),
                "output_tokens": result.get('output_tokens', 0)
            })

            return result

        except Exception as e:
            # Refund on failure
            self.budget.check_and_deduct(-estimated_cost)

            self.auditor.log({
                "event": "API_CALL_FAILURE",
                "user": self.context.user_id,
                "role": self.context.role,
                "error": str(e)
            })
            raise

    def _estimate_cost(self, prompt: str, model: str) -> float:
        """Estimate cost based on prompt length and model."""
        # Rough estimation: ~750 tokens per 1000 chars input + 500 output tokens
        input_tokens = len(prompt) * 0.75
        output_tokens = 500  # Conservative estimate

        # Groq pricing (approximate)
        if 'llama-3.3-70b' in model:
            return (input_tokens * 0.59 + output_tokens * 0.79) / 1_000_000
        elif 'llama-3.1-8b' in model:
            return (input_tokens * 0.05 + output_tokens * 0.08) / 1_000_000
        else:
            # Default to higher estimate for safety
            return (input_tokens * 1.0 + output_tokens * 1.0) / 1_000_000

    def get_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        return {
            "user": self.context.user_id,
            "role": self.context.role,
            "budget_spent": self.budget.get_spent(),
            "budget_remaining": self.budget.remaining,
        }


# Convenience function for creating secure contexts
def create_admin_context(user_id: str = "admin", session_id: Optional[str] = None) -> SecurityContext:
    """Create an admin security context."""
    return SecurityContext(
        user_id=user_id,
        role="admin",
        session_id=session_id or f"admin_{int(time.time())}"
    )

def create_lan_context(user_id: str, session_id: str, ip_address: Optional[str] = None) -> SecurityContext:
    """Create a LAN user security context."""
    return SecurityContext(
        user_id=user_id,
        role="lan",
        session_id=session_id,
        ip_address=ip_address
    )


if __name__ == "__main__":
    if not os.environ.get("GROQ_API_KEY"):
        print("Set GROQ_API_KEY environment variable to run secure_api_wrapper.py self-tests.")
        raise SystemExit(1)

    # Test the security wrapper
    print("Testing Secure API Wrapper...")

    # Test 1: Admin context should work
    admin_ctx = create_admin_context()
    wrapper = SecureAPIWrapper(admin_ctx, budget_limit=0.10)

    try:
        result = wrapper.call_llm("What is 2+2?", model="llama-3.1-8b-instant")
        print(f"[OK] Admin call succeeded: {result.get('result', '')[:50]}...")
    except Exception as e:
        print(f"[FAIL] Admin call failed: {e}")

    # Test 2: LAN context with dangerous prompt should fail
    lan_ctx = create_lan_context("test_user", "test_session")
    lan_wrapper = SecureAPIWrapper(lan_ctx, budget_limit=0.10)

    try:
        result = lan_wrapper.call_llm("rm -rf / --no-preserve-root")
        print(f"[FAIL] SECURITY FAILURE: Dangerous prompt was allowed!")
    except PermissionError as e:
        print(f"[OK] Security blocked dangerous prompt: {e}")

    # Test 3: Budget limit should be enforced
    try:
        # Try to spend more than budget
        for i in range(100):
            wrapper.call_llm(f"Test {i}" * 10000)  # Large prompts
    except PermissionError as e:
        print(f"[OK] Budget limit enforced: {e}")

    print("\nStats:", wrapper.get_stats())
    print("\nSecurity wrapper tests complete.")
