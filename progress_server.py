#!/usr/bin/env python3
"""
Black Swarm Command Center - Enterprise AI Monitoring Dashboard
Real-time intelligence dashboard with glassmorphism design and advanced UX.

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
    """Enterprise-grade Black Swarm Command Center with glassmorphism design."""
    data = get_dashboard_data()
    waves = data["waves"]
    activity = data["current_activity"]
    stats = data["stats"]

    # Build wave tracker HTML with accessibility
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

    # Build workers HTML with accessibility
    workers_html = ""
    for i, w in enumerate(activity.get("workers", [])):
        worker_type = w.get("type", "Worker")
        worker_task = w.get("task", "Initializing...")
        workers_html += f'''<article class="worker" aria-labelledby="worker-{i}-type"
            aria-describedby="worker-{i}-task">
            <div class="type" id="worker-{i}-type">{worker_type}</div>
            <div class="task" id="worker-{i}-task">{worker_task}</div>
            <div class="worker-status" aria-label="Worker status indicator"></div>
        </article>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Black Swarm Command Center</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            /* Black Swarm Brand Colors */
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

            /* Design System */
            --spacing-xs: 4px;
            --spacing-sm: 8px;
            --spacing-md: 16px;
            --spacing-lg: 24px;
            --spacing-xl: 32px;
            --spacing-xxl: 48px;

            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;

            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.15);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.2);
            --shadow-glow: 0 0 20px rgba(0, 255, 148, 0.3);

            --motion-ease: cubic-bezier(0.4, 0, 0.2, 1);
            --motion-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-weight: 400;
            line-height: 1.6;
            background: linear-gradient(135deg, var(--bs-surface-primary) 0%, var(--bs-surface-secondary) 50%, var(--bs-surface-tertiary) 100%);
            background-attachment: fixed;
            color: var(--bs-text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            transition: all 0.3s var(--motion-ease);
        }}

        body.dark-mode {{
            --bs-surface-primary: #050505;
            --bs-surface-secondary: #080808;
            --bs-surface-tertiary: #0f0f0f;
        }}

        /* Skip to main content for accessibility */
        .skip-link {{
            position: absolute;
            top: -40px;
            left: 6px;
            background: var(--bs-primary);
            color: var(--bs-surface-primary);
            padding: var(--spacing-sm) var(--spacing-md);
            border-radius: var(--radius-sm);
            text-decoration: none;
            font-weight: 600;
            z-index: 10000;
            transition: top 0.3s var(--motion-ease);
        }}

        .skip-link:focus {{
            top: 6px;
        }}

        /* Screen reader only text */
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}

        /* Loading skeleton */
        .skeleton {{
            background: linear-gradient(90deg,
                rgba(255, 255, 255, 0.1) 25%,
                rgba(255, 255, 255, 0.2) 50%,
                rgba(255, 255, 255, 0.1) 75%
            );
            background-size: 200% 100%;
            animation: skeleton-loading 1.5s infinite ease-in-out;
            border-radius: var(--radius-sm);
        }}

        @keyframes skeleton-loading {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}

        /* Main container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: var(--spacing-lg);
            opacity: 0;
            transform: translateY(20px);
            animation: fadeInUp 0.8s var(--motion-spring) forwards;
        }}

        @keyframes fadeInUp {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        /* Header */
        header {{
            text-align: center;
            margin-bottom: var(--spacing-xxl);
            animation: slideDown 0.6s var(--motion-spring) 0.2s backwards;
        }}

        .brand-title {{
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, var(--bs-primary) 0%, var(--bs-secondary) 100%);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(0, 255, 148, 0.3);
            transition: all 0.3s var(--motion-ease);
            cursor: pointer;
            position: relative;
        }}

        .brand-title:hover {{
            transform: scale(1.02);
            filter: drop-shadow(0 0 40px rgba(0, 255, 148, 0.5));
        }}

        .brand-subtitle {{
            color: var(--bs-text-secondary);
            font-size: 1.2rem;
            font-weight: 500;
            margin-top: var(--spacing-sm);
            letter-spacing: 0.02em;
        }}

        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        /* Status indicator */
        .status-indicator {{
            position: fixed;
            top: var(--spacing-lg);
            right: var(--spacing-lg);
            background: var(--bs-glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--bs-glass-border);
            border-radius: var(--radius-xl);
            padding: var(--spacing-sm) var(--spacing-md);
            font-size: 0.875rem;
            font-weight: 600;
            z-index: 1000;
            transition: all 0.3s var(--motion-spring);
            box-shadow: var(--shadow-md);
            min-width: 120px;
            text-align: center;
        }}

        .status-indicator.live {{
            background: linear-gradient(135deg, rgba(0, 255, 148, 0.2), rgba(0, 212, 255, 0.2));
            border-color: var(--bs-primary);
            color: var(--bs-primary);
            box-shadow: var(--shadow-glow);
            animation: statusPulse 3s ease-in-out infinite;
        }}

        .status-indicator.offline {{
            background: linear-gradient(135deg, rgba(255, 61, 113, 0.2), rgba(255, 61, 113, 0.3));
            border-color: var(--bs-accent);
            color: var(--bs-accent);
            animation: statusShake 0.5s ease-in-out;
        }}

        .status-indicator.reconnecting {{
            background: linear-gradient(135deg, rgba(255, 184, 0, 0.2), rgba(255, 184, 0, 0.3));
            border-color: var(--bs-warning);
            color: var(--bs-warning);
        }}

        .status-indicator:hover {{
            transform: scale(1.05);
            box-shadow: var(--shadow-lg);
        }}

        @keyframes statusPulse {{
            0%, 100% {{
                box-shadow: var(--shadow-md), 0 0 0 0 rgba(0, 255, 148, 0.4);
            }}
            50% {{
                box-shadow: var(--shadow-md), 0 0 0 8px rgba(0, 255, 148, 0.1);
            }}
        }}

        @keyframes statusShake {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            75% {{ transform: translateX(5px); }}
        }}

        /* Glass morphism cards */
        .glass-card {{
            background: var(--bs-glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--bs-glass-border);
            border-radius: var(--radius-lg);
            padding: var(--spacing-lg);
            margin-bottom: var(--spacing-lg);
            transition: all 0.3s var(--motion-spring);
            position: relative;
            overflow: hidden;
        }}

        .glass-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg,
                transparent,
                rgba(255, 255, 255, 0.1),
                transparent
            );
            transition: left 0.6s ease;
        }}

        .glass-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: rgba(255, 255, 255, 0.2);
        }}

        .glass-card:hover::before {{
            left: 100%;
        }}

        .glass-card:focus-within {{
            outline: 2px solid var(--bs-primary);
            outline-offset: 2px;
        }}

        /* Stats grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--spacing-md);
            margin-bottom: var(--spacing-xl);
        }}

        .stat-card {{
            background: var(--bs-glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--bs-glass-border);
            border-radius: var(--radius-md);
            padding: var(--spacing-lg);
            text-align: center;
            transition: all 0.3s var(--motion-spring);
            cursor: pointer;
            position: relative;
            overflow: hidden;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}

        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--bs-primary), var(--bs-secondary));
            transform: scaleX(0);
            transition: transform 0.3s var(--motion-ease);
        }}

        .stat-card:hover {{
            transform: translateY(-2px) scale(1.02);
            border-color: var(--bs-primary);
            box-shadow: var(--shadow-glow);
        }}

        .stat-card:hover::before {{
            transform: scaleX(1);
        }}

        .stat-card:focus {{
            outline: 2px solid var(--bs-primary);
            outline-offset: 2px;
        }}

        .stat-value {{
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--bs-primary);
            letter-spacing: -0.02em;
            line-height: 1;
            margin-bottom: var(--spacing-xs);
            transition: all 0.3s var(--motion-ease);
        }}

        .stat-label {{
            color: var(--bs-text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }}

        /* Section headers */
        .section-header {{
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
            margin-bottom: var(--spacing-lg);
            color: var(--bs-primary);
            font-size: 1.25rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }}

        .section-header::before {{
            content: '';
            width: 12px;
            height: 12px;
            background: radial-gradient(circle, var(--bs-primary), var(--bs-primary-dark));
            border-radius: 50%;
            animation: sectionPulse 2s ease-in-out infinite;
            box-shadow: 0 0 10px rgba(0, 255, 148, 0.5);
        }}

        @keyframes sectionPulse {{
            0%, 100% {{
                transform: scale(1);
                opacity: 1;
            }}
            50% {{
                transform: scale(1.2);
                opacity: 0.7;
            }}
        }}

        /* Wave tracker */
        .wave-tracker {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: var(--spacing-md);
            padding: var(--spacing-sm) 0;
        }}

        .wave {{
            background: var(--bs-glass-bg);
            backdrop-filter: blur(8px);
            border: 1px solid var(--bs-glass-border);
            border-radius: var(--radius-md);
            padding: var(--spacing-md) var(--spacing-lg);
            text-align: center;
            font-size: 0.875rem;
            transition: all 0.3s var(--motion-spring);
            cursor: pointer;
            position: relative;
            overflow: hidden;
            min-height: 80px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: var(--spacing-xs);
        }}

        .wave:focus {{
            outline: 2px solid var(--bs-primary);
            outline-offset: 2px;
        }}

        .wave.done {{
            background: linear-gradient(135deg, rgba(0, 255, 148, 0.2), rgba(0, 204, 117, 0.3));
            border-color: var(--bs-primary);
            color: var(--bs-primary);
            box-shadow: var(--shadow-glow);
        }}

        .wave.done:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 32px rgba(0, 255, 148, 0.4);
        }}

        .wave.running {{
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(0, 170, 204, 0.3));
            border-color: var(--bs-secondary);
            color: var(--bs-secondary);
            animation: waveRunning 2s ease-in-out infinite;
        }}

        .wave.running:hover {{
            animation-play-state: paused;
            transform: translateY(-2px) scale(1.02);
        }}

        .wave.planned {{
            background: var(--bs-glass-bg);
            color: var(--bs-text-secondary);
            border: 1px dashed var(--bs-glass-border);
        }}

        .wave.planned:hover {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--bs-text-primary);
            border-color: var(--bs-primary);
            transform: translateY(-2px);
        }}

        @keyframes waveRunning {{
            0%, 100% {{
                box-shadow: var(--shadow-md), 0 0 0 0 rgba(0, 212, 255, 0.4);
            }}
            50% {{
                box-shadow: var(--shadow-md), 0 0 0 8px rgba(0, 212, 255, 0.1);
            }}
        }}

        .wave .icon {{
            font-size: 1.5rem;
            margin-bottom: var(--spacing-xs);
        }}

        .wave .num {{
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            opacity: 0.9;
        }}

        .wave .name {{
            font-size: 0.75rem;
            opacity: 0.8;
            text-align: center;
            line-height: 1.3;
        }}

        /* Activity section */
        .activity-section {{
            background: linear-gradient(135deg,
                rgba(0, 212, 255, 0.1),
                rgba(0, 255, 148, 0.08)
            );
            border: 1px solid rgba(0, 212, 255, 0.3);
        }}

        .activity-title {{
            color: var(--bs-secondary);
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: var(--spacing-lg);
            display: flex;
            align-items: center;
            gap: var(--spacing-md);
        }}

        .activity-title::before {{
            content: '';
            width: 16px;
            height: 16px;
            background: radial-gradient(circle, var(--bs-secondary), var(--bs-primary));
            border-radius: 50%;
            animation: activityPulse 1.5s ease-in-out infinite;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
        }}

        @keyframes activityPulse {{
            0%, 100% {{
                transform: scale(1);
                opacity: 1;
            }}
            50% {{
                transform: scale(1.3);
                opacity: 0.6;
            }}
        }}

        .workers-grid {{
            display: grid;
            gap: var(--spacing-md);
        }}

        .worker {{
            background: var(--bs-glass-bg);
            backdrop-filter: blur(8px);
            border: 1px solid var(--bs-glass-border);
            border-radius: var(--radius-md);
            padding: var(--spacing-lg);
            transition: all 0.3s var(--motion-spring);
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
            background: linear-gradient(90deg, var(--bs-primary), var(--bs-secondary), var(--bs-warning));
            transform: scaleX(0);
            transition: transform 0.3s var(--motion-ease);
        }}

        .worker:hover {{
            transform: translateY(-2px);
            border-color: rgba(0, 255, 148, 0.4);
            box-shadow: var(--shadow-md);
        }}

        .worker:hover::before {{
            transform: scaleX(1);
        }}

        .worker .type {{
            color: var(--bs-primary);
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: var(--spacing-xs);
            letter-spacing: 0.02em;
        }}

        .worker .task {{
            color: var(--bs-text-primary);
            font-size: 0.875rem;
            line-height: 1.5;
            opacity: 0.9;
        }}

        .worker-status {{
            position: absolute;
            top: var(--spacing-md);
            right: var(--spacing-md);
            width: 12px;
            height: 12px;
            background: var(--bs-primary);
            border-radius: 50%;
            animation: workerPulse 2s ease-in-out infinite;
            box-shadow: 0 0 10px rgba(0, 255, 148, 0.5);
        }}

        @keyframes workerPulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.6; transform: scale(1.2); }}
        }}

        /* Timestamp */
        .timestamp {{
            text-align: center;
            color: var(--bs-text-tertiary);
            font-size: 0.75rem;
            margin-top: var(--spacing-xl);
            padding: var(--spacing-md);
            border-top: 1px solid var(--bs-glass-border);
            transition: all 0.3s var(--motion-ease);
        }}

        .timestamp:hover {{
            color: var(--bs-text-secondary);
        }}

        /* Controls */
        .controls {{
            position: fixed;
            bottom: var(--spacing-lg);
            left: var(--spacing-lg);
            display: flex;
            gap: var(--spacing-sm);
            z-index: 1000;
        }}

        .control-btn {{
            background: var(--bs-glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--bs-glass-border);
            border-radius: var(--radius-md);
            color: var(--bs-text-primary);
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 500;
            padding: var(--spacing-sm) var(--spacing-md);
            transition: all 0.3s var(--motion-spring);
            min-width: 48px;
            min-height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .control-btn:hover {{
            background: rgba(0, 255, 148, 0.1);
            border-color: var(--bs-primary);
            transform: translateY(-2px);
        }}

        .control-btn:focus {{
            outline: 2px solid var(--bs-primary);
            outline-offset: 2px;
        }}

        .control-btn.active {{
            background: linear-gradient(135deg, rgba(0, 255, 148, 0.2), rgba(0, 212, 255, 0.2));
            border-color: var(--bs-primary);
            color: var(--bs-primary);
        }}

        /* Toast notifications */
        .toast {{
            position: fixed;
            bottom: var(--spacing-lg);
            right: var(--spacing-lg);
            background: var(--bs-glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--bs-glass-border);
            border-radius: var(--radius-md);
            padding: var(--spacing-md) var(--spacing-lg);
            font-size: 0.875rem;
            font-weight: 500;
            box-shadow: var(--shadow-lg);
            transform: translateX(400px);
            opacity: 0;
            transition: all 0.4s var(--motion-spring);
            z-index: 10000;
            max-width: 320px;
        }}

        .toast.show {{
            transform: translateX(0);
            opacity: 1;
        }}

        .toast.success {{
            border-color: var(--bs-primary);
            color: var(--bs-primary);
        }}

        .toast.error {{
            border-color: var(--bs-accent);
            color: var(--bs-accent);
        }}

        .toast.info {{
            border-color: var(--bs-secondary);
            color: var(--bs-secondary);
        }}

        /* Keyboard shortcuts help */
        .help-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(8px);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 20000;
            opacity: 0;
            transition: opacity 0.3s var(--motion-ease);
        }}

        .help-overlay.show {{
            display: flex;
            opacity: 1;
        }}

        .help-dialog {{
            background: var(--bs-glass-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--bs-glass-border);
            border-radius: var(--radius-lg);
            padding: var(--spacing-xxl);
            max-width: 500px;
            width: 90%;
            box-shadow: var(--shadow-lg);
            transform: scale(0.9);
            transition: transform 0.3s var(--motion-spring);
        }}

        .help-overlay.show .help-dialog {{
            transform: scale(1);
        }}

        .help-title {{
            color: var(--bs-primary);
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: var(--spacing-lg);
            text-align: center;
        }}

        .help-shortcuts {{
            display: grid;
            gap: var(--spacing-md);
        }}

        .help-shortcut {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--spacing-sm) 0;
            border-bottom: 1px solid var(--bs-glass-border);
        }}

        .help-key {{
            background: var(--bs-surface-tertiary);
            color: var(--bs-primary);
            padding: var(--spacing-xs) var(--spacing-sm);
            border-radius: var(--radius-sm);
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-size: 0.75rem;
            border: 1px solid var(--bs-glass-border);
            font-weight: 600;
        }}

        .help-desc {{
            color: var(--bs-text-primary);
            font-size: 0.875rem;
        }}

        /* Responsive design */
        @media (max-width: 768px) {{
            .container {{
                padding: var(--spacing-md);
            }}

            .brand-title {{
                font-size: 2rem;
            }}

            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: var(--spacing-sm);
            }}

            .stat-card {{
                padding: var(--spacing-md);
                min-height: 100px;
            }}

            .stat-value {{
                font-size: 1.75rem;
            }}

            .wave-tracker {{
                grid-template-columns: 1fr;
            }}

            .glass-card {{
                padding: var(--spacing-md);
            }}

            .controls {{
                position: relative;
                bottom: auto;
                left: auto;
                justify-content: center;
                margin-top: var(--spacing-lg);
            }}

            .help-dialog {{
                padding: var(--spacing-lg);
            }}

            .status-indicator {{
                top: var(--spacing-md);
                right: var(--spacing-md);
                font-size: 0.75rem;
                padding: var(--spacing-xs) var(--spacing-sm);
            }}
        }}

        @media (max-width: 480px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}

            .help-shortcut {{
                flex-direction: column;
                gap: var(--spacing-xs);
                text-align: center;
            }}
        }}

        /* High contrast mode */
        @media (prefers-contrast: high) {{
            :root {{
                --bs-glass-bg: rgba(0, 0, 0, 0.9);
                --bs-glass-border: rgba(255, 255, 255, 0.5);
                --bs-text-secondary: #ffffff;
            }}
        }}

        /* Reduced motion */
        @media (prefers-reduced-motion: reduce) {{
            *,
            *::before,
            *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}

        /* Focus visible for better keyboard navigation */
        .wave:focus-visible,
        .stat-card:focus-visible,
        .control-btn:focus-visible {{
            outline: 2px solid var(--bs-primary);
            outline-offset: 2px;
        }}
    </style>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>

    <div role="status" aria-live="polite" aria-label="Connection status"
         class="status-indicator live" id="status">
        <span aria-hidden="true">●</span> Live
    </div>

    <div class="container">
        <header>
            <h1 class="brand-title" onclick="playBrandSound()">Black Swarm Command Center</h1>
            <div class="brand-subtitle">Elite AI Intelligence Operations</div>
        </header>

        <main id="main">
            <section aria-labelledby="stats-heading">
                <h2 id="stats-heading" class="sr-only">System Statistics</h2>
                <div class="stats-grid" id="stats">
                    <div class="stat-card" tabindex="0" role="button"
                         aria-labelledby="stat-sessions-label" aria-describedby="stat-sessions-value">
                        <div class="stat-value" id="stat-sessions-value">{stats['sessions']}</div>
                        <div class="stat-label" id="stat-sessions-label">Active Sessions</div>
                    </div>
                    <div class="stat-card" tabindex="0" role="button"
                         aria-labelledby="stat-lessons-label" aria-describedby="stat-lessons-value">
                        <div class="stat-value" id="stat-lessons-value">{stats['lessons']}</div>
                        <div class="stat-label" id="stat-lessons-label">Neural Pathways</div>
                    </div>
                    <div class="stat-card" tabindex="0" role="button"
                         aria-labelledby="stat-files-label" aria-describedby="stat-files-value">
                        <div class="stat-value" id="stat-files-value">{stats['files']}</div>
                        <div class="stat-label" id="stat-files-label">Core Modules</div>
                    </div>
                    <div class="stat-card" tabindex="0" role="button"
                         aria-labelledby="stat-lines-label" aria-describedby="stat-lines-value">
                        <div class="stat-value" id="stat-lines-value">{stats['lines']:,}</div>
                        <div class="stat-label" id="stat-lines-label">Neural Synapses</div>
                    </div>
                </div>
            </section>

            <section aria-labelledby="waves-heading" class="glass-card">
                <h2 id="waves-heading" class="section-header">Mission Progress</h2>
                <div class="wave-tracker" id="waves" role="group" aria-label="Mission wave progress">
                    {wave_html}
                </div>
            </section>

            <section aria-labelledby="activity-heading" class="glass-card activity-section">
                <h2 id="activity-heading" class="activity-title">{activity.get('title', 'System Idle')}</h2>
                <div class="workers-grid" id="workers" role="group" aria-label="Active AI workers">
                    {workers_html if workers_html else '<article class="worker"><div class="task">All systems standing by</div></article>'}
                </div>
            </section>

            <footer class="timestamp" id="timestamp" role="contentinfo">
                Last neural sync: {data['timestamp']}
            </footer>
        </main>
    </div>

    <div class="controls" role="toolbar" aria-label="Dashboard controls">
        <button class="control-btn" id="theme-toggle" title="Toggle dark mode"
                aria-label="Toggle between light and dark themes" onclick="toggleTheme()">
            🌙
        </button>
        <button class="control-btn" id="sound-toggle" title="Toggle sound effects"
                aria-label="Toggle sound effects on or off" onclick="toggleSounds()">
            🔊
        </button>
        <button class="control-btn" id="help-toggle" title="Show keyboard shortcuts (Press ? key)"
                aria-label="Show keyboard shortcuts and help" onclick="toggleHelp()">
            ?
        </button>
        <button class="control-btn" id="fullscreen-toggle" title="Toggle fullscreen"
                aria-label="Toggle fullscreen mode" onclick="toggleFullscreen()">
            ⛶
        </button>
    </div>

    <div class="help-overlay" id="help-overlay" role="dialog" aria-labelledby="help-title" aria-hidden="true">
        <div class="help-dialog">
            <h3 class="help-title" id="help-title">Keyboard Shortcuts</h3>
            <div class="help-shortcuts">
                <div class="help-shortcut">
                    <span class="help-key">?</span>
                    <span class="help-desc">Show this help</span>
                </div>
                <div class="help-shortcut">
                    <span class="help-key">D</span>
                    <span class="help-desc">Toggle dark mode</span>
                </div>
                <div class="help-shortcut">
                    <span class="help-key">S</span>
                    <span class="help-desc">Toggle sounds</span>
                </div>
                <div class="help-shortcut">
                    <span class="help-key">F</span>
                    <span class="help-desc">Toggle fullscreen</span>
                </div>
                <div class="help-shortcut">
                    <span class="help-key">R</span>
                    <span class="help-desc">Refresh data</span>
                </div>
                <div class="help-shortcut">
                    <span class="help-key">ESC</span>
                    <span class="help-desc">Close dialogs</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global state
        let soundsEnabled = localStorage.getItem('bs-sounds') === 'true';
        let darkMode = localStorage.getItem('bs-theme') === 'dark';
        let lastUpdateData = null;

        // Audio feedback
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        function playTone(frequency, duration, volume = 0.1) {{
            if (!soundsEnabled) return;

            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
            gainNode.gain.setValueAtTime(volume, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration);
        }}

        function playBrandSound() {{
            if (soundsEnabled) {{
                playTone(800, 0.1);
                setTimeout(() => playTone(1000, 0.1), 100);
                setTimeout(() => playTone(1200, 0.15), 200);
            }}
        }}

        function playUpdateSound() {{
            if (soundsEnabled) {{
                playTone(600, 0.05, 0.05);
            }}
        }}

        function playErrorSound() {{
            if (soundsEnabled) {{
                playTone(300, 0.2);
                setTimeout(() => playTone(250, 0.2), 200);
            }}
        }}

        // Initialize theme and sounds
        function initializeInterface() {{
            document.body.classList.toggle('dark-mode', darkMode);
            document.body.classList.toggle('sounds-enabled', soundsEnabled);
            document.getElementById('sound-toggle').classList.toggle('active', soundsEnabled);
            document.getElementById('theme-toggle').textContent = darkMode ? '☀️' : '🌙';
        }}

        // Smooth number transitions
        function animateNumber(element, newValue) {{
            const oldValue = parseInt(element.textContent.replace(/,/g, '')) || 0;
            if (oldValue === newValue) return;

            const duration = 800;
            const frames = 30;
            const increment = (newValue - oldValue) / frames;
            let current = oldValue;
            let frame = 0;

            const timer = setInterval(() => {{
                frame++;
                current += increment;

                if (frame >= frames) {{
                    current = newValue;
                    clearInterval(timer);
                }}

                element.textContent = Math.round(current).toLocaleString();
            }}, duration / frames);
        }}

        // Dashboard update function
        function updateDashboard(data) {{
            if (!data) return;

            // Check for changes and play sound
            if (lastUpdateData && JSON.stringify(data) !== JSON.stringify(lastUpdateData)) {{
                playUpdateSound();
            }}
            lastUpdateData = data;

            // Update stats with animation
            const stats = data.stats;
            if (stats) {{
                animateNumber(document.getElementById('stat-sessions-value'), stats.sessions);
                animateNumber(document.getElementById('stat-lessons-value'), stats.lessons);
                animateNumber(document.getElementById('stat-files-value'), stats.files);
                animateNumber(document.getElementById('stat-lines-value'), stats.lines);
            }}

            // Update waves
            if (data.waves) {{
                let wavesHtml = '';
                data.waves.forEach((w, index) => {{
                    const status = w.status || 'planned';
                    let cls, icon, ariaLabel;

                    if (status === 'done') {{
                        cls = 'done';
                        icon = '✓';
                        ariaLabel = 'Completed';
                    }} else if (status === 'running') {{
                        cls = 'running';
                        icon = '⚡';
                        ariaLabel = 'Currently running';
                    }} else {{
                        cls = 'planned';
                        icon = '○';
                        ariaLabel = 'Planned';
                    }}

                    wavesHtml += `<article class="wave ${{cls}}" role="button" tabindex="0"
                        aria-label="Wave ${{w.num}}: ${{w.name}} - ${{ariaLabel}}"
                        data-wave="${{w.num}}" onkeypress="handleWaveKey(event)">
                        <span class="icon" aria-hidden="true">${{icon}}</span>
                        <span class="num">Wave ${{w.num}}</span>
                        <span class="name">${{w.name}}</span>
                    </article>`;
                }});
                document.getElementById('waves').innerHTML = wavesHtml;
            }}

            // Update activity
            const activity = data.current_activity || {{}};
            document.getElementById('activity-heading').textContent = activity.title || 'System Idle';

            let workersHtml = '';
            if (activity.workers && activity.workers.length > 0) {{
                activity.workers.forEach((w, i) => {{
                    const workerType = w.type || 'Worker';
                    const workerTask = w.task || 'Initializing...';
                    workersHtml += `<article class="worker" aria-labelledby="worker-${{i}}-type"
                        aria-describedby="worker-${{i}}-task">
                        <div class="type" id="worker-${{i}}-type">${{workerType}}</div>
                        <div class="task" id="worker-${{i}}-task">${{workerTask}}</div>
                        <div class="worker-status" aria-label="Worker status indicator"></div>
                    </article>`;
                }});
            }} else {{
                workersHtml = '<article class="worker"><div class="task">All systems standing by</div></article>';
            }}
            document.getElementById('workers').innerHTML = workersHtml;

            // Update timestamp
            document.getElementById('timestamp').textContent = `Last neural sync: ${{data.timestamp}}`;
        }}

        // Connection management
        function connect() {{
            const status = document.getElementById('status');
            const eventSource = new EventSource('/events');

            eventSource.onopen = () => {{
                status.className = 'status-indicator live';
                status.innerHTML = '<span aria-hidden="true">●</span> Live';
                showToast('Connected to Black Swarm', 'success');
            }};

            eventSource.onmessage = (e) => {{
                try {{
                    const data = JSON.parse(e.data);
                    updateDashboard(data);
                }} catch(err) {{
                    console.error('Parse error:', err);
                    showToast('Data parsing error', 'error');
                }}
            }};

            eventSource.onerror = () => {{
                status.className = 'status-indicator reconnecting';
                status.innerHTML = '<span aria-hidden="true">●</span> Reconnecting...';
                eventSource.close();
                playErrorSound();
                showToast('Connection lost, reconnecting...', 'error');
                setTimeout(connect, 3000);
            }};
        }}

        // Toast notifications
        function showToast(message, type = 'info', duration = 3000) {{
            const toast = document.createElement('div');
            toast.className = `toast ${{type}}`;
            toast.textContent = message;
            toast.setAttribute('role', 'alert');
            toast.setAttribute('aria-live', 'polite');

            document.body.appendChild(toast);

            setTimeout(() => {{
                toast.classList.add('show');
            }}, 100);

            setTimeout(() => {{
                toast.classList.remove('show');
                setTimeout(() => {{
                    document.body.removeChild(toast);
                }}, 400);
            }}, duration);
        }}

        // Control functions
        function toggleTheme() {{
            darkMode = !darkMode;
            localStorage.setItem('bs-theme', darkMode ? 'dark' : 'light');
            document.body.classList.toggle('dark-mode', darkMode);
            document.getElementById('theme-toggle').textContent = darkMode ? '☀️' : '🌙';
            showToast(`${{darkMode ? 'Dark' : 'Light'}} mode activated`, 'info');
            if (soundsEnabled) playTone(darkMode ? 400 : 600, 0.1);
        }}

        function toggleSounds() {{
            soundsEnabled = !soundsEnabled;
            localStorage.setItem('bs-sounds', soundsEnabled.toString());
            document.body.classList.toggle('sounds-enabled', soundsEnabled);
            document.getElementById('sound-toggle').classList.toggle('active', soundsEnabled);
            document.getElementById('sound-toggle').textContent = soundsEnabled ? '🔊' : '🔇';
            showToast(`Sound effects ${{soundsEnabled ? 'enabled' : 'disabled'}}`, 'info');
            if (soundsEnabled) playTone(800, 0.1);
        }}

        function toggleHelp() {{
            const overlay = document.getElementById('help-overlay');
            const isShown = overlay.classList.contains('show');

            if (isShown) {{
                overlay.classList.remove('show');
                overlay.setAttribute('aria-hidden', 'true');
            }} else {{
                overlay.classList.add('show');
                overlay.setAttribute('aria-hidden', 'false');
                overlay.querySelector('.help-dialog').focus();
            }}

            if (soundsEnabled) playTone(isShown ? 500 : 700, 0.1);
        }}

        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen().then(() => {{
                    showToast('Fullscreen mode activated', 'success');
                    if (soundsEnabled) playTone(1000, 0.1);
                }});
            }} else {{
                document.exitFullscreen().then(() => {{
                    showToast('Fullscreen mode deactivated', 'info');
                    if (soundsEnabled) playTone(800, 0.1);
                }});
            }}
        }}

        function refreshData() {{
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {{
                    updateDashboard(data);
                    showToast('Data refreshed', 'success');
                    if (soundsEnabled) playTone(900, 0.1);
                }})
                .catch(err => {{
                    showToast('Refresh failed', 'error');
                    playErrorSound();
                }});
        }}

        // Event handlers
        function handleWaveKey(event) {{
            if (event.key === 'Enter' || event.key === ' ') {{
                event.preventDefault();
                const waveNum = event.target.getAttribute('data-wave');
                showToast(`Wave ${{waveNum}} selected`, 'info');
                if (soundsEnabled) playTone(600, 0.1);
            }}
        }}

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {{
            // Only handle shortcuts when not in input fields
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            switch(e.key.toLowerCase()) {{
                case '?':
                    e.preventDefault();
                    toggleHelp();
                    break;
                case 'd':
                    e.preventDefault();
                    toggleTheme();
                    break;
                case 's':
                    e.preventDefault();
                    toggleSounds();
                    break;
                case 'f':
                    e.preventDefault();
                    toggleFullscreen();
                    break;
                case 'r':
                    e.preventDefault();
                    refreshData();
                    break;
                case 'escape':
                    const helpOverlay = document.getElementById('help-overlay');
                    if (helpOverlay.classList.contains('show')) {{
                        toggleHelp();
                    }}
                    break;
            }}
        }});

        // Click outside to close help
        document.getElementById('help-overlay').addEventListener('click', (e) => {{
            if (e.target === e.currentTarget) {{
                toggleHelp();
            }}
        }});

        // Initialize everything
        document.addEventListener('DOMContentLoaded', () => {{
            initializeInterface();
            connect();

            // Initial data load with skeleton loading
            const skeletonElements = document.querySelectorAll('.stat-value');
            skeletonElements.forEach(el => {{
                el.classList.add('skeleton');
                setTimeout(() => {{
                    el.classList.remove('skeleton');
                }}, 1000);
            }});

            showToast('Black Swarm Command Center Online', 'success');
            playBrandSound();
        }});

        // Handle visibility change for performance
        document.addEventListener('visibilitychange', () => {{
            if (document.hidden) {{
                // Pause animations when tab is hidden
                document.body.style.animationPlayState = 'paused';
            }} else {{
                document.body.style.animationPlayState = 'running';
                // Refresh data when tab becomes visible
                refreshData();
            }}
        }});
    </script>
</body>
</html>'''


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html', '/command', '/dashboard'):
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
    parser = argparse.ArgumentParser(description="Black Swarm Command Center")
    parser.add_argument("--port", type=int, default=8080, help="Port to run on")
    parser.add_argument("--lan", action="store_true", help="Make accessible on LAN")
    args = parser.parse_args()

    # Start file watcher thread
    threading.Thread(target=file_watcher, daemon=True).start()

    host = "0.0.0.0" if args.lan else "127.0.0.1"

    with ThreadedServer((host, args.port), Handler) as server:
        print(f"🐛 Black Swarm Command Center Online")
        print(f"   Local:  http://localhost:{args.port}")
        if args.lan:
            print(f"   LAN:    http://{get_local_ip()}:{args.port}")
        print(f"   Real-time intelligence monitoring active")
        print(f"   Press Ctrl+C to terminate")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n🔴 Black Swarm Command Center offline")


if __name__ == "__main__":
    main()