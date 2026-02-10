import ipaddress
from fastapi import HTTPException, Request

# List of allowed LAN CIDR blocks
LAN_CIDRS = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
]

def is_lan_ip(ip: str) -> bool:
    """Return True if the IP belongs to one of the allowed LAN CIDR blocks."""
    try:
        addr = ipaddress.IPv4Address(ip)
        return any(addr in net for net in LAN_CIDRS)
    except ValueError:
        return False

async def validate_request(request: Request):
    """Raise HTTPException if the request violates LAN safety rules."""
    client_ip = request.client.host

    # 1️⃣ IP origin check
    if not is_lan_ip(client_ip):
        raise HTTPException(status_code=403, detail="Access denied: non‑LAN IP")

    # 2️⃣ Command‑scope validation (only for mutating methods)
    if request.method in ("POST", "PUT", "PATCH"):
        try:
            body = await request.json()
        except Exception:
            # If body is not JSON, ignore scope validation (will be caught later)
            return

        target = body.get("target_machine")
        if target and target != client_ip:
            raise HTTPException(
                status_code=400,
                detail="Invalid target_machine: must match caller's IP",
            )