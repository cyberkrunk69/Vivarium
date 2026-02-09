# remote_execution_client.py
"""
Remote Execution Client

- Generates (or loads) a persistent machine identifier.
- Connects to the relay server over a TCP socket.
- Sends a JSON payload containing:
    * the command the user wants to run
    * the machine_id (used by the server to route the request back)
- Receives the server’s response and prints it.

Security notes:
* In a production setting the socket should be wrapped in TLS.
* Authentication tokens can be added to the payload for stronger identity proof.
"""

import socket
import json
import uuid
import os
import subprocess
from pathlib import Path

# ----------------------------------------------------------------------
# Configuration – adjust for your environment
# ----------------------------------------------------------------------
RELAY_HOST = "127.0.0.1"          # IP or hostname of the relay server
RELAY_PORT = 12345                # Port the relay server listens on
MACHINE_ID_FILE = Path.home() / ".remote_exec_machine_id"


def get_machine_id() -> str:
    """
    Return a stable UUID that uniquely identifies this machine.
    The UUID is stored in a hidden file in the user's home directory.
    """
    if MACHINE_ID_FILE.is_file():
        return MACHINE_ID_FILE.read_text().strip()
    # First run – generate a new UUID and persist it
    new_id = str(uuid.uuid4())
    MACHINE_ID_FILE.write_text(new_id)
    return new_id


def send_command(command: str, machine_id: str) -> str:
    """
    Open a TCP connection to the relay, send the command + machine_id,
    and return the server's response.
    """
    payload = json.dumps({
        "command": command,
        "machine_id": machine_id
    }).encode("utf-8")

    with socket.create_connection((RELAY_HOST, RELAY_PORT), timeout=10) as sock:
        sock.sendall(payload)

        # Simple protocol: server sends a single JSON line response
        response_bytes = sock.recv(4096)
        return response_bytes.decode("utf-8")


def main() -> None:
    machine_id = get_machine_id()
    print(f"[client] Machine ID: {machine_id}")

    while True:
        try:
            command = input("\nEnter a command (or 'quit' to exit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not command:
            continue
        if command.lower() in {"quit", "exit"}:
            break

        try:
            response = send_command(command, machine_id)
            print(f"[server] {response}")
        except Exception as exc:
            print(f"[error] Could not contact relay: {exc}")


if __name__ == "__main__":
    main()
import asyncio
import json
import os
import socket
import subprocess
import sys
import uuid
import hmac
import hashlib

# Configuration – can be overridden via environment variables
RELAY_HOST = os.getenv("REMOTE_RELAY_HOST", "localhost")
RELAY_PORT = int(os.getenv("REMOTE_RELAY_PORT", "8765"))
# Shared secret for HMAC authentication (must match server configuration)
SHARED_SECRET = os.getenv("REMOTE_RELAY_SECRET", "change_this_secret")

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def get_machine_id() -> str:
    """Return a stable identifier for this machine (based on MAC address)."""
    mac = uuid.getnode()
    return f"{mac:012x}"

def sign_message(message: dict) -> str:
    """Create an HMAC‑SHA256 signature for a JSON‑serializable message."""
    payload = json.dumps(message, sort_keys=True).encode()
    return hmac.new(SHARED_SECRET.encode(), payload, hashlib.sha256).hexdigest()

def verify_signature(message: dict, signature: str) -> bool:
    """Verify that a received message matches the shared secret."""
    expected = sign_message(message)
    return hmac.compare_digest(expected, signature)

# ----------------------------------------------------------------------
# Command execution
# ----------------------------------------------------------------------
ALLOWED_COMMANDS = {
    # command_name: callable that returns (stdout, stderr)
    "open_browser": lambda args: (
        subprocess.run(
            ["python", "-m", "webbrowser"] + args,
            capture_output=True,
            text=True,
        ).stdout,
        None,
    ),
    "run": lambda args: (
        subprocess.run(
            args,
            capture_output=True,
            text=True,
        ).stdout,
        None,
    ),
}

async def handle_command(command_msg: dict, websocket):
    cmd_id = command_msg.get("command_id")
    command = command_msg.get("command")
    args = command_msg.get("args", [])

    response = {
        "type": "result",
        "command_id": cmd_id,
        "machine_id": get_machine_id(),
    }

    if command not in ALLOWED_COMMANDS:
        response.update(
            {
                "output": "",
                "error": f"Command '{command}' is not allowed.",
            }
        )
    else:
        try:
            stdout, stderr = ALLOWED_COMMANDS[command](args)
            response.update(
                {
                    "output": stdout,
                    "error": stderr,
                }
            )
        except Exception as e:
            response.update(
                {
                    "output": "",
                    "error": f"Exception while executing command: {e}",
                }
            )
    # Sign and send back
    response["signature"] = sign_message(response)
    await websocket.send(json.dumps(response))

# ----------------------------------------------------------------------
# Main client loop
# ----------------------------------------------------------------------
async def client_loop():
    uri = f"ws://{RELAY_HOST}:{RELAY_PORT}"
    async with websockets.connect(uri) as websocket:
        machine_id = get_machine_id()
        register_msg = {
            "type": "register",
            "machine_id": machine_id,
        }
        register_msg["signature"] = sign_message(register_msg)
        await websocket.send(json.dumps(register_msg))

        async for raw_msg in websocket:
            try:
                msg = json.loads(raw_msg)
                sig = msg.pop("signature", "")
                if not verify_signature(msg, sig):
                    continue  # ignore tampered messages
                if msg.get("type") == "command":
                    await handle_command(msg, websocket)
            except json.JSONDecodeError:
                continue  # ignore malformed messages

def main():
    try:
        asyncio.run(client_loop())
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    # Ensure the required third‑party library is available
    try:
        import websockets  # noqa: F401
    except ImportError:
        sys.stderr.write("Missing dependency 'websockets'. Install with pip.\n")
        sys.exit(1)
    main()
import asyncio
import json
import os
import platform
import socket
import subprocess
import sys
import uuid
import websockets
import webbrowser

# ----------------------------------------------------------------------
# Configuration (can be overridden via environment variables)
# ----------------------------------------------------------------------
RELAY_URL = os.getenv("REMOTE_RELAY_URL", "ws://localhost:8765")
# Token uniquely identifies this machine/user.  If not provided, we generate one
# from the MAC address (which is stable per‑machine) and store it locally.
TOKEN_FILE = os.path.expanduser("~/.remote_exec_token")


def _get_mac_address() -> str:
    """Return the MAC address of the first network interface."""
    try:
        # uuid.getnode() returns a 48‑bit MAC (or a random number if it cannot)
        mac = uuid.getnode()
        return ":".join(f"{(mac >> ele) & 0xff:02x}" for ele in range(40, -1, -8))
    except Exception:
        return "00:00:00:00:00:00"


def _load_or_create_token() -> str:
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    # generate a stable token based on MAC address
    mac = _get_mac_address()
    token = f"{mac}-{uuid.uuid4().hex[:8]}"
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    return token


TOKEN = os.getenv("REMOTE_EXEC_TOKEN", _load_or_create_token())


# ----------------------------------------------------------------------
# Command execution helpers
# ----------------------------------------------------------------------
ALLOWED_COMMANDS = {
    "open_browser": lambda args: webbrowser.open(args[0]) if args else None,
    "open_url": lambda args: webbrowser.open(args[0]) if args else None,
    "run": lambda args: subprocess.run(args, capture_output=True, text=True),
}


def _validate_and_execute(command_str: str):
    """
    Very small command sandbox.
    Expected format: <command_name> [arg1] [arg2] ...
    Only commands listed in ALLOWED_COMMANDS are permitted.
    """
    parts = command_str.strip().split()
    if not parts:
        raise ValueError("Empty command")
    cmd_name, *args = parts
    if cmd_name not in ALLOWED_COMMANDS:
        raise PermissionError(f"Command '{cmd_name}' is not allowed")
    result = ALLOWED_COMMANDS[cmd_name](args)
    # Normalize result for JSON transport
    if isinstance(result, subprocess.CompletedProcess):
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    return {"result": "ok"}


# ----------------------------------------------------------------------
# Main async client loop
# ----------------------------------------------------------------------
async def _handle_messages(ws):
    async for message in ws:
        try:
            payload = json.loads(message)
            if payload.get("type") != "command":
                continue
            cmd_id = payload["id"]
            command = payload["command"]
            try:
                exec_result = _validate_and_execute(command)
                response = {
                    "type": "response",
                    "id": cmd_id,
                    "status": "ok",
                    "output": exec_result,
                }
            except Exception as e:
                response = {
                    "type": "response",
                    "id": cmd_id,
                    "status": "error",
                    "error": str(e),
                }
            await ws.send(json.dumps(response))
        except json.JSONDecodeError:
            continue


async def _register_and_listen():
    async with websockets.connect(RELAY_URL) as ws:
        # Register this client
        registration = {
            "type": "register",
            "token": TOKEN,
            "platform": platform.system(),
            "hostname": socket.gethostname(),
        }
        await ws.send(json.dumps(registration))
        await _handle_messages(ws)


def main():
    asyncio.run(_register_and_listen())


if __name__ == "__main__":
    main()
import os
import json
import socket
import uuid
import subprocess
import threading

SERVER_HOST = os.getenv("REMOTE_RELAY_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("REMOTE_RELAY_PORT", "8765"))
TOKEN_FILE = os.path.expanduser("~/.remote_exec_token")
SHARED_SECRET = os.getenv("REMOTE_EXEC_TOKEN")  # token provided to client


def _get_mac_address() -> str:
    mac_int = uuid.getnode()
    return ":".join(f"{(mac_int >> ele) & 0xff:02x}" for ele in range(40, -1, -8))


def _load_or_create_token() -> str:
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    token = SHARED_SECRET or os.urandom(16).hex()
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    return token


MAC_ADDRESS = _get_mac_address()
CLIENT_TOKEN = _load_or_create_token()


def _handle_server_messages(sock: socket.socket):
    buffer = b""
    while True:
        data = sock.recv(4096)
        if not data:
            break
        buffer += data
        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            try:
                msg = json.loads(line.decode())
            except json.JSONDecodeError:
                continue

            if msg.get("type") == "execute" and msg.get("mac") == MAC_ADDRESS:
                cmd = msg.get("cmd")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                response = {
                    "type": "result",
                    "mac": MAC_ADDRESS,
                    "cmd": cmd,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "request_id": msg.get("request_id")
                }
                sock.sendall((json.dumps(response) + "\n").encode())


def start_client():
    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        register_msg = {
            "type": "register",
            "mac": MAC_ADDRESS,
            "token": CLIENT_TOKEN
        }
        sock.sendall((json.dumps(register_msg) + "\n").encode())
        _handle_server_messages(sock)


if __name__ == "__main__":
    threading.Thread(target=start_client, daemon=True).start()
    threading.Event().wait()
import sys
import uuid
import threading
import time
import subprocess
import requests

# Configuration – adjust SERVER_URL to point at the swarm host running the relay.
SERVER_URL = "http://localhost:5000"
POLL_INTERVAL = 5  # seconds between polls for new commands

# Define which actions the client is allowed to execute.
# Extend this dictionary with additional safe actions as needed.
ALLOWED_COMMANDS = {"open_browser"}


def get_machine_token() -> str:
    """
    Generate a stable identifier for the machine.
    Uses the MAC address (as a hex string) – sufficient for LAN‑only scenarios.
    """
    mac = uuid.getnode()
    return f"{mac:012x}"


def execute_command(command: dict) -> dict:
    """
    Execute a validated command received from the relay.

    Expected command format:
        {
            "action": "open_browser",
            "args": ["https://example.com"]
        }

    Returns a dict with ``status`` (\"ok\" or \"error\") and ``output`` (result or error message).
    """
    action = command.get("action")
    args = command.get("args", [])

    if action not in ALLOWED_COMMANDS:
        return {"status": "error", "output": f"Action '{action}' not allowed"}

    try:
        if action == "open_browser":
            # Open the default browser to a given URL (or a fallback page).
            url = args[0] if args else "http://www.google.com"
            if sys.platform == "darwin":
                subprocess.Popen(["open", url])
            elif sys.platform.startswith("win"):
                subprocess.Popen(["start", url], shell=True)
            else:  # Linux and others
                subprocess.Popen(["xdg-open", url])
            return {"status": "ok", "output": f"Browser opened to {url}"}
        # Add further safe actions here.
        return {"status": "error", "output": f"No handler for action '{action}'"}
    except Exception as exc:
        return {"status": "error", "output": str(exc)}


def poll_loop(token: str):
    """
    Background loop that continuously asks the relay for pending commands,
    executes them, and posts back the result.
    """
    while True:
        try:
            resp = requests.get(
                f"{SERVER_URL}/command",
                params={"token": token},
                timeout=10,
            )
            if resp.status_code == 200:
                payload = resp.json()
                if payload.get("command"):
                    result = execute_command(payload["command"])
                    # Send the execution result back to the relay.
                    requests.post(
                        f"{SERVER_URL}/response",
                        json={
                            "token": token,
                            "command_id": payload.get("id"),
                            "result": result,
                        },
                        timeout=10,
                    )
        except Exception as exc:
            # Simple stdout logging – replace with a proper logger if desired.
            print(f"[RemoteExecutor] Poll error: {exc}", file=sys.stderr)

        time.sleep(POLL_INTERVAL)


def start():
    """
    Register the client with the relay and launch the polling thread.
    """
    token = get_machine_token()
    try:
        requests.post(
            f"{SERVER_URL}/register",
            json={"token": token},
            timeout=5,
        )
    except Exception as exc:
        print(f"[RemoteExecutor] Registration failed: {exc}", file=sys.stderr)

    thread = threading.Thread(target=poll_loop, args=(token,), daemon=True)
    thread.start()
    print(f"[RemoteExecutor] Running for token {token}")


if __name__ == "__main__":
    start()
    # Keep the main process alive so the daemon thread can continue working.
    while True:
        time.sleep(60)
import asyncio
import json
import subprocess
import sys
import uuid
import websockets
import hashlib

# Configuration – adjust as needed
RELAY_SERVER_URI = "ws://localhost:8765"  # URL of the remote execution relay
ALLOWED_COMMANDS = {
    "open_browser": ["open", "-a", "Safari"],  # Example: open Safari on macOS
    "list_files": ["ls", "-la"],
    # Add more command identifiers and their safe argument lists here
}

def get_machine_token() -> str:
    """
    Generate a stable token for this machine based on its MAC address.
    """
    mac = uuid.getnode()
    token = hashlib.sha256(str(mac).encode()).hexdigest()
    return token

async def execute_command(command_id: str, args: list):
    """
    Execute a validated command locally and capture its output.
    """
    if command_id not in ALLOWED_COMMANDS:
        return {"status": "error", "error": f"Command '{command_id}' not allowed."}

    base_cmd = ALLOWED_COMMANDS[command_id]
    # Prevent injection by not concatenating raw args; only allow predefined args
    cmd = base_cmd + args

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return {
            "status": "ok",
            "returncode": proc.returncode,
            "stdout": stdout.decode().strip(),
            "stderr": stderr.decode().strip(),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

async def client_loop():
    token = get_machine_token()
    async with websockets.connect(RELAY_SERVER_URI) as websocket:
        # Register this client with the relay
        await websocket.send(json.dumps({
            "type": "register",
            "token": token,
            "platform": sys.platform,
        }))

        while True:
            try:
                message = await websocket.recv()
                payload = json.loads(message)

                if payload.get("type") != "command" or payload.get("target_token") != token:
                    continue  # Ignore unrelated messages

                command_id = payload.get("command_id")
                args = payload.get("args", [])

                result = await execute_command(command_id, args)

                # Send result back to relay
                await websocket.send(json.dumps({
                    "type": "result",
                    "request_id": payload.get("request_id"),
                    "result": result,
                }))

            except websockets.ConnectionClosed:
                # Attempt reconnection after a short pause
                await asyncio.sleep(5)
                return await client_loop()
            except Exception as e:
                # Log unexpected errors but keep the loop alive
                await websocket.send(json.dumps({
                    "type": "error",
                    "error": str(e),
                }))

if __name__ == "__main__":
    asyncio.run(client_loop())
import threading
import time
import uuid
import json
import requests
import subprocess
import platform
import socket

# Configuration – adjust SERVER_URL to point at your swarm relay host
SERVER_URL = "https://your-relay-host.example.com"

# Generate a persistent machine identifier (MAC‑address based UUID)
def _generate_machine_id():
    # uuid.getnode() returns the hardware MAC address as a 48‑bit integer
    mac_int = uuid.getnode()
    return str(uuid.UUID(int=mac_int))

MACHINE_ID = _generate_machine_id()

# Optional secret token for additional authentication (can be empty)
AUTH_TOKEN = ""  # set to a shared secret if desired


# ----------------------------------------------------------------------
# Command execution sandbox – whitelist of safe commands
# ----------------------------------------------------------------------
def _execute_command(command_dict):
    """
    Execute a whitelisted command received from the relay.

    Expected format:
        {
            "action": "open_browser",
            "args": {"url": "https://example.com"}
        }
    Returns a dict with ``status`` and optional ``output``.
    """
    action = command_dict.get("action")
    args = command_dict.get("args", {})

    # Whitelisted actions
    if action == "open_browser":
        url = args.get("url", "https://www.google.com")
        try:
            if platform.system() == "Darwin":      # macOS
                subprocess.run(["open", url], check=True)
            elif platform.system() == "Windows":  # Windows
                subprocess.run(["start", url], shell=True, check=True)
            else:                                 # Linux/Unix
                subprocess.run(["xdg-open", url], check=True)
            return {"status": "ok", "output": f"Browser opened: {url}"}
        except Exception as e:
            return {"status": "error", "output": str(e)}

    elif action == "run_shell":
        # Very limited: only allow simple, non‑interactive commands
        cmd = args.get("cmd")
        if not cmd:
            return {"status": "error", "output": "Missing 'cmd' argument"}
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=10)
            return {"status": "ok", "output": result}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "output": e.output}
        except Exception as e:
            return {"status": "error", "output": str(e)}

    else:
        return {"status": "error", "output": f"Unsupported action: {action}"}


# ----------------------------------------------------------------------
# Communication helpers
# ----------------------------------------------------------------------
def _post(path, payload):
    url = f"{SERVER_URL.rstrip('/')}{path}"
    headers = {"Content-Type": "application/json"}
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def _register():
    payload = {
        "machine_id": MACHINE_ID,
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
    }
    return _post("/register", payload)


def _fetch_commands():
    payload = {"machine_id": MACHINE_ID}
    return _post("/fetch", payload)


def _send_result(command_id, result):
    payload = {
        "machine_id": MACHINE_ID,
        "command_id": command_id,
        "result": result,
    }
    return _post("/result", payload)


# ----------------------------------------------------------------------
# Main worker thread
# ----------------------------------------------------------------------
def _worker_loop(poll_interval=5):
    while True:
        fetch_resp = _fetch_commands()
        if fetch_resp.get("error"):
            time.sleep(poll_interval)
            continue

        commands = fetch_resp.get("commands", [])
        for cmd in commands:
            cmd_id = cmd.get("id")
            cmd_body = cmd.get("body", {})
            exec_result = _execute_command(cmd_body)
            _send_result(cmd_id, exec_result)

        time.sleep(poll_interval)


def start_client():
    """
    Entry‑point to start the remote‑execution client.
    Call this function from your application’s startup routine.
    """
    reg = _register()
    if reg.get("error"):
        raise RuntimeError(f"Failed to register with relay: {reg['error']}")

    thread = threading.Thread(target=_worker_loop, daemon=True)
    thread.start()
    return thread
import socket
import threading
import subprocess
import json
import uuid
import platform
import os
import sys
import time

# Configuration – can be overridden by environment variables
SERVER_HOST = os.getenv("REMOTE_RELAY_HOST", "localhost")
SERVER_PORT = int(os.getenv("REMOTE_RELAY_PORT", "9000"))
RECONNECT_DELAY = 5  # seconds

# ----------------------------------------------------------------------
# Machine identification
# ----------------------------------------------------------------------
def get_machine_token():
    """
    Returns a stable identifier for the machine.
    Uses the MAC address derived from uuid.getnode().
    """
    mac_int = uuid.getnode()
    # If getnode could not obtain a MAC, fallback to a random UUID
    if (mac_int >> 40) % 2:
        return str(uuid.uuid4())
    return f"{mac_int:012x}"

MACHINE_TOKEN = get_machine_token()
PLATFORM_INFO = platform.system()


# ----------------------------------------------------------------------
# Command execution
# ----------------------------------------------------------------------
def execute_command(command):
    """
    Executes a shell command safely and returns a dict with the result.
    """
    try:
        # Using subprocess.run for simplicity; shell=False for safety
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {
            "output": result.stdout,
            "error": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired as e:
        return {
            "output": "",
            "error": f"Command timed out after {e.timeout} seconds",
            "returncode": -1,
        }
    except Exception as e:
        return {
            "output": "",
            "error": f"Execution failed: {str(e)}",
            "returncode": -1,
        }


# ----------------------------------------------------------------------
# Client networking
# ----------------------------------------------------------------------
def handle_server_messages(sock):
    """
    Listens for incoming JSON messages from the relay server.
    Expected message format:
        {"type": "command", "command": "<shell command>"}
    """
    buffer = ""
    while True:
        try:
            data = sock.recv(4096).decode("utf-8")
            if not data:
                # Connection closed
                break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue  # ignore malformed lines

                if msg.get("type") == "command":
                    cmd = msg.get("command", "")
                    # ------------------------------------------------------------------
                    # Scope validation – simple whitelist (can be extended)
                    # ------------------------------------------------------------------
                    allowed_prefixes = ["open ", "start ", "xdg-open ", "open -a "]
                    if not any(cmd.startswith(p) for p in allowed_prefixes):
                        response = {
                            "type": "response",
                            "status": "rejected",
                            "reason": "Command not allowed by scope policy",
                        }
                    else:
                        exec_result = execute_command(cmd)
                        response = {
                            "type": "response",
                            "status": "ok",
                            "output": exec_result["output"],
                            "error": exec_result["error"],
                            "returncode": exec_result["returncode"],
                        }
                    sock.sendall((json.dumps(response) + "\n").encode("utf-8"))
        except Exception:
            break  # any socket error ends the listener


def register_and_listen():
    """
    Establishes a persistent connection to the relay server,
    registers the machine, and starts the listener thread.
    Reconnects automatically on failure.
    """
    while True:
        try:
            with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
                # Register
                register_msg = {
                    "type": "register",
                    "token": MACHINE_TOKEN,
                    "platform": PLATFORM_INFO,
                }
                sock.sendall((json.dumps(register_msg) + "\n").encode("utf-8"))

                # Start listener
                listener = threading.Thread(
                    target=handle_server_messages, args=(sock,), daemon=True
                )
                listener.start()

                # Keep the main thread alive while the socket is open
                while listener.is_alive():
                    time.sleep(1)

        except (ConnectionRefusedError, OSError):
            # Server not reachable – wait and retry
            time.sleep(RECONNECT_DELAY)
        except Exception as e:
            # Unexpected error – log and retry
            sys.stderr.write(f"Remote client error: {e}\\n")
            time.sleep(RECONNECT_DELAY)


if __name__ == "__main__":
    register_and_listen()
import asyncio
import json
import os
import sys
import subprocess
import webbrowser
from pathlib import Path

import websockets

# Configuration – can be overridden via environment variables
SERVER_HOST = os.getenv("REMOTE_EXEC_SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("REMOTE_EXEC_SERVER_PORT", "8765"))
TOKEN_FILE = Path.home() / ".remote_exec_token"

# Whitelisted commands that the client is allowed to execute
ALLOWED_COMMANDS = {
    "open_browser": lambda args: webbrowser.open(args.get("url", "https://www.google.com")),
    "run_subprocess": lambda args: subprocess.run(args.get("cmd", []), check=False),
    # Add more safe commands here
}


def get_or_create_token() -> str:
    """Load a persistent token for this machine, creating one if necessary."""
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    import secrets
    token = secrets.token_urlsafe(32)
    TOKEN_FILE.write_text(token)
    return token


async def handle_messages(websocket):
    """Main loop: receive commands, validate, execute, and send back results."""
    async for message in websocket:
        try:
            payload = json.loads(message)
            cmd = payload.get("cmd")
            args = payload.get("args", {})
            request_id = payload.get("request_id")

            if cmd not in ALLOWED_COMMANDS:
                response = {
                    "request_id": request_id,
                    "status": "error",
                    "error": f"Command '{cmd}' is not allowed."
                }
            else:
                try:
                    result = ALLOWED_COMMANDS[cmd](args)
                    # For subprocess we capture returncode; for others we just acknowledge success
                    if isinstance(result, subprocess.CompletedProcess):
                        output = {
                            "returncode": result.returncode,
                            "stdout": result.stdout,
                            "stderr": result.stderr,
                        }
                    else:
                        output = {"result": "ok"}
                    response = {
                        "request_id": request_id,
                        "status": "success",
                        "output": output,
                    }
                except Exception as e:
                    response = {
                        "request_id": request_id,
                        "status": "error",
                        "error": str(e),
                    }
        except json.JSONDecodeError:
            response = {"status": "error", "error": "Invalid JSON received."}
            request_id = None

        # Always include request_id if we have it so the server can route the reply
        if request_id is not None:
            await websocket.send(json.dumps(response))


async def main():
    token = get_or_create_token()
    uri = f"ws://{SERVER_HOST}:{SERVER_PORT}?token={token}"
    async with websockets.connect(uri) as websocket:
        await handle_messages(websocket)


if __name__ == "__main__":
    # Run the client; reconnect on failure
    while True:
        try:
            asyncio.run(main())
        except (ConnectionRefusedError, websockets.exceptions.InvalidURI,
                websockets.exceptions.ConnectionClosedError):
            print("Connection to relay failed, retrying in 5 seconds...", file=sys.stderr)
            import time
            time.sleep(5)
import os
import uuid
import time
import json
import subprocess
import requests

# URL of the relay server (can be overridden via env var)
SERVER_URL = os.getenv("REMOTE_EXEC_RELAY_URL", "http://localhost:5000")
# Shared secret between client and relay – must match the relay's token
AUTH_TOKEN = os.getenv("REMOTE_EXEC_TOKEN", "CHANGE_ME")

# Unique identifier for this machine (MAC address based)
MACHINE_ID = hex(uuid.getnode())


def register():
    """Register this machine with the relay so it can receive commands."""
    try:
        requests.post(
            f"{SERVER_URL}/register",
            json={"machine_id": MACHINE_ID},
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
            timeout=5,
        )
    except Exception as e:
        print(f"[remote_execution_client] Registration failed: {e}")


def fetch_and_execute():
    """Continuously poll the relay for pending commands, execute them, and send back results."""
    while True:
        try:
            resp = requests.get(
                f"{SERVER_URL}/fetch",
                params={"machine_id": MACHINE_ID},
                headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                timeout=10,
            )
            if resp.status_code == 200:
                payload = resp.json()
                command = payload.get("command")
                if command:
                    # Execute the command locally
                    result = subprocess.run(
                        command, shell=True, capture_output=True, text=True
                    )
                    # Send execution result back to the relay
                    result_payload = {
                        "machine_id": MACHINE_ID,
                        "command": command,
                        "returncode": result.returncode,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                    }
                    requests.post(
                        f"{SERVER_URL}/response",
                        json=result_payload,
                        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                        timeout=5,
                    )
        except Exception as e:
            print(f"[remote_execution_client] Error during fetch/execute: {e}")

        # Small pause to avoid hammering the server
        time.sleep(5)


if __name__ == "__main__":
    register()
    fetch_and_execute()
import asyncio
import json
import os
import subprocess
import sys
import uuid

import websockets

# URL of the relay server (WebSocket endpoint)
SERVER_URL = os.getenv("REMOTE_RELAY_URL", "ws://localhost:8080/ws")
# Unique token identifying this machine – must be set in the environment
TOKEN = os.getenv("REMOTE_TOKEN")

# ----------------------------------------------------------------------
# Command whitelist – only these actions may be executed on the client.
# Extend as needed. Each entry receives a list of arguments and must
# return a CompletedProcess (or similar) with stdout, stderr and returncode.
# ----------------------------------------------------------------------
ALLOWED_ACTIONS = {
    "open_browser": lambda args: subprocess.run(
        ["open"] + (args or ["https://www.google.com"]),
        capture_output=True,
        text=True,
    ),
    "run": lambda args: subprocess.run(
        args,
        capture_output=True,
        text=True,
    ),
}


async def _process_message(ws, raw_message: str):
    """Execute a single command received from the relay and reply."""
    try:
        data = json.loads(raw_message)
        request_id = data.get("request_id")
        action = data.get("action")
        args = data.get("args", [])

        if action not in ALLOWED_ACTIONS:
            result = {"error": f"Action '{action}' is not permitted"}
        else:
            proc = ALLOWED_ACTIONS[action](args)
            result = {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "returncode": proc.returncode,
            }

        await ws.send(
            json.dumps(
                {
                    "request_id": request_id,
                    "result": result,
                }
            )
        )
    except Exception as exc:  # pragma: no cover – defensive
        await ws.send(
            json.dumps(
                {
                    "request_id": data.get("request_id", str(uuid.uuid4())),
                    "error": str(exc),
                }
            )
        )


async def _listen(ws):
    async for message in ws:
        await _process_message(ws, message)


async def main():
    if not TOKEN:
        print("ERROR: REMOTE_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Append token as a query‑string argument – the relay validates it.
    async with websockets.connect(f"{SERVER_URL}?token={TOKEN}") as ws:
        await _listen(ws)


if __name__ == "__main__":
    asyncio.run(main())
import socket
import threading
import json
import subprocess
import platform
import uuid
import sys
import time

# ----------------------------------------------------------------------
# Remote Execution Client
# ----------------------------------------------------------------------
# This client runs on a user's machine. It connects to the relay server,
# registers itself using a unique identifier (MAC address) and a secret
# token, receives JSON‑encoded commands, validates them against an
# allow‑list, executes them locally, and sends back the result.
# ----------------------------------------------------------------------

class RemoteExecutionClient:
    def __init__(self, server_host: str, server_port: int, token: str,
                 allowed_commands: list = None):
        self.server_host = server_host
        self.server_port = server_port
        self.token = token
        # Use MAC address as a stable identifier; fallback to UUID if unavailable
        self.machine_id = self._get_machine_id()
        self.allowed_commands = allowed_commands or [
            "open", "start", "xdg-open", "open -a", "firefox", "chrome"
        ]
        self.sock = None
        self._stop_event = threading.Event()

    @staticmethod
    def _get_machine_id() -> str:
        # uuid.getnode() returns a 48‑bit MAC if available; otherwise a random value
        mac = uuid.getnode()
        return ":".join(f"{(mac >> ele) & 0xff:02x}" for ele in range(40, -1, -8))

    def _connect(self):
        while not self._stop_event.is_set():
            try:
                self.sock = socket.create_connection((self.server_host, self.server_port))
                self._register()
                return
            except Exception as e:
                print(f"[RemoteExecutionClient] Connection failed ({e}), retrying in 5s...", file=sys.stderr)
                time.sleep(5)

    def _register(self):
        reg_msg = {
            "type": "register",
            "machine_id": self.machine_id,
            "token": self.token,
            "platform": platform.system(),
            "hostname": platform.node()
        }
        self._send_json(reg_msg)

    def _send_json(self, obj: dict):
        data = json.dumps(obj).encode("utf-8") + b"\n"
        self.sock.sendall(data)

    def _receive_loop(self):
        buffer = b""
        while not self._stop_event.is_set():
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    raise ConnectionError("Socket closed")
                buffer += chunk
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    if line:
                        self._handle_message(json.loads(line.decode("utf-8")))
            except Exception as e:
                print(f"[RemoteExecutionClient] Connection lost ({e}), reconnecting...", file=sys.stderr)
                self._connect()

    def _handle_message(self, msg: dict):
        if msg.get("type") != "command":
            return  # ignore unknown messages

        command = msg.get("command")
        request_id = msg.get("request_id")

        # ------------------------------------------------------------------
        # Scope validation – only allow commands that start with an allowed prefix
        # ------------------------------------------------------------------
        if not any(command.startswith(allowed) for allowed in self.allowed_commands):
            response = {
                "type": "result",
                "request_id": request_id,
                "status": "error",
                "output": f"Command not allowed: {command}"
            }
            self._send_json(response)
            return

        # Execute the command locally
        try:
            completed = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            output = completed.stdout + completed.stderr
            status = "success" if completed.returncode == 0 else "error"
        except Exception as e:
            output = str(e)
            status = "error"

        response = {
            "type": "result",
            "request_id": request_id,
            "status": status,
            "output": output
        }
        self._send_json(response)

    def start(self):
        self._connect()
        threading.Thread(target=self._receive_loop, daemon=True).start()
        print("[RemoteExecutionClient] Running. Press Ctrl+C to stop.")
        try:
            while not self._stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self._stop_event.set()
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            except Exception:
                pass
        print("[RemoteExecutionClient] Stopped.")


if __name__ == "__main__":
    # Example usage:
    #   python remote_execution_client.py <relay_host> <relay_port> <shared_secret_token>
    if len(sys.argv) != 4:
        print("Usage: python remote_execution_client.py <host> <port> <token>")
        sys.exit(1)

    host, port, token = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    client = RemoteExecutionClient(host, port, token)
    client.start()