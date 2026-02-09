# remote_execution_relay.py
"""
Remote Execution Relay Server

- Listens for inbound TCP connections from clients.
- Validates that the incoming payload contains a known machine_id.
- Performs a very lightweight *scope validation* (only a whitelist of safe commands).
- Executes the command **on the server itself** for the demo.
  In a real deployment you would forward the request to the originating
  machine (e.g., via SSH, a reverse tunnel, or a peer‑to‑peer channel).
- Sends the execution result back to the originating client.

Security notes:
* Replace the plain socket with TLS (e.g., `ssl.wrap_socket`).
* Add per‑machine authentication tokens or certificates.
* Harden `ALLOWED_COMMANDS` or replace with a policy engine.
"""

import socket
import json
import threading
import subprocess
from typing import Dict, List

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
HOST = "0.0.0.0"
PORT = 12345

# Very simple command whitelist – expand as needed.
ALLOWED_COMMANDS: List[str] = [
    "open",          # macOS `open <url>` or `open -a <app>`
    "start",         # Windows `start <file>`
    "xdg-open",      # Linux generic opener
    "echo",          # harmless demo command
]

# In‑memory store of known machine IDs (could be persisted in a DB)
known_machines: Dict[str, str] = {}   # machine_id -> last_seen_ip


def is_command_allowed(command: str) -> bool:
    """
    Very basic scope validation: the first token of the command must be
    present in the ALLOWED_COMMANDS list.
    """
    token = command.strip().split()[0] if command.strip() else ""
    return token in ALLOWED_COMMANDS


def execute_locally(command: str) -> str:
    """
    Execute the command on the relay host (demo only). Returns stdout+stderr.
    """
    try:
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        output = completed.stdout + completed.stderr
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return "(command timed out)"
    except Exception as exc:
        return f"(execution error: {exc})"


def handle_client(conn: socket.socket, addr):
    with conn:
        try:
            raw = conn.recv(4096).decode("utf-8")
            if not raw:
                return

            payload = json.loads(raw)
            command = payload.get("command", "")
            machine_id = payload.get("machine_id", "")

            # Record the machine's last seen IP (useful for debugging)
            known_machines[machine_id] = addr[0]

            # --------------------------------------------------------------
            # 1️⃣ Scope validation
            # --------------------------------------------------------------
            if not is_command_allowed(command):
                response = f"Command not allowed: {command!r}"
                conn.sendall(response.encode("utf-8"))
                return

            # --------------------------------------------------------------
            # 2️⃣ Execute (demo – on the relay host)
            # --------------------------------------------------------------
            result = execute_locally(command)

            # --------------------------------------------------------------
            # 3️⃣ Respond
            # --------------------------------------------------------------
            conn.sendall(result.encode("utf-8"))

        except json.JSONDecodeError:
            conn.sendall(b"Invalid JSON payload")
        except Exception as exc:
            err_msg = f"Server error: {exc}"
            conn.sendall(err_msg.encode("utf-8"))


def start_server():
    print(f"[relay] Listening on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(5)

        while True:
            client_conn, client_addr = srv.accept()
            print(f"[relay] Connection from {client_addr}")
            threading.Thread(
                target=handle_client,
                args=(client_conn, client_addr),
                daemon=True
            ).start()


if __name__ == "__main__":
    start_server()
import asyncio
import json
import logging
import os
import uuid
import hmac
import hashlib
from collections import defaultdict

import websockets

# Configuration – can be overridden via environment variables
RELAY_HOST = os.getenv("REMOTE_RELAY_HOST", "0.0.0.0")
RELAY_PORT = int(os.getenv("REMOTE_RELAY_PORT", "8765"))
SHARED_SECRET = os.getenv("REMOTE_RELAY_SECRET", "change_this_secret")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("remote_execution_relay")

# ----------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------
# Mapping from machine_id -> websocket connection
connected_clients = {}
# Mapping from command_id -> asyncio.Future awaiting result
pending_commands = {}
# Simple counter for generating unique command IDs
_command_counter = 0

def sign_message(message: dict) -> str:
    payload = json.dumps(message, sort_keys=True).encode()
    return hmac.new(SHARED_SECRET.encode(), payload, hashlib.sha256).hexdigest()

def verify_signature(message: dict, signature: str) -> bool:
    expected = sign_message(message)
    return hmac.compare_digest(expected, signature)

def next_command_id() -> str:
    global _command_counter
    _command_counter += 1
    return f"cmd-{_command_counter}"

# ----------------------------------------------------------------------
# WebSocket handler for client machines
# ----------------------------------------------------------------------
async def client_handler(websocket, path):
    try:
        async for raw_msg in websocket:
            try:
                msg = json.loads(raw_msg)
                sig = msg.pop("signature", "")
                if not verify_signature(msg, sig):
                    logger.warning("Invalid signature from client; ignoring.")
                    continue

                msg_type = msg.get("type")
                if msg_type == "register":
                    machine_id = msg.get("machine_id")
                    if machine_id:
                        connected_clients[machine_id] = websocket
                        logger.info(f"Registered client {machine_id}")
                elif msg_type == "result":
                    cmd_id = msg.get("command_id")
                    future = pending_commands.pop(cmd_id, None)
                    if future and not future.done():
                        future.set_result(msg)
                else:
                    logger.debug(f"Unhandled message type from client: {msg_type}")
            except json.JSONDecodeError:
                logger.exception("Failed to decode JSON from client.")
    except websockets.exceptions.ConnectionClosed:
        # Cleanup any stale registrations
        stale = [mid for mid, ws in connected_clients.items() if ws == websocket]
        for mid in stale:
            del connected_clients[mid]
            logger.info(f"Client {mid} disconnected.")
    finally:
        # Ensure removal from the registry
        for mid, ws in list(connected_clients.items()):
            if ws == websocket:
                del connected_clients[mid]

# ----------------------------------------------------------------------
# Public API – used by other parts of the swarm to issue commands
# ----------------------------------------------------------------------
async def send_command(machine_id: str, command: str, args=None, timeout: float = 30.0):
    """
    Send a command to a specific registered client and await its response.
    Returns a dict with keys: output, error, command_id, machine_id.
    """
    if args is None:
        args = []
    client_ws = connected_clients.get(machine_id)
    if not client_ws:
        raise ValueError(f"No connected client with machine_id {machine_id}")

    cmd_id = next_command_id()
    command_msg = {
        "type": "command",
        "command_id": cmd_id,
        "command": command,
        "args": args,
        "machine_id": machine_id,
    }
    command_msg["signature"] = sign_message(command_msg)

    # Prepare a Future to capture the response
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    pending_commands[cmd_id] = future

    await client_ws.send(json.dumps(command_msg))

    try:
        result = await asyncio.wait_for(future, timeout=timeout)
        return result
    except asyncio.TimeoutError:
        pending_commands.pop(cmd_id, None)
        raise TimeoutError(f"Command {cmd_id} to {machine_id} timed out")

# ----------------------------------------------------------------------
# Server entry point
# ----------------------------------------------------------------------
async def main():
    async with websockets.serve(client_handler, RELAY_HOST, RELAY_PORT):
        logger.info(f"Remote execution relay listening on {RELAY_HOST}:{RELAY_PORT}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Relay shutdown requested by user.")
import asyncio
import json
import uuid
from collections import defaultdict

import aiohttp
from aiohttp import web
import websockets

# ----------------------------------------------------------------------
# Global state
# ----------------------------------------------------------------------
# token -> websocket
CONNECTED_CLIENTS = {}
# command_id -> asyncio.Future awaiting a response
PENDING_RESPONSES = defaultdict(asyncio.Future)


# ----------------------------------------------------------------------
# WebSocket server: handles client registration and command responses
# ----------------------------------------------------------------------
async def client_handler(ws, path):
    try:
        registration_msg = await ws.recv()
        reg = json.loads(registration_msg)
        if reg.get("type") != "register" or "token" not in reg:
            await ws.close()
            return
        token = reg["token"]
        CONNECTED_CLIENTS[token] = ws
        print(f"[Relay] Client registered: {token}")

        async for message in ws:
            try:
                payload = json.loads(message)
                if payload.get("type") == "response" and "id" in payload:
                    cmd_id = payload["id"]
                    fut = PENDING_RESPONSES.pop(cmd_id, None)
                    if fut and not fut.done():
                        fut.set_result(payload)
            except json.JSONDecodeError:
                continue
    finally:
        # Cleanup on disconnect
        token = None
        for t, client_ws in list(CONNECTED_CLIENTS.items()):
            if client_ws == ws:
                token = t
                del CONNECTED_CLIENTS[t]
                break
        if token:
            print(f"[Relay] Client disconnected: {token}")


# ----------------------------------------------------------------------
# HTTP API for users to issue commands to a specific machine
# ----------------------------------------------------------------------
async def execute_handler(request):
    """
    Expected JSON body:
    {
        "token": "<client token>",
        "command": "<command string>"
    }
    """
    try:
        data = await request.json()
        token = data["token"]
        command = data["command"]
    except (json.JSONDecodeError, KeyError):
        return web.json_response(
            {"error": "Invalid JSON payload; requires 'token' and 'command'"},
            status=400,
        )

    ws = CONNECTED_CLIENTS.get(token)
    if not ws:
        return web.json_response({"error": "Client not connected"}, status=404)

    cmd_id = str(uuid.uuid4())
    request_msg = {"type": "command", "id": cmd_id, "command": command}
    await ws.send(json.dumps(request_msg))

    # Wait for the client to respond (timeout after 30 seconds)
    future = asyncio.get_event_loop().create_future()
    PENDING_RESPONSES[cmd_id] = future
    try:
        response = await asyncio.wait_for(future, timeout=30)
        return web.json_response(response)
    except asyncio.TimeoutError:
        PENDING_RESPONSES.pop(cmd_id, None)
        return web.json_response({"error": "Command timed out"}, status=504)


# ----------------------------------------------------------------------
# Server startup
# ----------------------------------------------------------------------
async def main():
    # Start WebSocket server for remote clients
    ws_server = await websockets.serve(client_handler, "0.0.0.0", 8765)
    print("[Relay] WebSocket server listening on ws://0.0.0.0:8765")

    # Start HTTP API server for user requests
    app = web.Application()
    app.router.add_post("/execute", execute_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    http_site = web.TCPSite(runner, "0.0.0.0", 8080)
    await http_site.start()
    print("[Relay] HTTP API listening on http://0.0.0.0:8080/execute")

    # Keep running forever
    await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
import os
import json
import asyncio

HOST = os.getenv("REMOTE_RELAY_HOST", "0.0.0.0")
PORT = int(os.getenv("REMOTE_RELAY_PORT", "8765"))
SHARED_SECRET = os.getenv("REMOTE_EXEC_SHARED_SECRET", "default_secret")

# Mapping of MAC address -> client writer
clients = {}
# Mapping of request_id -> origin writer (who issued the command)
pending_requests = {}


async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        while not reader.at_eof():
            line = await reader.readline()
            if not line:
                break
            try:
                msg = json.loads(line.decode())
            except json.JSONDecodeError:
                continue

            # Client registration
            if msg.get("type") == "register":
                if msg.get("token") != SHARED_SECRET:
                    writer.close()
                    await writer.wait_closed()
                    return
                mac = msg.get("mac")
                clients[mac] = writer
                continue

            # Command execution request (from a user/other service)
            if msg.get("type") == "execute":
                if msg.get("token") != SHARED_SECRET:
                    continue
                target_mac = msg.get("target_mac")
                client_writer = clients.get(target_mac)
                if client_writer:
                    request_id = os.urandom(8).hex()
                    pending_requests[request_id] = writer
                    forward = {
                        "type": "execute",
                        "mac": target_mac,
                        "cmd": msg.get("cmd"),
                        "request_id": request_id
                    }
                    client_writer.write((json.dumps(forward) + "\n").encode())
                    await client_writer.drain()
                continue

            # Result coming back from a client
            if msg.get("type") == "result":
                request_id = msg.get("request_id")
                origin_writer = pending_requests.pop(request_id, None)
                if origin_writer:
                    origin_writer.write((json.dumps(msg) + "\n").encode())
                    await origin_writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_connection, HOST, PORT)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# ----------------------------------------------------------------------
# In‑memory store – suitable for a simple LAN demo.
# For production you would replace this with a persistent DB and proper auth.
# ----------------------------------------------------------------------
_commands_lock = threading.Lock()
_registered_tokens = set()                # Tokens that have successfully registered.
_pending_commands = {}                    # token -> list of {"id": int, "command": dict}
_pending_responses = {}                   # token -> list of {"id": int, "result": dict}
_command_counter = 0


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _ensure_token(token: str):
    """Raise a 404 if the token is unknown."""
    if token not in _registered_tokens:
        raise ValueError("unknown token")


# ----------------------------------------------------------------------
# Registration endpoint – called by each client once on startup.
# ----------------------------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    token = data.get("token")
    if not token:
        return "Missing token", 400

    with _commands_lock:
        _registered_tokens.add(token)
        _pending_commands.setdefault(token, [])
        _pending_responses.setdefault(token, [])
    return "Registered", 200


# ----------------------------------------------------------------------
# Admin endpoint – push a command to a specific client.
# The request body must contain:
#   { "token": "<client-token>", "command": { "action": "...", "args": [...] } }
# ----------------------------------------------------------------------
@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    token = data.get("token")
    command = data.get("command")
    if not token or not command:
        return "Missing token or command", 400

    try:
        _ensure_token(token)
    except ValueError:
        return "Unknown token", 404

    global _command_counter
    with _commands_lock:
        _command_counter += 1
        entry = {"id": _command_counter, "command": command}
        _pending_commands[token].append(entry)

    return jsonify({"status": "queued", "id": _command_counter}), 200


# ----------------------------------------------------------------------
# Client polling endpoint – returns the next pending command for the caller.
# ----------------------------------------------------------------------
@app.route("/command", methods=["GET"])
def command():
    token = request.args.get("token")
    if not token:
        return "Missing token", 400

    try:
        _ensure_token(token)
    except ValueError:
        return "Unknown token", 404

    with _commands_lock:
        if _pending_commands[token]:
            cmd = _pending_commands[token].pop(0)
            return jsonify(cmd), 200

    # No command waiting – return empty JSON.
    return jsonify({}), 200


# ----------------------------------------------------------------------
# Client response endpoint – client posts the result of a command execution.
# ----------------------------------------------------------------------
@app.route("/response", methods=["POST"])
def response():
    data = request.get_json()
    token = data.get("token")
    cmd_id = data.get("command_id")
    result = data.get("result")
    if not token or cmd_id is None or result is None:
        return "Missing fields", 400

    try:
        _ensure_token(token)
    except ValueError:
        return "Unknown token", 404

    with _commands_lock:
        _pending_responses[token].append({"id": cmd_id, "result": result})

    return "OK", 200


# ----------------------------------------------------------------------
# Optional: fetch accumulated responses for a token (useful for debugging).
# ----------------------------------------------------------------------
@app.route("/responses", methods=["GET"])
def responses():
    token = request.args.get("token")
    if not token:
        return "Missing token", 400

    try:
        _ensure_token(token)
    except ValueError:
        return "Unknown token", 404

    with _commands_lock:
        resp = _pending_responses.get(token, [])
        _pending_responses[token] = []  # clear after retrieval
    return jsonify(resp), 200


if __name__ == "__main__":
    # Listen on all interfaces so LAN machines can reach the relay.
    app.run(host="0.0.0.0", port=5000)
import asyncio
import json
import hashlib
import uuid
import websockets
from collections import defaultdict

# Configuration – adjust as needed
HOST = "0.0.0.0"
PORT = 8765

# In‑memory registry of connected clients: token -> websocket
connected_clients = {}
# Mapping of request_id -> websocket of the original requester (e.g., the host UI)
pending_requests = {}

def generate_request_id() -> str:
    return uuid.uuid4().hex

async def handler(websocket, path):
    """
    Handles both client registrations and command forwarding.
    The first message from a client must be a registration payload.
    """
    try:
        register_msg = await websocket.recv()
        reg = json.loads(register_msg)

        if reg.get("type") != "register" or "token" not in reg:
            await websocket.close(code=1008, reason="Invalid registration")
            return

        token = reg["token"]
        connected_clients[token] = websocket

        # Keep the connection alive to receive commands or results
        async for message in websocket:
            payload = json.loads(message)

            if payload.get("type") == "command_request":
                # Received from the host (e.g., UI) – forward to the target client
                target_token = payload.get("target_token")
                if target_token not in connected_clients:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "error": f"No client registered with token {target_token}"
                    }))
                    continue

                request_id = generate_request_id()
                pending_requests[request_id] = websocket

                forward_msg = {
                    "type": "command",
                    "request_id": request_id,
                    "command_id": payload.get("command_id"),
                    "args": payload.get("args", []),
                    "target_token": target_token,
                }
                await connected_clients[target_token].send(json.dumps(forward_msg))

            elif payload.get("type") in ("result", "error"):
                # Result coming back from a client
                request_id = payload.get("request_id")
                requester_ws = pending_requests.pop(request_id, None)
                if requester_ws:
                    await requester_ws.send(json.dumps(payload))

            else:
                # Unknown message type – ignore or log
                continue

    finally:
        # Cleanup on disconnect
        tokens_to_remove = [t for t, ws in connected_clients.items() if ws == websocket]
        for t in tokens_to_remove:
            del connected_clients[t]

async def start_server():
    async with websockets.serve(handler, HOST, PORT):
        print(f"Remote Execution Relay listening on ws://{HOST}:{PORT}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(start_server())
import threading
from flask import Flask, request, jsonify
import uuid
import time

app = Flask(__name__)

# In‑memory store for registered machines and pending commands
# {
#   machine_id: {
#       "info": {...},
#       "queue": [ {"id": cmd_id, "body": {...}} ],
#   }
# }
MACHINES = {}
LOCK = threading.Lock()


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _auth_request(req):
    # Placeholder for future auth – currently accepts all requests
    return True


def _make_command_id():
    return str(uuid.uuid4())


# ----------------------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    if not _auth_request(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    machine_id = data.get("machine_id")
    if not machine_id:
        return jsonify({"error": "machine_id required"}), 400

    with LOCK:
        MACHINES.setdefault(machine_id, {"info": data, "queue": []})
    return jsonify({"status": "registered"})


@app.route("/fetch", methods=["POST"])
def fetch():
    if not _auth_request(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    machine_id = data.get("machine_id")
    if not machine_id:
        return jsonify({"error": "machine_id required"}), 400

    with LOCK:
        machine = MACHINES.get(machine_id)
        if not machine:
            return jsonify({"error": "machine not registered"}), 404
        # Return a copy of the queue and clear it
        cmds = list(machine["queue"])
        machine["queue"].clear()
    return jsonify({"commands": cmds})


@app.route("/result", methods=["POST"])
def result():
    if not _auth_request(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    machine_id = data.get("machine_id")
    command_id = data.get("command_id")
    result = data.get("result")

    # For this minimal implementation we just log the result.
    # In a production system you would forward it to the originating user session.
    print(f"[Relay] Result from {machine_id} for cmd {command_id}: {result}")

    return jsonify({"status": "received"})


@app.route("/command", methods=["POST"])
def command():
    """
    Endpoint used by a LAN user (e.g., via a UI or chatbot) to request
    execution on a specific machine.

    Expected JSON:
    {
        "target_machine_id": "<machine-id>",
        "action": "open_browser",
        "args": {"url": "https://example.com"}
    }
    """
    if not _auth_request(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    target_id = data.get("target_machine_id")
    action = data.get("action")
    args = data.get("args", {})

    if not target_id or not action:
        return jsonify({"error": "target_machine_id and action required"}), 400

    cmd_id = _make_command_id()
    command_payload = {
        "id": cmd_id,
        "body": {
            "action": action,
            "args": args,
        },
    }

    with LOCK:
        machine = MACHINES.get(target_id)
        if not machine:
            return jsonify({"error": f"Machine {target_id} not registered"}), 404
        machine["queue"].append(command_payload)

    # In a real deployment you would also store a correlation ID so the UI
    # can later retrieve the result via a /result_lookup endpoint.
    return jsonify({"status": "queued", "command_id": cmd_id})


# ----------------------------------------------------------------------
# Server startup helper
# ----------------------------------------------------------------------
def start_relay(host="0.0.0.0", port=5000, use_tls=False, certfile=None, keyfile=None):
    """
    Starts the Flask relay server.
    - If ``use_tls`` is True, ``certfile`` and ``keyfile`` must be provided.
    """
    if use_tls:
        if not certfile or not keyfile:
            raise ValueError("TLS enabled but certfile/keyfile not supplied")
        app.run(host=host, port=port, ssl_context=(certfile, keyfile), threaded=True)
    else:
        app.run(host=host, port=port, threaded=True)


if __name__ == "__main__":
    # Example: start_relay(use_tls=False)
    start_relay()
import socket
import threading
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configuration – can be overridden by environment variables
LISTEN_HOST = os.getenv("REMOTE_RELAY_HOST", "0.0.0.0")
LISTEN_PORT = int(os.getenv("REMOTE_RELAY_PORT", "9000"))
HTTP_PORT = int(os.getenv("REMOTE_RELAY_HTTP_PORT", "9001"))

# ----------------------------------------------------------------------
# Client connection management
# ----------------------------------------------------------------------
clients_lock = threading.Lock()
clients = {}  # token -> socket


def client_handler(conn, addr):
    """
    Handles a connected remote client.
    Expected first message: registration JSON with type 'register'.
    Subsequent messages are command responses.
    """
    buffer = ""
    token = None
    try:
        while True:
            data = conn.recv(4096).decode("utf-8")
            if not data:
                break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if msg.get("type") == "register":
                    token = msg.get("token")
                    with clients_lock:
                        clients[token] = conn
                elif msg.get("type") == "response" and token:
                    # Store the response for the HTTP handler to retrieve
                    response_queue = response_queues.get(token)
                    if response_queue:
                        response_queue.put(msg)
    finally:
        # Cleanup on disconnect
        if token:
            with clients_lock:
                clients.pop(token, None)
        conn.close()


def start_tcp_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((LISTEN_HOST, LISTEN_PORT))
    server_sock.listen()
    print(f"Remote execution relay listening on {LISTEN_HOST}:{LISTEN_PORT}")

    while True:
        conn, addr = server_sock.accept()
        threading.Thread(target=client_handler, args=(conn, addr), daemon=True).start()


# ----------------------------------------------------------------------
# HTTP API for users to request remote execution
# ----------------------------------------------------------------------
from queue import Queue, Empty

response_queues = {}  # token -> Queue of responses


class ExecRequestHandler(BaseHTTPRequestHandler):
    def _set_json(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_POST(self):
        if self.path != "/execute":
            self.send_error(404, "Not Found")
            return

        length = int(self.headers.get("Content-Length", 0))
        payload = self.rfile.read(length)
        try:
            data = json.loads(payload)
            token = data["token"]
            command = data["command"]
        except (KeyError, json.JSONDecodeError):
            self.send_error(400, "Invalid JSON payload")
            return

        # Locate the client
        with clients_lock:
            client_sock = clients.get(token)

        if not client_sock:
            self.send_error(404, "Client not connected")
            return

        # Prepare a queue for the response
        resp_queue = Queue()
        response_queues[token] = resp_queue

        # Send command to the client
        cmd_msg = {"type": "command", "command": command}
        try:
            client_sock.sendall((json.dumps(cmd_msg) + "\n").encode("utf-8"))
        except Exception:
            self.send_error(502, "Failed to send command to client")
            response_queues.pop(token, None)
            return

        # Wait for response (with timeout)
        try:
            resp = resp_queue.get(timeout=30)  # seconds
        except Empty:
            self.send_error(504, "Client did not respond in time")
            response_queues.pop(token, None)
            return
        finally:
            response_queues.pop(token, None)

        self._set_json()
        self.wfile.write(json.dumps(resp).encode("utf-8"))


def start_http_server():
    httpd = HTTPServer((LISTEN_HOST, HTTP_PORT), ExecRequestHandler)
    print(f"Remote execution HTTP API listening on {LISTEN_HOST}:{HTTP_PORT}")
    httpd.serve_forever()


if __name__ == "__main__":
    threading.Thread(target=start_tcp_server, daemon=True).start()
    start_http_server()
import asyncio
import json
import os
from collections import defaultdict

from flask import Flask, request, jsonify
import websockets
from websockets.exceptions import ConnectionClosedOK

app = Flask(__name__)

# In‑memory mapping: token -> websocket connection
connections = {}
# Pending requests: request_id -> asyncio.Future
pending = {}

# Simple request id generator
_request_counter = 0


def next_request_id():
    global _request_counter
    _request_counter += 1
    return str(_request_counter)


async def register_client(websocket, path):
    """
    WebSocket handler for remote execution clients.
    Expected query string: ?token=XYZ
    """
    query = dict(pair.split("=") for pair in websocket.path.split("?")[1].split("&"))
    token = query.get("token")
    if not token:
        await websocket.close(code=4000, reason="Missing token")
        return

    # Store the connection
    connections[token] = websocket
    try:
        async for message in websocket:
            # Replies from client come here
            try:
                payload = json.loads(message)
                request_id = payload.get("request_id")
                if request_id and request_id in pending:
                    pending[request_id].set_result(payload)
            except json.JSONDecodeError:
                continue
    finally:
        # Cleanup on disconnect
        if connections.get(token) is websocket:
            del connections[token]


@app.route("/execute", methods=["POST"])
def execute():
    """
    HTTP endpoint used by the swarm UI (or any authorized user) to request
    remote execution on a specific machine.
    JSON body:
    {
        "token": "machine-token",
        "cmd": "open_browser",
        "args": {"url": "https://example.com"}
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    token = data.get("token")
    cmd = data.get("cmd")
    args = data.get("args", {})

    if token not in connections:
        return jsonify({"error": "Target machine not connected"}), 404

    request_id = next_request_id()
    payload = {
        "request_id": request_id,
        "cmd": cmd,
        "args": args,
    }

    future = asyncio.get_event_loop().create_future()
    pending[request_id] = future

    # Send command to the client
    asyncio.create_task(connections[token].send(json.dumps(payload)))

    # Wait for response (with timeout)
    try:
        result = asyncio.wait_for(future, timeout=30.0)
        response = asyncio.run(result)  # Resolve the future
        return jsonify(response)
    except asyncio.TimeoutError:
        pending.pop(request_id, None)
        return jsonify({"error": "Execution timed out"}), 504
    finally:
        pending.pop(request_id, None)


def start_flask():
    # Run Flask in a separate thread to coexist with asyncio loop
    from threading import Thread
    server = Thread(target=lambda: app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False))
    server.daemon = True
    server.start()


async def main():
    start_flask()
    async with websockets.serve(register_client, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# In‑memory storage: pending commands and collected responses per machine
_pending_commands = {}   # machine_id -> list of command strings
_responses = {}          # machine_id -> list of response dicts
_store_lock = threading.Lock()

# Shared secret for simple token authentication (replace in production)
AUTH_TOKEN = "CHANGE_ME"

def _is_authorized(req):
    auth_header = req.headers.get("Authorization", "")
    return auth_header == f"Bearer {AUTH_TOKEN}"

# Whitelisted command templates – keys are user‑friendly identifiers
ALLOWED_COMMANDS = {
    # Example: open the default browser on macOS
    "open_browser": "open -a Safari",
    # Example: list current directory contents
    "list_dir": "ls -la",
    # Add additional safe commands here
}


@app.route("/register", methods=["POST"])
def register():
    """Endpoint for a client machine to announce itself."""
    if not _is_authorized(request):
        return "Unauthorized", 401

    data = request.get_json(silent=True) or {}
    machine_id = data.get("machine_id")
    if not machine_id:
        return "machine_id required", 400

    with _store_lock:
        _pending_commands.setdefault(machine_id, [])
        _responses.setdefault(machine_id, [])
    return "OK", 200


@app.route("/fetch", methods=["GET"])
def fetch():
    """Client polls for the next pending command."""
    if not _is_authorized(request):
        return "Unauthorized", 401

    machine_id = request.args.get("machine_id")
    if not machine_id:
        return "machine_id required", 400

    with _store_lock:
        cmds = _pending_commands.get(machine_id, [])
        if cmds:
            cmd = cmds.pop(0)
            return jsonify({"command": cmd})
    return jsonify({}), 200


@app.route("/response", methods=["POST"])
def response():
    """Client posts execution result back to the relay."""
    if not _is_authorized(request):
        return "Unauthorized", 401

    data = request.get_json(silent=True) or {}
    machine_id = data.get("machine_id")
    if not machine_id:
        return "machine_id required", 400

    with _store_lock:
        _responses.setdefault(machine_id, []).append(data)
    return "OK", 200


@app.route("/submit", methods=["POST"])
def submit():
    """
    External user (e.g., a LAN participant) submits a command request for a
    specific machine. Payload: {"machine_id": "...", "command_key": "..."}
    """
    if not _is_authorized(request):
        return "Unauthorized", 401

    data = request.get_json(silent=True) or {}
    machine_id = data.get("machine_id")
    command_key = data.get("command_key")
    if not machine_id or not command_key:
        return "machine_id and command_key required", 400

    if command_key not in ALLOWED_COMMANDS:
        return "Command not allowed", 403

    command = ALLOWED_COMMANDS[command_key]

    with _store_lock:
        _pending_commands.setdefault(machine_id, []).append(command)
    return "Queued", 200


@app.route("/responses", methods=["GET"])
def get_responses():
    """
    Retrieve and clear stored responses for a given machine.
    Useful for debugging or UI feedback.
    """
    if not _is_authorized(request):
        return "Unauthorized", 401

    machine_id = request.args.get("machine_id")
    if not machine_id:
        return "machine_id required", 400

    with _store_lock:
        msgs = _responses.get(machine_id, [])
        _responses[machine_id] = []  # clear after fetch
    return jsonify(msgs), 200


if __name__ == "__main__":
    # Run on all interfaces so LAN users can reach it
    app.run(host="0.0.0.0", port=5000)
import asyncio
import json
import os
import uuid
from urllib.parse import parse_qs, urlparse

from aiohttp import web

# ----------------------------------------------------------------------
# In‑memory registry of connected clients.
# Key: token string, Value: WebSocketResponse instance.
# ----------------------------------------------------------------------
connected_clients: dict[str, web.WebSocketResponse] = {}


def _is_valid_token(token: str) -> bool:
    """
    Placeholder token validation.
    Replace with proper authentication (e.g., HMAC, signed JWT) as required.
    """
    return bool(token)


# ----------------------------------------------------------------------
# WebSocket endpoint for remote execution clients.
# Clients connect with: ws://HOST:PORT/ws?token=YOUR_TOKEN
# ----------------------------------------------------------------------
async def ws_handler(request: web.Request):
    token = request.query.get("token")
    if not token or not _is_valid_token(token):
        return web.Response(status=400, text="Missing or invalid token")

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Register the client
    connected_clients[token] = ws

    try:
        async for msg in ws:
            # The relay only forwards commands; any inbound messages are
            # responses that will be handled per request in `execute`.
            # We simply store them for later retrieval.
            # (No action needed here – messages are consumed by `execute`.)
            pass
    finally:
        # Cleanup on disconnect
        connected_clients.pop(token, None)

    return ws


# ----------------------------------------------------------------------
# HTTP endpoint used by the swarm host (or any trusted caller) to
# request execution on a specific client.
# ----------------------------------------------------------------------
async def execute(request: web.Request):
    try:
        payload = await request.json()
        token = payload["token"]
        action = payload["action"]
        args = payload.get("args", [])
        request_id = payload.get("request_id", str(uuid.uuid4()))
    except Exception as exc:  # pragma: no cover – defensive
        return web.json_response({"error": f"Invalid request: {exc}"}, status=400)

    ws = connected_clients.get(token)
    if not ws:
        return web.json_response({"error": "Target client not connected"}, status=404)

    # Send the command to the client
    await ws.send_json(
        {
            "request_id": request_id,
            "action": action,
            "args": args,
        }
    )

    # Wait for the matching response from the client
    try:
        while True:
            msg = await ws.receive_json()
            if msg.get("request_id") == request_id:
                # Normal successful reply
                return web.json_response(msg.get("result", {}))
            # If the client sent an error for this request, forward it
            if msg.get("request_id") == request_id and "error" in msg:
                return web.json_response({"error": msg["error"]}, status=500)
    except asyncio.TimeoutError:  # pragma: no cover – unlikely in tests
        return web.json_response({"error": "Timeout waiting for client response"}, status=504)


# ----------------------------------------------------------------------
# Application bootstrap
# ----------------------------------------------------------------------
def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/ws", ws_handler)
    app.router.add_post("/execute", execute)
    return app


if __name__ == "__main__":
    port = int(os.getenv("RELAY_PORT", "8080"))
    web.run_app(create_app(), port=port)
import socket
import threading
import json
import uuid
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# ----------------------------------------------------------------------
# Remote Execution Relay (Server)
# ----------------------------------------------------------------------
# Listens for persistent TCP connections from RemoteExecutionClient instances,
# maintains a mapping of machine_id -> socket, and exposes a simple HTTP API
# for external callers (e.g., the Claude swarm) to request command execution
# on a specific machine.
# ----------------------------------------------------------------------

class ClientConnection:
    def __init__(self, sock: socket.socket, address):
        self.sock = sock
        self.address = address
        self.machine_id = None
        self.token = None
        self.last_seen = time.time()
        self.lock = threading.Lock()
        self.buffer = b""

    def send(self, obj: dict):
        data = json.dumps(obj).encode("utf-8") + b"\n"
        with self.lock:
            self.sock.sendall(data)

    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except Exception:
            pass


class RemoteExecutionRelay:
    def __init__(self, listen_host="0.0.0.0", listen_port=9000, http_port=8000, shared_secret=""):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.http_port = http_port
        self.shared_secret = shared_secret
        self.clients = {}                # machine_id -> ClientConnection
        self.clients_lock = threading.Lock()
        self._stop_event = threading.Event()

    # ------------------------------------------------------------------
    # TCP listener – accepts client registrations and forwards messages
    # ------------------------------------------------------------------
    def _tcp_listener(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.listen_host, self.listen_port))
        server_sock.listen()
        print(f"[Relay] TCP listening on {self.listen_host}:{self.listen_port}")

        while not self._stop_event.is_set():
            try:
                client_sock, addr = server_sock.accept()
                threading.Thread(target=self._handle_client, args=(client_sock, addr), daemon=True).start()
            except Exception as e:
                print(f"[Relay] Accept error: {e}", file=sys.stderr)

    def _handle_client(self, client_sock: socket.socket, addr):
        conn = ClientConnection(client_sock, addr)
        try:
            while not self._stop_event.is_set():
                chunk = client_sock.recv(4096)
                if not chunk:
                    break
                conn.buffer += chunk
                while b"\n" in conn.buffer:
                    line, conn.buffer = conn.buffer.split(b"\n", 1)
                    if not line:
                        continue
                    msg = json.loads(line.decode("utf-8"))
                    self._process_message(conn, msg)
        except Exception as e:
            print(f"[Relay] Client {addr} error: {e}", file=sys.stderr)
        finally:
            self._unregister(conn)
            conn.close()
            print(f"[Relay] Disconnected client {addr}")

    def _process_message(self, conn: ClientConnection, msg: dict):
        msg_type = msg.get("type")
        if msg_type == "register":
            token = msg.get("token")
            if token != self.shared_secret:
                print(f"[Relay] Invalid token from {conn.address}, closing.")
                conn.close()
                return
            conn.machine_id = msg.get("machine_id")
            conn.token = token
            with self.clients_lock:
                self.clients[conn.machine_id] = conn
            print(f"[Relay] Registered client {conn.machine_id} ({conn.address})")
        elif msg_type == "result":
            # Forward result back to the waiting HTTP request handler via a simple queue
            request_id = msg.get("request_id")
            with self.clients_lock:
                pending = getattr(self, "_pending_requests", {})
                if request_id in pending:
                    pending[request_id]["response"] = msg
        else:
            print(f"[Relay] Unknown message type: {msg_type}")

    def _unregister(self, conn: ClientConnection):
        if conn.machine_id:
            with self.clients_lock:
                self.clients.pop(conn.machine_id, None)

    # ------------------------------------------------------------------
    # HTTP API – /execute?machine_id=...&command=...
    # Returns JSON with status and output.
    # ------------------------------------------------------------------
    class _HTTPRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            parsed_path = urlparse(self.path)
            if parsed_path.path != "/execute":
                self.send_error(404, "Not Found")
                return

            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                machine_id = data["machine_id"]
                command = data["command"]
                request_id = str(uuid.uuid4())
            except Exception:
                self.send_error(400, "Invalid JSON payload")
                return

            relay: RemoteExecutionRelay = self.server.relay_instance
            client = relay._get_client(machine_id)
            if not client:
                self._write_json(404, {"error": f"No client with machine_id {machine_id}"})
                return

            # Prepare a placeholder for the async response
            with relay.clients_lock:
                if not hasattr(relay, "_pending_requests"):
                    relay._pending_requests = {}
                relay._pending_requests[request_id] = {"response": None}

            # Send command to client
            client.send({
                "type": "command",
                "command": command,
                "request_id": request_id
            })

            # Wait (with timeout) for the client to respond
            timeout = 30  # seconds
            start = time.time()
            while time.time() - start < timeout:
                with relay.clients_lock:
                    resp = relay._pending_requests[request_id]["response"]
                if resp:
                    break
                time.sleep(0.1)

            # Clean up pending request
            with relay.clients_lock:
                relay._pending_requests.pop(request_id, None)

            if not resp:
                self._write_json(504, {"error": "Client did not respond in time"})
                return

            self._write_json(200, resp)

        def log_message(self, format, *args):
            # Suppress default logging
            return

        def _write_json(self, code: int, payload: dict):
            response = json.dumps(payload).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    def _get_client(self, machine_id: str):
        with self.clients_lock:
            return self.clients.get(machine_id)

    def start(self):
        # Start TCP listener thread
        threading.Thread(target=self._tcp_listener, daemon=True).start()

        # Start HTTP server
        server_address = (self.listen_host, self.http_port)
        httpd = HTTPServer(server_address, self._HTTPRequestHandler)
        httpd.relay_instance = self
        print(f"[Relay] HTTP API listening on http://{self.listen_host}:{self.http_port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("[Relay] Shutting down...")
            self.stop()
            httpd.server_close()

    def stop(self):
        self._stop_event.set()
        with self.clients_lock:
            for client in list(self.clients.values()):
                client.close()


if __name__ == "__main__":
    # Example usage:
    #   python remote_execution_relay.py <shared_secret_token>
    if len(sys.argv) != 2:
        print("Usage: python remote_execution_relay.py <shared_secret_token>")
        sys.exit(1)

    secret = sys.argv[1]
    relay = RemoteExecutionRelay(shared_secret=secret)
    relay.start()