"""
Black Swarm API Server (Groq-only)

Endpoint:
  POST /grind  - Execute a task using Groq API
"""

from typing import Optional, Any, Dict

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from config import (
    GROQ_API_KEY,
    GROQ_API_URL,
    DEFAULT_GROQ_MODEL,
    validate_model_id,
    validate_config,
)

load_dotenv()

app = FastAPI(title="Black Swarm", version="1.0")


class GrindRequest(BaseModel):
    """
    Request model for the /grind endpoint.

    Attributes:
        prompt: Task prompt to send to the Groq API.
        model: Optional Groq model id (must be in whitelist).
        max_tokens: Maximum completion tokens.
        temperature: Sampling temperature.
        min_budget/max_budget/intensity: Optional metadata for logging.
        task_id: Optional task identifier (echoed in response).
    """

    prompt: str = Field(..., min_length=1)
    model: Optional[str] = None
    max_tokens: int = Field(default=2048, ge=1, le=65536)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    intensity: Optional[str] = None
    task_id: Optional[str] = None


class GrindResponse(BaseModel):
    """
    Response model for the /grind endpoint.
    """

    status: str
    result: str
    model: str
    task_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None


@app.post("/grind", response_model=GrindResponse)
async def grind(req: GrindRequest) -> GrindResponse:
    """
    Execute a task by calling Groq's OpenAI-compatible chat completions API.
    """

    validate_config(require_groq_key=True)

    model = req.model or DEFAULT_GROQ_MODEL
    validate_model_id(model)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": req.prompt}],
        "temperature": req.temperature,
        "max_tokens": req.max_tokens,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(GROQ_API_URL, headers=headers, json=payload)
    except httpx.TimeoutException as e:
        raise HTTPException(status_code=500, detail=f"Groq timeout: {e}") from e
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Groq request error: {e}") from e

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Groq API error: {response.text}")

    data = response.json()
    try:
        result_text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail=f"Invalid Groq response: {e}") from e

    return GrindResponse(
        status="completed",
        result=result_text,
        model=model,
        task_id=req.task_id,
        usage=data.get("usage"),
    )
