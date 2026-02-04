"""
import self_observer
Groq API Client - Drop-in replacement for Claude CLI execution.

Provides LocalInferenceEngine that routes to Groq's API with:
- Adaptive model selection (8B for simple, 70B for complex)
- Cost tracking
- Rate limiting awareness
- Fail-safe error handling
"""

import os
import json
import time
import threading
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

# Groq SDK import
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("[GROQ] Warning: groq package not installed. Run: pip install groq")


@dataclass
class GroqModel:
    """Model configuration for Groq."""
    model_id: str
    display_name: str
    input_cost_per_1m: float  # USD per 1M input tokens
    output_cost_per_1m: float  # USD per 1M output tokens
    context_window: int
    max_completion: int
    tokens_per_second: int


# Groq model registry
GROQ_MODELS = {
    # GPT-OSS 120B - The big one, always use this
    "openai/gpt-oss-120b": GroqModel(
        model_id="openai/gpt-oss-120b",
        display_name="GPT-OSS 120B",
        input_cost_per_1m=0.20,
        output_cost_per_1m=0.80,
        context_window=131072,
        max_completion=32768,
        tokens_per_second=300
    ),
    # COMPOUND: Auto-selects model (keeping for backwards compat)
    "groq/compound": GroqModel(
        model_id="groq/compound",
        display_name="Groq Compound (Auto-Select)",
        input_cost_per_1m=0.15,
        output_cost_per_1m=0.60,
        context_window=131072,
        max_completion=32768,
        tokens_per_second=400
    ),
    # COMPOUND-MINI: Fast auto-select, single tool call, 3x lower latency
    "groq/compound-mini": GroqModel(
        model_id="groq/compound-mini",
        display_name="Groq Compound Mini (Fast Auto)",
        input_cost_per_1m=0.10,
        output_cost_per_1m=0.40,
        context_window=131072,
        max_completion=16384,
        tokens_per_second=600
    ),
    # Fast/cheap executor (Haiku equivalent)
    "llama-3.1-8b-instant": GroqModel(
        model_id="llama-3.1-8b-instant",
        display_name="Llama 3.1 8B Instant",
        input_cost_per_1m=0.05,
        output_cost_per_1m=0.08,
        context_window=131072,
        max_completion=8192,
        tokens_per_second=560
    ),
    # Versatile strategist (Opus equivalent)
    "llama-3.3-70b-versatile": GroqModel(
        model_id="llama-3.3-70b-versatile",
        display_name="Llama 3.3 70B Versatile",
        input_cost_per_1m=0.59,
        output_cost_per_1m=0.79,
        context_window=131072,
        max_completion=32768,
        tokens_per_second=280
    ),
    # Safety-focused model
    "llama-guard-3-8b": GroqModel(
        model_id="llama-guard-3-8b",
        display_name="Llama Guard 3 8B",
        input_cost_per_1m=0.20,
        output_cost_per_1m=0.20,
        context_window=8192,
        max_completion=1024,
        tokens_per_second=1200
    ),
}

# Model aliases - DEFAULT is GPT-OSS 120B
MODEL_ALIASES = {
    "auto": "openai/gpt-oss-120b",     # Default: GPT-OSS 120B
    "default": "openai/gpt-oss-120b",  # Explicit default
    "120b": "openai/gpt-oss-120b",     # Direct 120B access
    "gpt-oss": "openai/gpt-oss-120b",  # Shorthand
    "compound": "groq/compound",       # Legacy compound (auto-select)
    "compound-mini": "groq/compound-mini",
    "haiku": "groq/compound-mini",
    "sonnet": "openai/gpt-oss-120b",
    "opus": "openai/gpt-oss-120b",
    "fast": "groq/compound-mini",
    "smart": "openai/gpt-oss-120b",
    "guard": "llama-guard-3-8b",
    "8b": "llama-3.1-8b-instant",
    "70b": "llama-3.3-70b-versatile",
}


class GroqInferenceEngine:
    """
    Local inference engine using Groq API.

    Replaces Claude CLI calls with Groq API requests.
    Supports adaptive model selection based on task complexity.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq client.

        Args:
            api_key: Groq API key. Falls back to GROQ_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Set it via environment variable or pass to constructor.\n"
                "Get your key at: https://console.groq.com/keys"
            )

        if not GROQ_AVAILABLE:
            raise ImportError("groq package required. Install with: pip install groq")

        self.client = Groq(api_key=self.api_key)
        self.total_cost = 0.0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.request_count = 0

        # Rate limiting state (thread-safe)
        # Groq free tier: 30 requests/minute = 2 seconds between requests
        self._rate_lock = threading.Lock()
        self.last_request_time = 0
        self.min_request_interval = 2.0  # 2 seconds between requests (Groq rate limit)

    def _resolve_model(self, model: str) -> str:
        """Resolve model alias to actual Groq model ID."""
        # Check if it's an alias
        if model.lower() in MODEL_ALIASES:
            return MODEL_ALIASES[model.lower()]

        # Check if it's a direct model ID
        if model in GROQ_MODELS:
            return model

        # Check for partial matches (e.g., "llama-3.1-8b" -> "llama-3.1-8b-instant")
        for model_id in GROQ_MODELS:
            if model.lower() in model_id.lower():
                return model_id

        # Default to fast model
        print(f"[GROQ] Unknown model '{model}', defaulting to openai/gpt-oss-120b")
        return "openai/gpt-oss-120b"

    def _select_model_for_complexity(self, base_model: str, complexity_score: float) -> str:
        """
        Model selection - NOW DELEGATED TO GROQ COMPOUND.

        Groq's compound system automatically selects from GPT-OSS 120B,
        Llama 4 Scout, or Llama 3.3 70B based on task complexity.
        We just pass "groq/compound" and let it handle the rest.

        Args:
            base_model: Requested model (ignored if using compound)
            complexity_score: Task complexity (ignored - Groq handles this)

        Returns:
            Selected model ID
        """
        resolved = self._resolve_model(base_model)

        # If they explicitly asked for a specific model (8b, 70b, guard), use it
        if resolved in ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "llama-guard-3-8b"]:
            return resolved

        # Default: GPT-OSS 120B
        return "openai/gpt-oss-120b"

    def _estimate_cost(self, model_id: str, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for a request."""
        if model_id not in GROQ_MODELS:
            return 0.0

        model = GROQ_MODELS[model_id]
        input_cost = (input_tokens / 1_000_000) * model.input_cost_per_1m
        output_cost = (output_tokens / 1_000_000) * model.output_cost_per_1m
        return input_cost + output_cost

    def _rate_limit_wait(self):
        """Enforce rate limiting between requests (thread-safe)."""
        with self._rate_lock:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.min_request_interval:
                time.sleep(self.min_request_interval - elapsed)
            self.last_request_time = time.time()

    def execute(
        self,
        prompt: str,
        model: str = "openai/gpt-oss-120b",  # DEFAULT: GPT-OSS 120B
        complexity_score: float = 0.0,  # Ignored - Groq Compound handles this automatically
        max_tokens: int = 4096,
        temperature: float = 0.7,
        timeout: int = 600,
    ) -> Dict[str, Any]:
        """
        Execute a prompt using Groq API.

        Args:
            prompt: The prompt to execute
            model: Model name or alias
            complexity_score: Task complexity (0.0-1.0) for adaptive selection
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            timeout: Request timeout in seconds

        Returns:
            Dict with keys: result, cost, input_tokens, output_tokens, model, elapsed
        """
        start_time = time.time()

        # Select appropriate model
        model_id = self._select_model_for_complexity(model, complexity_score)
        model_config = GROQ_MODELS.get(model_id)

        if not model_config:
            return {
                "error": f"Unknown model: {model_id}",
                "returncode": 1,
                "result": "",
                "cost": 0.0
            }

        # Enforce rate limiting
        self._rate_limit_wait()

        try:
            # Make API request
            response = self.client.chat.completions.create(
                model=model_id,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software engineer executing tasks precisely. Follow instructions exactly."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=min(max_tokens, model_config.max_completion),
                temperature=temperature,
                timeout=timeout
            )

            # Extract response
            result_text = response.choices[0].message.content or ""
            input_tokens = response.usage.prompt_tokens if response.usage else 0
            output_tokens = response.usage.completion_tokens if response.usage else 0

            # Calculate cost
            cost = self._estimate_cost(model_id, input_tokens, output_tokens)

            # Update totals
            self.total_cost += cost
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            self.request_count += 1

            elapsed = time.time() - start_time

            return {
                "result": result_text,
                "returncode": 0,
                "cost": cost,
                "total_cost_usd": cost,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "model": model_id,
                "model_display": model_config.display_name,
                "elapsed": elapsed,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e)

            # Check for specific error types
            if "rate_limit" in error_msg.lower():
                # Try fallback model if we hit rate limit on primary
                if model_id == "openai/gpt-oss-120b":
                    print(f"[GROQ] Rate limit on 120B, falling back to 70B...")
                    time.sleep(2)  # Brief wait before fallback
                    return self.execute(
                        prompt=prompt,
                        model="llama-3.3-70b-versatile",  # Fallback
                        complexity_score=complexity_score,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        timeout=timeout
                    )
                return {
                    "error": "rate_limit",
                    "error_message": error_msg,
                    "returncode": 429,
                    "result": "",
                    "cost": 0.0,
                    "elapsed": elapsed
                }
            elif "timeout" in error_msg.lower():
                return {
                    "error": "timeout",
                    "error_message": error_msg,
                    "returncode": 408,
                    "result": "",
                    "cost": 0.0,
                    "elapsed": elapsed
                }
            else:
                return {
                    "error": "api_error",
                    "error_message": error_msg,
                    "returncode": 1,
                    "result": "",
                    "cost": 0.0,
                    "elapsed": elapsed
                }

    def get_stats(self) -> Dict[str, Any]:
        """Get cumulative usage statistics."""
        return {
            "total_cost_usd": self.total_cost,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_requests": self.request_count,
            "avg_cost_per_request": self.total_cost / max(self.request_count, 1)
        }

    def check_budget(self, budget_limit: float) -> Tuple[bool, float]:
        """
        Check if we're within budget.

        Args:
            budget_limit: Maximum budget in USD

        Returns:
            (within_budget, remaining)
        """
        remaining = budget_limit - self.total_cost
        return remaining > 0, remaining


# Global instance (lazy initialization)
_groq_engine: Optional[GroqInferenceEngine] = None


def get_groq_engine() -> GroqInferenceEngine:
    """Get or create the global Groq engine instance."""
    global _groq_engine
    if _groq_engine is None:
        _groq_engine = GroqInferenceEngine()
    return _groq_engine


def execute_with_groq(
    prompt: str,
    model: str = "openai/gpt-oss-120b",  # DEFAULT: GPT-OSS 120B
    complexity_score: float = 0.0,  # Ignored - Groq Compound handles this
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience function to execute a prompt with Groq.

    Args:
        prompt: The prompt to execute
        model: Model name or alias
        complexity_score: Task complexity for adaptive selection
        **kwargs: Additional arguments passed to execute()

    Returns:
        Execution result dict
    """
    engine = get_groq_engine()
    return engine.execute(prompt, model, complexity_score, **kwargs)


if __name__ == "__main__":
    # Quick test
    print("Testing Groq client...")

    if not os.environ.get("GROQ_API_KEY"):
        print("Set GROQ_API_KEY environment variable to test")
    else:
        engine = GroqInferenceEngine()

        # Test with simple prompt
        result = engine.execute(
            prompt="Say 'Hello from Groq!' and nothing else.",
            model="fast",
            max_tokens=50
        )

        print(f"Result: {result.get('result', 'ERROR')}")
        print(f"Model: {result.get('model')}")
        print(f"Cost: ${result.get('cost', 0):.6f}")
        print(f"Tokens: {result.get('input_tokens', 0)} in / {result.get('output_tokens', 0)} out")
        print(f"Stats: {engine.get_stats()}")