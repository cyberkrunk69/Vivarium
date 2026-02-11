"""Groq API key blueprint: read, save, and clear key from file."""
from __future__ import annotations

import os
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request

from vivarium.runtime import config as runtime_config

bp = Blueprint('groq_key', __name__, url_prefix='/api')


def _get_key_file() -> Path:
    return current_app.config['GROQ_API_KEY_FILE']


def _mask_secret(secret: str) -> str:
    value = (secret or "").strip()
    if len(value) <= 8:
        return "****"
    return f"{value[:4]}...{value[-4:]}"


def _persist_key(api_key: str) -> None:
    key_file = _get_key_file()
    key_file.parent.mkdir(parents=True, exist_ok=True)
    key_file.write_text(api_key.strip() + "\n", encoding="utf-8")
    try:
        os.chmod(key_file, 0o600)
    except OSError:
        pass


def _delete_persisted_key() -> None:
    key_file = _get_key_file()
    try:
        if key_file.exists():
            key_file.unlink()
    except OSError:
        pass


def _load_persisted_key() -> str:
    key_file = _get_key_file()
    if not key_file.exists():
        return ""
    try:
        return key_file.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def _reload_groq_runtime_clients() -> None:
    """Reset Groq client singleton so new key is used immediately."""
    try:
        from vivarium.runtime import groq_client
        groq_client._groq_engine = None
    except Exception:
        pass


def _ensure_groq_key_loaded() -> dict:
    live_key = (runtime_config.get_groq_api_key() or "").strip()
    if live_key:
        return {"configured": True, "key": live_key, "source": "env"}

    persisted = _load_persisted_key()
    if persisted:
        runtime_config.set_groq_api_key(persisted)
        _reload_groq_runtime_clients()
        return {"configured": True, "key": persisted, "source": "security_file"}

    return {"configured": False, "key": "", "source": None}


@bp.route('/groq_key', methods=['GET'])
def get_groq_key():
    """GET /api/groq_key - Return masked key status."""
    state = _ensure_groq_key_loaded()
    return jsonify(
        {
            "success": True,
            "configured": state["configured"],
            "source": state["source"],
            "masked_key": _mask_secret(state["key"]) if state["configured"] else None,
        }
    )


@bp.route('/groq_key', methods=['POST'])
def set_groq_key():
    """POST /api/groq_key - Save new key."""
    data = request.json or {}
    api_key = str(data.get("api_key", "")).strip()
    if not api_key:
        return jsonify({"success": False, "error": "api_key is required"}), 400
    if len(api_key) < 16:
        return jsonify({"success": False, "error": "api_key is too short"}), 400
    if len(api_key) > 256:
        return jsonify({"success": False, "error": "api_key is too long"}), 400

    _persist_key(api_key)
    runtime_config.set_groq_api_key(api_key)
    _reload_groq_runtime_clients()
    return jsonify(
        {
            "success": True,
            "configured": True,
            "masked_key": _mask_secret(api_key),
            "source": "security_file",
        }
    )


@bp.route('/groq_key', methods=['DELETE'])
def delete_groq_key():
    """DELETE /api/groq_key - Clear key"""
    _delete_persisted_key()
    runtime_config.set_groq_api_key(None)
    _reload_groq_runtime_clients()
    return jsonify({"success": True, "configured": False})
