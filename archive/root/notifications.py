import asyncio
from typing import Any, Dict, List
from fastapi import WebSocket

class NotificationManager:
    """
    Manages real‑time client connections and broadcasts events.
    Supports both WebSocket push and SSE (via an async queue).
    """
    def __init__(self):
        self._websockets: List[WebSocket] = []
        self._queue: asyncio.Queue = asyncio.Queue()

    # ------------------------------------------------------------------
    # WebSocket management
    # ------------------------------------------------------------------
    def register_websocket(self, ws: WebSocket) -> None:
        """Add a new WebSocket connection."""
        self._websockets.append(ws)

    def unregister_websocket(self, ws: WebSocket) -> None:
        """Remove a WebSocket connection."""
        if ws in self._websockets:
            self._websockets.remove(ws)

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    async def broadcast(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Broadcast an event to all connected WebSocket clients and
        push it onto the SSE queue.
        """
        event = {"type": event_type, "data": data}
        # Queue for SSE consumers
        await self._queue.put(event)

        # Push to all active WebSockets
        dead_sockets = []
        for ws in self._websockets:
            try:
                await ws.send_json(event)
            except Exception:
                # Mark sockets that failed (e.g., client disconnected)
                dead_sockets.append(ws)
        # Clean up dead sockets
        for ws in dead_sockets:
            await self.unregister_websocket(ws)

    async def next_event(self) -> Dict[str, Any]:
        """
        Retrieve the next event for SSE consumers.
        This coroutine blocks until an event is available.
        """
        return await self._queue.get()


# Global instance used throughout the application
notification_manager = NotificationManager()