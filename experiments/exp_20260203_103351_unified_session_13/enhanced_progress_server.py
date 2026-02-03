#!/usr/bin/env python3
"""
Enhanced Black Swarm Progress Server with Engine/Model Visibility
Real-time tracking of inference engines, models, and costs per worker node.

Integration with existing progress_server.py - adds engine visibility features.
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
from typing import Dict, List, Optional, Any

PORT = 8080
WORKSPACE = Path(__file__).parent.parent.parent  # Go up to main directory

# Global: list of SSE client queues and file modification times
sse_clients = []
sse_lock = threading.Lock()
last_mtimes = {}

# Engine/Model tracking
engine_stats = {
    "total_claude_calls": 0,
    "total_groq_calls": 0,
    "claude_cost": 0.0,
    "groq_cost": 0.0,
    "model_usage": {},
    "engine_switches": [],
    "current_workers": {}
}

def load_engine_data():
    """Load engine and model usage data from workers."""
    try:
        # Load from grind_spawner_unified.py state if available
        unified_state_file = WORKSPACE / "unified_session_state.json"
        if unified_state_file.exists():
            data = json.loads(unified_state_file.read_text(encoding='utf-8'))
            return data.get('engine_stats', {})
    except:
        pass

    return {}

def get_worker_engine_info():
    """Extract engine/model info for each active worker."""
    workers = []

    try:
        # Load wave status for active workers
        wave_file = WORKSPACE / "wave_status.json"
        if wave_file.exists():
            wave_data = json.loads(wave_file.read_text(encoding='utf-8'))
            active_workers = wave_data.get("current_activity", {}).get("workers", [])

            # Enhance each worker with engine info
            for i, worker in enumerate(active_workers):
                enhanced_worker = {
                    "id": f"W{i+1:02d}",
                    "type": worker.get("type", "Worker"),
                    "task": worker.get("task", "Idle"),
                    "status": worker.get("status", "active"),
                    # Engine information
                    "engine": worker.get("engine", "AUTO"),  # CLAUDE or GROQ
                    "model": worker.get("model", "Unknown"),  # e.g., claude-sonnet-4, llama-3.3-70b
                    "selection_reason": worker.get("selection_reason", "Auto-selected"),
                    "cost_this_session": worker.get("cost", 0.0),
                    "tokens_used": worker.get("tokens", 0),
                    "engine_switches": worker.get("engine_switches", 0)
                }
                workers.append(enhanced_worker)

    except Exception as e:
        print(f"Error loading worker engine info: {e}")

    return workers

def get_engine_summary():
    """Get summary statistics for engine usage."""
    summary = {
        "claude_percentage": 0,
        "groq_percentage": 0,
        "total_cost": 0.0,
        "cost_breakdown": {
            "claude": 0.0,
            "groq": 0.0
        },
        "model_distribution": {},
        "engine_switches_today": 0
    }

    try:
        # Load cost tracking data
        cost_file = WORKSPACE / "cost_tracker.py"  # Check if cost tracking exists
        if cost_file.exists():
            # Parse cost data - this would need actual implementation
            # based on how costs are currently tracked
            pass

        # Calculate from worker data
        workers = get_worker_engine_info()
        if workers:
            claude_workers = sum(1 for w in workers if w["engine"] == "CLAUDE")
            groq_workers = sum(1 for w in workers if w["engine"] == "GROQ")
            total_workers = len(workers)

            if total_workers > 0:
                summary["claude_percentage"] = round((claude_workers / total_workers) * 100, 1)
                summary["groq_percentage"] = round((groq_workers / total_workers) * 100, 1)

            # Model distribution
            for worker in workers:
                model = worker["model"]
                if model not in summary["model_distribution"]:
                    summary["model_distribution"][model] = 0
                summary["model_distribution"][model] += 1

            # Total costs
            summary["total_cost"] = sum(w["cost_this_session"] for w in workers)
            summary["cost_breakdown"]["claude"] = sum(w["cost_this_session"] for w in workers if w["engine"] == "CLAUDE")
            summary["cost_breakdown"]["groq"] = sum(w["cost_this_session"] for w in workers if w["engine"] == "GROQ")

    except Exception as e:
        print(f"Error calculating engine summary: {e}")

    return summary

def get_file_mtimes():
    """Get modification times of monitored files."""
    files = [
        WORKSPACE / "wave_status.json",
        WORKSPACE / "SUMMARY.md",
        WORKSPACE / "learned_lessons.json",
        WORKSPACE / "unified_session_state.json"  # Add engine state tracking
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

def get_enhanced_dashboard_data():
    """Get all data needed for enhanced dashboard as JSON."""
    wave_data = load_wave_status()
    stats = get_stats()
    workers_with_engine_info = get_worker_engine_info()
    engine_summary = get_engine_summary()

    return {
        "waves": wave_data.get("waves", []),
        "current_activity": wave_data.get("current_activity", {}),
        "stats": stats,
        "workers_enhanced": workers_with_engine_info,
        "engine_summary": engine_summary,
        "timestamp": datetime.now().strftime('%H:%M:%S')
    }

def broadcast_update():
    """Send update to all SSE clients."""
    data = json.dumps(get_enhanced_dashboard_data())
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

def get_enhanced_dashboard_html():
    """Enhanced dashboard with engine/model visibility."""
    data = get_enhanced_dashboard_data()
    waves = data["waves"]
    activity = data["current_activity"]
    stats = data["stats"]
    workers = data["workers_enhanced"]
    engine_summary = data["engine_summary"]

    # Build enhanced workers HTML with engine info
    workers_html = ""
    for worker in workers:
        engine_badge_class = "engine-claude" if worker["engine"] == "CLAUDE" else "engine-groq"
        engine_icon = "🧠" if worker["engine"] == "CLAUDE" else "⚡"

        workers_html += f'''<article class="worker enhanced-worker" aria-labelledby="worker-{worker['id']}-type"
            aria-describedby="worker-{worker['id']}-task">
            <div class="worker-header">
                <div class="worker-title">
                    <span class="worker-id">{worker['id']}</span>
                    <span class="engine-badge {engine_badge_class}">
                        <span class="engine-icon">{engine_icon}</span>
                        <span class="engine-name">{worker['engine']}</span>
                    </span>
                </div>
                <div class="worker-status" aria-label="Worker status indicator"></div>
            </div>
            <div class="worker-details">
                <div class="worker-model">
                    <span class="label">Model:</span>
                    <span class="value">{worker['model']}</span>
                </div>
                <div class="worker-reason">
                    <span class="label">Why:</span>
                    <span class="value">{worker['selection_reason']}</span>
                </div>
                <div class="worker-cost">
                    <span class="label">Cost:</span>
                    <span class="value">${worker['cost_this_session']:.4f}</span>
                </div>
            </div>
            <div class="worker-task" id="worker-{worker['id']}-task">{worker['task']}</div>
        </article>'''

    # Build engine summary panel
    engine_summary_html = f'''
    <div class="engine-summary-grid">
        <div class="summary-card claude-card">
            <div class="summary-header">
                <span class="summary-icon">🧠</span>
                <span class="summary-title">Claude Usage</span>
            </div>
            <div class="summary-value">{engine_summary['claude_percentage']}%</div>
            <div class="summary-cost">${engine_summary['cost_breakdown']['claude']:.4f}</div>
        </div>
        <div class="summary-card groq-card">
            <div class="summary-header">
                <span class="summary-icon">⚡</span>
                <span class="summary-title">Groq Usage</span>
            </div>
            <div class="summary-value">{engine_summary['groq_percentage']}%</div>
            <div class="summary-cost">${engine_summary['cost_breakdown']['groq']:.4f}</div>
        </div>
        <div class="summary-card total-card">
            <div class="summary-header">
                <span class="summary-icon">💰</span>
                <span class="summary-title">Total Cost</span>
            </div>
            <div class="summary-value">${engine_summary['total_cost']:.4f}</div>
            <div class="summary-cost">Combined</div>
        </div>
    </div>
    '''

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

    # Enhanced HTML with engine visibility styles
    enhanced_css = '''
        /* Engine visibility enhancements */
        .enhanced-worker {
            position: relative;
            padding: 16px;
            background: linear-gradient(135deg, var(--bs-glass-bg), rgba(17, 17, 21, 0.9));
        }

        .worker-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .worker-title {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .worker-id {
            color: var(--bs-primary);
            font-weight: 700;
            font-size: 0.9rem;
        }

        .engine-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .engine-claude {
            background: linear-gradient(135deg, rgba(57, 73, 171, 0.3), rgba(57, 73, 171, 0.2));
            border: 1px solid #3949ab;
            color: #7986cb;
        }

        .engine-groq {
            background: linear-gradient(135deg, rgba(255, 143, 0, 0.3), rgba(255, 143, 0, 0.2));
            border: 1px solid #ff8f00;
            color: #ffb74d;
        }

        .worker-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin-bottom: 8px;
            font-size: 0.75rem;
        }

        .worker-details .label {
            color: var(--bs-text-secondary);
            font-weight: 500;
        }

        .worker-details .value {
            color: var(--bs-text-primary);
            font-weight: 600;
        }

        .worker-cost {
            grid-column: 1 / -1;
        }

        /* Engine summary panel */
        .engine-summary-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        .summary-card {
            background: var(--bs-glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--bs-glass-border);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            transition: all 0.3s var(--motion-spring);
        }

        .claude-card:hover {
            border-color: #3949ab;
            box-shadow: 0 0 20px rgba(57, 73, 171, 0.3);
        }

        .groq-card:hover {
            border-color: #ff8f00;
            box-shadow: 0 0 20px rgba(255, 143, 0, 0.3);
        }

        .total-card:hover {
            border-color: var(--bs-primary);
            box-shadow: 0 0 20px rgba(0, 255, 148, 0.3);
        }

        .summary-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-bottom: 8px;
        }

        .summary-icon {
            font-size: 1.2rem;
        }

        .summary-title {
            color: var(--bs-text-secondary);
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .summary-value {
            color: var(--bs-primary);
            font-size: 1.8rem;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .summary-cost {
            color: var(--bs-text-tertiary);
            font-size: 0.7rem;
        }

        /* Real-time update animations */
        .engine-switch-indicator {
            position: absolute;
            top: 8px;
            right: 8px;
            width: 8px;
            height: 8px;
            background: var(--bs-warning);
            border-radius: 50%;
            animation: engineSwitch 1s ease-in-out;
        }

        @keyframes engineSwitch {
            0%, 100% { opacity: 0; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.5); }
        }

        /* Model distribution chart styles */
        .model-distribution {
            margin-top: 16px;
        }

        .model-bar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            padding: 4px 0;
            border-bottom: 1px solid var(--bs-glass-border);
        }

        .model-name {
            color: var(--bs-text-primary);
            font-size: 0.75rem;
            font-weight: 500;
        }

        .model-count {
            color: var(--bs-primary);
            font-size: 0.75rem;
            font-weight: 700;
        }
    '''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Black Swarm Command Center - Enhanced</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        /* Base styles from original progress_server.py */
        :root {{
            --bs-primary: #00ff94;
            --bs-primary-dark: #00cc75;
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
            --motion-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--bs-surface-primary) 0%, var(--bs-surface-secondary) 50%, var(--bs-surface-tertiary) 100%);
            background-attachment: fixed;
            color: var(--bs-text-primary);
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
        }}

        .glass-card {{
            background: var(--bs-glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--bs-glass-border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            transition: all 0.3s var(--motion-spring);
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 24px;
            color: var(--bs-primary);
            font-size: 1.25rem;
            font-weight: 600;
        }}

        .workers-grid {{
            display: grid;
            gap: 16px;
        }}

        .worker {{
            background: var(--bs-glass-bg);
            backdrop-filter: blur(8px);
            border: 1px solid var(--bs-glass-border);
            border-radius: 12px;
            padding: 16px;
            transition: all 0.3s var(--motion-spring);
        }}

        {enhanced_css}
    </style>
</head>
<body>
    <div class="container">
        <header style="text-align: center; margin-bottom: 48px;">
            <h1 style="font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, var(--bs-primary) 0%, var(--bs-secondary) 100%); background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Black Swarm Command Center
            </h1>
            <p style="color: var(--bs-text-secondary); margin-top: 8px;">Enhanced Engine & Model Visibility</p>
        </header>

        <section class="glass-card">
            <h2 class="section-header">Engine Distribution</h2>
            {engine_summary_html}
            <div class="model-distribution">
                <h3 style="color: var(--bs-text-secondary); font-size: 0.9rem; margin-bottom: 12px;">Model Distribution</h3>
                {''.join([f'<div class="model-bar"><span class="model-name">{model}</span><span class="model-count">{count}</span></div>' for model, count in engine_summary.get('model_distribution', {}).items()])}
            </div>
        </section>

        <section class="glass-card">
            <h2 class="section-header">{activity.get('title', 'AI Workers')}</h2>
            <div class="workers-grid" id="workers">
                {workers_html if workers_html else '<div style="text-align: center; color: var(--bs-text-secondary); padding: 40px;">No active workers</div>'}
            </div>
        </section>

        <footer style="text-align: center; color: var(--bs-text-tertiary); margin-top: 48px;">
            Last updated: {data['timestamp']} | Engine visibility enabled
        </footer>
    </div>

    <script>
        // Enhanced dashboard with real-time engine updates
        const eventSource = new EventSource('/events');

        eventSource.onmessage = function(event) {{
            try {{
                const data = JSON.parse(event.data);
                updateEnhancedDashboard(data);
            }} catch (e) {{
                console.error('Error parsing update:', e);
            }}
        }};

        function updateEnhancedDashboard(data) {{
            if (data.workers_enhanced) {{
                updateEnhancedWorkers(data.workers_enhanced);
            }}
            if (data.engine_summary) {{
                updateEngineSummary(data.engine_summary);
            }}
        }}

        function updateEnhancedWorkers(workers) {{
            const workersGrid = document.getElementById('workers');
            if (!workers.length) return;

            let html = '';
            workers.forEach(worker => {{
                const engineClass = worker.engine === 'CLAUDE' ? 'engine-claude' : 'engine-groq';
                const engineIcon = worker.engine === 'CLAUDE' ? '🧠' : '⚡';

                html += `
                    <article class="worker enhanced-worker">
                        <div class="worker-header">
                            <div class="worker-title">
                                <span class="worker-id">${{worker.id}}</span>
                                <span class="engine-badge ${{engineClass}}">
                                    <span class="engine-icon">${{engineIcon}}</span>
                                    <span class="engine-name">${{worker.engine}}</span>
                                </span>
                            </div>
                            <div class="worker-status"></div>
                        </div>
                        <div class="worker-details">
                            <div class="worker-model">
                                <span class="label">Model:</span>
                                <span class="value">${{worker.model}}</span>
                            </div>
                            <div class="worker-reason">
                                <span class="label">Why:</span>
                                <span class="value">${{worker.selection_reason}}</span>
                            </div>
                            <div class="worker-cost">
                                <span class="label">Cost:</span>
                                <span class="value">$${{worker.cost_this_session.toFixed(4)}}</span>
                            </div>
                        </div>
                        <div class="worker-task">${{worker.task}}</div>
                    </article>
                `;
            }});

            workersGrid.innerHTML = html;
        }}

        function updateEngineSummary(summary) {{
            // Update summary cards with new data
            const claudeCard = document.querySelector('.claude-card .summary-value');
            const groqCard = document.querySelector('.groq-card .summary-value');
            const totalCard = document.querySelector('.total-card .summary-value');

            if (claudeCard) claudeCard.textContent = summary.claude_percentage + '%';
            if (groqCard) groqCard.textContent = summary.groq_percentage + '%';
            if (totalCard) totalCard.textContent = '$' + summary.total_cost.toFixed(4);
        }}

        // Initialize
        console.log('Enhanced Black Swarm Command Center loaded');
    </script>
</body>
</html>'''


class EnhancedHandler(http.server.BaseHTTPRequestHandler):
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
                data = json.dumps(get_enhanced_dashboard_data())
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
            self.wfile.write(json.dumps(get_enhanced_dashboard_data()).encode('utf-8'))

        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress logs for cleaner output


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def main():
    parser = argparse.ArgumentParser(description="Enhanced Black Swarm Command Center")
    parser.add_argument("--port", type=int, default=8080, help="Port to run on")
    parser.add_argument("--lan", action="store_true", help="Make accessible on LAN")
    args = parser.parse_args()

    # Start file watcher thread
    threading.Thread(target=file_watcher, daemon=True).start()

    host = "0.0.0.0" if args.lan else "127.0.0.1"

    with ThreadedServer((host, args.port), EnhancedHandler) as server:
        print(f"🧠 Enhanced Black Swarm Command Center Online")
        print(f"   Local:  http://localhost:{args.port}")
        if args.lan:
            import socket
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                print(f"   LAN:    http://{ip}:{args.port}")
            except:
                pass
        print(f"   Engine/Model visibility active")
        print(f"   Press Ctrl+C to terminate")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n🔴 Enhanced Command Center offline")


if __name__ == "__main__":
    main()