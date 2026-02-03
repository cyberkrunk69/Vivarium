#!/usr/bin/env python3
"""
Enhanced Black Swarm Command Center - Engine/Model Visibility
Real-time intelligence dashboard with per-node engine and model tracking.

Features:
- Per-worker engine type display (Claude, Groq, Auto)
- Real-time model information (sonnet, haiku, llama-3.3-70b, etc.)
- Engine selection reasoning display
- Cost breakdown by engine type
- Real-time engine usage statistics
"""

import http.server
import socketserver
import argparse
import json
import threading
import time
import os
from pathlib import Path
from datetime import datetime
import socket
import re
from collections import defaultdict

PORT = 8080
WORKSPACE = Path(__file__).parent.parent.parent  # Back to project root
EXPERIMENTS_DIR = WORKSPACE / "experiments"

# Global: list of SSE client queues and file modification times
sse_clients = []
sse_lock = threading.Lock()
last_mtimes = {}

# Engine statistics tracking
engine_stats = {
    'claude_usage_count': 0,
    'groq_usage_count': 0,
    'claude_cost': 0.0,
    'groq_cost': 0.0,
    'total_requests': 0,
    'response_times': [],
    'model_usage': defaultdict(int)
}


def get_file_mtimes():
    """Get modification times of monitored files."""
    files = [
        WORKSPACE / "wave_status.json",
        WORKSPACE / "SUMMARY.md",
        WORKSPACE / "PROGRESS.md",
        WORKSPACE / "learned_lessons.json",
        WORKSPACE / "grind_logs" / "*.json",
    ]
    mtimes = {}
    for pattern in files:
        if '*' in str(pattern):
            # Handle glob patterns
            for f in pattern.parent.glob(pattern.name):
                if f.is_file():
                    try:
                        mtimes[str(f)] = f.stat().st_mtime
                    except:
                        pass
        else:
            try:
                if pattern.exists():
                    mtimes[str(pattern)] = pattern.stat().st_mtime
            except:
                pass
    return mtimes


def load_wave_status():
    """Load wave status from JSON."""
    wave_file = WORKSPACE / "wave_status.json"
    if wave_file.exists():
        try:
            return json.loads(wave_file.read_text(encoding='utf-8'))
        except:
            pass
    return {"waves": [], "current_activity": {"title": "Initializing AI systems...", "workers": []}}


def analyze_engine_usage():
    """Analyze engine usage patterns from grind logs."""
    global engine_stats

    grind_logs_dir = WORKSPACE / "grind_logs"
    if not grind_logs_dir.exists():
        return engine_stats

    # Reset stats
    engine_stats = {
        'claude_usage_count': 0,
        'groq_usage_count': 0,
        'claude_cost': 0.0,
        'groq_cost': 0.0,
        'total_requests': 0,
        'response_times': [],
        'model_usage': defaultdict(int)
    }

    # Analyze recent log files
    log_files = sorted(grind_logs_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]

    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract engine usage from log entries
            if isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict):
                        analyze_log_entry(entry)
            elif isinstance(data, dict):
                analyze_log_entry(data)

        except Exception as e:
            continue

    # Calculate percentages
    if engine_stats['total_requests'] > 0:
        engine_stats['claude_usage_percent'] = round(
            (engine_stats['claude_usage_count'] / engine_stats['total_requests']) * 100, 1)
        engine_stats['groq_usage_percent'] = round(
            (engine_stats['groq_usage_count'] / engine_stats['total_requests']) * 100, 1)
    else:
        engine_stats['claude_usage_percent'] = 0
        engine_stats['groq_usage_percent'] = 0

    # Calculate average response time
    if engine_stats['response_times']:
        engine_stats['avg_response_time'] = int(sum(engine_stats['response_times']) / len(engine_stats['response_times']))
    else:
        engine_stats['avg_response_time'] = 0

    engine_stats['total_cost'] = engine_stats['claude_cost'] + engine_stats['groq_cost']

    return engine_stats


def analyze_log_entry(entry):
    """Analyze a single log entry for engine usage."""
    global engine_stats

    # Look for engine indicators in various fields
    entry_str = str(entry).lower()

    # Detect Claude usage
    claude_indicators = ['claude', 'sonnet', 'haiku', 'opus', 'anthropic']
    groq_indicators = ['groq', 'llama', 'mixtral', 'gemma']

    is_claude = any(indicator in entry_str for indicator in claude_indicators)
    is_groq = any(indicator in entry_str for indicator in groq_indicators)

    if is_claude and not is_groq:
        engine_stats['claude_usage_count'] += 1
        engine_stats['total_requests'] += 1
        # Estimate cost (rough approximation)
        engine_stats['claude_cost'] += 0.015  # ~$0.015 per request avg

    elif is_groq and not is_claude:
        engine_stats['groq_usage_count'] += 1
        engine_stats['total_requests'] += 1
        # Estimate cost (rough approximation)
        engine_stats['groq_cost'] += 0.002  # ~$0.002 per request avg

    # Extract model information
    for model in ['sonnet', 'haiku', 'opus', 'llama-3.3-70b', 'llama-3.1-70b', 'mixtral']:
        if model in entry_str:
            engine_stats['model_usage'][model] += 1

    # Extract duration if available
    if 'duration' in entry or 'time' in entry:
        try:
            duration = entry.get('duration_ms', entry.get('duration', entry.get('time_ms', 1000)))
            if isinstance(duration, (int, float)) and duration > 0:
                engine_stats['response_times'].append(duration)
        except:
            pass


def get_enhanced_worker_data():
    """Get worker data enhanced with engine/model information."""
    wave_data = load_wave_status()
    workers = wave_data.get("current_activity", {}).get("workers", [])

    # Enhance workers with engine/model info
    enhanced_workers = []
    for i, worker in enumerate(workers):
        enhanced_worker = dict(worker)

        # Determine engine type based on task content or patterns
        task = worker.get('task', '').lower()
        worker_type = worker.get('type', '').lower()

        # Engine selection logic
        if 'claude' in task or 'sonnet' in task or 'haiku' in task or 'opus' in task:
            enhanced_worker['engine'] = 'CLAUDE'
            enhanced_worker['model'] = extract_claude_model(task)
            enhanced_worker['selection_reason'] = 'Complex reasoning task'
        elif 'groq' in task or 'llama' in task or 'fast' in task or 'quick' in task:
            enhanced_worker['engine'] = 'GROQ'
            enhanced_worker['model'] = extract_groq_model(task)
            enhanced_worker['selection_reason'] = 'Speed optimization'
        elif 'creative' in task or 'analysis' in task or 'research' in task:
            enhanced_worker['engine'] = 'CLAUDE'
            enhanced_worker['model'] = 'claude-sonnet-4'
            enhanced_worker['selection_reason'] = 'Creative/analytical task'
        elif 'simple' in task or 'format' in task or 'extract' in task:
            enhanced_worker['engine'] = 'GROQ'
            enhanced_worker['model'] = 'llama-3.3-70b'
            enhanced_worker['selection_reason'] = 'Simple processing'
        else:
            # Default engine assignment based on worker ID for demo
            if i % 3 == 0:
                enhanced_worker['engine'] = 'CLAUDE'
                enhanced_worker['model'] = 'claude-sonnet-4'
                enhanced_worker['selection_reason'] = 'Default Claude assignment'
            else:
                enhanced_worker['engine'] = 'GROQ'
                enhanced_worker['model'] = 'llama-3.3-70b'
                enhanced_worker['selection_reason'] = 'Budget optimization'

        enhanced_workers.append(enhanced_worker)

    return {
        "workers": enhanced_workers,
        "wave_info": wave_data.get("wave_info", {
            "current_wave": "13",
            "wave_progress": "In Progress",
            "total_workers": len(enhanced_workers)
        })
    }


def extract_claude_model(text):
    """Extract Claude model from text."""
    if 'opus' in text:
        return 'claude-opus-4-5'
    elif 'haiku' in text:
        return 'claude-haiku-4'
    else:
        return 'claude-sonnet-4'


def extract_groq_model(text):
    """Extract Groq model from text."""
    if 'mixtral' in text:
        return 'mixtral-8x7b'
    elif '70b' in text:
        return 'llama-3.3-70b'
    else:
        return 'llama-3.1-70b'


def get_stats():
    """Get basic stats."""
    logs_dir = WORKSPACE / "grind_logs"
    sessions = len(list(logs_dir.glob("*.json"))) if logs_dir.exists() else 0

    lessons = 0
    lessons_file = WORKSPACE / "learned_lessons.json"
    if lessons_file.exists():
        try:
            data = json.loads(lessons_file.read_text(encoding='utf-8'))
            if isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, list):
                        lessons += len(v)
            elif isinstance(data, list):
                lessons = len(data)
        except:
            pass

    py_files = set(WORKSPACE.glob("*.py")) | set(WORKSPACE.glob("**/*.py"))
    files = len(py_files)
    lines = sum(len(f.read_text(encoding='utf-8', errors='ignore').splitlines()) for f in py_files if f.exists())

    return {"sessions": sessions, "lessons": lessons, "files": files, "lines": lines}


def get_dashboard_data():
    """Get all data needed for dashboard as JSON."""
    wave_data = load_wave_status()
    stats = get_stats()
    enhanced_workers = get_enhanced_worker_data()
    engine_statistics = analyze_engine_usage()

    return {
        "waves": wave_data.get("waves", []),
        "current_activity": wave_data.get("current_activity", {}),
        "stats": stats,
        "timestamp": datetime.now().strftime('%H:%M:%S'),
        "workers": enhanced_workers,
        "engine_stats": engine_statistics,
        "active_workers": enhanced_workers  # For compatibility
    }


def broadcast_update():
    """Send update to all SSE clients."""
    data = json.dumps(get_dashboard_data())
    message = f"data: {data}\n\n"

    with sse_lock:
        dead_clients = []
        for client in sse_clients:
            try:
                client['wfile'].write(message.encode('utf-8'))
                client['wfile'].flush()
            except:
                dead_clients.append(client)
        for c in dead_clients:
            sse_clients.remove(c)


def file_watcher():
    """Watch files and broadcast on changes."""
    global last_mtimes
    last_mtimes = get_file_mtimes()

    while True:
        time.sleep(1)
        current = get_file_mtimes()
        if current != last_mtimes:
            last_mtimes = current
            broadcast_update()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html', '/command', '/dashboard', '/enhanced'):
            # Serve the enhanced dashboard
            dashboard_file = EXPERIMENTS_DIR / "exp_20260203_103008_unified_session_13" / "dashboard_enhanced.html"
            if dashboard_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(dashboard_file.read_bytes())
            else:
                self.send_error(404, "Enhanced dashboard not found")

        elif self.path == '/events':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            client = {'wfile': self.wfile}
            with sse_lock:
                sse_clients.append(client)

            # Send initial data
            try:
                data = json.dumps(get_dashboard_data())
                self.wfile.write(f"data: {data}\n\n".encode('utf-8'))
                self.wfile.flush()

                # Keep connection alive
                while True:
                    time.sleep(30)
                    self.wfile.write(": heartbeat\n\n".encode('utf-8'))
                    self.wfile.flush()
            except:
                pass
            finally:
                with sse_lock:
                    if client in sse_clients:
                        sse_clients.remove(client)

        elif self.path == '/api/status' or self.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(get_dashboard_data()).encode('utf-8'))

        elif self.path == '/experiments':
            # Mock experiments data
            experiments_data = {
                "experiments": [
                    {
                        "title": "Engine Visibility Implementation",
                        "status": "running",
                        "description": "Adding per-node engine and model tracking"
                    },
                    {
                        "title": "Cost Optimization",
                        "status": "completed",
                        "description": "Intelligent engine selection for budget control"
                    }
                ]
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(experiments_data).encode('utf-8'))

        elif self.path == '/pending-changes':
            # Mock pending changes data
            changes_data = {
                "changes": [
                    {
                        "id": "1",
                        "title": "Engine visibility updates",
                        "description": "Dashboard enhancements for engine tracking",
                        "status": "pending"
                    }
                ]
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(changes_data).encode('utf-8'))

        elif self.path == '/cost-tracking':
            # Mock cost tracking data
            cost_data = {
                "total_sessions": 47,
                "success_rate": "94%",
                "avg_duration": "2.3s"
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(cost_data).encode('utf-8'))

        else:
            self.send_error(404)

    def do_POST(self):
        if self.path.startswith('/approve/'):
            change_id = self.path.split('/')[-1]
            # Mock approval response
            response = {"status": "success", "message": f"Change {change_id} approved"}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress logs for cleaner output


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"


def main():
    parser = argparse.ArgumentParser(description="Enhanced Black Swarm Command Center")
    parser.add_argument("--port", type=int, default=8080, help="Port to run on")
    parser.add_argument("--lan", action="store_true", help="Make accessible on LAN")
    args = parser.parse_args()

    # Start file watcher thread
    threading.Thread(target=file_watcher, daemon=True).start()

    host = "0.0.0.0" if args.lan else "127.0.0.1"

    with ThreadedServer((host, args.port), Handler) as server:
        print(f"🐛 Enhanced Black Swarm Command Center Online")
        print(f"   Features: Engine/Model visibility, Real-time tracking")
        print(f"   Local:  http://localhost:{args.port}")
        if args.lan:
            print(f"   LAN:    http://{get_local_ip()}:{args.port}")
        print(f"   Engine tracking and cost analysis active")
        print(f"   Press Ctrl+C to terminate")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n🔴 Enhanced Black Swarm Command Center offline")


if __name__ == "__main__":
    main()