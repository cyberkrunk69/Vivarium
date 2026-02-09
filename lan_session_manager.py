# lan_session_manager.py
import time
import asyncio
from collections import defaultdict
import websockets
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """
    Manages LAN sessions on a per‑IP basis.

    Features
    --------
    * Per‑IP session tracking
    * Separate containers for “Your tasks” and “Network activity”
    * Activity log (timestamped)
    * Automatic timeout / cleanup
    * WebSocket client registration for real‑time push updates
    """

    def __init__(self, timeout_seconds: int = 60):
        # { ip_address: {created_at, tasks, network_activity} }
        self.sessions: defaultdict[str, dict] = defaultdict(dict)
        self.timeout = timeout_seconds
        self.activity_log: list[tuple[str, str, float]] = []   # (ip, activity, ts)
        self.websocket_clients: set[websockets.WebSocketServerProtocol] = set()

    # ------------------------------------------------------------------ #
    # WebSocket helpers
    # ------------------------------------------------------------------ #
    async def register_ws(self, ws: websockets.WebSocketServerProtocol) -> None:
        """Add a new websocket client."""
        self.websocket_clients.add(ws)
        logger.debug("WebSocket client registered: %s", ws.remote_address)

    async def unregister_ws(self, ws: websockets.WebSocketServerProtocol) -> None:
        """Remove a websocket client."""
        self.websocket_clients.discard(ws)
        logger.debug("WebSocket client unregistered: %s", ws.remote_address)

    async def broadcast(self, message: str) -> None:
        """Push a JSON‑serialisable string to every connected client."""
        if not self.websocket_clients:
            return
        await asyncio.wait([client.send(message) for client in self.websocket_clients])

    # ------------------------------------------------------------------ #
    # Session lifecycle
    # ------------------------------------------------------------------ #
    def _ensure_session(self, ip: str) -> None:
        """Create a fresh session dict for *ip* if it does not exist."""
        if ip not in self.sessions:
            self.sessions[ip] = {
                "created_at": time.time(),
                "tasks": [],               # “Your tasks”
                "network_activity": []     # “Network activity”
            }
            logger.info("New session created for %s", ip)

    def create_session(self, ip: str) -> None:
        """Public entry point – idempotent."""
        self._ensure_session(ip)

    def add_task(self, ip: str, task: str) -> None:
        """Append a user‑task to the session."""
        self._ensure_session(ip)
        self.sessions[ip]["tasks"].append(task)
        self.log_activity(ip, f"Task added: {task}")

    def add_network_activity(self, ip: str, activity: str) -> None:
        """Append a network‑activity entry to the session."""
        self._ensure_session(ip)
        self.sessions[ip]["network_activity"].append(activity)
        self.log_activity(ip, f"Network activity: {activity}")

    def get_session(self, ip: str) -> dict | None:
        """Return the raw session dict (or None)."""
        return self.sessions.get(ip)

    def get_all_sessions(self) -> dict:
        """Snapshot of all sessions – useful for the dashboard."""
        return dict(self.sessions)

    def update_session(self, ip: str, **kwargs) -> None:
        """Merge arbitrary keys into the session dict."""
        if ip in self.sessions:
            self.sessions[ip].update(kwargs)

    # ------------------------------------------------------------------ #
    # Timeout handling
    # ------------------------------------------------------------------ #
    def _is_expired(self, created_at: float) -> bool:
        return (time.time() - created_at) > self.timeout

    def purge_expired(self) -> None:
        """Delete any sessions that have exceeded the timeout."""
        now = time.time()
        expired_ips = [
            ip for ip, sess in self.sessions.items()
            if now - sess["created_at"] > self.timeout
        ]
        for ip in expired_ips:
            del self.sessions[ip]
            logger.info("Session for %s expired and removed", ip)

    # ------------------------------------------------------------------ #
    # Activity logging
    # ------------------------------------------------------------------ #
    def log_activity(self, ip: str, activity: str) -> None:
        """Append a timestamped entry to the global activity log."""
        entry = (ip, activity, time.time())
        self.activity_log.append(entry)
        logger.debug("Activity logged: %s – %s", ip, activity)

    def get_activity_log(self) -> list[tuple[str, str, float]]:
        """Return a copy of the activity log."""
        return list(self.activity_log)

# ---------------------------------------------------------------------- #
# WebSocket server entry‑point
# ---------------------------------------------------------------------- #
async def ws_handler(websocket: websockets.WebSocketServerProtocol, path: str):
    """
    Simple echo‑style handler that registers the client,
    forwards any incoming messages to the logger,
    and keeps the connection alive until the client disconnects.
    """
    manager = ws_handler.session_manager   # attached later
    await manager.register_ws(websocket)

    try:
        async for message in websocket:
            logger.info("Received WS message from %s: %s", websocket.remote_address, message)
            # In a real app you would parse JSON commands here.
            # For demo purposes we just echo back.
            await websocket.send(f"ECHO: {message}")
    finally:
        await manager.unregister_ws(websocket)

def start_ws_server(host: str = "0.0.0.0", port: int = 8765, timeout: int = 60):
    """
    Starts the WebSocket server that powers real‑time dashboard updates.
    Returns the asyncio.Task that runs the server.
    """
    manager = SessionManager(timeout_seconds=timeout)
    ws_handler.session_manager = manager   # bind manager to handler

    server = websockets.serve(ws_handler, host, port)
    logger.info("WebSocket server listening on %s:%s", host, port)
    return server, manager

# ---------------------------------------------------------------------- #
# Example usage (run directly for a quick test)
# ---------------------------------------------------------------------- #
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    server_coro, manager = start_ws_server()
    server = loop.run_until_complete(server_coro)

    try:
        # Keep the loop alive – in a real app you would have other async tasks.
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
```python
"""
lan_session_manager.py

Implements a LAN Session Manager that tracks per‑IP sessions, logs activity,
segregates user‑task activity from generic network activity, handles session
timeouts, and provides WebSocket support for real‑time dashboard updates.
"""

import asyncio
import datetime
import threading
from typing import Any, Dict, Set


class SessionManager:
    """
    Core manager for LAN sessions.

    Features
    --------
    * Per‑IP session tracking.
    * Separate logs for "Your tasks" and "Network activity".
    * Automatic cleanup of idle sessions (timeout configurable).
    * Async broadcast of activity updates to registered WebSocket listeners.
    """

    def __init__(self, timeout_seconds: int = 300, cleanup_interval: int = 60):
        """
        Parameters
        ----------
        timeout_seconds: int
            Seconds of inactivity after which a session is considered expired.
        cleanup_interval: int
            Seconds between automatic cleanup runs.
        """
        self._timeout = datetime.timedelta(seconds=timeout_seconds)
        self._cleanup_interval = cleanup_interval

        # Structure:
        # {
        #   ip_address: {
        #       "last_active": datetime,
        #       "tasks":   List[Dict],
        #       "network": List[Dict],
        #   },
        #   ...
        # }
        self._sessions: Dict[str, Dict[str, Any]] = {}

        # WebSocket listener queues – each listener receives a copy of every
        # activity message via an asyncio.Queue.
        self._ws_clients: Set[asyncio.Queue] = set()

        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True
        )
        self._cleanup_thread.start()

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _now(self) -> datetime.datetime:
        return datetime.datetime.utcnow()

    def _ensure_session(self, ip: str) -> None:
        """Create a fresh session entry for *ip* if it does not yet exist."""
        if ip not in self._sessions:
            self._sessions[ip] = {
                "last_active": self._now(),
                "tasks": [],   # List of activity dicts
                "network": [],  # List of activity dicts
            }

    # --------------------------------------------------------------------- #
    # Public API – activity recording
    # --------------------------------------------------------------------- #
    def record_activity(self, ip: str, category: str, detail: str) -> None:
        """
        Record an activity for a given IP address.

        Parameters
        ----------
        ip: str
            The source IP address.
        category: str
            Either ``"tasks"`` (your tasks) or ``"network"`` (network activity).
        detail: str
            Human‑readable description of the activity.
        """
        if category not in ("tasks", "network"):
            raise ValueError("category must be 'tasks' or 'network'")

        timestamp = self._now()
        entry = {"timestamp": timestamp.isoformat(), "detail": detail}

        with self._lock:
            self._ensure_session(ip)
            sess = self._sessions[ip]
            sess["last_active"] = timestamp
            sess[category].append(entry)

            # Trim logs to avoid unbounded growth
            if len(sess[category]) > 1000:
                sess[category] = sess[category][-500:]

        # Fire‑and‑forget broadcast to WebSocket listeners
        asyncio.run(self._broadcast_update(ip, category, entry))

    # --------------------------------------------------------------------- #
    # Public API – snapshot & cleanup
    # --------------------------------------------------------------------- #
    def get_snapshot(self) -> Dict[str, Any]:
        """
        Return a deep‑copy snapshot of all current sessions.
        Useful for initial dashboard rendering.
        """
        with self._lock:
            return {
                ip: {
                    "last_active": sess["last_active"].isoformat(),
                    "tasks": list(sess["tasks"]),
                    "network": list(sess["network"]),
                }
                for ip, sess in self._sessions.items()
            }

    def _cleanup_sessions(self) -> None:
        """Remove sessions that have been idle longer than the configured timeout."""
        now = self._now()
        with self._lock:
            expired = [
                ip
                for ip, sess in self._sessions.items()
                if now - sess["last_active"] > self._timeout
            ]
            for ip in expired:
                del self._sessions[ip]

    def _cleanup_loop(self) -> None:
        """Background thread that periodically invokes session cleanup."""
        while not self._stop_event.wait(self._cleanup_interval):
            self._cleanup_sessions()

    def stop(self) -> None:
        """Gracefully stop the background cleanup thread."""
        self._stop_event.set()
        self._cleanup_thread.join()

    # --------------------------------------------------------------------- #
    # WebSocket integration
    # --------------------------------------------------------------------- #
    async def _broadcast_update(
        self, ip: str, category: str, entry: Dict[str, Any]
    ) -> None:
        """
        Send a JSON‑serialisable activity update to every registered WebSocket
        listener. Listeners receive a dict of the form::

            {
                "type": "activity",
                "ip": "<ip>",
                "category": "tasks" | "network",
                "entry": {"timestamp": "...", "detail": "..."}
            }
        """
        if not self._ws_clients:
            return

        message = {
            "type": "activity",
            "ip": ip,
            "category": category,
            "entry": entry,
        }

        # Broadcast without blocking a single slow consumer.
        awaitables = [queue.put(message) for queue in self._ws_clients]
        await asyncio.gather(*awaitables, return_exceptions=True)

    def register_ws(self, queue: asyncio.Queue) -> None:
        """
        Register a new WebSocket listener. The caller should create an
        ``asyncio.Queue`` and forward its items to the client.
        """
        self._ws_clients.add(queue)

    def unregister_ws(self, queue: asyncio.Queue) -> None:
        """Remove a previously registered WebSocket listener."""
        self._ws_clients.discard(queue)


# -------------------------------------------------------------------------
# Helper for FastAPI (or any ASGI framework) – optional but convenient.
# -------------------------------------------------------------------------
async def websocket_endpoint(websocket):
    """
    Example FastAPI WebSocket endpoint that streams live session updates.
    Usage::

        @app.websocket("/ws/sessions")
        async def ws_sessions(ws: WebSocket):
            await websocket_endpoint(ws)
    """
    await websocket.accept()
    queue: asyncio.Queue = asyncio.Queue()
    manager.register_ws(queue)

    try:
        while True:
            msg = await queue.get()
            await websocket.send_json(msg)
    except Exception:
        # Any exception (client disconnect, etc.) ends the loop.
        pass
    finally:
        manager.unregister_ws(queue)
        await websocket.close()


# A module‑level singleton is convenient for the rest of the codebase.
manager = SessionManager()
```
```python
"""
LAN Session Manager
-------------------

Implements per‑IP session tracking, activity logging, segregation of
'Your tasks' vs 'Network activity', session timeout handling and
WebSocket based real‑time updates.

The design is described in ``LAN_SESSION_DESIGN.md``.
"""

import time
import json
import asyncio
from typing import Dict, List, Any

from fastapi import WebSocket

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
SESSION_TIMEOUT = 30 * 60  # 30 minutes inactivity before a session expires
CLEANUP_INTERVAL = 60      # Run cleanup every 60 seconds


# --------------------------------------------------------------------------- #
# Helper data structure representing a single client session
# --------------------------------------------------------------------------- #
class Session:
    """
    Holds all information for a single client identified by its IP address.
    """

    def __init__(self, ip: str):
        self.ip: str = ip
        self.last_activity: float = time.time()
        self.activity_log: List[Dict[str, Any]] = []   # chronological log
        self.tasks: List[Any] = []                     # 'Your tasks' entries
        self.network_activity: List[Any] = []         # 'Network activity' entries

    # ------------------------------------------------------------------- #
    # Internal helpers
    # ------------------------------------------------------------------- #
    def touch(self) -> None:
        """Refresh the last‑activity timestamp."""
        self.last_activity = time.time()

    def is_expired(self) -> bool:
        """Return True if the session has been idle longer than SESSION_TIMEOUT."""
        return (time.time() - self.last_activity) > SESSION_TIMEOUT

    def serialize(self) -> Dict[str, Any]:
        """Convert the session to a JSON‑serialisable dict for WebSocket transport."""
        return {
            "ip": self.ip,
            "last_activity": self.last_activity,
            "tasks": self.tasks,
            "network_activity": self.network_activity,
            "activity_log": self.activity_log,
        }

    # ------------------------------------------------------------------- #
    # Public mutation methods
    # ------------------------------------------------------------------- #
    def add_task(self, task: Any) -> None:
        """Record a task performed by the client."""
        self.touch()
        entry = {"type": "task", "data": task, "timestamp": time.time()}
        self.activity_log.append(entry)
        self.tasks.append(task)

    def add_network(self, activity: Any) -> None:
        """Record a network‑related activity."""
        self.touch()
        entry = {"type": "network", "data": activity, "timestamp": time.time()}
        self.activity_log.append(entry)
        self.network_activity.append(activity)


# --------------------------------------------------------------------------- #
# Core manager exposing the required API
# --------------------------------------------------------------------------- #
class SessionManager:
    """
    Central manager that tracks sessions per IP, provides CRUD‑style
    access, handles automatic timeout cleanup and pushes updates to
    any connected WebSocket client.
    """

    def __init__(self):
        # Mapping from IP address -> Session instance
        self._sessions: Dict[str, Session] = {}

        # Active WebSocket connections that receive real‑time updates
        self._ws_clients: List[WebSocket] = []

        # Kick off the background cleanup coroutine
        asyncio.create_task(self._cleanup_loop())

    # ------------------------------------------------------------------- #
    # Session lookup / creation
    # ------------------------------------------------------------------- #
    def _get_or_create(self, ip: str) -> Session:
        """Return an existing session for *ip* or create a fresh one."""
        if ip not in self._sessions:
            self._sessions[ip] = Session(ip)
        return self._sessions[ip]

    # ------------------------------------------------------------------- #
    # Public recording API
    # ------------------------------------------------------------------- #
    def record_task(self, ip: str, task: Any) -> None:
        """
        Record a user‑initiated task for the given *ip*.
        Triggers an asynchronous broadcast to all WebSocket listeners.
        """
        session = self._get_or_create(ip)
        session.add_task(task)
        asyncio.create_task(self._broadcast(session))

    def record_network(self, ip: str, activity: Any) -> None:
        """
        Record a network‑related activity for the given *ip*.
        Triggers an asynchronous broadcast to all WebSocket listeners.
        """
        session = self._get_or_create(ip)
        session.add_network(activity)
        asyncio.create_task(self._broadcast(session))

    # ------------------------------------------------------------------- #
    # Query helpers
    # ------------------------------------------------------------------- #
    def get_session(self, ip: str) -> Session | None:
        """Return the Session object for *ip* or ``None`` if it does not exist."""
        return self._sessions.get(ip)

    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Return a list of serialised sessions – convenient for dashboards."""
        return [s.serialize() for s in self._sessions.values()]

    # ------------------------------------------------------------------- #
    # WebSocket integration
    # ------------------------------------------------------------------- #
    async def register_ws(self, websocket: WebSocket) -> None:
        """
        Register a new WebSocket client. The socket receives an initial snapshot
        of all sessions and thereafter incremental ``session_update`` messages.
        """
        await websocket.accept()
        self._ws_clients.append(websocket)

        # Send a full snapshot so the client can render the current state.
        await websocket.send_text(
            json.dumps({"type": "snapshot", "sessions": self.get_all_sessions()})
        )

        try:
            while True:
                # Keep the connection alive – we simply await any inbound message.
                # Clients may send ping/pong or a close command.
                await websocket.receive_text()
        except Exception:
            # Any exception (including disconnect) results in cleanup.
            pass
        finally:
            if websocket in self._ws_clients:
                self._ws_clients.remove(websocket)

    async def _broadcast(self, session: Session) -> None:
        """
        Push a JSON payload describing the updated *session* to all active
        WebSocket connections. Faulty connections are pruned.
        """
        if not self._ws_clients:
            return

        payload = json.dumps(
            {"type": "session_update", "session": session.serialize()}
        )
        dead_clients: List[WebSocket] = []
        for ws in self._ws_clients:
            try:
                await ws.send_text(payload)
            except Exception:
                dead_clients.append(ws)

        # Remove dead connections
        for ws in dead_clients:
            if ws in self._ws_clients:
                self._ws_clients.remove(ws)

    # ------------------------------------------------------------------- #
    # Background cleanup
    # ------------------------------------------------------------------- #
    async def _cleanup_loop(self) -> None:
        """
        Periodically scans the session table and discards any session that
        has been idle longer than ``SESSION_TIMEOUT``. A removal also triggers
        a broadcast so the UI can drop the stale entry.
        """
        while True:
            await asyncio.sleep(CLEANUP_INTERVAL)
            expired_ips = [
                ip for ip, sess in self._sessions.items() if sess.is_expired()
            ]
            for ip in expired_ips:
                sess = self._sessions.pop(ip)
                # Notify clients that the session disappeared.
                await self._broadcast_expiration(sess)

    async def _broadcast_expiration(self, session: Session) -> None:
        """Inform WebSocket listeners that *session* has been removed."""
        if not self._ws_clients:
            return
        payload = json.dumps({"type": "session_removed", "ip": session.ip})
        dead_clients: List[WebSocket] = []
        for ws in self._ws_clients:
            try:
                await ws.send_text(payload)
            except Exception:
                dead_clients.append(ws)
        for ws in dead_clients:
            if ws in self._ws_clients:
                self._ws_clients.remove(ws)


# --------------------------------------------------------------------------- #
# Global singleton – importable by the rest of the application
# --------------------------------------------------------------------------- #
session_manager = SessionManager()
```
```python
"""
lan_session_manager.py
----------------------
Implements a LAN‑wide session manager with per‑IP isolation, activity logging,
automatic timeout cleanup, and optional WebSocket broadcasting for real‑time
updates to a dashboard.
"""

import asyncio
import json
import threading
import time
from typing import Dict, List, Any

# Optional import – if the `websockets` package is not installed the
# WebSocket functionality will be disabled but the core manager will still work.
try:
    import websockets
except Exception:  # pragma: no cover
    websockets = None  # type: ignore


class SessionManager:
    """
    Singleton manager that tracks sessions per client IP.

    Each session contains two segregated logs:
        * ``tasks`` – actions initiated by the user (“Your tasks”)
        * ``network`` – observed network activity (“Network activity”)

    Sessions automatically expire after ``timeout_seconds`` of inactivity.
    """
    _instance = None
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, timeout_seconds: int = 300) -> "SessionManager":
        """Return the global singleton, creating it on first use."""
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls(timeout_seconds=timeout_seconds)
            return cls._instance

    def __init__(self, timeout_seconds: int = 300):
        # Private – use ``instance()`` to obtain the manager.
        self.timeout_seconds = timeout_seconds
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._stop_cleanup = threading.Event()
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True, name="SessionCleanupThread"
        )
        self._cleanup_thread.start()

    # --------------------------------------------------------------------- #
    # Session handling
    # --------------------------------------------------------------------- #
    def _ensure_session(self, ip: str) -> Dict[str, Any]:
        """Create a new session dict for *ip* if it does not exist yet."""
        with self._lock:
            if ip not in self._sessions:
                self._sessions[ip] = {
                    "last_active": time.time(),
                    "tasks": [],          # “Your tasks”
                    "network": [],        # “Network activity”
                }
            return self._sessions[ip]

    def _touch(self, ip: str) -> None:
        """Refresh the ``last_active`` timestamp for *ip*."""
        with self._lock:
            session = self._ensure_session(ip)
            session["last_active"] = time.time()

    def add_task(self, ip: str, task: Dict[str, Any]) -> None:
        """
        Record a user‑initiated task for the given *ip*.

        ``task`` should be a JSON‑serialisable mapping describing the action.
        """
        with self._lock:
            session = self._ensure_session(ip)
            session["tasks"].append({"timestamp": time.time(), "detail": task})
            self._touch(ip)

    def add_network_activity(self, ip: str, activity: Dict[str, Any]) -> None:
        """
        Record observed network activity for the given *ip*.

        ``activity`` should be a JSON‑serialisable mapping.
        """
        with self._lock:
            session = self._ensure_session(ip)
            session["network"].append({"timestamp": time.time(), "detail": activity})
            self._touch(ip)

    def get_session(self, ip: str) -> Dict[str, Any]:
        """Return a **copy** of the session data for *ip* (or an empty dict)."""
        with self._lock:
            session = self._sessions.get(ip)
            if not session:
                return {}
            # shallow copy is enough – inner lists are not mutated outside.
            return {
                "tasks": list(session["tasks"]),
                "network": list(session["network"]),
                "last_active": session["last_active"],
            }

    def get_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Return a snapshot of all sessions (IP → session dict)."""
        with self._lock:
            return {
                ip: {
                    "tasks": list(data["tasks"]),
                    "network": list(data["network"]),
                    "last_active": data["last_active"],
                }
                for ip, data in self._sessions.items()
            }

    # --------------------------------------------------------------------- #
    # Cleanup
    # --------------------------------------------------------------------- #
    def _cleanup_loop(self) -> None:
        """Background thread that removes stale sessions."""
        while not self._stop_cleanup.is_set():
            now = time.time()
            with self._lock:
                stale_ips = [
                    ip
                    for ip, sess in self._sessions.items()
                    if now - sess["last_active"] > self.timeout_seconds
                ]
                for ip in stale_ips:
                    del self._sessions[ip]
            # Sleep half the timeout to keep cleanup responsive but not busy.
            self._stop_cleanup.wait(self.timeout_seconds / 2)

    def shutdown(self) -> None:
        """Stop the cleanup thread – useful for graceful application exit."""
        self._stop_cleanup.set()
        self._cleanup_thread.join()

    # --------------------------------------------------------------------- #
    # WebSocket broadcasting
    # --------------------------------------------------------------------- #
    async def _ws_broadcast(self, websocket, path):
        """
        WebSocket handler that pushes the full session snapshot to each client
        once per second.  The client side (dashboard) can decide how to render
        the data.
        """
        try:
            while True:
                snapshot = self.get_all_sessions()
                await websocket.send(json.dumps(snapshot))
                await asyncio.sleep(1)
        except (asyncio.CancelledError, websockets.ConnectionClosed):
            # Normal termination – just exit the coroutine.
            pass

    def start_websocket_server(self, host: str = "0.0.0.0", port: int = 8765) -> None:
        """
        Spin up an ``asyncio`` WebSocket server in a background thread.
        If the ``websockets`` library is unavailable this method becomes a no‑op.
        """
        if websockets is None:  # pragma: no cover
            raise RuntimeError(
                "The 'websockets' package is required for real‑time updates."
            )

        def _run_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            start_server = websockets.serve(self._ws_broadcast, host, port)
            server = loop.run_until_complete(start_server)
            try:
                loop.run_forever()
            finally:
                server.close()
                loop.run_until_complete(server.wait_closed())
                loop.close()

        thread = threading.Thread(
            target=_run_loop, daemon=True, name="SessionWebSocketThread"
        )
        thread.start()


# ------------------------------------------------------------------------- #
# Convenience shortcut for modules that import this file directly.
# ------------------------------------------------------------------------- #
session_manager = SessionManager.instance()
```
import asyncio
import datetime
from typing import Dict, List, Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

# ----------------------------------------------------------------------
# Session data structures
# ----------------------------------------------------------------------
class Session:
    """
    Holds information for a single IP session.
    """
    def __init__(self, ip: str):
        self.ip: str = ip
        self.tasks: List[Dict[str, Any]] = []          # "Your tasks"
        self.network_activity: List[Dict[str, Any]] = []  # "Network activity"
        self.last_active: datetime.datetime = datetime.datetime.utcnow()

    def touch(self):
        self.last_active = datetime.datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ip": self.ip,
            "tasks": self.tasks,
            "network_activity": self.network_activity,
            "last_active": self.last_active.isoformat(),
        }

# ----------------------------------------------------------------------
# Connection manager for WebSocket clients
# ----------------------------------------------------------------------
class ConnectionManager:
    """
    Manages active WebSocket connections and broadcasts session updates.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                dead_connections.append(connection)
        for dc in dead_connections:
            self.disconnect(dc)

# ----------------------------------------------------------------------
# Core SessionManager
# ----------------------------------------------------------------------
class SessionManager:
    """
    Tracks sessions per IP, logs activity, and handles timeout cleanup.
    Provides real‑time updates via WebSocket.
    """
    def __init__(self, timeout_seconds: int = 300):
        self._sessions: Dict[str, Session] = {}
        self._lock = asyncio.Lock()
        self.timeout_seconds = timeout_seconds
        self.conn_manager = ConnectionManager()
        self.router = APIRouter()
        self._setup_routes()
        # launch background tasks
        asyncio.create_task(self._periodic_cleanup())
        asyncio.create_task(self._periodic_broadcast())

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    async def get_session(self, ip: str) -> Session:
        async with self._lock:
            session = self._sessions.get(ip)
            if not session:
                session = Session(ip)
                self._sessions[ip] = session
            session.touch()
            return session

    async def log_task(self, ip: str, task_info: Dict[str, Any]):
        """
        Log a user‑level task under "Your tasks".
        """
        session = await self.get_session(ip)
        async with self._lock:
            session.tasks.append({
                "timestamp": datetime.datetime.utcnow().isoformat(),
                **task_info,
            })
            session.touch()

    async def log_network(self, ip: str, net_info: Dict[str, Any]):
        """
        Log a network‑level event under "Network activity".
        """
        session = await self.get_session(ip)
        async with self._lock:
            session.network_activity.append({
                "timestamp": datetime.datetime.utcnow().isoformat(),
                **net_info,
            })
            session.touch()

    async def snapshot(self) -> List[Dict[str, Any]]:
        """
        Return a list of all active sessions for UI consumption.
        """
        async with self._lock:
            return [s.to_dict() for s in self._sessions.values()]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    async def _periodic_cleanup(self):
        """
        Remove sessions that have been idle longer than ``timeout_seconds``.
        Runs forever in the background.
        """
        while True:
            await asyncio.sleep(self.timeout_seconds // 2)
            now = datetime.datetime.utcnow()
            async with self._lock:
                stale_ips = [
                    ip for ip, sess in self._sessions.items()
                    if (now - sess.last_active).total_seconds() > self.timeout_seconds
                ]
                for ip in stale_ips:
                    del self._sessions[ip]

    async def _periodic_broadcast(self):
        """
        Broadcast the current session snapshot to all connected WebSocket clients
        every few seconds.
        """
        while True:
            await asyncio.sleep(2)  # frequency of UI updates
            snapshot = await self.snapshot()
            await self.conn_manager.broadcast(message=json.dumps(snapshot))

    # ------------------------------------------------------------------
    # FastAPI router & WebSocket endpoint
    # ------------------------------------------------------------------
    def _setup_routes(self):
        @self.router.websocket("/ws/sessions")
        async def websocket_endpoint(websocket: WebSocket):
            await self.conn_manager.connect(websocket)
            try:
                # Keep connection alive; we don't expect inbound messages.
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                self.conn_manager.disconnect(websocket)
            except Exception:
                self.conn_manager.disconnect(websocket)

        @self.router.get("/sessions/snapshot")
        async def get_snapshot():
            """
            HTTP endpoint returning the current session snapshot (useful for
            initial page load before WebSocket updates start).
            """
            return await self.snapshot()

# Instantiate a global manager that can be imported elsewhere
session_manager = SessionManager()
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any

from fastapi import WebSocket, WebSocketDisconnect


class Session:
    """
    Holds per‑IP session data.
    - ``tasks`` stores user‑level activity (your “tasks”).
    - ``network_activity`` stores low‑level LAN traffic logs (your “network activity”).
    """
    def __init__(self, ip: str):
        self.ip: str = ip
        self.last_active: datetime = datetime.utcnow()
        self.tasks: List[Dict[str, Any]] = []
        self.network_activity: List[Dict[str, Any]] = []

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the session for the dashboard / WS broadcast."""
        return {
            "ip": self.ip,
            "last_active": self.last_active.isoformat(),
            "tasks": self.tasks,
            "network_activity": self.network_activity,
        }


class SessionManager:
    """
    LAN Session Manager

    Features
    --------
    * Per‑IP session tracking.
    * Separate logs for “Your tasks” and “Network activity”.
    * Automatic timeout/cleanup of idle sessions.
    * WebSocket broadcast for real‑time dashboard updates.
    """
    def __init__(self, timeout_seconds: int = 300):
        self.sessions: Dict[str, Session] = {}
        self.timeout: timedelta = timedelta(seconds=timeout_seconds)

        # Connected WebSocket clients that receive live updates
        self._ws_clients: List[WebSocket] = []

        # Fire‑and‑forget the background cleanup coroutine
        asyncio.create_task(self._cleanup_loop())

    # --------------------------------------------------------------------- #
    # Session handling helpers
    # --------------------------------------------------------------------- #
    def _get_or_create(self, ip: str) -> Session:
        """Return existing Session for *ip* or create a new one."""
        if ip not in self.sessions:
            self.sessions[ip] = Session(ip)
        return self.sessions[ip]

    # --------------------------------------------------------------------- #
    # Public logging API
    # --------------------------------------------------------------------- #
    def log_task(self, ip: str, task: Dict[str, Any]) -> None:
        """
        Record a high‑level user task for the given *ip*.

        ``task`` is a free‑form dict describing the operation (e.g. ``{"action":
        "open_file", "file": "notes.txt"}``).
        """
        sess = self._get_or_create(ip)
        sess.tasks.append({
            "timestamp": datetime.utcnow().isoformat(),
            **task,
        })
        sess.last_active = datetime.utcnow()
        asyncio.create_task(self._broadcast())

    def log_network(self, ip: str, activity: Dict[str, Any]) -> None:
        """
        Record low‑level network activity for the given *ip*.

        ``activity`` could contain fields like ``{"src": "...", "dst": "...",
        "protocol": "TCP", "size": 128}``.
        """
        sess = self._get_or_create(ip)
        sess.network_activity.append({
            "timestamp": datetime.utcnow().isoformat(),
            **activity,
        })
        sess.last_active = datetime.utcnow()
        asyncio.create_task(self._broadcast())

    # --------------------------------------------------------------------- #
    # WebSocket support
    # --------------------------------------------------------------------- #
    async def _broadcast(self) -> None:
        """Push the current dashboard payload to every connected WS client."""
        payload = self.dashboard_data()
        dead_clients: List[WebSocket] = []
        for ws in self._ws_clients:
            try:
                await ws.send_json(payload)
            except Exception:
                dead_clients.append(ws)
        # Clean up any clients that raised during send
        for ws in dead_clients:
            self._ws_clients.remove(ws)

    async def websocket_endpoint(self, websocket: WebSocket) -> None:
        """
        FastAPI WebSocket endpoint.

        Clients connect, receive JSON updates whenever a session changes,
        and stay alive until they disconnect.
        """
        await websocket.accept()
        self._ws_clients.append(websocket)
        try:
            while True:
                # We only care about keeping the connection alive.
                await websocket.receive_text()
        except WebSocketDisconnect:
            self._ws_clients.remove(websocket)

    # --------------------------------------------------------------------- #
    # Dashboard payload
    # --------------------------------------------------------------------- #
    def dashboard_data(self) -> Dict[str, Any]:
        """Return a serialisable snapshot of all active sessions."""
        return {"sessions": [s.to_dict() for s in self.sessions.values()]}

    # --------------------------------------------------------------------- #
    # Session timeout / cleanup
    # --------------------------------------------------------------------- #
    async def _cleanup_loop(self) -> None:
        """Background task that purges stale sessions."""
        while True:
            now = datetime.utcnow()
            stale_ips = [
                ip for ip, sess in self.sessions.items()
                if now - sess.last_active > self.timeout
            ]
            for ip in stale_ips:
                del self.sessions[ip]
            # Sleep for half the timeout period – a good trade‑off between
            # responsiveness and CPU usage.
            await asyncio.sleep(self.timeout.total_seconds() / 2)
import asyncio
import json
import time
from typing import Dict, List, Any

class SessionManager:
    """
    Manages LAN sessions per client IP.
    - Tracks per‑IP activity (tasks vs network activity)
    - Provides an activity log per session
    - Handles automatic timeout cleanup
    - Supplies real‑time data for WebSocket consumers
    """

    def __init__(self, timeout_seconds: int = 300, cleanup_interval: int = 60):
        """
        :param timeout_seconds: seconds of inactivity after which a session is discarded
        :param cleanup_interval: how often (seconds) the cleanup coroutine runs
        """
        self.timeout = timeout_seconds
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup(cleanup_interval))

    def _ensure_session(self, ip: str) -> Dict[str, Any]:
        """Create a new session entry for the IP if it does not exist."""
        if ip not in self.sessions:
            self.sessions[ip] = {
                "ip": ip,
                "created_at": time.time(),
                "last_active": time.time(),
                "tasks": [],               # “Your tasks” – user‑initiated actions
                "network_activity": [],   # “Network activity” – system‑generated events
                "log": []                 # chronological activity log
            }
        return self.sessions[ip]

    def log_activity(self, ip: str, category: str, payload: Any) -> None:
        """
        Record an activity for a given IP.

        :param ip: client IP address
        :param category: either "tasks" or "network_activity"
        :param payload: arbitrary JSON‑serialisable data describing the activity
        """
        if category not in ("tasks", "network_activity"):
            raise ValueError("category must be 'tasks' or 'network_activity'")

        session = self._ensure_session(ip)
        timestamp = time.time()
        entry = {"timestamp": timestamp, "category": category, "payload": payload}

        # Append to the appropriate bucket
        session[category].append(entry)
        # Also keep a unified chronological log
        session["log"].append(entry)

        # Refresh activity timer
        session["last_active"] = timestamp

    def get_session(self, ip: str) -> Dict[str, Any]:
        """Return a shallow copy of the session data for the given IP."""
        return self.sessions.get(ip, {}).copy()

    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Return a list of all active sessions (suitable for dashboard rendering)."""
        return [sess.copy() for sess in self.sessions.values()]

    async def _periodic_cleanup(self, interval: int) -> None:
        """Background coroutine that removes stale sessions."""
        while True:
            await asyncio.sleep(interval)
            now = time.time()
            stale_ips = [
                ip for ip, sess in self.sessions.items()
                if now - sess["last_active"] > self.timeout
            ]
            for ip in stale_ips:
                del self.sessions[ip]

    async def shutdown(self) -> None:
        """Cancel the cleanup task – to be called when the application stops."""
        self._cleanup_task.cancel()
        try:
            await self._cleanup_task
        except asyncio.CancelledError:
            pass
import asyncio
import datetime
from typing import Dict, List, Any

# FastAPI imports for WebSocket support
try:
    from fastapi import WebSocket, WebSocketDisconnect
except ImportError:
    # FastAPI may not be installed yet; placeholder for type checking
    WebSocket = Any
    WebSocketDisconnect = Exception

# -------------------------------------------------------------------------
# Session data structures
# -------------------------------------------------------------------------
class _Session:
    """
    Internal representation of a LAN session tied to a specific client IP.
    """
    __slots__ = ("ip", "last_activity", "tasks", "network_activity", "ws_clients")

    def __init__(self, ip: str):
        self.ip: str = ip
        self.last_activity: datetime.datetime = datetime.datetime.utcnow()
        self.tasks: List[Dict[str, Any]] = []               # Your tasks log
        self.network_activity: List[Dict[str, Any]] = []   # Network activity log
        self.ws_clients: List[WebSocket] = []              # Connected WebSocket clients

    def touch(self):
        self.last_activity = datetime.datetime.utcnow()

    def add_task(self, description: str):
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "description": description,
        }
        self.tasks.append(entry)
        self.touch()
        return entry

    def add_network(self, direction: str, payload: Any):
        """
        direction: 'inbound' or 'outbound'
        payload: any serialisable data describing the network packet/event
        """
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "direction": direction,
            "payload": payload,
        }
        self.network_activity.append(entry)
        self.touch()
        return entry

    def to_dict(self) -> Dict[str, Any]:
        """Serialise session for dashboard / WS transmission."""
        return {
            "ip": self.ip,
            "last_activity": self.last_activity.isoformat(),
            "tasks": self.tasks,
            "network_activity": self.network_activity,
        }


# -------------------------------------------------------------------------
# Public SessionManager
# -------------------------------------------------------------------------
class SessionManager:
    """
    Manages per‑IP LAN sessions, activity logs and real‑time WebSocket updates.
    """
    DEFAULT_TIMEOUT_SECONDS = 300  # 5 minutes

    def __init__(self, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS):
        self._sessions: Dict[str, _Session] = {}
        self._timeout = datetime.timedelta(seconds=timeout_seconds)
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    # -----------------------------------------------------------------
    # Session lifecycle
    # -----------------------------------------------------------------
    def _get_or_create(self, ip: str) -> _Session:
        if ip not in self._sessions:
            self._sessions[ip] = _Session(ip)
        return self._sessions[ip]

    def get_session(self, ip: str) -> Dict[str, Any]:
        """
        Return a serialisable snapshot of the session for the given IP.
        """
        session = self._sessions.get(ip)
        if session:
            return session.to_dict()
        return {}

    # -----------------------------------------------------------------
    # Logging helpers
    # -----------------------------------------------------------------
    def log_task(self, ip: str, description: str) -> Dict[str, Any]:
        """
        Record a user‑initiated task under the 'Your tasks' bucket.
        """
        session = self._get_or_create(ip)
        entry = session.add_task(description)
        asyncio.create_task(self._broadcast(ip, {"type": "task", "data": entry}))
        return entry

    def log_network(self, ip: str, direction: str, payload: Any) -> Dict[str, Any]:
        """
        Record a network event under the 'Network activity' bucket.
        """
        session = self._get_or_create(ip)
        entry = session.add_network(direction, payload)
        asyncio.create_task(self._broadcast(ip, {"type": "network", "data": entry}))
        return entry

    # -----------------------------------------------------------------
    # WebSocket handling
    # -----------------------------------------------------------------
    async def register_ws(self, ip: str, websocket: WebSocket):
        """
        Attach a WebSocket client to a session. Called when a client connects.
        """
        await websocket.accept()
        session = self._get_or_create(ip)
        session.ws_clients.append(websocket)
        # Push current snapshot immediately
        await websocket.send_json({"type": "snapshot", "data": session.to_dict()})

    async def unregister_ws(self, ip: str, websocket: WebSocket):
        """Remove a WebSocket client from a session."""
        session = self._sessions.get(ip)
        if session and websocket in session.ws_clients:
            session.ws_clients.remove(websocket)

    async def _broadcast(self, ip: str, message: Dict[str, Any]):
        """
        Send a JSON message to all WebSocket clients attached to the session.
        Silently drop connections that raise errors and clean them up.
        """
        session = self._sessions.get(ip)
        if not session:
            return
        dead: List[WebSocket] = []
        for ws in session.ws_clients:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            await self.unregister_ws(ip, ws)

    async def websocket_endpoint(self, websocket: WebSocket, ip: str):
        """
        FastAPI‑compatible WebSocket endpoint.
        Usage example:
            @app.websocket("/ws/{client_ip}")
            async def ws_endpoint(ws: WebSocket, client_ip: str):
                await session_manager.websocket_endpoint(ws, client_ip)
        """
        await self.register_ws(ip, websocket)
        try:
            while True:
                # Keep the connection alive; we don't expect inbound messages,
                # but we read to detect disconnects.
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        finally:
            await self.unregister_ws(ip, websocket)

    # -----------------------------------------------------------------
    # Session timeout / cleanup
    # -----------------------------------------------------------------
    async def _periodic_cleanup(self):
        """
        Background task that purges stale sessions every minute.
        """
        while True:
            now = datetime.datetime.utcnow()
            stale_ips = [
                ip for ip, sess in self._sessions.items()
                if now - sess.last_activity > self._timeout
            ]
            for ip in stale_ips:
                del self._sessions[ip]
            await asyncio.sleep(60)

    # -----------------------------------------------------------------
    # Utility
    # -----------------------------------------------------------------
    def active_sessions(self) -> List[Dict[str, Any]]:
        """Return a list of snapshot dicts for all active sessions."""
        return [s.to_dict() for s in self._sessions.values()]

# -------------------------------------------------------------------------
# Instantiate a global manager for import‑side usage
# -------------------------------------------------------------------------
session_manager = SessionManager()
import asyncio
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set, Any

import websockets

# ----------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------
@dataclass
class ActivityRecord:
    timestamp: float
    category: str   # "task" or "network"
    description: str

@dataclass
class Session:
    ip: str
    last_active: float = field(default_factory=lambda: time.time())
    activities: List[ActivityRecord] = field(default_factory=list)

    def log(self, category: str, description: str) -> None:
        self.last_active = time.time()
        self.activities.append(
            ActivityRecord(timestamp=self.last_active,
                           category=category,
                           description=description)
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ip": self.ip,
            "last_active": self.last_active,
            "activities": [
                {
                    "timestamp": a.timestamp,
                    "category": a.category,
                    "description": a.description,
                }
                for a in self.activities
            ],
        }

# ----------------------------------------------------------------------
# Session Manager
# ----------------------------------------------------------------------
class SessionManager:
    """
    Manages LAN sessions per IP address.
    - Tracks activity logs separated into "task" and "network" categories.
    - Handles session timeout cleanup.
    - Provides real‑time updates via WebSocket.
    """
    def __init__(self,
                 timeout_seconds: int = 300,
                 ws_host: str = "0.0.0.0",
                 ws_port: int = 8765):
        self._sessions: Dict[str, Session] = {}
        self._timeout = timeout_seconds
        self._ws_host = ws_host
        self._ws_port = ws_port
        self._ws_clients: Set[websockets.WebSocketServerProtocol] = set()
        self._cleanup_task: asyncio.Task | None = None
        self._ws_server: websockets.server.Serve | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_sessions_snapshot(self) -> List[Dict[str, Any]]:
        """Return a snapshot of all sessions suitable for JSON serialization."""
        return [s.to_dict() for s in self._sessions.values()]

    def log_activity(self,
                     ip: str,
                     category: str,
                     description: str) -> None:
        """
        Record an activity for a given IP.
        ``category`` must be either "task" or "network".
        """
        if category not in {"task", "network"}:
            raise ValueError("category must be 'task' or 'network'")

        session = self._sessions.get(ip)
        if not session:
            session = Session(ip=ip)
            self._sessions[ip] = session

        session.log(category, description)
        # push update to all WebSocket listeners
        asyncio.create_task(self._broadcast_update())

    async def start(self) -> None:
        """Start background cleanup and WebSocket server."""
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
        self._ws_server = await websockets.serve(
            self._ws_handler, self._ws_host, self._ws_port
        )
        print(f"[SessionManager] WebSocket listening on ws://{self._ws_host}:{self._ws_port}")

    async def stop(self) -> None:
        """Gracefully stop background tasks and WebSocket server."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        if self._ws_server:
            self._ws_server.close()
            await self._ws_server.wait_closed()

        # close all client connections
        await asyncio.gather(
            *(client.close() for client in self._ws_clients),
            return_exceptions=True
        )
        self._ws_clients.clear()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    async def _periodic_cleanup(self) -> None:
        """Remove sessions that have been idle longer than the timeout."""
        while True:
            now = time.time()
            expired_ips = [
                ip for ip, sess in self._sessions.items()
                if now - sess.last_active > self._timeout
            ]
            for ip in expired_ips:
                del self._sessions[ip]
            if expired_ips:
                await self._broadcast_update()
            await asyncio.sleep(self._timeout // 2)

    async def _ws_handler(self,
                          websocket: websockets.WebSocketServerProtocol,
                          path: str) -> None:
        """Handle a new WebSocket client."""
        self._ws_clients.add(websocket)
        try:
            # Send initial snapshot
            await websocket.send(json.dumps({
                "type": "snapshot",
                "sessions": self.get_sessions_snapshot()
            }))

            # Keep connection open; we don't expect inbound messages
            async for _ in websocket:
                pass
        finally:
            self._ws_clients.discard(websocket)

    async def _broadcast_update(self) -> None:
        """Send the latest session state to all connected WebSocket clients."""
        if not self._ws_clients:
            return
        message = json.dumps({
            "type": "update",
            "sessions": self.get_sessions_snapshot()
        })
        await asyncio.gather(
            *(client.send(message) for client in self._ws_clients),
            return_exceptions=True
        )
import asyncio
import datetime
import json
import threading
from collections import defaultdict
from typing import Dict, List, Set

import websockets

# ----------------------------------------------------------------------
# Session data structures
# ----------------------------------------------------------------------
class Session:
    """Tracks per‑IP session state, activity logs and last activity timestamp."""
    def __init__(self, ip: str):
        self.ip: str = ip
        self.last_active: datetime.datetime = datetime.datetime.utcnow()
        self.tasks: List[Dict] = []          # “Your tasks” logs
        self.network: List[Dict] = []        # “Network activity” logs

    def touch(self):
        """Refresh the last‑active timestamp."""
        self.last_active = datetime.datetime.utcnow()

    def log_task(self, description: str):
        """Add a task entry to the session."""
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "description": description
        }
        self.tasks.append(entry)
        self.touch()
        return entry

    def log_network(self, direction: str, payload: dict):
        """Add a network activity entry to the session."""
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "direction": direction,   # 'inbound' or 'outbound'
            "payload": payload
        }
        self.network.append(entry)
        self.touch()
        return entry

    def to_dict(self):
        """Serialise the session for WebSocket transmission."""
        return {
            "ip": self.ip,
            "last_active": self.last_active.isoformat(),
            "tasks": self.tasks,
            "network": self.network
        }

# ----------------------------------------------------------------------
# Session manager
# ----------------------------------------------------------------------
class SessionManager:
    """
    Core manager that:
      • Tracks a Session object per client IP.
      • Provides separate logs for “Your tasks” and “Network activity”.
      • Handles automatic timeout/expiry of idle sessions.
      • Pushes real‑time updates to connected WebSocket clients.
    """
    DEFAULT_TIMEOUT_SECONDS = 300   # 5 minutes of inactivity

    def __init__(self, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS):
        self.sessions: Dict[str, Session] = {}
        self.timeout_seconds = timeout_seconds
        self._ws_clients: Set[websockets.WebSocketServerProtocol] = set()
        self._cleanup_thread = threading.Thread(target=self._periodic_cleanup, daemon=True)
        self._cleanup_thread.start()

    # ------------------------------------------------------------------
    # Session lookup / creation
    # ------------------------------------------------------------------
    def _get_or_create(self, ip: str) -> Session:
        if ip not in self.sessions:
            self.sessions[ip] = Session(ip)
        return self.sessions[ip]

    def get_session(self, ip: str) -> Session:
        """Public accessor – returns a session (creates if missing)."""
        return self._get_or_create(ip)

    # ------------------------------------------------------------------
    # Logging helpers
    # ------------------------------------------------------------------
    def log_task(self, ip: str, description: str) -> Dict:
        """Record a task under the “Your tasks” bucket."""
        session = self._get_or_create(ip)
        entry = session.log_task(description)
        asyncio.run_coroutine_threadsafe(self._broadcast(session), asyncio.get_event_loop())
        return entry

    def log_network(self, ip: str, direction: str, payload: dict) -> Dict:
        """Record a network event under the “Network activity” bucket."""
        session = self._get_or_create(ip)
        entry = session.log_network(direction, payload)
        asyncio.run_coroutine_threadsafe(self._broadcast(session), asyncio.get_event_loop())
        return entry

    # ------------------------------------------------------------------
    # Timeout / cleanup
    # ------------------------------------------------------------------
    def _periodic_cleanup(self):
        """Background thread that purges sessions idle longer than the timeout."""
        while True:
            now = datetime.datetime.utcnow()
            expired_ips = [
                ip for ip, sess in self.sessions.items()
                if (now - sess.last_active).total_seconds() > self.timeout_seconds
            ]
            for ip in expired_ips:
                del self.sessions[ip]
            # Sleep a short interval; too frequent would waste CPU, too sparse would delay cleanup.
            threading.Event().wait(30)

    # ------------------------------------------------------------------
    # WebSocket support
    # ------------------------------------------------------------------
    async def _handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Register a new client, keep the connection alive, and clean up on disconnect."""
        self._ws_clients.add(websocket)
        try:
            # Send an initial snapshot of all current sessions
            await websocket.send(json.dumps({
                "type": "snapshot",
                "sessions": [s.to_dict() for s in self.sessions.values()]
            }))
            async for _ in websocket:
                # The server is push‑only; we simply discard any client messages.
                pass
        finally:
            self._ws_clients.remove(websocket)

    async def _broadcast(self, session: Session):
        """Push the latest session state to every connected WebSocket client."""
        if not self._ws_clients:
            return
        message = json.dumps({
            "type": "update",
            "session": session.to_dict()
        })
        await asyncio.wait([client.send(message) for client in self._ws_clients])

    def start_websocket_server(self, host: str = "0.0.0.0", port: int = 8765):
        """
        Launch the WebSocket server in an asyncio event loop.
        Call this once from the main entry‑point of the application.
        """
        loop = asyncio.get_event_loop()
        server = websockets.serve(self._handler, host, port)
        loop.run_until_complete(server)
        # Run the loop in a background thread so the rest of the app can continue.
        threading.Thread(target=loop.run_forever, daemon=True).start()
import asyncio
import json
import threading
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any

# Optional: If the project uses FastAPI for WebSocket handling, import here.
# from fastapi import WebSocket

class SessionManager:
    """
    LAN Session Manager:
    - Tracks sessions per client IP.
    - Logs two separate activity streams: "Your tasks" and "Network activity".
    - Handles session timeout and automatic cleanup.
    - Provides WebSocket registration for real‑time dashboard updates.
    """

    def __init__(self, timeout_seconds: int = 300, cleanup_interval: int = 60):
        """
        :param timeout_seconds: Seconds of inactivity after which a session is discarded.
        :param cleanup_interval: How often (seconds) the cleanup thread runs.
        """
        self.timeout = timedelta(seconds=timeout_seconds)
        self.sessions: Dict[str, Dict[str, Any]] = defaultdict(self._new_session)
        self._lock = threading.Lock()
        self._cleanup_interval = cleanup_interval
        self._stop_event = threading.Event()
        self._cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
        self._cleanup_thread.start()

    def _new_session(self) -> Dict[str, Any]:
        """Factory for a fresh session dictionary."""
        return {
            "last_active": datetime.utcnow(),
            "tasks": [],               # List of dicts: {"ts": ..., "desc": ...}
            "network_activity": [],   # List of dicts: {"ts": ..., "desc": ...}
            "sockets": set(),          # Set of WebSocket objects for real‑time push
        }

    # ----------------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------------
    def update_activity(self, ip: str, category: str, description: str) -> None:
        """
        Record an activity for a given IP.

        :param ip: Client IP address.
        :param category: Either "tasks" (Your tasks) or "network" (Network activity).
        :param description: Human‑readable description of the event.
        """
        if category not in ("tasks", "network"):
            raise ValueError("category must be 'tasks' or 'network'")

        now = datetime.utcnow()
        entry = {"ts": now.isoformat() + "Z", "desc": description}

        with self._lock:
            session = self.sessions[ip]
            session["last_active"] = now
            if category == "tasks":
                session["tasks"].append(entry)
            else:
                session["network_activity"].append(entry)

            # Push update to any registered websockets for this IP
            asyncio.run(self._push_update(ip, category, entry))

    def get_session(self, ip: str) -> Dict[str, Any]:
        """Return a shallow copy of the session data for the given IP."""
        with self._lock:
            session = self.sessions.get(ip)
            if not session:
                return {}
            # Return copies to avoid external mutation
            return {
                "last_active": session["last_active"],
                "tasks": list(session["tasks"]),
                "network_activity": list(session["network_activity"]),
            }

    def register_socket(self, ip: str, websocket) -> None:
        """
        Register a WebSocket connection for real‑time updates.

        The caller is responsible for closing the socket; on close,
        ``unregister_socket`` should be called.
        """
        with self._lock:
            self.sessions[ip]["sockets"].add(websocket)

    def unregister_socket(self, ip: str, websocket) -> None:
        """Remove a previously registered WebSocket."""
        with self._lock:
            self.sessions[ip]["sockets"].discard(websocket)

    def stop(self) -> None:
        """Gracefully stop the background cleanup thread."""
        self._stop_event.set()
        self._cleanup_thread.join()

    # ----------------------------------------------------------------------
    # Internal helpers
    # ----------------------------------------------------------------------
    async def _push_update(self, ip: str, category: str, entry: Dict[str, str]) -> None:
        """
        Send a JSON payload to all websockets registered for *ip*.

        Payload format:
        {
            "type": "update",
            "category": "tasks" | "network",
            "entry": {"ts": "...", "desc": "..."}
        }
        """
        payload = json.dumps({
            "type": "update",
            "category": category,
            "entry": entry,
        })

        # Snapshot the socket set to avoid race conditions while iterating.
        with self._lock:
            sockets = list(self.sessions[ip]["sockets"])

        # Fire‑and‑forget each send; ignore failures (they will be cleaned up on close).
        await asyncio.gather(
            *(self._safe_send(ws, payload) for ws in sockets),
            return_exceptions=True,
        )

    async def _safe_send(self, websocket, payload: str) -> None:
        """Attempt to send payload; silently ignore closed sockets."""
        try:
            await websocket.send_text(payload)
        except Exception:
            # Assume the socket is dead; let the caller clean it up later.
            pass

    def _cleanup_worker(self) -> None:
        """Background thread that removes stale sessions."""
        while not self._stop_event.is_set():
            self._remove_expired_sessions()
            self._stop_event.wait(self._cleanup_interval)

    def _remove_expired_sessions(self) -> None:
        """Delete sessions that have been idle longer than the timeout."""
        now = datetime.utcnow()
        with self._lock:
            expired_ips = [
                ip for ip, sess in self.sessions.items()
                if now - sess["last_active"] > self.timeout
            ]
            for ip in expired_ips:
                # Close any lingering websockets gracefully
                for ws in self.sessions[ip]["sockets"]:
                    try:
                        # If the websocket object has an async close method, schedule it.
                        asyncio.run(ws.close())
                    except Exception:
                        pass
                del self.sessions[ip]

# ----------------------------------------------------------------------
# WebSocket endpoint example (FastAPI style)
# ----------------------------------------------------------------------
# The following coroutine can be wired into a FastAPI app like:
#   @app.websocket("/ws/{client_ip}")
#   async def ws_endpoint(websocket: WebSocket, client_ip: str):
#       await websocket.accept()
#       manager.register_socket(client_ip, websocket)
#       try:
#           while True:
#               await websocket.receive_text()  # keep connection alive
#       finally:
#           manager.unregister_socket(client_ip, websocket)

# Instantiate a global manager for the application.
manager = SessionManager()