# session_manager.py (simplified)
import uuid, redis, subprocess, json, socket

r = redis.Redis()
LAN_IFACE = "eth0"

def get_ip(conn):
    return conn.getpeername()[0]

def ensure_session(ip):
    sid = r.get(f"ip:{ip}")
    if sid:
        return sid.decode()
    sid = str(uuid.uuid4())
    r.set(f"ip:{ip}", sid, ex=1800)   # 30‑min TTL
    launch_sandbox(sid, ip)
    return sid

def launch_sandbox(sid, ip):
    # Example: firecracker VM with network namespace bound to IP
    subprocess.run([
        "firecracker", "--id", sid,
        "--net", f"{LAN_IFACE}:{ip}"
    ], check=True)

def handle_conn(conn):
    ip = get_ip(conn)
    sid = ensure_session(ip)
    # forward data to sandbox via unix socket or HTTP