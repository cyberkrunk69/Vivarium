#!/usr/bin/env python3
"""
Local monitoring dashboard server for the Claude swarm.
Provides real-time monitoring of workers, experiments, and system health.
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from flask import Flask, jsonify, request, render_template_string
from flask_socketio import SocketIO, emit
import threading
import glob
import hashlib

# File watcher for auto-reload
WATCH_FILES = ['dashboard.html', 'templates/dashboard.html']
file_hashes = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'swarm_monitor_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state
pending_changes = []
change_counter = 0

def load_json_file(filepath: str, default=None):
    """Load JSON file with error handling."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
    return default or {}

def get_grind_session_status():
    """Get status from grind session logs."""
    grind_logs = glob.glob("grind_logs/session_*.json")
    sessions = []

    for log_file in sorted(grind_logs)[-10:]:  # Last 10 sessions
        try:
            with open(log_file, 'r') as f:
                session_data = json.load(f)
                sessions.append({
                    'file': os.path.basename(log_file),
                    'returncode': session_data.get('returncode', 'unknown'),
                    'duration_ms': session_data.get('duration_ms', 0),
                    'timestamp': session_data.get('timestamp', 'unknown'),
                    'status': 'success' if session_data.get('returncode') == 0 else 'failed'
                })
        except Exception as e:
            print(f"Error reading {log_file}: {e}")

    return sessions

def get_cost_tracking():
    """Get cost information from cost tracker."""
    # Try to load actual cost tracking data if available
    cost_data = {}
    performance_data = load_json_file('performance_history.json', {})

    # Calculate metrics from session data
    sessions = get_grind_session_status()
    total_sessions = len(sessions)
    success_count = sum(1 for s in sessions if s.get('status') == 'success')
    success_rate = f"{(success_count/total_sessions*100):.1f}%" if total_sessions > 0 else "0%"

    # Calculate average duration
    total_duration = sum(s.get('duration_ms', 0) for s in sessions)
    avg_duration = f"{(total_duration/total_sessions/1000):.1f}s" if total_sessions > 0 else "0s"

    return {
        'total_sessions': total_sessions,
        'success_rate': success_rate,
        'avg_duration': avg_duration,
        'performance_metrics': performance_data
    }

def get_active_workers():
    """Get information about active workers."""
    opus_state = load_json_file('opus_orchestrator_state.json', {})
    wave_status = load_json_file('wave_status.json', {})

    workers = []

    # Extract worker info from opus state
    if 'workers' in opus_state:
        for worker_id, worker_data in opus_state['workers'].items():
            workers.append({
                'id': worker_id,
                'status': worker_data.get('status', 'unknown'),
                'current_task': worker_data.get('current_task', 'idle'),
                'last_update': worker_data.get('last_update', 'unknown')
            })

    # Add wave status info
    wave_info = {
        'current_wave': wave_status.get('current_wave', 'unknown'),
        'wave_progress': wave_status.get('progress', 'unknown'),
        'total_workers': len(workers) or 10  # Default from recent logs
    }

    return {'workers': workers, 'wave_info': wave_info}

def get_recent_experiments():
    """Get recent experiments and their status."""
    experiments = load_json_file('experiments_manifest.json', {})
    grind_tasks = load_json_file('grind_tasks.json', {})

    recent_experiments = []

    # Add experiments from manifest
    if 'experiments' in experiments:
        for exp_id, exp_data in experiments['experiments'].items():
            recent_experiments.append({
                'id': exp_id,
                'title': exp_data.get('title', 'Unknown'),
                'status': exp_data.get('status', 'pending'),
                'created_at': exp_data.get('created_at', 'unknown'),
                'description': exp_data.get('description', '')[:100] + '...'
            })

    return recent_experiments[:10]  # Last 10 experiments

@app.route('/')
def index():
    """Serve the dashboard HTML."""
    with open('dashboard.html', 'r') as f:
        return f.read()

@app.route('/status')
def status():
    """Get overall system status."""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'uptime': time.time(),
        'active_workers': get_active_workers(),
        'session_health': get_grind_session_status()[-5:],  # Last 5 sessions
        'system_health': 'healthy'
    })

@app.route('/experiments')
def experiments():
    """Get recent experiments."""
    return jsonify({
        'experiments': get_recent_experiments(),
        'total_count': len(get_recent_experiments())
    })

@app.route('/pending-changes')
def pending_changes_endpoint():
    """Get pending code changes."""
    global pending_changes
    return jsonify({
        'changes': pending_changes,
        'count': len(pending_changes)
    })

@app.route('/approve/<int:change_id>', methods=['POST'])
def approve_change(change_id):
    """Approve a pending change."""
    global pending_changes

    for i, change in enumerate(pending_changes):
        if change['id'] == change_id:
            change['status'] = 'approved'
            change['approved_at'] = datetime.now().isoformat()

            # Emit update via WebSocket
            socketio.emit('change_approved', change)

            return jsonify({
                'status': 'success',
                'message': f'Change {change_id} approved',
                'change': change
            })

    return jsonify({
        'status': 'error',
        'message': f'Change {change_id} not found'
    }), 404

@app.route('/cost-tracking')
def cost_tracking():
    """Get cost and performance tracking data."""
    return jsonify(get_cost_tracking())

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    emit('connected', {'message': 'Connected to swarm monitor'})

@socketio.on('request_update')
def handle_update_request():
    """Handle client request for updates."""
    emit('status_update', {
        'workers': get_active_workers(),
        'experiments': get_recent_experiments()[:5],
        'cost_data': get_cost_tracking(),
        'timestamp': datetime.now().isoformat()
    })

def get_file_hash(filepath):
    """Get MD5 hash of file contents."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
    except:
        pass
    return None

def check_file_changes():
    """Check if any watched files have changed."""
    global file_hashes
    changed = False
    for filepath in WATCH_FILES:
        current_hash = get_file_hash(filepath)
        if filepath in file_hashes and file_hashes[filepath] != current_hash:
            print(f"[AUTO-RELOAD] Detected change in {filepath}")
            changed = True
        file_hashes[filepath] = current_hash
    return changed

def background_monitor():
    """Background thread for periodic updates and file watching."""
    global file_hashes
    # Initialize file hashes
    for filepath in WATCH_FILES:
        file_hashes[filepath] = get_file_hash(filepath)

    while True:
        time.sleep(2)  # Check every 2 seconds

        # Check for file changes - trigger browser reload
        if check_file_changes():
            print("[AUTO-RELOAD] Broadcasting reload signal to clients")
            socketio.emit('reload', {'reason': 'file_changed'})

        # Regular status update every 10 seconds (use modulo)
        socketio.emit('live_update', {
            'workers': get_active_workers(),
            'session_count': len(get_grind_session_status()),
            'timestamp': datetime.now().isoformat()
        })

# Start background monitoring thread
monitor_thread = threading.Thread(target=background_monitor, daemon=True)
monitor_thread.start()

if __name__ == '__main__':
    print("Starting swarm monitoring dashboard on http://localhost:8420")
    socketio.run(app, host='0.0.0.0', port=8420, debug=True)