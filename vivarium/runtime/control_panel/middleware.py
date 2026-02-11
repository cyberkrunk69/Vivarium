"""
Security middleware for the control panel: localhost-only enforcement and security headers.
"""

from ipaddress import ip_address

from flask import request, jsonify


def _is_loopback_host(host: str) -> bool:
    value = (host or "").strip().lower()
    if not value:
        return False
    if value in {"localhost", "testclient"}:
        return True
    try:
        return ip_address(value).is_loopback
    except ValueError:
        return False


def _request_source_host() -> str:
    forwarded = (request.headers.get("X-Forwarded-For") or "").strip()
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return (request.remote_addr or "").strip()


def is_request_from_loopback() -> bool:
    """Return True if the current request is from a loopback host."""
    return _is_loopback_host(_request_source_host())


def enforce_localhost_only():
    if is_request_from_loopback():
        return None
    return jsonify({"success": False, "error": "Control panel is localhost-only"}), 403


def apply_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response
