#!/usr/bin/env python3
"""
Enhanced Progress Server with Engine/Model Visibility
Real-time engine tracking, cost monitoring, and model usage statistics.
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
from typing import Dict, List, Any, Optional

PORT = 8080
WORKSPACE = Path(__file__).parent.parent.parent

# Global: SSE clients and file monitoring
sse_clients = []
sse_lock = threading.Lock()
last_mtimes = {}

# Engine tracking state
engine_stats = {
    "claude": {"requests": 0, "cost": 0.0, "tokens": 0},
    "groq": {"requests": 0, "cost": 0.0, "tokens": 0},
    "total_switches": 0,
    "current_distribution": {"claude": 0, "groq": 0}
}

# Worker engine tracking
active_workers = {}  # worker_id -> engine_data

class EngineTracker:
    """Tracks engine usage, model selection, and costs in real-time."""

    def __init__(self):
        self.engine_usage = {}
        self.model_usage = {}
        self.cost_tracking = {
            "claude": {"total": 0.0, "sessions": 0},
            "groq": {"total": 0.0, "sessions": 0}
        }
        self.selection_reasons = []

    def record_engine_selection(self, worker_id: str, engine: str, model: str,
                              reason: str, cost: float = 0.0):
        """Record an engine selection for a worker."""
        selection_data = {
            "worker_id": worker_id,
            "engine": engine,
            "model": model,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "cost": cost
        }

        # Update global stats
        if engine in engine_stats:
            engine_stats[engine]["requests"] += 1
            engine_stats[engine]["cost"] += cost
            engine_stats["current_distribution"][engine] += 1

        # Track worker state
        active_workers[worker_id] = {
            "engine": engine,
            "model": model,
            "reason": reason,
            "cost_accumulated": cost,
            "switches": active_workers.get(worker_id, {}).get("switches", 0)
        }

        # Record for history
        self.selection_reasons.append(selection_data)
        if len(self.selection_reasons) > 100:  # Keep last 100
            self.selection_reasons.pop(0)

    def switch_engine(self, worker_id: str, new_engine: str, new_model: str, reason: str):
        """Record an engine switch during execution."""
        if worker_id in active_workers:
            old_engine = active_workers[worker_id].get("engine", "unknown")
            if old_engine != new_engine:
                engine_stats["total_switches"] += 1
                active_workers[worker_id]["switches"] += 1

                # Update distribution counts
                if old_engine in engine_stats["current_distribution"]:
                    engine_stats["current_distribution"][old_engine] = max(0,
                        engine_stats["current_distribution"][old_engine] - 1)

                self.record_engine_selection(worker_id, new_engine, new_model,
                                           f"Switch from {old_engine}: {reason}")

    def get_engine_summary(self) -> Dict[str, Any]:
        """Get comprehensive engine usage summary."""
        total_requests = sum(engine_stats[engine]["requests"] for engine in ["claude", "groq"])
        total_cost = sum(engine_stats[engine]["cost"] for engine in ["claude", "groq"])

        return {
            "total_requests": total_requests,
            "total_cost": total_cost,
            "claude_percentage": (engine_stats["claude"]["requests"] / max(total_requests, 1)) * 100,
            "groq_percentage": (engine_stats["groq"]["requests"] / max(total_requests, 1)) * 100,
            "cost_savings": engine_stats["groq"]["cost"],  # Assuming Groq is cheaper
            "total_switches": engine_stats["total_switches"],
            "active_distribution": engine_stats["current_distribution"],
            "recent_selections": self.selection_reasons[-10:]  # Last 10
        }

# Global tracker instance
tracker = EngineTracker()

def get_file_mtimes():
    """Get modification times of monitored files."""
    files = [
        WORKSPACE / "wave_status.json",
        WORKSPACE / "SUMMARY.md",
        WORKSPACE / "learned_lessons.json",
        WORKSPACE / "grind_logs" / "*.json"
    ]
    mtimes = {}
    for f in files:
        try:
            if f.exists():
                mtimes[str(f)] = f.stat().st_mtime
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

def get_engine_enhanced_workers():
    """Get worker data enhanced with engine/model visibility."""
    wave_data = load_wave_status()
    workers = wave_data.get("current_activity", {}).get("workers", [])

    enhanced_workers = []
    for i, worker in enumerate(workers):
        worker_id = worker.get("id", str(i))

        # Get engine data for this worker
        engine_data = active_workers.get(worker_id, {
            "engine": "CLAUDE",  # Default
            "model": "claude-sonnet-4",
            "reason": "Default selection",
            "cost_accumulated": 0.0,
            "switches": 0
        })

        enhanced_worker = {
            **worker,
            "id": worker_id,
            "engine_type": engine_data["engine"].upper(),
            "model_name": engine_data["model"],
            "selection_reason": engine_data["reason"],
            "cost_accumulated": engine_data["cost_accumulated"],
            "engine_switches": engine_data["switches"],
            "engine_color": "claude" if engine_data["engine"].lower() == "claude" else "groq"
        }
        enhanced_workers.append(enhanced_worker)

    return enhanced_workers

def get_dashboard_data():
    """Get all data needed for dashboard as JSON with engine visibility."""
    wave_data = load_wave_status()

    # Get enhanced workers with engine data
    enhanced_workers = get_engine_enhanced_workers()

    # Get engine summary
    engine_summary = tracker.get_engine_summary()

    # Enhanced activity data
    enhanced_activity = {
        **wave_data.get("current_activity", {}),
        "workers": enhanced_workers,
        "engine_summary": engine_summary
    }

    return {
        "waves": wave_data.get("waves", []),
        "current_activity": enhanced_activity,
        "engine_stats": engine_stats,
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

def get_dashboard_html():
    """Enhanced dashboard HTML with engine/model visibility."""
    data = get_dashboard_data()
    waves = data["waves"]
    activity = data["current_activity"]
    engine_summary = activity.get("engine_summary", {})

    # Build wave tracker HTML
    wave_html = ""
    for i, w in enumerate(waves):
        status = w.get("status", "planned")
        if status == "done":
            cls, icon, aria_label = "done", "✓", "Completed"
        elif status == "running":
            cls, icon, aria_label = "running", "⚡", "Currently running"
        else:
            cls, icon, aria_label = "planned", "○", "Planned"

        wave_html += f'''<article class="wave {cls}" role="button" tabindex="0"
            aria-label="Wave {w['num']}: {w['name']} - {aria_label}"
            data-wave="{w['num']}" onkeypress="handleWaveKey(event)">
            <span class="icon" aria-hidden="true">{icon}</span>
            <span class="num">Wave {w["num"]}</span>
            <span class="name">{w["name"]}</span>
        </article>'''

    # Build enhanced workers HTML with engine visibility
    workers_html = ""
    for i, w in enumerate(activity.get("workers", [])):
        worker_type = w.get("type", "Worker")
        worker_task = w.get("task", "Initializing...")
        engine_type = w.get("engine_type", "CLAUDE")
        model_name = w.get("model_name", "claude-sonnet-4")
        selection_reason = w.get("selection_reason", "Default")
        cost = w.get("cost_accumulated", 0.0)
        switches = w.get("engine_switches", 0)

        engine_badge_class = "claude" if engine_type == "CLAUDE" else "groq"

        workers_html += f'''<article class="worker" aria-labelledby="worker-{i}-type"
            aria-describedby="worker-{i}-task">
            <div class="worker-header">
                <div class="type" id="worker-{i}-type">{worker_type}</div>
                <div class="engine-badge {engine_badge_class}">{engine_type}</div>
            </div>
            <div class="model-info">{model_name}</div>
            <div class="selection-reason">{selection_reason}</div>
            <div class="task" id="worker-{i}-task">{worker_task}</div>
            <div class="worker-metrics">
                <span class="cost">${cost:.3f}</span>
                <span class="switches">{switches} switches</span>
            </div>
            <div class="worker-status" aria-label="Worker status indicator"></div>
        </article>'''

    # Build engine summary panel
    claude_pct = engine_summary.get("claude_percentage", 0)
    groq_pct = engine_summary.get("groq_percentage", 0)
    total_cost = engine_summary.get("total_cost", 0)
    total_switches = engine_summary.get("total_switches", 0)

    engine_summary_html = f'''
    <div class="engine-summary">
        <div class="usage-split">
            <div class="engine-bar">
                <div class="claude-portion" style="width: {claude_pct}%"></div>
                <div class="groq-portion" style="width: {groq_pct}%"></div>
            </div>
            <div class="usage-labels">
                <span class="claude-label">Claude {claude_pct:.1f}%</span>
                <span class="groq-label">Groq {groq_pct:.1f}%</span>
            </div>
        </div>
        <div class="summary-metrics">
            <div class="metric">
                <span class="value">${total_cost:.2f}</span>
                <span class="label">Total Cost</span>
            </div>
            <div class="metric">
                <span class="value">{total_switches}</span>
                <span class="label">Engine Switches</span>
            </div>
        </div>
    </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Black Swarm Command Center - Engine Visibility</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bs-primary: #00ff94;
            --bs-secondary: #00d4ff;
            --bs-accent: #ff3d71;
            --bs-warning: #ffb800;
            --bs-surface-primary: #0a0a0a;
            --bs-surface-secondary: #111115;
            --bs-surface-tertiary: #1a1a1f;
            --bs-glass-bg: rgba(17, 17, 21, 0.7);
            --bs-glass-border: rgba(255, 255, 255, 0.1);
            --bs-text-primary: #ffffff;
            --bs-text-secondary: #a0a0a0;
            --bs-text-tertiary: #666666;

            /* Engine colors */
            --claude-color: #00ff94;
            --groq-color: #ff6b35;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--bs-surface-primary) 0%, var(--bs-surface-secondary) 50%, var(--bs-surface-tertiary) 100%);
            background-attachment: fixed;
            color: var(--bs-text-primary);
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 24px;
        }}

        header {{
            text-align: center;
            margin-bottom: 32px;
        }}

        .brand-title {{
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 800;
            background: linear-gradient(135deg, var(--bs-primary) 0%, var(--bs-secondary) 100%);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}

        .glass-card {{
            background: var(--bs-glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--bs-glass-border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            transition: all 0.3s ease;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            color: var(--bs-primary);
            font-size: 1.25rem;
            font-weight: 600;
        }}

        /* Enhanced worker cards with engine visibility */
        .workers-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 16px;
        }}

        .worker {{
            background: var(--bs-glass-bg);
            border: 1px solid var(--bs-glass-border);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .worker::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--claude-color), var(--groq-color));
        }}

        .worker-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .type {{
            color: var(--bs-primary);
            font-weight: 700;
            font-size: 1rem;
        }}

        .engine-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .engine-badge.claude {{
            background: rgba(0, 255, 148, 0.2);
            color: var(--claude-color);
            border: 1px solid var(--claude-color);
        }}

        .engine-badge.groq {{
            background: rgba(255, 107, 53, 0.2);
            color: var(--groq-color);
            border: 1px solid var(--groq-color);
        }}

        .model-info {{
            font-size: 0.875rem;
            color: var(--bs-text-secondary);
            margin-bottom: 8px;
            font-family: 'SF Mono', monospace;
        }}

        .selection-reason {{
            font-size: 0.75rem;
            color: var(--bs-text-tertiary);
            margin-bottom: 12px;
            font-style: italic;
        }}

        .task {{
            color: var(--bs-text-primary);
            font-size: 0.875rem;
            line-height: 1.5;
            margin-bottom: 12px;
        }}

        .worker-metrics {{
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: var(--bs-text-secondary);
        }}

        .cost {{
            color: var(--bs-warning);
            font-weight: 600;
        }}

        .switches {{
            color: var(--bs-secondary);
        }}

        /* Engine summary panel */
        .engine-summary {{
            background: linear-gradient(135deg, rgba(0, 255, 148, 0.1), rgba(255, 107, 53, 0.1));
            border: 1px solid rgba(0, 255, 148, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}

        .usage-split {{
            margin-bottom: 16px;
        }}

        .engine-bar {{
            height: 8px;
            background: var(--bs-surface-secondary);
            border-radius: 4px;
            overflow: hidden;
            display: flex;
            margin-bottom: 8px;
        }}

        .claude-portion {{
            background: var(--claude-color);
            transition: width 0.5s ease;
        }}

        .groq-portion {{
            background: var(--groq-color);
            transition: width 0.5s ease;
        }}

        .usage-labels {{
            display: flex;
            justify-content: space-between;
            font-size: 0.875rem;
        }}

        .claude-label {{
            color: var(--claude-color);
            font-weight: 600;
        }}

        .groq-label {{
            color: var(--groq-color);
            font-weight: 600;
        }}

        .summary-metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 16px;
        }}

        .metric {{
            text-align: center;
        }}

        .metric .value {{
            display: block;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--bs-primary);
            margin-bottom: 4px;
        }}

        .metric .label {{
            font-size: 0.75rem;
            color: var(--bs-text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .wave-tracker {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 16px;
        }}

        .wave {{
            background: var(--bs-glass-bg);
            border: 1px solid var(--bs-glass-border);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .wave.done {{
            background: linear-gradient(135deg, rgba(0, 255, 148, 0.2), rgba(0, 204, 117, 0.3));
            border-color: var(--bs-primary);
            color: var(--bs-primary);
        }}

        .wave.running {{
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(0, 170, 204, 0.3));
            border-color: var(--bs-secondary);
            color: var(--bs-secondary);
            animation: waveRunning 2s ease-in-out infinite;
        }}

        @keyframes waveRunning {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(0, 212, 255, 0.4); }}
            50% {{ box-shadow: 0 0 0 8px rgba(0, 212, 255, 0.1); }}
        }}

        .timestamp {{
            text-align: center;
            color: var(--bs-text-tertiary);
            font-size: 0.75rem;
            margin-top: 32px;
            padding: 16px;
            border-top: 1px solid var(--bs-glass-border);
        }}

        @media (max-width: 768px) {{
            .workers-grid {{
                grid-template-columns: 1fr;
            }}
            .container {{
                padding: 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 class="brand-title">Black Swarm Command Center</h1>
            <div style="color: var(--bs-text-secondary); font-size: 1.2rem;">Engine Visibility Dashboard</div>
        </header>

        <main>
            <!-- Engine Summary -->
            <section class="glass-card">
                <h2 class="section-header">Engine Usage Distribution</h2>
                {engine_summary_html}
            </section>

            <!-- Mission Progress -->
            <section class="glass-card">
                <h2 class="section-header">Mission Progress</h2>
                <div class="wave-tracker">
                    {wave_html}
                </div>
            </section>

            <!-- Active Workers with Engine Visibility -->
            <section class="glass-card">
                <h2 class="section-header">{activity.get('title', 'AI Workers')}</h2>
                <div class="workers-grid">
                    {workers_html if workers_html else '<div style="text-align: center; color: var(--bs-text-secondary); padding: 40px;">All systems standing by</div>'}
                </div>
            </section>

            <footer class="timestamp">
                Last neural sync: {data['timestamp']} | Engine tracking active
            </footer>
        </main>
    </div>

    <script>
        // Auto-refresh every 5 seconds
        let eventSource;

        function connect() {{
            eventSource = new EventSource('/events');

            eventSource.onmessage = function(e) {{
                try {{
                    const data = JSON.parse(e.data);
                    updateDashboard(data);
                }} catch(err) {{
                    console.error('Parse error:', err);
                }}
            }};

            eventSource.onerror = function() {{
                console.log('Connection lost, reconnecting...');
                eventSource.close();
                setTimeout(connect, 3000);
            }};
        }}

        function updateDashboard(data) {{
            // Real-time updates would be implemented here
            // For now, we'll do a simple reload
            if (data && data.engine_stats) {{
                console.log('Engine stats updated:', data.engine_stats);
            }}
        }}

        // Initialize connection
        document.addEventListener('DOMContentLoaded', connect);
    </script>
</body>
</html>'''

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html', '/dashboard'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(get_dashboard_html().encode('utf-8'))

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

        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(get_dashboard_data()).encode('utf-8'))

        elif self.path == '/api/engine/record':
            # API endpoint for recording engine selections
            if self.command == 'POST':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    tracker.record_engine_selection(
                        data['worker_id'],
                        data['engine'],
                        data['model'],
                        data['reason'],
                        data.get('cost', 0.0)
                    )
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "recorded"}).encode('utf-8'))
                    broadcast_update()  # Notify clients
                except Exception as e:
                    self.send_error(400, str(e))
            else:
                self.send_error(405)

        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/engine/record':
            self.do_GET()  # Reuse the GET logic
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress logs

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

def main():
    parser = argparse.ArgumentParser(description="Enhanced Progress Server with Engine Visibility")
    parser.add_argument("--port", type=int, default=8080, help="Port to run on")
    parser.add_argument("--lan", action="store_true", help="Make accessible on LAN")
    args = parser.parse_args()

    # Start file watcher thread
    threading.Thread(target=file_watcher, daemon=True).start()

    host = "0.0.0.0" if args.lan else "127.0.0.1"

    with ThreadedServer((host, args.port), Handler) as server:
        print(f"🚀 Enhanced Black Swarm Command Center Online")
        print(f"   Local:  http://localhost:{args.port}")
        print(f"   Engine tracking: ACTIVE")
        print(f"   Model visibility: ENABLED")
        if args.lan:
            import socket
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                print(f"   LAN:    http://{ip}:{args.port}")
            except:
                print(f"   LAN:    http://0.0.0.0:{args.port}")
        print(f"   Press Ctrl+C to terminate")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n🔴 Enhanced Command Center offline")

if __name__ == "__main__":
    main()