#!/usr/bin/env python3
"""
Live progress dashboard with real-time Server-Sent Events.
Simple, reliable, and actually works - now with P2 polish improvements.

Usage:
    py progress_server.py          # Local only on port 8080
    py progress_server.py --lan    # LAN accessible
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

PORT = 8080
WORKSPACE = Path(__file__).parent

# Global: list of SSE client queues and file modification times
sse_clients = []
sse_lock = threading.Lock()
last_mtimes = {}


def get_file_mtimes():
    """Get modification times of monitored files."""
    files = [
        WORKSPACE / "wave_status.json",
        WORKSPACE / "SUMMARY.md",
        WORKSPACE / "PROGRESS.md",
        WORKSPACE / "learned_lessons.json",
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
    return {"waves": [], "current_activity": {"title": "Loading...", "workers": []}}


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
    return {
        "waves": wave_data.get("waves", []),
        "current_activity": wave_data.get("current_activity", {}),
        "stats": stats,
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
    """Single-page dashboard with SSE auto-refresh and P2 polish."""
    data = get_dashboard_data()
    waves = data["waves"]
    activity = data["current_activity"]
    stats = data["stats"]

    # Build wave tracker HTML
    wave_html = ""
    for w in waves:
        status = w.get("status", "planned")
        if status == "done":
            cls, icon = "done", "✓"
        elif status == "running":
            cls, icon = "running", "⚡"
        else:
            cls, icon = "planned", "○"

        wave_html += f'''<div class="wave {cls}">
            <span class="icon">{icon}</span>
            <span class="num">Wave {w["num"]}</span>
            <span class="name">{w["name"]}</span>
        </div>'''

    # Build workers HTML
    workers_html = ""
    for w in activity.get("workers", []):
        workers_html += f'''<div class="worker">
            <div class="type">{w.get("type", "Worker")}</div>
            <div class="task">{w.get("task", "Working...")}</div>
        </div>'''

    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Black Swarm Dashboard</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, -apple-system-ui-rounded, sans-serif;
            background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #21262d 100%);
            background-attachment: fixed;
            color: #e6edf3;
            min-height: 100vh;
            padding: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            opacity: 0;
            transform: translateY(20px);
            animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }}

        @keyframes fadeInUp {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        header {{
            text-align: center;
            margin-bottom: 30px;
            animation: slideInDown 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.2s backwards;
        }}

        h1 {{
            color: #58a6ff;
            font-size: 2.2em;
            margin-bottom: 8px;
            font-weight: 700;
            letter-spacing: -0.02em;
            text-shadow: 0 0 30px rgba(88, 166, 255, 0.3);
            transition: all 0.3s ease;
        }}

        h1:hover {{
            transform: scale(1.02);
            text-shadow: 0 0 40px rgba(88, 166, 255, 0.5);
        }}

        .subtitle {{
            color: #7ee787;
            font-size: 1.1em;
            font-weight: 500;
            letter-spacing: 0.02em;
            opacity: 0.9;
        }}

        @keyframes slideInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .status-badge {{
            position: fixed;
            top: 15px;
            right: 15px;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 0.85em;
            font-weight: 600;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 1000;
        }}

        .status-badge.live {{
            background: linear-gradient(135deg, #238636, #2ea043);
            color: white;
            animation: subtlePulse 3s ease-in-out infinite;
        }}

        .status-badge.offline {{
            background: linear-gradient(135deg, #da3633, #f85149);
            color: white;
            animation: shake 0.5s ease-in-out;
        }}

        .status-badge:hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }}

        @keyframes subtlePulse {{
            0%, 100% {{ box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), 0 0 0 0 rgba(35, 134, 54, 0.4); }}
            50% {{ box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), 0 0 0 4px rgba(35, 134, 54, 0.2); }}
        }}

        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            75% {{ transform: translateX(5px); }}
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 25px;
        }}

        @media (max-width: 600px) {{
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
        }}

        .stat {{
            background: linear-gradient(145deg, #161b22, #1c2128);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 18px;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}

        .stat::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(88, 166, 255, 0.1), transparent);
            transition: left 0.5s ease;
        }}

        .stat:hover {{
            transform: translateY(-2px);
            border-color: #58a6ff;
            box-shadow: 0 8px 25px rgba(88, 166, 255, 0.1);
        }}

        .stat:hover::before {{
            left: 100%;
        }}

        .stat .value {{
            font-size: 2.2em;
            font-weight: 800;
            color: #58a6ff;
            letter-spacing: -0.02em;
            transition: all 0.3s ease;
        }}

        .stat .label {{
            color: #8b949e;
            font-size: 0.9em;
            margin-top: 6px;
            font-weight: 500;
            letter-spacing: 0.02em;
        }}

        .section {{
            background: linear-gradient(145deg, #161b22, #1c2128);
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
        }}

        .section:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            border-color: rgba(126, 231, 135, 0.3);
        }}

        .section-title {{
            color: #7ee787;
            font-size: 1.2em;
            margin-bottom: 18px;
            font-weight: 600;
            letter-spacing: 0.02em;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .section-title::before {{
            content: '●';
            color: #7ee787;
            font-size: 0.6em;
            animation: pulse 2s ease-in-out infinite;
        }}

        .wave-tracker {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 5px 0;
        }}

        .wave {{
            flex-shrink: 0;
            padding: 12px 18px;
            border-radius: 10px;
            text-align: center;
            font-size: 0.85em;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}

        .wave::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
            transform: translateX(-100%);
            transition: transform 0.6s ease;
        }}

        .wave:hover::before {{
            transform: translateX(100%);
        }}

        .wave.done {{
            background: linear-gradient(135deg, #238636, #2ea043);
            color: white;
            box-shadow: 0 2px 8px rgba(35, 134, 54, 0.3);
        }}

        .wave.done:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(35, 134, 54, 0.4);
        }}

        .wave.running {{
            background: linear-gradient(135deg, #1f6feb, #58a6ff);
            color: white;
            animation: runningWave 2s ease-in-out infinite;
            box-shadow: 0 2px 8px rgba(31, 111, 235, 0.3);
        }}

        .wave.running:hover {{
            animation-play-state: paused;
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 6px 20px rgba(31, 111, 235, 0.5);
        }}

        .wave.planned {{
            background: linear-gradient(145deg, #21262d, #2d333b);
            color: #8b949e;
            border: 1px dashed #30363d;
            transition: all 0.3s ease;
        }}

        .wave.planned:hover {{
            background: linear-gradient(145deg, #2d333b, #373e47);
            color: #c9d1d9;
            border-color: #58a6ff;
            transform: translateY(-2px);
        }}

        @keyframes runningWave {{
            0%, 100% {{
                box-shadow: 0 2px 8px rgba(31, 111, 235, 0.3), 0 0 0 0 rgba(88,166,255,0.4);
            }}
            50% {{
                box-shadow: 0 2px 8px rgba(31, 111, 235, 0.3), 0 0 0 8px rgba(88,166,255,0.1);
            }}
        }}

        .wave .icon {{
            margin-right: 6px;
            font-size: 1.1em;
        }}

        .wave .name {{
            display: block;
            font-size: 0.8em;
            margin-top: 4px;
            opacity: 0.95;
            font-weight: 500;
        }}

        .activity {{
            background: linear-gradient(135deg, rgba(31, 111, 235, 0.08), rgba(88, 166, 255, 0.12));
            border: 1px solid rgba(31, 111, 235, 0.3);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(31, 111, 235, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .activity:hover {{
            transform: translateY(-2px);
            border-color: rgba(88, 166, 255, 0.5);
            box-shadow: 0 8px 25px rgba(31, 111, 235, 0.15);
        }}

        .activity-title {{
            color: #58a6ff;
            font-size: 1.2em;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            letter-spacing: 0.02em;
        }}

        .activity-title::before {{
            content: '';
            width: 12px;
            height: 12px;
            background: radial-gradient(circle, #58a6ff, #1f6feb);
            border-radius: 50%;
            animation: activityPulse 1.5s ease-in-out infinite;
            box-shadow: 0 0 10px rgba(88, 166, 255, 0.5);
        }}

        @keyframes activityPulse {{
            0%, 100% {{
                transform: scale(1);
                opacity: 1;
            }}
            50% {{
                transform: scale(1.2);
                opacity: 0.7;
            }}
        }}

        .workers {{
            display: grid;
            gap: 12px;
        }}

        .worker {{
            background: linear-gradient(145deg, rgba(13, 17, 23, 0.8), rgba(22, 27, 34, 0.9));
            padding: 16px;
            border-radius: 10px;
            border: 1px solid rgba(48, 54, 61, 0.5);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}

        .worker::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #d2a8ff, #a5a6ff, #79c0ff);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}

        .worker:hover {{
            transform: translateY(-2px);
            border-color: rgba(210, 168, 255, 0.4);
            box-shadow: 0 4px 12px rgba(210, 168, 255, 0.1);
        }}

        .worker:hover::before {{
            transform: scaleX(1);
        }}

        .worker .type {{
            color: #d2a8ff;
            font-weight: 700;
            margin-bottom: 6px;
            font-size: 0.9em;
            letter-spacing: 0.02em;
        }}

        .worker .task {{
            color: #c9d1d9;
            font-size: 0.85em;
            line-height: 1.4;
            opacity: 0.9;
        }}

        .timestamp {{
            text-align: center;
            color: #484f58;
            font-size: 0.8em;
            margin-top: 20px;
            opacity: 0.8;
            transition: opacity 0.3s ease;
        }}

        .timestamp:hover {{
            opacity: 1;
        }}

        /* Toast notifications */
        .toast {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #238636, #2ea043);
            color: white;
            padding: 12px 20px;
            border-radius: 10px;
            font-size: 0.9em;
            font-weight: 500;
            box-shadow: 0 4px 15px rgba(35, 134, 54, 0.3);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 1000;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }}

        .toast.show {{
            transform: translateY(0);
            opacity: 1;
        }}

        .toast.error {{
            background: linear-gradient(135deg, #da3633, #f85149);
        }}

        .toast.info {{
            background: linear-gradient(135deg, #1f6feb, #58a6ff);
        }}

        /* Help overlay */
        .help-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(5px);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 2000;
        }}

        .help-dialog {{
            background: linear-gradient(145deg, #161b22, #1c2128);
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 30px;
            max-width: 400px;
            width: 90%;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }}

        .help-title {{
            color: #58a6ff;
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 20px;
            text-align: center;
        }}

        .help-shortcuts {{
            display: grid;
            gap: 12px;
        }}

        .help-shortcut {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid rgba(48, 54, 61, 0.3);
        }}

        .help-key {{
            background: #21262d;
            padding: 4px 8px;
            border-radius: 6px;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-size: 0.8em;
            color: #58a6ff;
            border: 1px solid #30363d;
        }}

        .help-desc {{
            color: #c9d1d9;
            font-size: 0.9em;
        }}

        /* Loading spinner */
        .loading-indicator {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: none;
        }}

        .spinner {{
            width: 40px;
            height: 40px;
            border: 3px solid rgba(88, 166, 255, 0.2);
            border-top: 3px solid #58a6ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}

        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        /* Responsive improvements */
        @media (max-width: 768px) {{
            body {{ padding: 15px; }}
            .container {{ animation-delay: 0.1s; }}
            h1 {{ font-size: 1.8em; }}
            .stats {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
            .section, .activity {{ padding: 18px; }}
            .wave {{ padding: 10px 14px; font-size: 0.8em; }}
            .help-dialog {{ padding: 20px; }}
            .toast {{ bottom: 15px; right: 15px; font-size: 0.85em; }}
        }}

        /* Improved focus styles for accessibility */
        button:focus, .wave:focus, .stat:focus {{
            outline: 2px solid #58a6ff;
            outline-offset: 2px;
        }}
    </style>
</head>
<body>
    <div class="status-badge live" id="status" role="status" aria-live="polite" aria-label="Connection status">● Live</div>

    <div class="loading-indicator" id="loading">
        <div class="spinner"></div>
    </div>

    <div class="help-overlay" id="helpOverlay">
        <div class="help-dialog">
            <div class="help-title">Keyboard Shortcuts</div>
            <div class="help-shortcuts">
                <div class="help-shortcut">
                    <span class="help-key">R</span>
                    <span class="help-desc">Refresh data</span>
                </div>
                <div class="help-shortcut">
                    <span class="help-key">?</span>
                    <span class="help-desc">Show this help</span>
                </div>
                <div class="help-shortcut">
                    <span class="help-key">Esc</span>
                    <span class="help-desc">Close dialogs</span>
                </div>
                <div class="help-shortcut">
                    <span class="help-key">F</span>
                    <span class="help-desc">Toggle fullscreen</span>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <header>
            <h1>Black Swarm Monitoring</h1>
            <div class="subtitle">Autonomous swarm intelligence in action</div>
        </header>

        <div class="stats" id="stats" role="region" aria-label="System statistics">
            <div class="stat"><div class="value" id="stat-sessions">{stats['sessions']}</div><div class="label">Sessions</div></div>
            <div class="stat"><div class="value" id="stat-lessons">{stats['lessons']}</div><div class="label">Lessons</div></div>
            <div class="stat"><div class="value" id="stat-files">{stats['files']}</div><div class="label">Files</div></div>
            <div class="stat"><div class="value" id="stat-lines">{stats['lines']:,}</div><div class="label">Lines</div></div>
        </div>

        <div class="section" role="region" aria-label="Wave progress tracking">
            <div class="section-title">Wave Progress</div>
            <div class="wave-tracker" id="waves" role="list" aria-label="Wave progression status">{wave_html}</div>
        </div>

        <div class="activity" id="activity" role="region" aria-label="Current activity and worker status">
            <div class="activity-title" id="activity-title">{activity.get('title', 'Idle')}</div>
            <div class="workers" id="workers" role="list" aria-label="Active workers">{workers_html if workers_html else '<div class="worker" role="listitem"><div class="task">No active workers</div></div>'}</div>
        </div>

        <div class="timestamp" id="timestamp">Updated: {data['timestamp']}</div>
    </div>

    <script>
        // State for animations and features
        let previousStats = {{}};
        let toastQueue = [];
        let isToastShowing = false;

        // Smooth number animation utility
        function animateNumber(element, from, to, duration = 800) {{
            const startTime = performance.now();
            const difference = to - from;

            function updateNumber(currentTime) {{
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                // Easing function for smooth animation
                const easeOut = 1 - Math.pow(1 - progress, 3);
                const current = Math.floor(from + (difference * easeOut));

                element.textContent = current.toLocaleString();

                if (progress < 1) {{
                    requestAnimationFrame(updateNumber);
                }}
            }}

            requestAnimationFrame(updateNumber);
        }}

        // Toast notification system
        function showToast(message, type = 'success') {{
            toastQueue.push({{ message, type }});
            if (!isToastShowing) {{
                processToastQueue();
            }}
        }}

        function processToastQueue() {{
            if (toastQueue.length === 0) {{
                isToastShowing = false;
                return;
            }}

            isToastShowing = true;
            const {{ message, type }} = toastQueue.shift();

            const toast = document.createElement('div');
            toast.className = `toast ${{type}}`;
            toast.textContent = message;

            document.body.appendChild(toast);

            // Show animation
            setTimeout(() => toast.classList.add('show'), 50);

            // Hide and remove after delay
            setTimeout(() => {{
                toast.classList.remove('show');
                setTimeout(() => {{
                    document.body.removeChild(toast);
                    processToastQueue(); // Process next toast
                }}, 400);
            }}, 3000);
        }}

        // Enhanced updateDashboard with animations
        function updateDashboard(data) {{
            // Animate stats changes
            const statsElements = {{
                sessions: document.getElementById('stat-sessions'),
                lessons: document.getElementById('stat-lessons'),
                files: document.getElementById('stat-files'),
                lines: document.getElementById('stat-lines')
            }};

            Object.keys(statsElements).forEach(key => {{
                const element = statsElements[key];
                const newValue = data.stats[key];
                const oldValue = previousStats[key] || 0;

                if (newValue !== oldValue) {{
                    if (key === 'lines') {{
                        // For large numbers, animate smoothly
                        animateNumber(element, oldValue, newValue, 1000);
                    }} else {{
                        // For smaller numbers, simple animation
                        animateNumber(element, oldValue, newValue, 600);
                    }}

                    // Show toast for significant changes
                    if (oldValue > 0 && newValue > oldValue) {{
                        const change = newValue - oldValue;
                        showToast(`+${{change}} ${{key}}`, 'info');
                    }}
                }}
            }});

            // Store current stats for next comparison
            previousStats = {{ ...data.stats }};

            // Update waves with status change detection
            const currentWaves = document.getElementById('waves').innerHTML;
            let wavesHtml = '';
            data.waves.forEach(w => {{
                let cls = w.status === 'done' ? 'done' : (w.status === 'running' ? 'running' : 'planned');
                let icon = w.status === 'done' ? '✓' : (w.status === 'running' ? '⚡' : '○');
                wavesHtml += `<div class="wave ${{cls}}"><span class="icon">${{icon}}</span><span class="num">Wave ${{w.num}}</span><span class="name">${{w.name}}</span></div>`;
            }});

            if (wavesHtml !== currentWaves) {{
                document.getElementById('waves').innerHTML = wavesHtml;
                // Check for wave completions
                data.waves.forEach(w => {{
                    if (w.status === 'done' && !currentWaves.includes(`Wave ${{w.num}}</span><span class="name">${{w.name}}</span></div>`)) {{
                        showToast(`Wave ${{w.num}} completed!`, 'success');
                    }}
                }});
            }}

            // Update activity
            document.getElementById('activity-title').innerHTML = data.current_activity.title || 'Idle';
            let workersHtml = '';
            (data.current_activity.workers || []).forEach(w => {{
                workersHtml += `<div class="worker"><div class="type">${{w.type || 'Worker'}}</div><div class="task">${{w.task || 'Working...'}}</div></div>`;
            }});
            document.getElementById('workers').innerHTML = workersHtml || '<div class="worker"><div class="task">No active workers</div></div>';

            // Update timestamp with smooth transition
            const timestampEl = document.getElementById('timestamp');
            timestampEl.style.opacity = '0.5';
            setTimeout(() => {{
                timestampEl.textContent = 'Updated: ' + data.timestamp;
                timestampEl.style.opacity = '1';
            }}, 150);
        }}

        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {{
            // Ignore if user is typing in an input
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            switch(e.key.toLowerCase()) {{
                case 'r':
                    e.preventDefault();
                    refreshData();
                    break;
                case '?':
                    e.preventDefault();
                    toggleHelp();
                    break;
                case 'escape':
                    e.preventDefault();
                    closeHelp();
                    break;
                case 'f':
                    e.preventDefault();
                    toggleFullscreen();
                    break;
            }}
        }});

        function refreshData() {{
            showToast('Refreshing data...', 'info');
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {{
                    updateDashboard(data);
                    showToast('Data refreshed', 'success');
                }})
                .catch(err => {{
                    showToast('Refresh failed', 'error');
                    console.error('Refresh error:', err);
                }});
        }}

        function toggleHelp() {{
            const overlay = document.getElementById('helpOverlay');
            if (overlay) {{
                overlay.style.display = overlay.style.display === 'flex' ? 'none' : 'flex';
            }}
        }}

        function closeHelp() {{
            const overlay = document.getElementById('helpOverlay');
            if (overlay) {{
                overlay.style.display = 'none';
            }}
        }}

        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen().then(() => {{
                    showToast('Entered fullscreen', 'info');
                }}).catch(err => {{
                    showToast('Fullscreen not supported', 'error');
                }});
            }} else {{
                document.exitFullscreen().then(() => {{
                    showToast('Exited fullscreen', 'info');
                }});
            }}
        }}

        // Enhanced connection handling
        function connect() {{
            const status = document.getElementById('status');
            const loading = document.getElementById('loading');

            if (loading) loading.style.display = 'block';

            const es = new EventSource('/events');

            es.onopen = () => {{
                status.className = 'status-badge live';
                status.textContent = '● Live';
                if (loading) loading.style.display = 'none';
                showToast('Connected to live updates', 'success');
            }};

            es.onmessage = (e) => {{
                try {{
                    updateDashboard(JSON.parse(e.data));
                }} catch(err) {{
                    console.error('Parse error:', err);
                    showToast('Data parsing error', 'error');
                }}
            }};

            es.onerror = () => {{
                status.className = 'status-badge offline';
                status.textContent = '● Reconnecting...';
                if (loading) loading.style.display = 'block';
                es.close();
                showToast('Connection lost, reconnecting...', 'error');
                setTimeout(connect, 3000);
            }};
        }}

        // Click handlers for help overlay
        document.addEventListener('click', function(e) {{
            if (e.target.id === 'helpOverlay') {{
                closeHelp();
            }}
        }});

        // Performance monitoring for smooth 60fps
        let frameCount = 0;
        let lastTime = performance.now();

        function monitorFPS() {{
            frameCount++;
            const currentTime = performance.now();

            if (currentTime >= lastTime + 1000) {{
                const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
                if (fps < 30) {{
                    console.warn(`Low FPS detected: ${{fps}}`);
                }}
                frameCount = 0;
                lastTime = currentTime;
            }}

            requestAnimationFrame(monitorFPS);
        }}

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {{
            monitorFPS();
            connect();

            // Add subtle entrance animations
            document.querySelectorAll('.stat, .section, .activity').forEach((el, index) => {{
                el.style.animationDelay = `${{index * 0.1}}s`;
                el.classList.add('fade-in');
            }});
        }});
    </script>
</body>
</html>'''


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html', '/dad', '/summary'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(get_dashboard_html().encode('utf-8'))

        elif self.path == '/events':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
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
                    self.wfile.write(": keepalive\n\n".encode('utf-8'))
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
            self.end_headers()
            self.wfile.write(json.dumps(get_dashboard_data()).encode('utf-8'))

        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress logs


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
    parser = argparse.ArgumentParser(description="Live progress dashboard")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--lan", action="store_true", help="LAN accessible")
    args = parser.parse_args()

    # Start file watcher
    threading.Thread(target=file_watcher, daemon=True).start()

    host = "0.0.0.0" if args.lan else ""

    with ThreadedServer((host, args.port), Handler) as server:
        print(f"Dashboard: http://localhost:{args.port}")
        if args.lan:
            print(f"LAN:       http://{get_local_ip()}:{args.port}")
        print("Live updates enabled. Ctrl+C to stop.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()