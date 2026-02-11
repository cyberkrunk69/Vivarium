"""Logs blueprint: recent logs and raw log file endpoints."""
from __future__ import annotations

from flask import Blueprint, jsonify, request, current_app

bp = Blueprint('logs', __name__, url_prefix='/api')


def _app_helpers():
    """Lazy import from control_panel_app to avoid circular imports."""
    from vivarium.runtime import control_panel_app as app

    return (
        app.ACTION_LOG,
        app.EXECUTION_LOG,
        app.API_AUDIT_LOG_FILE,
        app.LEGACY_API_AUDIT_LOG_FILE,
        app._read_jsonl_tail,
        app._read_api_audit_entries,
        app._map_execution_entry_to_log,
        app._map_api_audit_entry_to_log,
        app._entry_timestamp_sort_key,
        app._log_entry_dedupe_key,
    )


@bp.route('/logs/recent', methods=['GET'])
def get_logs_recent():
    """GET /api/logs/recent?limit=N - Return a recent tail of action + execution entries for UI backfill."""
    (
        ACTION_LOG,
        EXECUTION_LOG,
        _,
        _,
        _read_jsonl_tail,
        _read_api_audit_entries,
        _map_execution_entry_to_log,
        _map_api_audit_entry_to_log,
        _entry_timestamp_sort_key,
        _log_entry_dedupe_key,
    ) = _app_helpers()

    limit = request.args.get('limit', 500, type=int)
    safe_limit = max(1, min(5000, int(limit)))
    action_entries = _read_jsonl_tail(ACTION_LOG, max_lines=safe_limit)
    execution_entries = _read_jsonl_tail(EXECUTION_LOG, max_lines=safe_limit)
    api_audit_entries = _read_api_audit_entries(max_lines=safe_limit)
    mapped_execution = []
    for raw in execution_entries:
        mapped_execution.append(_map_execution_entry_to_log(raw))
    mapped_api_audit = []
    for raw in api_audit_entries:
        mapped_api_audit.append(_map_api_audit_entry_to_log(raw))
    merged = list(action_entries) + mapped_execution + mapped_api_audit
    merged.sort(key=_entry_timestamp_sort_key)
    deduped_entries = []
    seen: set[tuple[str, str, str, str, str, str]] = set()
    for entry in merged:
        dedupe_key = _log_entry_dedupe_key(entry)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        deduped_entries.append(entry)
    trimmed_entries = deduped_entries[-safe_limit:]
    return jsonify({
        'success': True,
        'entries': trimmed_entries,
        'limit': safe_limit,
        'returned': len(trimmed_entries),
        'available': len(deduped_entries),
        'is_truncated': len(deduped_entries) > safe_limit,
    })


@bp.route('/logs/raw', methods=['GET'])
def get_logs_raw():
    """GET /api/logs/raw?kind=action|execution|api - Return raw log file content for operator inspection/download."""
    (
        ACTION_LOG,
        EXECUTION_LOG,
        API_AUDIT_LOG_FILE,
        LEGACY_API_AUDIT_LOG_FILE,
        *_,
    ) = _app_helpers()

    kind = str(request.args.get('kind', 'action') or 'action').strip().lower()
    if kind in {'action', 'actions'}:
        source = ACTION_LOG
    elif kind in {'execution', 'exec'}:
        source = EXECUTION_LOG
    elif kind in {'api', 'audit', 'api_audit'}:
        source = API_AUDIT_LOG_FILE if API_AUDIT_LOG_FILE.exists() else LEGACY_API_AUDIT_LOG_FILE
    else:
        return jsonify({'success': False, 'error': 'kind must be action, execution, or api'}), 400

    if not source.exists():
        return current_app.response_class("", mimetype="text/plain")
    try:
        raw_text = source.read_text(encoding='utf-8')
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)}), 500
    return current_app.response_class(raw_text, mimetype="text/plain")
