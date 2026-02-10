"""
def is_port_open(port: int, host: str = "127.0.0.1") -> bool:
    """
    Quick utility used by the test suite to verify that a TCP port is
    listening on *host*. Returns ``True`` if a connection can be made,
    ``False`` otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        try:
            sock.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False
lan_server.py
--------------

Dual-server implementation for the swarm project.

- **AdminServer** – binds only to 127.0.0.1 (loopback).  Handles privileged
  administrative requests.
- **LANServer** – binds to 0.0.0.0 (all interfaces) but only accepts
  connections from a configurable whitelist of LAN IPs.  Handles normal
  user requests.

Both servers share a tiny request‑routing layer that inspects the
originating IP address and enforces a privilege level before delegating
to the appropriate handler.

The module can be started directly; it will launch both servers in
separate threads so they run concurrently.
"""

import threading
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from enum import Enum
import json
import os

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Port numbers – feel free to adjust in the future
ADMIN_PORT = int(os.getenv("ADMIN_PORT", "8080"))
LAN_PORT = int(os.getenv("LAN_PORT", "8081"))

# LAN whitelist – only these IPv4 addresses are allowed to talk to the LAN
# server.  Use CIDR notation or a simple list; for simplicity we use a list.
LAN_WHITELIST = {
    "192.168.1.0/24",   # typical home/office LAN
    "10.0.0.0/8",       # corporate LANs
    "172.16.0.0/12",    # private networks
}

# --------------------------------------------------------------------------- #
# Privilege model
# --------------------------------------------------------------------------- #

class PrivilegeLevel(Enum):
    ADMIN = "admin"
    USER = "user"

def ip_in_whitelist(ip: str) -> bool:
    """Very small CIDR matcher – sufficient for the demo."""
    import ipaddress
    try:
        ip_obj = ipaddress.ip_address(ip)
        for net in LAN_WHITELIST:
            if ip_obj in ipaddress.ip_network(net, strict=False):
                return True
    except ValueError:
        pass
    return False

def determine_privilege(remote_ip: str) -> PrivilegeLevel:
    """Return the privilege level for a given remote IP."""
    if remote_ip == "127.0.0.1":
        return PrivilegeLevel.ADMIN
    if ip_in_whitelist(remote_ip):
        return PrivilegeLevel.USER
    # Anything else is treated as unauthenticated / no‑privilege
    return None

# --------------------------------------------------------------------------- #
# Core request handler – shared logic
# --------------------------------------------------------------------------- #

class DualRequestHandler(BaseHTTPRequestHandler):
    """
    A single handler class used by both servers.  It inspects the remote
    address, decides the privilege level and then dispatches to the
    appropriate method.
    """

    # Mapping of (privilege, path) -> handler method
    ROUTES = {
        (PrivilegeLevel.ADMIN, "/admin/status"): "handle_admin_status",
        (PrivilegeLevel.USER,  "/user/echo"):    "handle_user_echo",
    }

    def _json_response(self, data, status=200):
        """Utility to send a JSON response."""
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _reject(self, reason="Forbidden"):
        """Send a 403 response."""
        self._json_response({"error": reason}, status=403)

    def do_GET(self):
        remote_ip = self.client_address[0]
        privilege = determine_privilege(remote_ip)

        if privilege is None:
            self._reject("IP not authorized")
            return

        parsed = urlparse(self.path)
        route_key = (privilege, parsed.path)

        handler_name = self.ROUTES.get(route_key)
        if not handler_name:
            self._reject("No route for this privilege/path")
            return

        # Dispatch to the concrete handler
        getattr(self, handler_name)(parsed)

    # ------------------------------------------------------------------- #
    # Admin handlers
    # ------------------------------------------------------------------- #

    def handle_admin_status(self, parsed):
        """Return a tiny status payload – only reachable from 127.0.0.1."""
        self._json_response({
            "server": "AdminServer",
            "status": "running",
            "origin": self.client_address[0],
        })

    # ------------------------------------------------------------------- #
    # User handlers
    # ------------------------------------------------------------------- #

    def handle_user_echo(self, parsed):
        """Echo back query parameters – reachable from whitelisted LAN IPs."""
        query = parse_qs(parsed.query)
        self._json_response({
            "server": "LANServer",
            "echo": query,
            "origin": self.client_address[0],
        })

    # Suppress noisy logging – optional but nice for a demo
    def log_message(self, format, *args):
        return  # comment this line to enable default logging

# --------------------------------------------------------------------------- #
# Server wrappers
# --------------------------------------------------------------------------- #

class AdminServer:
    """
    Listens only on the loopback interface (127.0.0.1).  Any request that
    reaches this server is automatically considered ADMIN privilege.
    """

    def __init__(self, host="127.0.0.1", port=ADMIN_PORT):
        self.host = host
        self.port = port
        self.httpd = HTTPServer((self.host, self.port), DualRequestHandler)

    def start(self):
        print(f"[AdminServer] Listening on http://{self.host}:{self.port}")
        self.httpd.serve_forever()


class LANServer:
    __all__ = ["LANServer"]
    """
    Listens on all interfaces (0.0.0.0) but enforces a whitelist of
    allowed client IPs.  Requests from non‑whitelisted IPs are rejected
    with a 403.
    """

    def __init__(self, host="0.0.0.0", port=LAN_PORT):
        self.host = host
        self.port = port
        self.httpd = HTTPServer((self.host, self.port), DualRequestHandler)

    def start(self):
        print(f"[LANServer] Listening on http://{self.host}:{self.port}")
        self.httpd.serve_forever()


# --------------------------------------------------------------------------- #
# Startup script – runs both servers concurrently
# --------------------------------------------------------------------------- #

def _run_admin():
    server = AdminServer()
    server.start()

def _run_lan():
    server = LANServer()
    server.start()

def main():
    """
    Entry‑point used when the module is executed directly:
        python lan_server.py

    It spawns two daemon threads – one for each server – and then joins
    them so the process stays alive until interrupted (Ctrl‑C).
    """
    admin_thread = threading.Thread(target=_run_admin, daemon=True)
    lan_thread   = threading.Thread(target=_run_lan,   daemon=True)

    admin_thread.start()
    lan_thread.start()

    print("[DualServer] Both AdminServer and LANServer are up and running.")
    try:
        # Keep the main thread alive while child threads run
        admin_thread.join()
        lan_thread.join()
    except KeyboardInterrupt:
        print("\n[DualServer] Shutdown requested – exiting.")
        # HTTPServer.serve_forever() respects KeyboardInterrupt internally,
        # so we just exit here.

if __name__ == "__main__":
    main()


def start_lan_servers_background():
    """Start both LAN servers in background threads. Safe to call from spawner init."""
    import threading
    admin_thread = threading.Thread(target=_run_admin, daemon=True, name="AdminServer")
    lan_thread = threading.Thread(target=_run_lan, daemon=True, name="LANServer")
    admin_thread.start()
    lan_thread.start()
    print("[LAN] AdminServer (127.0.0.1:8080) and LANServer (0.0.0.0:8081) started")