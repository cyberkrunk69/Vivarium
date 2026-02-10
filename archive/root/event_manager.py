import asyncio
from typing import Dict, Any, Set

from fastapi import WebSocket
from fastapi.responses import EventSourceResponse

# ----------------------------------------------------------------------
# Global containers for active connections
# ----------------------------------------------------------------------
_websocket_clients: Set[WebSocket] = set()
_sse_queues: Set[asyncio.Queue] = set()


async def _broadcast_message(message: str) -> None:
    """Send a JSON‑encoded string to all connected listeners."""
    # WebSocket clients
    dead_ws = set()
    for ws in _websocket_clients:
        try:
            await ws.send_text(message)
        except Exception:
            dead_ws.add(ws)
    _websocket_clients.difference_update(dead_ws)

    # SSE listeners – each listener has its own asyncio.Queue
    dead_queues = set()
    for q in _sse_queues:
        try:
            await q.put(message)
        except Exception:
            dead_queues.add(q)
    _sse_queues.difference_update(dead_queues)


def broadcast(event: str, payload: Dict[str, Any]) -> None:
    """
    Public API used by the rest of the code base.
    ``event`` is one of: task_start, task_complete, task_fail, checkpoint_save.
    ``payload`` will be JSON‑serialisable.
    """
    import json
    message = json.dumps({"event": event, "payload": payload})
    # Fire‑and‑forget – the broadcast runs in the background.
    asyncio.create_task(_broadcast_message(message))


# ----------------------------------------------------------------------
# WebSocket endpoint utilities
# ----------------------------------------------------------------------
async def register_websocket(ws: WebSocket) -> None:
    await ws.accept()
    _websocket_clients.add(ws)
    try:
        while True:
            # Keep connection alive – ignore any client messages.
            await ws.receive_text()
    except Exception:
        pass
    finally:
        _websocket_clients.discard(ws)


# ----------------------------------------------------------------------
# SSE endpoint utilities
# ----------------------------------------------------------------------
async def sse_event_generator():
    """
    Async generator used by FastAPI's EventSourceResponse.
    Each connected client gets its own queue.
    """
    queue: asyncio.Queue = asyncio.Queue()
    _sse_queues.add(queue)
    try:
        while True:
            data = await queue.get()
            yield f"data: {data}\n\n"
    finally:
        _sse_queues.discard(queue)