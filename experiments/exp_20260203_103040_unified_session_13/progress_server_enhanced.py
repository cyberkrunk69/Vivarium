#!/usr/bin/env python3
"""
Enhanced Progress Server with Engine/Model Visibility

Extends the existing progress server to include:
- Engine type (Claude/Groq) per worker
- Model name per worker
- Selection reasoning
- Real-time engine switching notifications
- Cost breakdown by engine
- Model usage statistics

Usage:
    python progress_server_enhanced.py --port 8080 --lan
"""

import http.server
import socketserver
import argparse
import json
import threading
import time
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

PORT = 8080
WORKSPACE = Path(__file__).parent.parent.parent  # Go back to main workspace

# Global: list of SSE client queues and file modification times
sse_clients = []
sse_lock = threading.Lock()
last_mtimes = {}

# Engine statistics tracking
engine_stats = {
    "claude_cost": 0.0,
    "groq_cost": 0.0,
    "claude_tokens": 0,
    "groq_tokens": 0,
    "claude_percentage": 0,
    "groq_percentage": 0,
    "efficiency_score": 0,
    "model_distribution": {}
}

def get_file_mtimes():
    """Get modification times of monitored files."""
    files = [
        WORKSPACE / "wave_status.json",
        WORKSPACE / "SUMMARY.md",
        WORKSPACE / "grind_logs",  # Monitor entire logs directory
        WORKSPACE / "learned_lessons.json",
        WORKSPACE / "cost_tracker.json",  # New cost tracking file
    ]
    mtimes = {}
    for f in files:
        try:
            if f.exists():
                if f.is_dir():
                    # Get latest modification in directory
                    latest = max(f.glob("*.json"), key=lambda x: x.stat().st_mtime, default=f)
                    mtimes[str(f)] = latest.stat().st_mtime
                else:
                    mtimes[str(f)] = f.stat().st_mtime
        except:
            pass
    return mtimes

def extract_engine_info_from_logs():
    """Extract engine usage information from grind logs."""
    logs_dir = WORKSPACE / "grind_logs"
    if not logs_dir.exists():
        return {}

    engine_usage = {"claude": 0, "groq": 0}
    model_usage = {}
    cost_tracking = {"claude": 0.0, "groq": 0.0}
    token_tracking = {"claude": 0, "groq": 0}

    # Parse recent log files for engine/model information
    log_files = sorted(logs_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:10]

    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

                # Extract engine information
                if 'engine' in log_data:
                    engine = log_data['engine'].lower()
                    engine_usage[engine] = engine_usage.get(engine, 0) + 1

                # Extract model information
                if 'model' in log_data:
                    model = log_data['model']
                    model_usage[model] = model_usage.get(model, 0) + 1

                # Extract cost information
                if 'cost_usd' in log_data and 'engine' in log_data:
                    engine = log_data['engine'].lower()
                    cost_tracking[engine] += log_data.get('cost_usd', 0.0)

                # Extract token information
                if 'tokens_total' in log_data and 'engine' in log_data:
                    engine = log_data['engine'].lower()
                    token_tracking[engine] += log_data.get('tokens_total', 0)

        except Exception as e:
            continue

    total_usage = sum(engine_usage.values())
    total_models = sum(model_usage.values())

    return {
        "claude_percentage": round((engine_usage.get("claude", 0) / max(total_usage, 1)) * 100, 1),
        "groq_percentage": round((engine_usage.get("groq", 0) / max(total_usage, 1)) * 100, 1),
        "claude_cost": cost_tracking.get("claude", 0.0),
        "groq_cost": cost_tracking.get("groq", 0.0),
        "claude_tokens": token_tracking.get("claude", 0),
        "groq_tokens": token_tracking.get("groq", 0),
        "efficiency_score": calculate_efficiency_score(cost_tracking, engine_usage),
        "model_distribution": {
            model: round((count / max(total_models, 1)) * 100, 1)
            for model, count in model_usage.items()
        }
    }

def calculate_efficiency_score(cost_tracking, engine_usage):
    """Calculate efficiency score based on cost vs usage ratio."""
    total_cost = sum(cost_tracking.values())
    total_usage = sum(engine_usage.values())

    if total_cost == 0 or total_usage == 0:
        return 100

    # Lower cost per usage = higher efficiency
    cost_per_usage = total_cost / total_usage

    # Normalize to 0-100 scale (arbitrary threshold of $0.10 per usage as "baseline")
    baseline_cost = 0.10
    efficiency = max(0, min(100, (1 - (cost_per_usage / baseline_cost)) * 100))

    return round(efficiency, 1)

def load_wave_status():
    """Load wave status from JSON with enhanced worker info."""
    wave_file = WORKSPACE / "wave_status.json"
    default_data = {
        "waves": [],
        "current_activity": {
            "title": "Initializing AI systems...",
            "workers": []
        }
    }

    if wave_file.exists():
        try:
            data = json.loads(wave_file.read_text(encoding='utf-8'))

            # Enhance worker data with engine/model information
            if 'current_activity' in data and 'workers' in data['current_activity']:
                enhanced_workers = []
                for i, worker in enumerate(data['current_activity']['workers']):
                    enhanced_worker = worker.copy()

                    # Add engine information if not present
                    if 'engine' not in enhanced_worker:
                        # Try to infer from task content
                        task = worker.get('task', '').lower()
                        if any(pattern in task for pattern in ['groq', 'fast', 'cheap']):
                            enhanced_worker['engine'] = 'groq'
                            enhanced_worker['model'] = 'llama-3.3-70b'
                            enhanced_worker['selection_reason'] = 'Fast execution'
                        elif any(pattern in task for pattern in ['claude', 'complex', 'analysis']):
                            enhanced_worker['engine'] = 'claude'
                            enhanced_worker['model'] = 'claude-sonnet-4'
                            enhanced_worker['selection_reason'] = 'Complex task'
                        else:
                            # Default assignments based on worker type
                            worker_type = worker.get('type', '').lower()
                            if 'optimizer' in worker_type or 'research' in worker_type:
                                enhanced_worker['engine'] = 'claude'
                                enhanced_worker['model'] = 'claude-sonnet-4'
                                enhanced_worker['selection_reason'] = 'Research task'
                            else:
                                enhanced_worker['engine'] = 'groq'
                                enhanced_worker['model'] = 'llama-3.3-70b'
                                enhanced_worker['selection_reason'] = 'Budget optimization'

                    enhanced_workers.append(enhanced_worker)

                data['current_activity']['workers'] = enhanced_workers

            return data
        except:
            pass

    return default_data

def get_stats():
    """Get basic stats with engine information."""
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
    lines = sum(len(f.read_text(encoding='utf-8', errors='ignore').splitlines())
                for f in py_files if f.exists())

    return {
        "sessions": sessions,
        "lessons": lessons,
        "files": files,
        "lines": lines
    }

def get_dashboard_data():
    """Get all data needed for dashboard as JSON."""
    wave_data = load_wave_status()
    stats = get_stats()
    engine_stats_data = extract_engine_info_from_logs()

    return {
        "waves": wave_data.get("waves", []),
        "current_activity": wave_data.get("current_activity", {}),
        "active_workers": wave_data.get("current_activity", {}),
        "stats": stats,
        "engine_stats": engine_stats_data,
        "timestamp": datetime.now().strftime('%H:%M:%S')
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

def broadcast_engine_switch(worker_id: str, from_engine: str, to_engine: str, reason: str):
    """Broadcast engine switching notification."""
    switch_data = {
        "worker_id": worker_id,
        "from_engine": from_engine,
        "to_engine": to_engine,
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }

    message = f"event: engine_switch\ndata: {json.dumps(switch_data)}\n\n"

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

def get_enhanced_dashboard_html():
    """Return enhanced dashboard HTML with engine visibility."""
    dashboard_file = Path(__file__).parent / "dashboard_enhanced.html"
    if dashboard_file.exists():
        return dashboard_file.read_text(encoding='utf-8')
    else:
        return "<html><body><h1>Enhanced dashboard not found</h1></body></html>"

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html', '/command', '/dashboard'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(get_enhanced_dashboard_html().encode('utf-8'))

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

        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(get_dashboard_data()).encode('utf-8'))

        elif self.path == '/experiments':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Mock experiments data
            experiments_data = {
                "experiments": [
                    {
                        "title": "Engine Visibility Implementation",
                        "status": "running",
                        "description": "Adding per-node engine/model display to dashboard"
                    }
                ]
            }
            self.wfile.write(json.dumps(experiments_data).encode('utf-8'))

        elif self.path == '/cost-tracking':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            engine_stats_data = extract_engine_info_from_logs()
            cost_data = {
                "total_sessions": get_stats()["sessions"],
                "success_rate": "85%",  # Mock data
                "avg_duration": "45s",   # Mock data
                "claude_cost": engine_stats_data.get("claude_cost", 0.0),
                "groq_cost": engine_stats_data.get("groq_cost", 0.0),
            }
            self.wfile.write(json.dumps(cost_data).encode('utf-8'))

        elif self.path.startswith('/api/engine-switch'):
            # API endpoint to trigger engine switching notifications (for testing)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Simulate an engine switch
            broadcast_engine_switch("worker_1", "groq", "claude", "Task complexity increased")
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress logs for cleaner output

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    parser = argparse.ArgumentParser(description="Enhanced Black Swarm Command Center with Engine Visibility")
    parser.add_argument("--port", type=int, default=8080, help="Port to run on")
    parser.add_argument("--lan", action="store_true", help="Make accessible on LAN")
    args = parser.parse_args()

    # Start file watcher thread
    threading.Thread(target=file_watcher, daemon=True).start()

    host = "0.0.0.0" if args.lan else "127.0.0.1"

    with ThreadedServer((host, args.port), Handler) as server:
        print(f"🐛 Enhanced Black Swarm Command Center Online")
        print(f"   ⚡ Engine/Model Visibility: ENABLED")
        print(f"   Local:  http://localhost:{args.port}")
        if args.lan:
            print(f"   LAN:    http://{get_local_ip()}:{args.port}")
        print(f"   Real-time engine monitoring active")
        print(f"   Press Ctrl+C to terminate")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n🔴 Enhanced Black Swarm Command Center offline")

if __name__ == "__main__":
    main()