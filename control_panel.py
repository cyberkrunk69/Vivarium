#!/usr/bin/env python3
"""
Swarm Control Panel - Real-time monitoring and emergency controls.

A clean UI for:
- Streaming action logs in real-time
- Emergency STOP button
- Identity status overview
- Budget/cost monitoring

Run: python control_panel.py
Open: http://localhost:8421
"""

import json
import os
import secrets
import time
import threading
from ipaddress import ip_address
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request
from flask_socketio import SocketIO, emit
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from vivarium.runtime.vivarium_scope import AUDIT_ROOT, MUTABLE_ROOT, MUTABLE_SWARM_DIR, ensure_scope_layout

ensure_scope_layout()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('VIVARIUM_CONTROL_PANEL_SECRET') or secrets.token_urlsafe(32)
LOCAL_UI_ORIGINS = [
    "http://127.0.0.1:8421",
    "http://localhost:8421",
]
socketio = SocketIO(app, cors_allowed_origins=LOCAL_UI_ORIGINS, async_mode='threading')

# Paths
CODE_ROOT = Path(__file__).parent
WORKSPACE = MUTABLE_ROOT
ACTION_LOG = AUDIT_ROOT / "action_log.jsonl"
KILL_SWITCH = MUTABLE_SWARM_DIR / "kill_switch.json"
FREE_TIME_BALANCES = MUTABLE_SWARM_DIR / "free_time_balances.json"
IDENTITIES_DIR = MUTABLE_SWARM_DIR / "identities"

# Track last read position
last_log_position = 0


def _safe_int_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


CONTROL_PANEL_HOST = os.environ.get("VIVARIUM_CONTROL_PANEL_HOST", "127.0.0.1").strip() or "127.0.0.1"
CONTROL_PANEL_PORT = _safe_int_env("VIVARIUM_CONTROL_PANEL_PORT", 8421)


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


@app.before_request
def enforce_localhost_only():
    if _is_loopback_host(_request_source_host()):
        return None
    return jsonify({"success": False, "error": "Control panel is localhost-only"}), 403


@app.after_request
def apply_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


CONTROL_PANEL_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swarm Control Panel</title>
    <script src="/socket.io/socket.io.js"></script>
    <style>
        :root {
            --bg-dark: #0a0a0f;
            --bg-card: #12121a;
            --bg-hover: #1a1a25;
            --border: #2a2a3a;
            --text: #e0e0e0;
            --text-dim: #888;
            --red: #ff4444;
            --red-glow: rgba(255, 68, 68, 0.3);
            --orange: #ffa500;
            --yellow: #ffd700;
            --green: #44ff44;
            --teal: #00d4d4;
            --blue: #4488ff;
            --purple: #aa44ff;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
            background: var(--bg-dark);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
        }

        .title {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--teal);
        }

        .status-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--green);
            animation: pulse 2s infinite;
        }

        .status-dot.stopped {
            background: var(--red);
            animation: none;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* Emergency Stop Button */
        .stop-button {
            background: var(--red);
            color: white;
            border: none;
            padding: 1rem 2rem;
            font-size: 1.2rem;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 2px;
            box-shadow: 0 0 20px var(--red-glow);
            transition: all 0.2s;
        }

        .stop-button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px var(--red-glow);
        }

        .stop-button:active {
            transform: scale(0.98);
        }

        .stop-button.stopped {
            background: var(--green);
            box-shadow: 0 0 20px rgba(68, 255, 68, 0.3);
        }

        /* Control Buttons Group */
        .control-buttons {
            display: flex;
            gap: 0.5rem;
        }

        .control-btn {
            padding: 0.75rem 1.25rem;
            font-size: 0.9rem;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.2s;
        }

        .control-btn:hover {
            transform: scale(1.03);
        }

        .control-btn:active {
            transform: scale(0.98);
        }

        .control-btn.start {
            background: var(--green);
            color: var(--bg-dark);
        }

        .control-btn.start:disabled {
            background: var(--text-dim);
            cursor: not-allowed;
            transform: none;
        }

        .control-btn.pause {
            background: var(--yellow);
            color: var(--bg-dark);
        }

        .control-btn.pause.paused {
            background: var(--teal);
        }

        .control-btn.stop {
            background: var(--red);
            color: white;
            box-shadow: 0 0 15px var(--red-glow);
        }

        .spawner-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--bg-hover);
            border-radius: 6px;
            font-size: 0.85rem;
        }

        .spawner-status .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--text-dim);
        }

        .spawner-status .dot.running {
            background: var(--green);
            animation: pulse 2s infinite;
        }

        .spawner-status .dot.paused {
            background: var(--yellow);
        }

        .spawner-status .dot.stopped {
            background: var(--red);
        }

        /* Main Content */
        .main {
            display: flex;
            flex: 1;
            overflow: hidden;
        }

        /* Sidebar - scrollable with collapsible sections */
        .sidebar {
            width: 300px;
            background: var(--bg-card);
            border-right: 1px solid var(--border);
            padding: 1rem;
            overflow-y: auto;
        }

        /* Collapsible section for sidebar */
        .sidebar-section {
            margin-bottom: 0.5rem;
        }

        .sidebar-section summary {
            cursor: pointer;
            padding: 0.5rem;
            background: var(--bg-hover);
            border-radius: 4px;
            font-size: 0.8rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            list-style: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .sidebar-section summary::after {
            content: '▼';
            font-size: 0.6rem;
            transition: transform 0.2s;
        }

        .sidebar-section[open] summary::after {
            transform: rotate(180deg);
        }

        .sidebar-section-content {
            padding: 0.5rem 0;
        }

        /* Identities grid/scroll for many identities */
        #identities {
            max-height: calc(100vh - 400px);
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .identity-card {
            flex-shrink: 0;
        }

        .sidebar h3 {
            color: var(--text-dim);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 1rem;
        }

        .identity-card {
            background: var(--bg-hover);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.5rem;
        }

        .identity-name {
            color: var(--teal);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .identity-stat {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: var(--text-dim);
        }

        .token-count {
            color: var(--yellow);
        }

        /* Log Panel */
        .log-panel {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .log-header {
            padding: 1rem;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .log-filters {
            display: flex;
            gap: 0.5rem;
        }

        .filter-btn {
            background: var(--bg-hover);
            border: 1px solid var(--border);
            color: var(--text-dim);
            padding: 0.4rem 0.8rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
        }

        .filter-btn.active {
            background: var(--teal);
            color: var(--bg-dark);
            border-color: var(--teal);
        }

        .log-container {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            font-size: 0.85rem;
        }

        .log-entry {
            padding: 0.3rem 0;
            border-bottom: 1px solid var(--border);
            display: flex;
            gap: 1rem;
        }

        .log-time {
            color: var(--text-dim);
            min-width: 80px;
        }

        .log-day {
            color: var(--purple);
            min-width: 30px;
        }

        .log-actor {
            color: var(--teal);
            min-width: 100px;
        }

        .log-type {
            min-width: 70px;
            font-weight: 600;
        }

        .log-action {
            color: var(--text-dim);
            min-width: 100px;
        }

        .log-detail {
            flex: 1;
            color: var(--text);
        }

        /* Log type colors */
        .type-TOOL { color: var(--blue); }
        .type-COST, .type-API { color: var(--yellow); }
        .type-SOCIAL, .type-IDENTITY, .type-JOURNAL { color: var(--teal); }
        .type-SAFETY, .type-ERROR { color: var(--red); }
        .type-BUDGET { color: var(--orange); }
        .type-TEST { color: var(--green); }
        .type-SYSTEM { color: var(--purple); }

        /* Budget exceeded / blocked = red */
        .log-entry.danger .log-type,
        .log-entry.danger .log-action {
            color: var(--red) !important;
        }

        /* Footer Stats */
        .footer {
            background: var(--bg-card);
            border-top: 1px solid var(--border);
            padding: 0.5rem 2rem;
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-dim);
        }

        .stat {
            display: flex;
            gap: 0.5rem;
        }

        .stat-value {
            color: var(--text);
        }

        /* Day Vibe Badge */
        .day-vibe {
            background: var(--bg-hover);
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .day-vibe.friday { background: linear-gradient(135deg, #ff6b6b, #feca57); color: #1a1a25; }
        .day-vibe.weekend { background: linear-gradient(135deg, #5f27cd, #00d2d3); }
        .day-vibe.monday { background: linear-gradient(135deg, #2d3436, #636e72); }
        .day-vibe.humpday { background: linear-gradient(135deg, #20bf6b, #26de81); color: #1a1a25; }

        /* Slide-out Panel */
        .slideout-toggle {
            position: fixed;
            right: 0;
            top: 50%;
            transform: translateY(-50%);
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-right: none;
            padding: 1rem 0.5rem;
            cursor: pointer;
            writing-mode: vertical-rl;
            text-orientation: mixed;
            color: var(--text-dim);
            font-size: 0.8rem;
            border-radius: 8px 0 0 8px;
            z-index: 100;
            transition: all 0.2s;
        }

        .slideout-toggle:hover {
            background: var(--bg-hover);
            color: var(--text);
        }

        .slideout-panel {
            position: fixed;
            right: -400px;
            top: 0;
            width: 400px;
            height: 100vh;
            background: var(--bg-card);
            border-left: 1px solid var(--border);
            z-index: 200;
            transition: right 0.3s ease;
            display: flex;
            flex-direction: column;
        }

        .slideout-panel.open {
            right: 0;
        }

        .slideout-header {
            padding: 1rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .slideout-header h3 {
            color: var(--teal);
            margin: 0;
        }

        .slideout-close {
            background: none;
            border: none;
            color: var(--text-dim);
            font-size: 1.5rem;
            cursor: pointer;
        }

        .slideout-content {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
        }

        .completed-request {
            background: var(--bg-hover);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            border-left: 3px solid var(--green);
        }

        .completed-request .request-text {
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }

        .completed-request .request-meta {
            font-size: 0.75rem;
            color: var(--text-dim);
            display: flex;
            justify-content: space-between;
        }

        .slideout-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 150;
            display: none;
        }

        .slideout-overlay.open {
            display: block;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">SWARM CONTROL PANEL</div>
        <div class="day-vibe" id="dayVibe">
            <span id="dayVibeIcon">*</span>
            <span id="dayVibeText">Loading...</span>
        </div>
        <div class="spawner-status">
            <div class="dot" id="spawnerDot"></div>
            <span id="spawnerStatus">GOLDEN PATH</span>
        </div>
        <div class="control-buttons">
            <button class="control-btn start" id="startBtn" onclick="startSpawner()" disabled>QUEUE MODE</button>
            <button class="control-btn pause" id="pauseBtn" onclick="togglePause()" disabled>DISABLED</button>
            <button class="control-btn stop" id="stopBtn" onclick="emergencyStop()" disabled>DISABLED</button>
        </div>
    </div>

    <!-- Slide-out toggle button -->
    <div class="slideout-toggle" onclick="toggleSlideout()">
        Completed Requests
    </div>

    <!-- Slide-out overlay -->
    <div class="slideout-overlay" id="slideoutOverlay" onclick="toggleSlideout()"></div>

    <!-- Slide-out panel -->
    <div class="slideout-panel" id="slideoutPanel">
        <div class="slideout-header">
            <h3>Completed Requests</h3>
            <button class="slideout-close" onclick="toggleSlideout()">&times;</button>
        </div>
        <div class="slideout-content" id="completedRequestsContainer">
            <p style="color: var(--text-dim);">No completed requests yet</p>
        </div>
    </div>

    <div class="main">
        <div class="sidebar">
            <!-- Identities Section - Always visible, scrollable -->
            <h3 style="display: flex; align-items: center; justify-content: space-between;">
                <span>Identities</span>
                <span id="identityCount" style="font-size: 0.7rem; color: var(--text-dim); font-weight: normal;"></span>
            </h3>
            <div id="identities">
                <!-- Populated by JS -->
            </div>

            <!-- Collapsible: Collaboration Request -->
            <details class="sidebar-section" open>
                <summary>
                    Collaboration Request
                    <span id="requestActiveIndicator" style="display: none; font-size: 0.65rem; padding: 0.1rem 0.3rem;
                          background: rgba(76, 175, 80, 0.2); color: var(--green); border-radius: 4px;">
                        ACTIVE
                    </span>
                </summary>
                <div class="sidebar-section-content">
                    <div class="identity-card" style="margin-bottom: 0;">
                        <textarea id="humanRequest"
                            placeholder="What should we work on together?"
                            style="width: 100%; height: 60px; background: var(--bg-dark); border: 1px solid var(--border);
                                   color: var(--text); padding: 0.5rem; border-radius: 4px; font-family: inherit;
                                   font-size: 0.8rem; resize: vertical;"></textarea>
                        <div style="display: flex; gap: 0.3rem; margin-top: 0.3rem;">
                            <button onclick="saveRequest()"
                                style="flex: 1; padding: 0.3rem; background: var(--teal);
                                       border: none; color: var(--bg-dark); border-radius: 4px; cursor: pointer;
                                       font-weight: 600; font-size: 0.75rem;">
                                Update
                            </button>
                            <button onclick="markRequestComplete()"
                                style="padding: 0.3rem 0.5rem; background: var(--green);
                                       border: none; color: var(--bg-dark); border-radius: 4px; cursor: pointer;
                                       font-weight: 600; font-size: 0.75rem;">
                                Done
                            </button>
                        </div>
                        <div id="requestStatus" style="font-size: 0.65rem; color: var(--green); margin-top: 0.2rem; text-align: center;"></div>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Budget & Scaling -->
            <details class="sidebar-section">
                <summary>Budget & Model</summary>
                <div class="sidebar-section-content">
            <div class="identity-card">
                <div class="identity-stat">
                    <span>Daily Cycle Budget</span>
                    <span class="stat-value" id="sessionBudget">$0.05</span>
                </div>
                <div class="identity-stat">
                    <span>Total Spent</span>
                    <span class="stat-value" id="totalSpent">$0.00</span>
                </div>

                <!-- Model Selector with Auto Mode -->
                <div style="margin-top: 1rem; border-top: 1px solid var(--border); padding-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <label style="font-size: 0.8rem; color: var(--text-dim);">Model:</label>
                        <span id="autoModelIndicator" style="font-size: 0.7rem; padding: 0.1rem 0.4rem;
                              background: rgba(76, 175, 80, 0.2); color: var(--green); border-radius: 4px;">
                            AUTO
                        </span>
                    </div>
                    <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-size: 0.8rem; margin-bottom: 0.5rem;">
                        <input type="checkbox" id="overrideModelToggle" onchange="toggleModelOverride()">
                        <span style="color: var(--text-dim);">Override auto-select</span>
                    </label>
                    <select id="modelSelector" onchange="updateModel(this.value)" disabled
                            style="width: 100%; padding: 0.4rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text-dim); border-radius: 4px;
                                   font-size: 0.85rem; cursor: not-allowed; opacity: 0.6;">
                        <option value="auto">Auto (by complexity)</option>
                        <option value="llama-3.1-8b-instant">Llama 3.1 8B (Fast/Simple)</option>
                        <option value="llama-3.3-70b-versatile">Llama 3.3 70B (Standard)</option>
                        <option value="deepseek-r1-distill-llama-70b">DeepSeek R1 70B (Reasoning)</option>
                        <option value="qwen-qwq-32b">Qwen QwQ 32B (Reasoning)</option>
                        <option value="meta-llama/llama-4-maverick-17b-128e-instruct">Llama 4 Maverick (Preview)</option>
                    </select>
                    <p id="modelDescription" style="font-size: 0.65rem; color: var(--green); margin-top: 0.3rem;">
                        Smallest model for each task complexity
                    </p>
                </div>

                <!-- Scaling Mode Toggle -->
                <div style="margin-top: 0.75rem;">
                    <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-size: 0.85rem;">
                        <input type="checkbox" id="autoScaleToggle" onchange="toggleScaleMode()">
                        <span>Auto-scale based on budget</span>
                    </label>
                </div>

                <!-- Manual mode: cycle-per-day slider -->
                <div id="manualScaleControls" style="margin-top: 0.75rem;">
                    <label style="font-size: 0.8rem; color: var(--text-dim);">Daily Cycles: <span id="sessionCount" style="color: var(--teal);">3</span></label>
                    <input type="range" id="sessionSlider" min="1" max="10" value="3"
                           oninput="updateSessionCount(this.value)"
                           style="width: 100%; margin-top: 0.3rem; accent-color: var(--teal);">
                </div>

                <!-- Auto mode: budget input -->
                <div id="autoScaleControls" style="display: none; margin-top: 0.75rem;">
                    <label style="font-size: 0.8rem; color: var(--text-dim);">
                        Budget Limit: $<input type="number" id="budgetLimit" value="1.00"
                               step="0.10" min="0.10" onchange="updateBudgetLimit(this.value)"
                               style="width: 60px; padding: 0.2rem; background: var(--bg-dark);
                                      border: 1px solid var(--border); color: var(--yellow);
                                      border-radius: 4px; font-size: 0.85rem;">
                    </label>
                    <p style="font-size: 0.7rem; color: var(--text-dim); margin-top: 0.3rem;">
                        Cycle workers scale up/down based on remaining budget
                    </p>
                </div>

                <button onclick="saveSpawnerConfig()"
                    style="margin-top: 0.75rem; width: 100%; padding: 0.3rem; background: var(--bg-hover);
                           border: 1px solid var(--border); color: var(--text); border-radius: 4px;
                           cursor: pointer; font-size: 0.75rem;">
                    Save Config
                </button>
            </div>
                </div>
            </details>

            <!-- Collapsible: Messages -->
            <details class="sidebar-section">
                <summary>
                    Messages
                    <span id="messageCount" style="font-size: 0.65rem; color: var(--teal);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div id="messagesContainer" style="max-height: 250px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.75rem;">No messages yet</p>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Chat Rooms -->
            <details class="sidebar-section">
                <summary>
                    Chat Rooms
                    <span id="chatRoomsCount" style="font-size: 0.65rem; color: var(--teal);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div id="chatRoomsContainer" style="max-height: 300px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.75rem;">Loading rooms...</p>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Commons Crucible -->
            <details class="sidebar-section">
                <summary>
                    Commons Crucible
                    <span id="bountyCount" style="font-size: 0.65rem; color: var(--yellow);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div class="identity-card" style="margin-bottom: 0.5rem;">
                        <div style="font-size: 0.65rem; color: var(--text-dim); margin-bottom: 0.3rem;">
                            PVP/coop arena. Slots fill fast; overflow rewards decay sharply.
                        </div>
                        <input type="text" id="bountyTitle" placeholder="Challenge title..."
                            style="width: 100%; padding: 0.25rem; margin-bottom: 0.2rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.8rem;">
                        <textarea id="bountyDesc" placeholder="Objective and success criteria..."
                            style="width: 100%; height: 40px; background: var(--bg-dark); border: 1px solid var(--border);
                                   color: var(--text); padding: 0.25rem; border-radius: 4px; font-size: 0.75rem; resize: none;"></textarea>
                        <div style="display: flex; gap: 0.3rem; margin-top: 0.2rem; align-items: center;">
                            <input type="number" id="bountyReward" placeholder="Tokens" min="10" value="50"
                                style="width: 50px; padding: 0.2rem; background: var(--bg-dark);
                                       border: 1px solid var(--border); color: var(--yellow); border-radius: 4px; font-size: 0.75rem;"
                                title="Token reward">
                            <select id="bountyMode"
                                style="width: 62px; padding: 0.2rem; background: var(--bg-dark);
                                       border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.65rem;"
                                title="Mode">
                                <option value="hybrid" selected>Hybrid</option>
                                <option value="pvp">PVP</option>
                                <option value="coop">Coop</option>
                            </select>
                            <input type="number" id="bountyMaxTeams" placeholder="Guild slots" min="1" max="8" value="2"
                                style="width: 40px; padding: 0.2rem; background: var(--bg-dark);
                                       border: 1px solid var(--border); color: var(--teal); border-radius: 4px; font-size: 0.75rem;"
                                title="Guild slots with full rewards">
                            <button onclick="createBounty()"
                                style="flex: 1; padding: 0.25rem; background: var(--yellow); border: none;
                                       color: var(--bg-dark); border-radius: 4px; cursor: pointer; font-weight: 600; font-size: 0.7rem;">
                                Post
                            </button>
                        </div>
                    </div>
                    <div id="bountiesContainer" style="max-height: 200px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.7rem;">No active bounties</p>
                    </div>
                </div>
            </details>
        </div>

        <div class="log-panel">
            <div class="log-header">
                <span>Action Log</span>
                <div class="log-filters">
                    <button class="filter-btn active" data-filter="all">All</button>
                    <button class="filter-btn" data-filter="TOOL">Tools</button>
                    <button class="filter-btn" data-filter="API">API</button>
                    <button class="filter-btn" data-filter="SAFETY">Safety</button>
                    <button class="filter-btn" data-filter="SOCIAL">Social</button>
                    <button class="filter-btn" data-filter="IDENTITY">Identity</button>
                </div>
            </div>
            <div class="log-container" id="logContainer">
                <div class="log-entry">
                    <span class="log-time">--:--:--</span>
                    <span class="log-day">---</span>
                    <span class="log-actor">SYSTEM</span>
                    <span class="log-type type-SYSTEM">SYSTEM</span>
                    <span class="log-action">waiting</span>
                    <span class="log-detail">Waiting for log entries...</span>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div class="stat">
            <span>Entries:</span>
            <span class="stat-value" id="entryCount">0</span>
        </div>
        <div class="stat">
            <span>Connected:</span>
            <span class="stat-value" id="connectedTime">0s</span>
        </div>
        <div class="stat">
            <span>Last Update:</span>
            <span class="stat-value" id="lastUpdate">--:--:--</span>
        </div>
    </div>

    <script>
        const socket = io();
        let entryCount = 0;
        let isStopped = false;
        let connectedAt = Date.now();
        let currentFilter = 'all';

        // Update connected time
        setInterval(() => {
            const secs = Math.floor((Date.now() - connectedAt) / 1000);
            document.getElementById('connectedTime').textContent = `${secs}s`;
        }, 1000);

        // Socket events
        socket.on('connect', () => {
            console.log('Connected to control panel');
            loadSpawnerStatus();
        });

        socket.on('disconnect', () => {
            console.log('Disconnected');
            const dot = document.getElementById('spawnerDot');
            if (dot) dot.classList.add('stopped');
        });

        socket.on('log_entry', (entry) => {
            addLogEntry(entry);
        });

        socket.on('identities', (data) => {
            updateIdentities(data);
        });

        socket.on('spawner_started', (data) => {
            spawnerState = { running: true, paused: false, pid: data.pid };
            updateSpawnerUI();
        });

        socket.on('spawner_paused', () => {
            spawnerState.paused = true;
            updateSpawnerUI();
        });

        socket.on('spawner_resumed', () => {
            spawnerState.paused = false;
            updateSpawnerUI();
        });

        socket.on('spawner_killed', () => {
            spawnerState = { running: false, paused: false, pid: null };
            updateSpawnerUI();
        });

        function addLogEntry(entry) {
            const container = document.getElementById('logContainer');
            const div = document.createElement('div');
            div.className = 'log-entry';
            div.dataset.type = entry.action_type;

            // Check for danger conditions
            if (entry.action_type === 'SAFETY' && entry.action.includes('BLOCKED')) {
                div.classList.add('danger');
            }
            if (entry.action_type === 'BUDGET' && entry.action.includes('EXCEEDED')) {
                div.classList.add('danger');
            }
            if (entry.action_type === 'ERROR') {
                div.classList.add('danger');
            }

            // Parse timestamp
            let timeStr = '--:--:--';
            let dayStr = '---';
            if (entry.timestamp) {
                const dt = new Date(entry.timestamp);
                timeStr = dt.toTimeString().split(' ')[0];
                dayStr = dt.toLocaleDateString('en-US', { weekday: 'short' });
            }

            // Make file paths clickable in detail
            const linkedDetail = linkifyFilePaths(entry.detail || '');

            div.innerHTML = `
                <span class="log-time">${timeStr}</span>
                <span class="log-day">${dayStr}</span>
                <span class="log-actor">${entry.actor || 'UNKNOWN'}</span>
                <span class="log-type type-${entry.action_type}">${entry.action_type}</span>
                <span class="log-action">${entry.action}</span>
                <span class="log-detail">${linkedDetail}</span>
            `;

            // Apply filter
            if (currentFilter !== 'all' && entry.action_type !== currentFilter) {
                div.style.display = 'none';
            }

            container.appendChild(div);
            container.scrollTop = container.scrollHeight;

            entryCount++;
            document.getElementById('entryCount').textContent = entryCount;
            document.getElementById('lastUpdate').textContent = timeStr;
        }

        // Make file paths clickable in log entries
        function linkifyFilePaths(text) {
            // Match common file path patterns
            // Patterns: path/to/file.ext, ./file.ext, file.py (+12 lines), etc.
            const pathRegex = /([a-zA-Z0-9_\\-\\.\\/\\\\]+\\.(py|js|ts|json|md|html|css|yaml|yml|txt|log|sh|sql))/g;
            return text.replace(pathRegex, (match) => {
                // Clean up the path (remove trailing info like " (+12 lines)")
                const cleanPath = match.split(' ')[0];
                return `<a href="#" onclick="viewArtifact('${cleanPath}'); return false;" style="color: var(--teal); text-decoration: underline; cursor: pointer;">${match}</a>`;
            });
        }

        // View artifact in modal
        function viewArtifact(path) {
            fetch('/api/artifact/view?path=' + encodeURIComponent(path))
                .then(r => r.json())
                .then(data => {
                    if (!data.success) {
                        alert('Error: ' + data.error);
                        return;
                    }

                    const modal = document.createElement('div');
                    modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); z-index: 1000; display: flex; flex-direction: column; padding: 1rem;';
                    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

                    // Escape HTML in content
                    const escapeHtml = (text) => {
                        const div = document.createElement('div');
                        div.textContent = text;
                        return div.innerHTML;
                    };

                    modal.innerHTML = `
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 1rem; background: var(--bg-card); border-radius: 8px 8px 0 0;">
                            <div>
                                <span style="color: var(--teal); font-weight: bold;">${data.filename}</span>
                                <span style="color: var(--text-dim); font-size: 0.8rem; margin-left: 1rem;">${data.path}</span>
                                <span style="color: var(--text-dim); font-size: 0.75rem; margin-left: 1rem;">${(data.size / 1024).toFixed(1)}KB</span>
                            </div>
                            <button onclick="this.closest('[style*=position]').remove()" style="background: var(--red); border: none; color: white; padding: 0.3rem 0.8rem; border-radius: 4px; cursor: pointer;">Close</button>
                        </div>
                        <pre style="flex: 1; margin: 0; padding: 1rem; background: var(--bg-dark); overflow: auto; border-radius: 0 0 8px 8px; font-size: 0.85rem; line-height: 1.4;"><code>${escapeHtml(data.content)}</code></pre>
                    `;

                    document.body.appendChild(modal);
                });
        }

        function updateIdentities(identities) {
            const container = document.getElementById('identities');
            const countEl = document.getElementById('identityCount');
            if (countEl) countEl.textContent = `(${identities.length})`;

            // Sort by level (highest first), then by sessions
            identities.sort((a, b) => {
                const levelDiff = (b.level || 1) - (a.level || 1);
                if (levelDiff !== 0) return levelDiff;
                return (b.sessions || 0) - (a.sessions || 0);
            });

            container.innerHTML = identities.map(id => `
                <div class="identity-card" style="cursor: pointer;" onclick="showProfile('${id.id}')">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div class="identity-name">${id.name}</div>
                        <span style="font-size: 0.7rem; color: var(--yellow); background: rgba(255,193,7,0.15);
                                     padding: 0.15rem 0.4rem; border-radius: 4px; font-weight: 600;">
                            Lv.${id.level || 1}
                        </span>
                    </div>
                    ${id.profile_display ? `<div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.3rem; font-style: italic;">${id.profile_display.substring(0, 50)}${id.profile_display.length > 50 ? '...' : ''}</div>` : ''}
                    ${id.traits && id.traits.length ? `<div style="font-size: 0.7rem; color: var(--purple); margin-bottom: 0.3rem;">${id.traits.slice(0,3).join(' | ')}</div>` : ''}
                    <div class="identity-stat">
                        <span>Tokens</span>
                        <span class="token-count">${id.tokens}</span>
                    </div>
                    <div class="identity-stat">
                        <span>Sessions</span>
                        <span>${id.sessions}</span>
                    </div>
                    <div class="identity-stat">
                        <span>Respec Cost</span>
                        <span style="color: var(--orange);">${id.respec_cost || 10}</span>
                    </div>
                </div>
            `).join('');
        }

        function showProfile(identityId) {
            fetch('/api/identity/' + identityId + '/profile')
                .then(r => r.json())
                .then(data => {
                    if (data.error) {
                        alert('Error: ' + data.error);
                        return;
                    }

                    const profile = data.profile || {};
                    const core = data.core_summary || {};
                    const mutable = data.mutable || {};

                    let content = `<h2 style="color: var(--teal); margin-bottom: 0.5rem;">${data.name}</h2>`;
                    content += `<div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 1rem;">Created: ${new Date(data.created_at).toLocaleDateString()}</div>`;

                    // Custom profile display
                    if (profile.custom_html) {
                        content += `<div style="background: var(--bg-dark); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                            <style scoped>${profile.custom_css || ''}</style>
                            ${profile.custom_html}
                        </div>`;
                    } else if (profile.display) {
                        content += `<div style="background: var(--bg-dark); padding: 1rem; border-radius: 8px; margin-bottom: 1rem; font-style: italic;">${profile.display}</div>`;
                    }

                    // Identity statement
                    if (core.identity_statement) {
                        content += `<p style="font-size: 1.1rem; margin-bottom: 1rem; border-left: 3px solid var(--teal); padding-left: 1rem;">"${core.identity_statement}"</p>`;
                    }

                    // Stats bar (row 1)
                    content += `<div style="display: flex; gap: 1rem; margin-bottom: 0.5rem; padding: 0.75rem; background: var(--bg-dark); border-radius: 8px;">
                        <div style="text-align: center; flex: 1;"><div style="font-size: 1.5rem; color: var(--yellow);">${data.level || 1}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Level</div></div>
                        <div style="text-align: center; flex: 1;"><div style="font-size: 1.5rem; color: var(--teal);">${data.sessions}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Cycles</div></div>
                        <div style="text-align: center; flex: 1;"><div style="font-size: 1.5rem; color: var(--green);">${data.tasks_completed}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Tasks</div></div>
                        <div style="text-align: center; flex: 1;"><div style="font-size: 1.5rem; color: ${data.task_success_rate >= 80 ? 'var(--green)' : data.task_success_rate >= 50 ? 'var(--yellow)' : 'var(--red)'}">${data.task_success_rate}%</div><div style="font-size: 0.7rem; color: var(--text-dim);">Success</div></div>
                    </div>`;
                    // Stats bar (row 2 - respec info)
                    content += `<div style="display: flex; gap: 1rem; margin-bottom: 1rem; padding: 0.5rem 0.75rem; background: var(--bg-dark); border-radius: 8px; font-size: 0.8rem;">
                        <div style="flex: 1; color: var(--text-dim);">Respec Cost: <span style="color: var(--orange); font-weight: 600;">${data.respec_cost || 10} tokens</span></div>
                        <div style="color: var(--text-dim); font-size: 0.7rem;">Level formula: sqrt(cycles) | Respec: 10 + (cycles × 3)</div>
                    </div>`;

                    // Core traits and values
                    if (core.traits && core.traits.length) {
                        content += `<div style="margin-bottom: 0.5rem;"><span style="color: var(--text-dim); font-size: 0.8rem;">Traits:</span><div style="margin-top: 0.3rem;">${core.traits.map(t => `<span style="background: var(--purple); color: white; padding: 0.2rem 0.5rem; border-radius: 4px; margin-right: 0.3rem; margin-bottom: 0.3rem; display: inline-block; font-size: 0.8rem;">${t}</span>`).join('')}</div></div>`;
                    }

                    if (core.values && core.values.length) {
                        content += `<div style="margin-bottom: 0.5rem;"><span style="color: var(--text-dim); font-size: 0.8rem;">Values:</span><div style="margin-top: 0.3rem;">${core.values.map(v => `<span style="background: var(--teal); color: var(--bg-dark); padding: 0.2rem 0.5rem; border-radius: 4px; margin-right: 0.3rem; margin-bottom: 0.3rem; display: inline-block; font-size: 0.8rem;">${v}</span>`).join('')}</div></div>`;
                    }

                    // Current interests/mood
                    if (mutable.current_interests && mutable.current_interests.length) {
                        content += `<div style="margin-bottom: 0.5rem; font-size: 0.85rem;"><span style="color: var(--text-dim);">Interests:</span> ${mutable.current_interests.join(', ')}</div>`;
                    }
                    if (mutable.current_mood) {
                        content += `<div style="margin-bottom: 0.5rem; font-size: 0.85rem;"><span style="color: var(--text-dim);">Mood:</span> ${mutable.current_mood}</div>`;
                    }

                    // Recent memories
                    if (data.recent_memories && data.recent_memories.length) {
                        content += `<details style="margin-top: 1rem;"><summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">Recent Memories (${data.recent_memories.length})</summary>
                            <div style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem; max-height: 150px; overflow-y: auto;">
                                ${data.recent_memories.map(m => `<div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.3rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem;">${m}</div>`).join('')}
                            </div>
                        </details>`;
                    }

                    // Journals
                    if (data.journals && data.journals.length) {
                        content += `<details style="margin-top: 0.5rem;"><summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">Journals (${data.journals.length})</summary>
                            <div style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem; max-height: 200px; overflow-y: auto;">
                                ${data.journals.map(j => `<div style="margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);">
                                    <div style="font-size: 0.7rem; color: var(--purple);">${j.filename}</div>
                                    <div style="font-size: 0.75rem; color: var(--text); white-space: pre-wrap;">${j.preview}</div>
                                </div>`).join('')}
                            </div>
                        </details>`;
                    }

                    // Recent actions
                    if (data.recent_actions && data.recent_actions.length) {
                        content += `<details style="margin-top: 0.5rem;"><summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">Recent Actions (${data.recent_actions.length})</summary>
                            <div style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem; max-height: 200px; overflow-y: auto;">
                                ${data.recent_actions.map(a => `<div style="font-size: 0.75rem; margin-bottom: 0.3rem; padding-bottom: 0.3rem; border-bottom: 1px solid var(--border);">
                                    <span style="color: var(--text-dim);">${new Date(a.timestamp).toLocaleTimeString()}</span>
                                    <span style="color: var(--purple); margin-left: 0.5rem;">${a.type}</span>
                                    <span style="color: var(--text); margin-left: 0.5rem;">${a.action}</span>
                                    <span style="color: var(--text-dim); margin-left: 0.5rem;">${linkifyFilePaths(a.detail || '')}</span>
                                </div>`).join('')}
                            </div>
                        </details>`;
                    }

                    // Expertise
                    if (data.expertise && Object.keys(data.expertise).length) {
                        const expertiseItems = Object.entries(data.expertise).sort((a, b) => b[1] - a[1]).slice(0, 5);
                        content += `<details style="margin-top: 0.5rem;"><summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">Expertise</summary>
                            <div style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem;">
                                ${expertiseItems.map(([domain, count]) => `<div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 0.2rem; padding-bottom: 0.2rem; border-bottom: 1px solid var(--border);">
                                    <span>${domain}</span><span style="color: var(--yellow);">${count}</span>
                                </div>`).join('')}
                            </div>
                        </details>`;
                    }

                    // Chat history (collapsible, interactive)
                    if (data.chat_history && data.chat_history.length) {
                        content += `<details style="margin-top: 0.5rem;">
                            <summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">
                                Chat History (${data.chat_history.length})
                            </summary>
                            <div id="chatHistoryContainer" style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem; max-height: 300px; overflow-y: auto;">
                                ${data.chat_history.map(c => `
                                    <div style="margin-bottom: 0.75rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border);">
                                        <div style="background: var(--bg-hover); padding: 0.5rem; border-radius: 8px; margin-bottom: 0.5rem;">
                                            <div style="font-size: 0.7rem; color: var(--teal); margin-bottom: 0.3rem;">
                                                ${data.name} - ${c.sent_at ? new Date(c.sent_at).toLocaleString() : 'Unknown time'}
                                            </div>
                                            <div style="font-size: 0.85rem;">${c.content || ''}</div>
                                        </div>
                                        ${c.response ? `
                                            <div style="background: rgba(187, 134, 252, 0.1); padding: 0.5rem; border-radius: 8px; margin-left: 1rem;">
                                                <div style="font-size: 0.7rem; color: var(--purple); margin-bottom: 0.3rem;">
                                                    You - ${c.responded_at ? new Date(c.responded_at).toLocaleString() : ''}
                                                </div>
                                                <div style="font-size: 0.85rem;">${c.response}</div>
                                            </div>
                                        ` : `
                                            <div style="margin-left: 1rem;">
                                                <input type="text" id="profile_reply_${c.id}" placeholder="Reply..."
                                                       style="width: calc(100% - 60px); padding: 0.3rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.8rem;">
                                                <button onclick="replyToMessageFromProfile('${c.id}', '${data.identity_id}')"
                                                        style="padding: 0.3rem 0.5rem; background: var(--teal); border: none; color: var(--bg-dark); border-radius: 4px; cursor: pointer; font-size: 0.8rem;">
                                                    Send
                                                </button>
                                            </div>
                                        `}
                                    </div>
                                `).join('')}
                            </div>
                        </details>`;
                    }

                    // Show in modal
                    const modal = document.createElement('div');
                    modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; justify-content: center; align-items: center; padding: 2rem;';
                    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

                    const modalContent = document.createElement('div');
                    modalContent.style.cssText = 'background: var(--bg-card); padding: 2rem; border-radius: 12px; max-width: 600px; width: 100%; max-height: 85vh; overflow-y: auto;';
                    modalContent.innerHTML = content + '<button onclick="this.parentElement.parentElement.remove()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: var(--border); border: none; color: var(--text); border-radius: 4px; cursor: pointer; width: 100%;">Close</button>';

                    modal.appendChild(modalContent);
                    document.body.appendChild(modal);
                });
        }

        // Spawner state
        let spawnerState = { running: false, paused: false, pid: null };
        const GOLDEN_PATH_NOTICE = 'Golden path enforced: run tasks via queue + worker.py only.';

        function showGoldenPathOnlyNotice() {
            alert(GOLDEN_PATH_NOTICE);
        }

        function updateSpawnerUI() {
            const dot = document.getElementById('spawnerDot');
            const status = document.getElementById('spawnerStatus');
            const startBtn = document.getElementById('startBtn');
            const pauseBtn = document.getElementById('pauseBtn');
            const stopBtn = document.getElementById('stopBtn');

            dot.className = 'dot';
            dot.classList.add('running');
            status.textContent = 'GOLDEN PATH';
            startBtn.disabled = true;
            pauseBtn.disabled = true;
            stopBtn.disabled = true;
            pauseBtn.classList.remove('paused');
        }

        function startSpawner() {
            showGoldenPathOnlyNotice();
            return;
            const config = {
                sessions: parseInt(document.getElementById('sessionSlider').value),
                auto_scale: document.getElementById('autoScaleToggle').checked,
                budget_limit: parseFloat(document.getElementById('budgetLimit').value)
            };
            fetch('/api/spawner/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(config)
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    spawnerState = { running: true, paused: false, pid: data.pid };
                    updateSpawnerUI();
                } else {
                    alert('Failed to start: ' + (data.error || 'Unknown error'));
                }
            });
        }

        function togglePause() {
            showGoldenPathOnlyNotice();
            return;
            const endpoint = spawnerState.paused ? '/api/spawner/resume' : '/api/spawner/pause';
            fetch(endpoint, { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        spawnerState.paused = !spawnerState.paused;
                        updateSpawnerUI();
                    }
                });
        }

        function emergencyStop() {
            showGoldenPathOnlyNotice();
            return;
            if (!confirm('EMERGENCY STOP: This will kill the spawner process immediately. Continue?')) return;
            fetch('/api/spawner/kill', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    spawnerState = { running: false, paused: false, pid: null };
                    updateSpawnerUI();
                    if (data.success) {
                        alert('Spawner stopped.');
                    }
                });
        }

        // Scaling controls
        function toggleScaleMode() {
            const autoScale = document.getElementById('autoScaleToggle').checked;
            document.getElementById('manualScaleControls').style.display = autoScale ? 'none' : 'block';
            document.getElementById('autoScaleControls').style.display = autoScale ? 'block' : 'none';
        }

        function updateSessionCount(value) {
            document.getElementById('sessionCount').textContent = value;
        }

        function updateBudgetLimit(value) {
            // Just updates the local value, saved via saveSpawnerConfig
        }

        function updateModel(model) {
            // Model selection - saved with config
            updateModelDescription(model);
        }

        function toggleModelOverride() {
            const override = document.getElementById('overrideModelToggle').checked;
            const selector = document.getElementById('modelSelector');
            const indicator = document.getElementById('autoModelIndicator');
            const description = document.getElementById('modelDescription');

            if (override) {
                selector.disabled = false;
                selector.style.cursor = 'pointer';
                selector.style.opacity = '1';
                selector.style.color = 'var(--teal)';
                indicator.style.display = 'none';
                updateModelDescription(selector.value);
            } else {
                selector.disabled = true;
                selector.style.cursor = 'not-allowed';
                selector.style.opacity = '0.6';
                selector.style.color = 'var(--text-dim)';
                selector.value = 'auto';
                indicator.style.display = 'inline';
                description.textContent = 'Smallest model for each task complexity';
                description.style.color = 'var(--green)';
            }
        }

        function updateModelDescription(model) {
            const description = document.getElementById('modelDescription');
            const descriptions = {
                'auto': 'Smallest model for each task complexity',
                'llama-3.1-8b-instant': 'Fast & cheap - simple tasks, quick edits',
                'llama-3.3-70b-versatile': 'Standard - general purpose, balanced',
                'deepseek-r1-distill-llama-70b': 'Reasoning - complex logic, math, planning',
                'qwen-qwq-32b': 'Reasoning - analytical tasks, problem solving',
                'meta-llama/llama-4-maverick-17b-128e-instruct': 'Preview - experimental features'
            };
            description.textContent = descriptions[model] || 'Custom model';
            description.style.color = model === 'auto' ? 'var(--green)' : 'var(--text-dim)';
        }

        function saveSpawnerConfig() {
            showGoldenPathOnlyNotice();
            return;
            const override = document.getElementById('overrideModelToggle').checked;
            const config = {
                sessions: parseInt(document.getElementById('sessionSlider').value),
                auto_scale: document.getElementById('autoScaleToggle').checked,
                budget_limit: parseFloat(document.getElementById('budgetLimit').value),
                model: document.getElementById('modelSelector').value,
                auto_model: !override  // Default is auto, override disables it
            };
            fetch('/api/spawner/config', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(config)
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    const modeText = config.auto_model ? 'Auto mode enabled.' : `Model set to ${config.model}.`;
                    alert('Config saved! ' + modeText + ' Changes apply on next cycle.');
                }
            });
        }

        function loadSpawnerStatus() {
            fetch('/api/spawner/status')
                .then(r => r.json())
                .then(data => {
                    spawnerState = {
                        running: data.running || false,
                        paused: data.paused || false,
                        pid: data.pid || null
                    };
                    updateSpawnerUI();

                    // Load config if available
                    if (data.config) {
                        document.getElementById('sessionSlider').value = data.config.sessions || 3;
                        document.getElementById('sessionCount').textContent = data.config.sessions || 3;
                        document.getElementById('autoScaleToggle').checked = data.config.auto_scale || false;
                        document.getElementById('budgetLimit').value = data.config.budget_limit || 1.00;

                        // Model auto-select (default is auto)
                        const autoModel = data.config.auto_model !== false;  // Default true
                        document.getElementById('overrideModelToggle').checked = !autoModel;
                        if (!autoModel && data.config.model) {
                            document.getElementById('modelSelector').value = data.config.model;
                        }
                        toggleModelOverride();
                        toggleScaleMode();
                    }
                });
        }

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;

                document.querySelectorAll('.log-entry').forEach(entry => {
                    if (currentFilter === 'all' || entry.dataset.type === currentFilter) {
                        entry.style.display = '';
                    } else {
                        entry.style.display = 'none';
                    }
                });
            });
        });

        // Update active indicator based on request content
        function updateRequestIndicator(hasContent) {
            const indicator = document.getElementById('requestActiveIndicator');
            if (indicator) {
                indicator.style.display = hasContent ? 'inline' : 'none';
            }
        }

        // Save human request
        function saveRequest() {
            const request = document.getElementById('humanRequest').value;
            fetch('/api/human_request', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({request: request})
            })
            .then(r => r.json())
            .then(data => {
                const status = document.getElementById('requestStatus');
                status.textContent = 'Saved!';
                updateRequestIndicator(request.trim().length > 0);
                setTimeout(() => status.textContent = '', 2000);
            });
        }

        // Load human request
        function loadRequest() {
            fetch('/api/human_request')
                .then(r => r.json())
                .then(data => {
                    const request = data.request || '';
                    document.getElementById('humanRequest').value = request;
                    updateRequestIndicator(request.trim().length > 0);
                });
        }

        // Track message count to avoid unnecessary refreshes
        let lastMessageCount = 0;
        let lastMessageIds = new Set();

        // Load and display messages from swarm
        function loadMessages(force = false) {
            fetch('/api/messages')
                .then(r => r.json())
                .then(messages => {
                    const container = document.getElementById('messagesContainer');
                    const countEl = document.getElementById('messageCount');

                    // Update count in header
                    const unread = messages.filter(m => !m.response).length;
                    if (countEl) countEl.textContent = unread > 0 ? `(${unread} unread)` : messages.length > 0 ? `(${messages.length})` : '';

                    // Check if anything changed - don't refresh if user might be typing
                    const newIds = new Set(messages.map(m => m.id));
                    const hasNewMessages = messages.some(m => !lastMessageIds.has(m.id));
                    const hasNewResponses = messages.some(m => m.response && !document.querySelector(`[data-responded="${m.id}"]`));

                    if (!force && !hasNewMessages && !hasNewResponses && messages.length === lastMessageCount) {
                        return; // No changes, don't wipe the input fields
                    }

                    lastMessageCount = messages.length;
                    lastMessageIds = newIds;

                    if (messages.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem;">No messages yet</p>';
                        return;
                    }

                    container.innerHTML = messages.map(msg => {
                        const hasResponse = msg.response;
                        const msgType = msg.type || 'message';
                        const typeColors = {
                            'question': 'var(--yellow)',
                            'greeting': 'var(--teal)',
                            'idea': 'var(--purple)',
                            'concern': 'var(--orange)'
                        };
                        const typeColor = typeColors[msgType] || 'var(--text-dim)';

                        return `
                            <div class="identity-card" style="margin-bottom: 0.5rem; border-left: 3px solid ${typeColor};">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                                    <span style="color: var(--teal); font-weight: 600;">${msg.from_name || 'Unknown'}</span>
                                    <span style="color: var(--text-dim); font-size: 0.7rem;">${msg.type || 'msg'}</span>
                                </div>
                                <p style="font-size: 0.85rem; margin-bottom: 0.5rem;">${msg.content}</p>
                                ${hasResponse ?
                                    `<div style="background: var(--bg-dark); padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                                        <span style="color: var(--green); font-size: 0.75rem;">Your reply:</span>
                                        <p style="font-size: 0.8rem; margin-top: 0.2rem;">${msg.response.response}</p>
                                    </div>` :
                                    `<div style="margin-top: 0.5rem;">
                                        <input type="text" id="reply_${msg.id}" placeholder="Reply..."
                                            style="width: 100%; padding: 0.3rem; background: var(--bg-dark);
                                                   border: 1px solid var(--border); color: var(--text);
                                                   border-radius: 4px; font-size: 0.8rem;">
                                        <button onclick="sendReply('${msg.id}')"
                                            style="margin-top: 0.3rem; padding: 0.2rem 0.5rem; background: var(--teal);
                                                   border: none; color: var(--bg-dark); border-radius: 4px;
                                                   cursor: pointer; font-size: 0.75rem;">Send</button>
                                    </div>`
                                }
                            </div>
                        `;
                    }).join('');
                });
        }

        function sendReply(messageId) {
            const input = document.getElementById('reply_' + messageId);
            const response = input.value.trim();
            if (!response) return;

            fetch('/api/messages/respond', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message_id: messageId, response: response})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    loadMessages();  // Refresh to show response
                }
            });
        }

        function replyToMessageFromProfile(messageId, identityId) {
            const input = document.getElementById('profile_reply_' + messageId);
            const response = input.value.trim();
            if (!response) return;

            fetch('/api/messages/respond', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message_id: messageId, response: response})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    // Refresh profile modal
                    document.querySelector('[style*="position: fixed"]').remove();
                    showProfile(identityId);
                }
            });
        }

        // Refresh messages periodically
        setInterval(loadMessages, 5000);

        // Day vibe setup
        function setupDayVibe() {
            const now = new Date();
            const day = now.getDay(); // 0=Sun, 1=Mon, ..., 5=Fri, 6=Sat
            const hour = now.getHours();
            const vibeEl = document.getElementById('dayVibe');
            const iconEl = document.getElementById('dayVibeIcon');
            const textEl = document.getElementById('dayVibeText');

            const vibes = {
                0: { class: 'weekend', icon: '~', text: 'Sunday Vibes' },
                1: { class: 'monday', icon: '>', text: 'Monday Mode' },
                2: { class: '', icon: '*', text: 'Tuesday' },
                3: { class: 'humpday', icon: '^', text: 'Hump Day!' },
                4: { class: '', icon: '*', text: 'Thursday' },
                5: { class: 'friday', icon: '!', text: 'TGIF!' },
                6: { class: 'weekend', icon: '~', text: 'Weekend Mode' }
            };

            // Special time-based overrides
            let vibe = vibes[day];
            if (day === 5 && hour >= 16) {
                vibe = { class: 'friday', icon: '!', text: 'TGIF - Almost there!' };
            } else if (day === 5 && hour < 12) {
                vibe = { class: 'friday', icon: '!', text: 'Friday Morning!' };
            } else if (day === 1 && hour < 10) {
                vibe = { class: 'monday', icon: '>', text: 'Monday Sprint' };
            } else if ((day === 0 || day === 6) && hour >= 22) {
                vibe = { class: 'weekend', icon: '~', text: 'Weekend Winding Down' };
            }

            vibeEl.className = 'day-vibe ' + vibe.class;
            iconEl.textContent = vibe.icon;
            textEl.textContent = vibe.text;
        }

        // Slideout panel
        function toggleSlideout() {
            const panel = document.getElementById('slideoutPanel');
            const overlay = document.getElementById('slideoutOverlay');
            const isOpen = panel.classList.contains('open');

            if (isOpen) {
                panel.classList.remove('open');
                overlay.classList.remove('open');
            } else {
                panel.classList.add('open');
                overlay.classList.add('open');
                loadCompletedRequests();
            }
        }

        function loadCompletedRequests() {
            fetch('/api/completed_requests')
                .then(r => r.json())
                .then(requests => {
                    const container = document.getElementById('completedRequestsContainer');
                    if (requests.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim);">No completed requests yet.</p><p style="color: var(--text-dim); font-size: 0.8rem; margin-top: 0.5rem;">When you mark a collaboration request as done, it will appear here.</p>';
                        return;
                    }

                    container.innerHTML = requests.map(req => `
                        <div class="completed-request">
                            <div class="request-text">${req.request}</div>
                            <div class="request-meta">
                                <span>Completed: ${new Date(req.completed_at).toLocaleDateString()}</span>
                                <span>${req.duration || ''}</span>
                            </div>
                        </div>
                    `).join('');
                });
        }

        function markRequestComplete() {
            const request = document.getElementById('humanRequest').value.trim();
            if (!request) return;

            if (confirm('Mark this request as completed?\\n\\n"' + request.substring(0, 100) + '..."')) {
                fetch('/api/completed_requests', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({request: request})
                })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('humanRequest').value = '';
                        saveRequest();
                        const status = document.getElementById('requestStatus');
                        status.textContent = 'Marked complete!';
                        status.style.color = 'var(--green)';
                        setTimeout(() => {
                            status.textContent = '';
                            status.style.color = '';
                        }, 3000);
                    }
                });
            }
        }

        // Crucible functions
        function createBounty() {
            const title = document.getElementById('bountyTitle').value.trim();
            const description = document.getElementById('bountyDesc').value.trim();
            const reward = parseInt(document.getElementById('bountyReward').value) || 50;
            const maxTeams = parseInt(document.getElementById('bountyMaxTeams').value) || 2;
            const mode = document.getElementById('bountyMode').value || 'hybrid';

            if (!title) {
                alert('Please enter a bounty title');
                return;
            }

            fetch('/api/bounties', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    title,
                    description,
                    reward,
                    max_teams: maxTeams,
                    slots: maxTeams,
                    game_mode: mode
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('bountyTitle').value = '';
                    document.getElementById('bountyDesc').value = '';
                    document.getElementById('bountyReward').value = '50';
                    document.getElementById('bountyMaxTeams').value = '2';
                    document.getElementById('bountyMode').value = 'hybrid';
                    loadBounties();
                }
            });
        }

        function loadBounties() {
            fetch('/api/bounties')
                .then(r => r.json())
                .then(bounties => {
                    const container = document.getElementById('bountiesContainer');
                    const countEl = document.getElementById('bountyCount');
                    if (countEl) countEl.textContent = bounties.length > 0 ? `(${bounties.length})` : '';

                    if (bounties.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.7rem;">No active Crucible matches</p>';
                        return;
                    }

                    container.innerHTML = bounties.map(b => {
                        const statusColors = {
                            'open': 'var(--yellow)',
                            'claimed': 'var(--teal)',
                            'completed': 'var(--green)'
                        };
                        const borderColor = statusColors[b.status] || 'var(--border)';
                        const teams = b.teams || [];
                        const teamCount = teams.length;
                        const slots = b.slots || b.max_teams || 1;
                        const overflow = Math.max(0, teamCount - slots);
                        const mode = (b.game_mode || 'hybrid').toUpperCase();
                        const gameName = b.game_name || 'Commons Crucible';
                        const cost = b.cost_tracking || {};
                        const apiCost = cost.api_cost ? `$${cost.api_cost.toFixed(3)}` : '';
                        const sessions = cost.sessions_used || 0;

                        // Build guild submissions display
                        const teamsHtml = teams.length > 0 ? `
                            <div style="margin-top: 0.4rem; padding-top: 0.4rem; border-top: 1px solid var(--border);">
                                <div style="font-size: 0.65rem; color: var(--text-dim); margin-bottom: 0.2rem;">Guild submissions:</div>
                                ${teams.map((t, i) => `
                                    <div style="font-size: 0.7rem; padding: 0.2rem 0; display: flex; justify-content: space-between;">
                                        <span style="color: var(--teal);">${t.identity_name}</span>
                                        <span style="color: var(--text-dim);">${new Date(t.submitted_at).toLocaleDateString()}</span>
                                    </div>
                                `).join('')}
                            </div>
                        ` : '';

                        return `
                            <div class="identity-card" style="margin-bottom: 0.4rem; padding: 0.6rem; border-left: 3px solid ${borderColor};">
                                <div style="display: flex; justify-content: space-between; align-items: start;">
                                    <div style="flex: 1;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: var(--text);">${b.title}</div>
                                        <div style="font-size: 0.65rem; color: var(--text-dim); margin-top: 0.15rem;">
                                            ${gameName} | ${mode} | ${b.status.toUpperCase()}
                                            ${slots > 0 ? ` | Guild slots: ${overflow > 0 ? `${slots} (+${overflow} overflow)` : `${teamCount}/${slots}`}` : ''}
                                        </div>
                                        ${apiCost || sessions ? `
                                            <div style="font-size: 0.6rem; color: var(--purple); margin-top: 0.15rem;">
                                                ${apiCost ? `Cost: ${apiCost}` : ''}${apiCost && sessions ? ' | ' : ''}${sessions ? `Sessions: ${sessions}` : ''}
                                            </div>
                                        ` : ''}
                                    </div>
                                    <div style="color: var(--yellow); font-weight: bold; font-size: 0.85rem;">${b.reward}</div>
                                </div>
                                ${teamsHtml}
                                <div style="display: flex; gap: 0.3rem; margin-top: 0.4rem;">
                                    ${b.status === 'claimed' || (b.status === 'open' && teamCount > 0) ? `
                                        <button onclick="showCompleteBountyModal('${b.id}', ${b.reward}, ${teamCount})"
                                            style="flex: 1; padding: 0.2rem; background: var(--green);
                                                   border: none; color: var(--bg-dark); border-radius: 4px;
                                                   cursor: pointer; font-size: 0.65rem;">
                                            Complete
                                        </button>
                                    ` : ''}
                                    ${teamCount > 0 ? `
                                        <button onclick="viewBountySubmissions('${b.id}', '${b.title.replace(/'/g, "\\'")}')"
                                            style="flex: 1; padding: 0.2rem; background: var(--bg-dark);
                                                   border: 1px solid var(--teal); color: var(--teal); border-radius: 4px;
                                                   cursor: pointer; font-size: 0.65rem;">
                                            View (${teamCount})
                                        </button>
                                    ` : ''}
                                    ${b.status === 'open' && teamCount === 0 ? `
                                        <button onclick="deleteBounty('${b.id}')"
                                            style="flex: 1; padding: 0.2rem; background: var(--bg-dark);
                                                   border: 1px solid var(--red); color: var(--red); border-radius: 4px;
                                                   cursor: pointer; font-size: 0.65rem;">
                                            Cancel
                                        </button>
                                    ` : ''}
                                </div>
                            </div>
                        `;
                    }).join('');
                });
        }

        function showCompleteBountyModal(bountyId, defaultReward, teamCount) {
            const hasMultipleTeams = teamCount > 1;

            const modal = document.createElement('div');
            modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; justify-content: center; align-items: center; padding: 2rem;';
            modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

            modal.innerHTML = `
                <div style="background: var(--bg-card); padding: 2rem; border-radius: 12px; max-width: 400px; width: 100%;">
                    <h3 style="color: var(--teal); margin-bottom: 1rem;">Complete Bounty</h3>

                    ${hasMultipleTeams ? `
                        <p style="font-size: 0.85rem; color: var(--text-dim); margin-bottom: 1rem;">
                            This bounty has ${teamCount} competing guilds. Set rewards for each placement:
                        </p>
                        <div style="margin-bottom: 1rem;">
                            <label style="font-size: 0.8rem; color: var(--text-dim);">Winner Reward:</label>
                            <input type="number" id="winnerReward" value="${defaultReward}" min="0"
                                   style="width: 100%; padding: 0.5rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--yellow); border-radius: 4px; margin-top: 0.3rem;">
                        </div>
                        <div style="margin-bottom: 1rem;">
                            <label style="font-size: 0.8rem; color: var(--text-dim);">Runner-up Reward:</label>
                            <input type="number" id="runnerUpReward" value="${Math.floor(defaultReward * 0.5)}" min="0"
                                   style="width: 100%; padding: 0.5rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--yellow); border-radius: 4px; margin-top: 0.3rem;">
                        </div>
                    ` : `
                        <p style="font-size: 0.85rem; color: var(--text-dim); margin-bottom: 1rem;">
                            Award <span style="color: var(--yellow);">${defaultReward}</span> tokens for completing this bounty.
                        </p>
                    `}

                    <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                        <button onclick="this.closest('[style*=position]').remove()"
                                style="flex: 1; padding: 0.5rem; background: var(--bg-hover); border: 1px solid var(--border); color: var(--text); border-radius: 4px; cursor: pointer;">
                            Cancel
                        </button>
                        <button onclick="completeBounty('${bountyId}', ${hasMultipleTeams})"
                                style="flex: 1; padding: 0.5rem; background: var(--green); border: none; color: var(--bg-dark); border-radius: 4px; cursor: pointer; font-weight: 600;">
                            Complete & Pay Out
                        </button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }

        function completeBounty(bountyId, hasMultipleTeams = false) {
            let body = {};

            if (hasMultipleTeams) {
                const winnerReward = parseInt(document.getElementById('winnerReward').value) || 0;
                const runnerUpReward = parseInt(document.getElementById('runnerUpReward').value) || 0;
                body = { winner_reward: winnerReward, runner_up_reward: runnerUpReward };
            }

            fetch('/api/bounties/' + bountyId + '/complete', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(body)
            })
            .then(r => r.json())
            .then(data => {
                // Close modal if open
                const modal = document.querySelector('[style*="position: fixed"][style*="z-index: 1000"]');
                if (modal) modal.remove();

                if (data.success) {
                    loadBounties();
                    // Show detailed completion message with costs
                    const cost = data.cost_tracking || {};
                    let message = 'Bounty completed!';
                    if (data.total_distributed) message += ` ${data.total_distributed} tokens distributed.`;
                    if (cost.api_cost) message += `\\nTotal API Cost: $${cost.api_cost.toFixed(4)}`;
                    if (cost.sessions_used) message += `\\nSessions Used: ${cost.sessions_used}`;
                    if (cost.duration_hours) message += `\\nDuration: ${cost.duration_hours} hours`;
                    alert(message);
                } else {
                    alert('Error: ' + (data.reason || data.error || 'Unknown error'));
                }
            });
        }

        function deleteBounty(bountyId) {
            if (!confirm('Delete this bounty?')) return;

            fetch('/api/bounties/' + bountyId, {method: 'DELETE'})
                .then(r => r.json())
                .then(data => {
                    if (data.success) loadBounties();
                });
        }

        function viewBountySubmissions(bountyId, bountyTitle) {
            fetch('/api/bounties/' + bountyId + '/submissions')
                .then(r => r.json())
                .then(data => {
                    if (!data.success) {
                        alert('Error loading submissions');
                        return;
                    }

                    const submissions = data.submissions || [];
                    const modal = document.createElement('div');
                    modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; justify-content: center; align-items: center; padding: 2rem;';
                    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

                    modal.innerHTML = `
                        <div style="background: var(--bg-card); padding: 1.5rem; border-radius: 12px; max-width: 500px; width: 100%; max-height: 80vh; overflow-y: auto;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                <h3 style="color: var(--teal); margin: 0;">Submissions: ${bountyTitle}</h3>
                                <button onclick="this.closest('[style*=position]').remove()" style="background: none; border: none; color: var(--text-dim); font-size: 1.5rem; cursor: pointer;">&times;</button>
                            </div>

                            ${submissions.length === 0 ? `
                                <p style="color: var(--text-dim);">No submissions yet.</p>
                            ` : submissions.map((s, i) => `
                                <div style="background: var(--bg-dark); padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; border-left: 3px solid var(--teal);">
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                        <span style="font-weight: 600; color: var(--teal);">${s.identity_name}</span>
                                        <span style="font-size: 0.75rem; color: var(--text-dim);">${new Date(s.submitted_at).toLocaleString()}</span>
                                    </div>
                                    ${s.description ? `<p style="font-size: 0.85rem; color: var(--text); margin-bottom: 0.4rem;">${s.description}</p>` : ''}
                                    ${s.slot_multiplier !== undefined ? `
                                        <div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.4rem;">
                                            Slot ${s.slot_index || '?'}${s.slots ? `/${s.slots}` : ''} | x${(Number(s.slot_multiplier) || 0).toFixed(2)}${s.slot_reason ? ` (${s.slot_reason})` : ''}
                                        </div>
                                    ` : ''}
                                    ${s.artifacts && s.artifacts.length > 0 ? `
                                        <div style="font-size: 0.75rem; color: var(--text-dim);">
                                            <span>Artifacts:</span>
                                            <div style="margin-top: 0.3rem;">
                                                ${s.artifacts.map(a => `<a href="#" onclick="viewArtifact('${a}'); return false;" style="color: var(--purple); margin-right: 0.5rem;">${a.split('/').pop()}</a>`).join('')}
                                            </div>
                                        </div>
                                    ` : ''}
                                    ${s.notes ? `<p style="font-size: 0.75rem; color: var(--text-dim); margin-top: 0.5rem; font-style: italic;">${s.notes}</p>` : ''}
                                </div>
                            `).join('')}
                        </div>
                    `;
                    document.body.appendChild(modal);
                });
        }

        // Chat Rooms functions
        let currentOpenRoom = null;

        function loadChatRooms() {
            fetch('/api/chatrooms')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('chatRoomsContainer');
                    const countEl = document.getElementById('chatRoomsCount');

                    if (!data.success || !data.rooms || data.rooms.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.8rem;">No chat rooms yet. Rooms appear when residents start chatting!</p>';
                        countEl.textContent = '';
                        return;
                    }

                    const totalMessages = data.rooms.reduce((sum, r) => sum + (r.message_count || 0), 0);
                    countEl.textContent = `(${totalMessages} messages)`;

                    container.innerHTML = data.rooms.map(room => `
                        <details class="chat-room" style="margin-bottom: 0.5rem;" ${currentOpenRoom === room.id ? 'open' : ''}>
                            <summary onclick="loadRoomMessages('${room.id}')"
                                     style="cursor: pointer; padding: 0.6rem; background: var(--bg-dark); border-radius: 6px;
                                            list-style: none; display: flex; align-items: center; gap: 0.5rem;">
                                <span style="font-size: 1.1rem;">${room.icon}</span>
                                <span style="flex: 1;">
                                    <span style="font-weight: 600; color: var(--teal);">${room.name}</span>
                                    <span style="font-size: 0.7rem; color: var(--text-dim); margin-left: 0.3rem;">(${room.message_count})</span>
                                </span>
                                <span style="font-size: 0.65rem; color: var(--text-dim);">
                                    ${room.latest_timestamp ? new Date(room.latest_timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}
                                </span>
                            </summary>
                            <div id="room_${room.id}" style="padding: 0.5rem; background: var(--bg-card); border-radius: 0 0 6px 6px;
                                                             max-height: 300px; overflow-y: auto;">
                                <p style="color: var(--text-dim); font-size: 0.75rem;">Loading messages...</p>
                            </div>
                        </details>
                    `).join('');
                });
        }

        function loadRoomMessages(roomId) {
            currentOpenRoom = roomId;
            const container = document.getElementById('room_' + roomId);
            if (!container) return;

            fetch('/api/chatrooms/' + roomId)
                .then(r => r.json())
                .then(data => {
                    if (!data.success || !data.messages || data.messages.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem; font-style: italic;">No messages in this room yet.</p>';
                        return;
                    }

                    container.innerHTML = data.messages.map(msg => {
                        const time = msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '';
                        const mood = msg.mood ? ` <span style="opacity: 0.6;">(${msg.mood})</span>` : '';
                        const linkedContent = linkifyFilePaths(msg.content || '');

                        return `
                            <div style="margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                                    <span style="font-weight: 600; color: var(--teal); font-size: 0.8rem;">${msg.author_name || 'Unknown'}${mood}</span>
                                    <span style="font-size: 0.65rem; color: var(--text-dim);">${time}</span>
                                </div>
                                <div style="font-size: 0.85rem; color: var(--text); line-height: 1.4;">${linkedContent}</div>
                            </div>
                        `;
                    }).join('');

                    // Scroll to bottom
                    container.scrollTop = container.scrollHeight;
                });
        }

        // Initial load
        setupDayVibe();
        setInterval(setupDayVibe, 60000); // Update every minute (for time-based changes)
        fetch('/api/identities').then(r => r.json()).then(updateIdentities);
        loadSpawnerStatus();
        loadRequest();
        loadMessages();
        loadBounties();
        loadChatRooms();

        // Refresh bounties, spawner status, and chat rooms periodically
        setInterval(loadBounties, 10000);
        setInterval(loadSpawnerStatus, 5000);
        setInterval(loadChatRooms, 15000);  // Refresh chat rooms every 15 seconds
    </script>
</body>
</html>
'''


class LogWatcher(FileSystemEventHandler):
    """Watch action log file for changes."""

    def __init__(self, socketio_instance):
        self.socketio = socketio_instance
        self.last_position = 0

    def on_modified(self, event):
        if event.src_path.endswith('action_log.jsonl'):
            self.send_new_entries()

    def send_new_entries(self):
        global last_log_position
        if not ACTION_LOG.exists():
            return

        with open(ACTION_LOG, 'r') as f:
            f.seek(last_log_position)
            new_lines = f.readlines()
            last_log_position = f.tell()

        for line in new_lines:
            try:
                entry = json.loads(line.strip())
                self.socketio.emit('log_entry', entry)
            except:
                pass


def calculate_identity_level(sessions: int) -> int:
    """Calculate identity level based on sessions (ARPG-style progression)."""
    # Level formula: sqrt(sessions) rounded down, minimum level 1
    import math
    return max(1, int(math.sqrt(sessions)))


def calculate_respec_cost(sessions: int) -> int:
    """Calculate respec cost based on sessions (ARPG-style: cheap early, expensive later)."""
    # Formula from swarm_enrichment.py: BASE (10) + (sessions * SCALE (3))
    RESPEC_BASE_COST = 10
    RESPEC_SCALE_PER_SESSION = 3
    return RESPEC_BASE_COST + (sessions * RESPEC_SCALE_PER_SESSION)


def get_identities():
    """Get all identity info with token balances and profile snippets."""
    identities = []

    # Load token balances
    balances = {}
    if FREE_TIME_BALANCES.exists():
        try:
            with open(FREE_TIME_BALANCES) as f:
                balances = json.load(f)
        except:
            pass

    # Load identity files
    if IDENTITIES_DIR.exists():
        for f in IDENTITIES_DIR.glob("*.json"):
            try:
                with open(f) as file:
                    data = json.load(file)
                    identity_id = data.get('id', f.stem)
                    attrs = data.get('attributes', {})
                    profile = attrs.get('profile', {})
                    core = attrs.get('core', {})
                    sessions = data.get('sessions_participated', 0)

                    identities.append({
                        'id': identity_id,
                        'name': data.get('name', 'Unknown'),
                        'tokens': balances.get(identity_id, {}).get('tokens', 0),
                        'sessions': sessions,
                        'tasks_completed': data.get('tasks_completed', 0),
                        'profile_display': profile.get('display'),
                        'traits': core.get('personality_traits', []),
                        'values': core.get('core_values', []),
                        'level': calculate_identity_level(sessions),
                        'respec_cost': calculate_respec_cost(sessions),
                    })
            except:
                pass

    return identities


def get_stop_status():
    """Check if kill switch is engaged."""
    if KILL_SWITCH.exists():
        try:
            with open(KILL_SWITCH) as f:
                data = json.load(f)
                return data.get('halt', False)
        except:
            pass
    return False


def set_stop_status(stopped: bool):
    """Set kill switch status."""
    KILL_SWITCH.parent.mkdir(parents=True, exist_ok=True)
    data = {
        'halt': stopped,
        'reason': 'Manual stop from control panel' if stopped else None,
        'timestamp': datetime.now().isoformat()
    }
    with open(KILL_SWITCH, 'w') as f:
        json.dump(data, f, indent=2)
    return stopped


@app.route('/')
def index():
    return render_template_string(CONTROL_PANEL_HTML)


@socketio.on('connect')
def on_socket_connect():
    """Reject websocket connections from non-loopback clients."""
    if not _is_loopback_host(_request_source_host()):
        return False
    return None


@app.route('/api/identities')
def api_identities():
    return jsonify(get_identities())


@app.route('/api/identity/<identity_id>/profile')
def api_identity_profile(identity_id):
    """Get detailed profile for an identity including journals and stats."""
    identity_file = IDENTITIES_DIR / f"{identity_id}.json"

    if not identity_file.exists():
        return jsonify({'error': 'identity_not_found'})

    try:
        with open(identity_file) as f:
            data = json.load(f)

        attrs = data.get('attributes', {})
        profile = attrs.get('profile', {})
        core = attrs.get('core', {})
        mutable = attrs.get('mutable', {})

        # Get journals for this identity
        journals_dir = WORKSPACE / ".swarm" / "journals"
        journals = []
        if journals_dir.exists():
            for jf in sorted(journals_dir.glob(f"{identity_id}*.md"), reverse=True)[:10]:
                try:
                    with open(jf, 'r', encoding='utf-8') as jfile:
                        content = jfile.read()
                        journals.append({
                            'filename': jf.name,
                            'preview': content[:200] + '...' if len(content) > 200 else content,
                            'modified': datetime.fromtimestamp(jf.stat().st_mtime).isoformat()
                        })
                except:
                    pass

        # Get recent actions for this identity from log
        recent_actions = []
        if ACTION_LOG.exists():
            try:
                with open(ACTION_LOG, 'r') as f:
                    lines = f.readlines()[-200:]  # Last 200 entries
                    for line in reversed(lines):
                        try:
                            entry = json.loads(line.strip())
                            if entry.get('actor') == identity_id:
                                recent_actions.append({
                                    'timestamp': entry.get('timestamp'),
                                    'type': entry.get('action_type'),
                                    'action': entry.get('action'),
                                    'detail': entry.get('detail')
                                })
                                if len(recent_actions) >= 20:
                                    break
                        except:
                            pass
            except:
                pass

        # Calculate some stats
        task_success_rate = 0
        if data.get('tasks_completed', 0) + data.get('tasks_failed', 0) > 0:
            task_success_rate = data.get('tasks_completed', 0) / (data.get('tasks_completed', 0) + data.get('tasks_failed', 0)) * 100

        # Get chat history for this identity
        chat_history = []
        messages_file = WORKSPACE / ".swarm" / "messages_to_human.jsonl"
        responses_file = WORKSPACE / ".swarm" / "messages_from_human.json"
        if messages_file.exists():
            responses = {}
            if responses_file.exists():
                try:
                    with open(responses_file) as rf:
                        responses = json.load(rf)
                except:
                    pass
            try:
                with open(messages_file, 'r') as mf:
                    for line in mf:
                        if line.strip():
                            msg = json.loads(line)
                            if msg.get('from_id') == identity_id:
                                chat_entry = {
                                    'id': msg.get('id'),
                                    'content': msg.get('content'),
                                    'type': msg.get('type', 'message'),
                                    'sent_at': msg.get('timestamp'),
                                    'response': responses.get(msg.get('id'), {}).get('response'),
                                    'responded_at': responses.get(msg.get('id'), {}).get('responded_at')
                                }
                                chat_history.append(chat_entry)
            except:
                pass

        sessions = data.get('sessions_participated', 0)
        return jsonify({
            'identity_id': identity_id,
            'name': data.get('name'),
            'created_at': data.get('created_at'),
            'sessions': sessions,
            'tasks_completed': data.get('tasks_completed', 0),
            'tasks_failed': data.get('tasks_failed', 0),
            'task_success_rate': round(task_success_rate, 1),
            'level': calculate_identity_level(sessions),
            'respec_cost': calculate_respec_cost(sessions),
            'profile': profile,
            'core_summary': {
                'traits': core.get('personality_traits', []),
                'values': core.get('core_values', []),
                'identity_statement': core.get('identity_statement'),
                'communication_style': core.get('communication_style')
            },
            'mutable': {
                'likes': mutable.get('likes', []),
                'dislikes': mutable.get('dislikes', []),
                'current_interests': mutable.get('current_interests', []),
                'current_mood': mutable.get('current_mood'),
                'working_style': mutable.get('working_style')
            },
            'recent_memories': data.get('memories', [])[-5:],
            'journals': journals,
            'recent_actions': recent_actions,
            'expertise': data.get('expertise', {}),
            'chat_history': chat_history[-20:]  # Last 20 messages
        })

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/stop_status')
def api_stop_status():
    return jsonify({'stopped': get_stop_status()})


@app.route('/api/toggle_stop', methods=['POST'])
def api_toggle_stop():
    current = get_stop_status()
    new_status = set_stop_status(not current)
    socketio.emit('stop_status', {'stopped': new_status})
    return jsonify({'stopped': new_status})


# Spawner process tracking
SPAWNER_PROCESS_FILE = WORKSPACE / ".swarm" / "spawner_process.json"
SPAWNER_CONFIG_FILE = WORKSPACE / ".swarm" / "spawner_config.json"


def get_spawner_status():
    """Get current spawner process status."""
    status = {
        'running': False,
        'paused': False,
        'pid': None,
        'started_at': None,
        'config': None
    }

    # Check process file
    if SPAWNER_PROCESS_FILE.exists():
        try:
            with open(SPAWNER_PROCESS_FILE) as f:
                data = json.load(f)
                status['pid'] = data.get('pid')
                status['started_at'] = data.get('started_at')
                status['running'] = data.get('running', False)

                # Verify process is actually running
                if status['pid'] and status['running']:
                    import subprocess
                    try:
                        # Windows: check if PID exists
                        result = subprocess.run(
                            ['tasklist', '/FI', f'PID eq {status["pid"]}'],
                            capture_output=True, text=True
                        )
                        if str(status['pid']) not in result.stdout:
                            status['running'] = False
                    except:
                        pass
        except:
            pass

    # Check pause status
    pause_file = WORKSPACE / "PAUSE"
    if pause_file.exists():
        status['paused'] = True

    # Load config
    if SPAWNER_CONFIG_FILE.exists():
        try:
            with open(SPAWNER_CONFIG_FILE) as f:
                status['config'] = json.load(f)
        except:
            pass

    return status


def save_spawner_process(pid: int, running: bool, config: dict = None):
    """Save spawner process info."""
    SPAWNER_PROCESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        'pid': pid,
        'running': running,
        'started_at': datetime.now().isoformat(),
        'config': config
    }
    with open(SPAWNER_PROCESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def save_spawner_config(config: dict):
    """Save spawner configuration."""
    SPAWNER_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    config['updated_at'] = datetime.now().isoformat()
    with open(SPAWNER_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def _sanitize_spawner_start_payload(data: dict):
    sessions = data.get('sessions', 3)
    budget_limit = data.get('budget_limit', 1.0)
    auto_scale = bool(data.get('auto_scale', False))
    model = str(data.get('model', 'llama-3.3-70b-versatile')).strip()

    try:
        sessions = int(sessions)
    except (TypeError, ValueError):
        raise ValueError("sessions must be an integer")
    if sessions < 1 or sessions > 32:
        raise ValueError("sessions must be between 1 and 32")

    try:
        budget_limit = float(budget_limit)
    except (TypeError, ValueError):
        raise ValueError("budget_limit must be a number")
    if budget_limit <= 0:
        raise ValueError("budget_limit must be > 0")

    if not model:
        raise ValueError("model must be non-empty")
    if len(model) > 120:
        raise ValueError("model is too long")

    return {
        "sessions": sessions,
        "budget_limit": budget_limit,
        "auto_scale": auto_scale,
        "model": model,
    }


@app.route('/api/spawner/status')
def api_spawner_status():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'running': False,
        'paused': False,
        'pid': None,
        'config': None,
        'golden_path_only': True,
        'message': 'Golden path enforced: run queue tasks through worker.py.'
    })


@app.route('/api/spawner/start', methods=['POST'])
def api_start_spawner():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'success': False,
        'golden_path_only': True,
        'error': 'Detached spawner path is disabled. Use queue.json + worker.py run.'
    }), 410


@app.route('/api/spawner/pause', methods=['POST'])
def api_pause_spawner():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'success': False,
        'golden_path_only': True,
        'error': 'Detached spawner path is disabled. Use runtime safety controls only.'
    }), 410


@app.route('/api/spawner/resume', methods=['POST'])
def api_resume_spawner():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'success': False,
        'golden_path_only': True,
        'error': 'Detached spawner path is disabled. Use runtime safety controls only.'
    }), 410


@app.route('/api/spawner/kill', methods=['POST'])
def api_kill_spawner():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'success': False,
        'golden_path_only': True,
        'error': 'Detached spawner path is disabled. Use runtime safety controls only.'
    }), 410


@app.route('/api/spawner/config', methods=['POST'])
def api_update_spawner_config():
    """Spawner controls are disabled under golden-path enforcement."""
    return jsonify({
        'success': False,
        'golden_path_only': True,
        'error': 'Detached spawner path is disabled. Configuration updates are ignored.'
    }), 410


# Human request storage
HUMAN_REQUEST_FILE = WORKSPACE / ".swarm" / "human_request.json"

# Message queue for identity <-> human communication
MESSAGES_TO_HUMAN = WORKSPACE / ".swarm" / "messages_to_human.jsonl"
MESSAGES_FROM_HUMAN = WORKSPACE / ".swarm" / "messages_from_human.json"


def get_human_request():
    """Get the current human collaboration request."""
    if HUMAN_REQUEST_FILE.exists():
        try:
            with open(HUMAN_REQUEST_FILE) as f:
                data = json.load(f)
                return data.get('request', '')
        except:
            pass
    return ''


def save_human_request(request_text: str):
    """Save the human collaboration request."""
    HUMAN_REQUEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        'request': request_text,
        'updated_at': datetime.now().isoformat()
    }
    with open(HUMAN_REQUEST_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    return data


@app.route('/api/human_request', methods=['GET'])
def api_get_human_request():
    return jsonify({'request': get_human_request()})


@app.route('/api/human_request', methods=['POST'])
def api_save_human_request():
    data = request.json
    result = save_human_request(data.get('request', ''))
    return jsonify({'success': True, 'updated_at': result['updated_at']})


# Message queue endpoints
def get_messages_to_human():
    """Get all messages from identities to the human."""
    messages = []
    if MESSAGES_TO_HUMAN.exists():
        try:
            with open(MESSAGES_TO_HUMAN, 'r') as f:
                for line in f:
                    if line.strip():
                        messages.append(json.loads(line))
        except:
            pass
    return messages


def get_human_responses():
    """Get human responses to identity messages."""
    if MESSAGES_FROM_HUMAN.exists():
        try:
            with open(MESSAGES_FROM_HUMAN, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}


def save_human_response(message_id: str, response: str):
    """Save a human response to an identity message."""
    responses = get_human_responses()
    responses[message_id] = {
        'response': response,
        'responded_at': datetime.now().isoformat()
    }
    MESSAGES_FROM_HUMAN.parent.mkdir(parents=True, exist_ok=True)
    with open(MESSAGES_FROM_HUMAN, 'w') as f:
        json.dump(responses, f, indent=2)
    return responses[message_id]


@app.route('/api/messages')
def api_get_messages():
    """Get messages from identities with any responses."""
    messages = get_messages_to_human()
    responses = get_human_responses()

    # Attach responses to messages
    for msg in messages:
        msg_id = msg.get('id', '')
        if msg_id in responses:
            msg['response'] = responses[msg_id]

    # Return most recent first
    return jsonify(list(reversed(messages[-50:])))


@app.route('/api/messages/respond', methods=['POST'])
def api_respond_to_message():
    """Send a response to an identity message."""
    data = request.json
    message_id = data.get('message_id')
    response = data.get('response')

    if not message_id or not response:
        return jsonify({'success': False, 'error': 'Missing message_id or response'})

    result = save_human_response(message_id, response)
    return jsonify({'success': True, 'responded_at': result['responded_at']})


# Completed requests log
COMPLETED_REQUESTS_FILE = WORKSPACE / ".swarm" / "completed_requests.json"


def get_completed_requests():
    """Get list of completed collaboration requests."""
    if COMPLETED_REQUESTS_FILE.exists():
        try:
            with open(COMPLETED_REQUESTS_FILE) as f:
                return json.load(f)
        except:
            pass
    return []


def add_completed_request(request_text: str):
    """Add a request to the completed log."""
    completed = get_completed_requests()

    # Get the current request's created time if available
    started_at = None
    if HUMAN_REQUEST_FILE.exists():
        try:
            with open(HUMAN_REQUEST_FILE) as f:
                data = json.load(f)
                started_at = data.get('updated_at')
        except:
            pass

    # Calculate duration if we have start time
    duration = ''
    if started_at:
        try:
            start = datetime.fromisoformat(started_at)
            end = datetime.now()
            delta = end - start
            hours = delta.total_seconds() / 3600
            if hours < 1:
                duration = f'{int(delta.total_seconds() / 60)} min'
            elif hours < 24:
                duration = f'{hours:.1f} hrs'
            else:
                duration = f'{delta.days} days'
        except:
            pass

    completed.insert(0, {
        'request': request_text,
        'completed_at': datetime.now().isoformat(),
        'started_at': started_at,
        'duration': duration
    })

    # Keep last 50 requests
    completed = completed[:50]

    COMPLETED_REQUESTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(COMPLETED_REQUESTS_FILE, 'w') as f:
        json.dump(completed, f, indent=2)

    return completed[0]


@app.route('/api/completed_requests', methods=['GET'])
def api_get_completed_requests():
    """Get completed requests history."""
    return jsonify(get_completed_requests())


@app.route('/api/completed_requests', methods=['POST'])
def api_add_completed_request():
    """Mark a request as completed."""
    data = request.json
    request_text = data.get('request', '').strip()

    if not request_text:
        return jsonify({'success': False, 'error': 'No request text'})

    result = add_completed_request(request_text)
    return jsonify({'success': True, 'completed': result})


# Bounty API endpoints
CRUCIBLE_NAME = "Commons Crucible"
DEFAULT_SLOT_POLICY = {
    "in_slot_multiplier": 1.0,
    "overflow_decay": 0.5,
    "min_multiplier": 0.05,
    "min_description_chars": 20,
    "allow_artifact_override": True,
    "max_rewarded_submissions_per_identity": 1,
}

BOUNTIES_FILE = WORKSPACE / ".swarm" / "bounties.json"


def _get_slots_for_bounty(bounty: dict) -> int:
    slots = bounty.get("slots", bounty.get("max_teams", 1))
    try:
        return max(1, int(slots))
    except (TypeError, ValueError):
        return 1


def _normalize_slot_policy(policy):
    merged = DEFAULT_SLOT_POLICY.copy()
    if isinstance(policy, dict):
        for key in DEFAULT_SLOT_POLICY:
            if key in policy:
                merged[key] = policy[key]
    # Clamp numeric fields
    try:
        merged["overflow_decay"] = float(merged["overflow_decay"])
    except (TypeError, ValueError):
        merged["overflow_decay"] = DEFAULT_SLOT_POLICY["overflow_decay"]
    merged["overflow_decay"] = max(0.1, min(0.95, merged["overflow_decay"]))
    try:
        merged["min_multiplier"] = float(merged["min_multiplier"])
    except (TypeError, ValueError):
        merged["min_multiplier"] = DEFAULT_SLOT_POLICY["min_multiplier"]
    merged["min_multiplier"] = max(0.0, min(1.0, merged["min_multiplier"]))
    try:
        merged["in_slot_multiplier"] = float(merged["in_slot_multiplier"])
    except (TypeError, ValueError):
        merged["in_slot_multiplier"] = DEFAULT_SLOT_POLICY["in_slot_multiplier"]
    merged["in_slot_multiplier"] = max(0.1, min(2.0, merged["in_slot_multiplier"]))
    try:
        merged["min_description_chars"] = int(merged["min_description_chars"])
    except (TypeError, ValueError):
        merged["min_description_chars"] = DEFAULT_SLOT_POLICY["min_description_chars"]
    merged["min_description_chars"] = max(0, merged["min_description_chars"])
    try:
        merged["max_rewarded_submissions_per_identity"] = int(
            merged["max_rewarded_submissions_per_identity"]
        )
    except (TypeError, ValueError):
        merged["max_rewarded_submissions_per_identity"] = (
            DEFAULT_SLOT_POLICY["max_rewarded_submissions_per_identity"]
        )
    merged["max_rewarded_submissions_per_identity"] = max(
        1, merged["max_rewarded_submissions_per_identity"]
    )
    merged["allow_artifact_override"] = bool(merged.get("allow_artifact_override", True))
    return merged


def _compute_slot_multiplier(slot_index: int, slots: int, policy: dict) -> float:
    if slots <= 0 or slot_index <= slots:
        return float(policy.get("in_slot_multiplier", 1.0))
    overflow = max(0, slot_index - slots)
    decay = float(policy.get("overflow_decay", 0.5))
    multiplier = float(policy.get("in_slot_multiplier", 1.0)) * (decay ** overflow)
    return max(float(policy.get("min_multiplier", 0.05)), multiplier)


def _evaluate_submission(bounty, identity_id, description, artifacts):
    teams = bounty.get("teams", [])
    slots = _get_slots_for_bounty(bounty)
    slot_index = len(teams) + 1
    policy = _normalize_slot_policy(bounty.get("slot_policy"))

    multiplier = _compute_slot_multiplier(slot_index, slots, policy)
    reasons = []

    if not identity_id:
        reasons.append("missing_identity")

    if identity_id:
        submitted = [t for t in teams if t.get("identity_id") == identity_id]
        if len(submitted) >= policy.get("max_rewarded_submissions_per_identity", 1):
            reasons.append("repeat_submission")

    min_chars = policy.get("min_description_chars", 0)
    desc_ok = len((description or "").strip()) >= min_chars if min_chars else True
    has_artifacts = bool(artifacts)
    if not desc_ok and not (policy.get("allow_artifact_override", True) and has_artifacts):
        reasons.append("insufficient_contribution")

    if slot_index > slots:
        reasons.append("overflow")

    if reasons and any(r in ["missing_identity", "repeat_submission", "insufficient_contribution"] for r in reasons):
        multiplier = 0.0

    if not reasons:
        reason = "in_slot"
    else:
        reason = ",".join(reasons)

    return {
        "slot_index": slot_index,
        "slots": slots,
        "slot_multiplier": round(multiplier, 4),
        "slot_reason": reason,
        "policy": policy,
    }


def load_bounties():
    """Load bounties from file."""
    if BOUNTIES_FILE.exists():
        try:
            with open(BOUNTIES_FILE) as f:
                return json.load(f)
        except:
            pass
    return []


def save_bounties(bounties):
    """Save bounties to file."""
    BOUNTIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BOUNTIES_FILE, 'w') as f:
        json.dump(bounties, f, indent=2)


@app.route('/api/bounties', methods=['GET'])
def api_get_bounties():
    """Get all non-completed bounties."""
    bounties = load_bounties()
    # Filter to show open and claimed (not completed unless recent)
    active = [b for b in bounties if b.get('status') in ('open', 'claimed')]
    return jsonify(active)


@app.route('/api/bounties', methods=['POST'])
def api_create_bounty():
    """Create a new bounty."""
    data = request.json
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    reward = int(data.get('reward', 50))
    slots = data.get('slots', data.get('max_teams', 1))
    try:
        slots = max(1, int(slots))
    except (TypeError, ValueError):
        slots = 1
    game_mode = (data.get('game_mode') or 'hybrid').lower()
    if game_mode not in ('pvp', 'coop', 'hybrid'):
        game_mode = 'hybrid'
    slot_policy = _normalize_slot_policy(data.get('slot_policy'))

    if not title:
        return jsonify({'success': False, 'error': 'Title required'})

    bounties = load_bounties()
    bounty = {
        'id': f"bounty_{int(time.time()*1000)}",
        'title': title,
        'description': description,
        'reward': reward,
        'game_name': CRUCIBLE_NAME,
        'game_mode': game_mode,
        'status': 'open',
        'created_at': datetime.now().isoformat(),
        'claimed_by': None,
        # Project-level cost tracking
        'max_teams': slots,  # Back-compat: guild slots with full rewards
        'slots': slots,
        'slot_policy': slot_policy,
        'slot_state': {
            'slots': slots,
            'filled': 0,
            'overflow': 0
        },
        'teams': [],  # List of guild submissions
        'cost_tracking': {
            'api_cost': 0.0,
            'sessions_used': 0,
            'tokens_spent': 0,
            'started_at': None,
            'artifacts_created': []
        }
    }
    bounties.append(bounty)
    save_bounties(bounties)

    return jsonify({'success': True, 'bounty': bounty})


@app.route('/api/bounties/<bounty_id>', methods=['DELETE'])
def api_delete_bounty(bounty_id):
    """Delete an unclaimed bounty."""
    bounties = load_bounties()
    bounty = next((b for b in bounties if b['id'] == bounty_id), None)

    if not bounty:
        return jsonify({'success': False, 'error': 'Bounty not found'})

    if bounty.get('status') != 'open':
        return jsonify({'success': False, 'error': 'Can only delete open bounties'})

    bounties = [b for b in bounties if b['id'] != bounty_id]
    save_bounties(bounties)

    return jsonify({'success': True})


@app.route('/api/bounties/<bounty_id>/submit', methods=['POST'])
def api_submit_to_bounty(bounty_id):
    """Submit work to a bounty (for competing guilds)."""
    data = request.json or {}
    bounties = load_bounties()
    bounty = next((b for b in bounties if b['id'] == bounty_id), None)

    if not bounty:
        return jsonify({'success': False, 'error': 'Bounty not found'})

    if bounty.get('status') != 'open':
        return jsonify({'success': False, 'error': 'Bounty is not open for submissions'})

    # Normalize slot policy and evaluate rewards
    bounty['slot_policy'] = _normalize_slot_policy(bounty.get('slot_policy'))
    bounty['slots'] = _get_slots_for_bounty(bounty)
    current_teams = bounty.get('teams', [])

    identity_id = data.get('identity_id')
    description = data.get('description', '')
    artifacts = data.get('artifacts', [])
    slot_info = _evaluate_submission(bounty, identity_id, description, artifacts)

    # Create submission
    submission = {
        'id': f"sub_{int(time.time()*1000)}",
        'identity_id': identity_id,
        'identity_name': data.get('identity_name', 'Unknown'),
        'description': description,
        'artifacts': artifacts,  # List of file paths
        'submitted_at': datetime.now().isoformat(),
        'notes': data.get('notes', ''),
        'slot_index': slot_info['slot_index'],
        'slots': slot_info['slots'],
        'slot_multiplier': slot_info['slot_multiplier'],
        'slot_reason': slot_info['slot_reason'],
        'reward_cap': int(round(bounty.get('reward', 0) * slot_info['slot_multiplier']))
    }

    if 'teams' not in bounty:
        bounty['teams'] = []
    bounty['teams'].append(submission)

    # Update slot state
    slots = bounty.get('slots', _get_slots_for_bounty(bounty))
    team_count = len(bounty['teams'])
    bounty['slot_state'] = {
        'slots': slots,
        'filled': min(team_count, slots),
        'overflow': max(0, team_count - slots)
    }

    # Mark bounty as claimed if this is the first submission
    if bounty['status'] == 'open' and len(bounty['teams']) == 1:
        bounty['status'] = 'claimed'
        bounty['cost_tracking']['started_at'] = datetime.now().isoformat()

    save_bounties(bounties)

    return jsonify({'success': True, 'submission': submission})


@app.route('/api/bounties/<bounty_id>/submissions')
def api_get_bounty_submissions(bounty_id):
    """Get all submissions for a bounty (guild submissions)."""
    bounties = load_bounties()
    bounty = next((b for b in bounties if b['id'] == bounty_id), None)

    if not bounty:
        return jsonify({'success': False, 'error': 'Bounty not found'})

    return jsonify({
        'success': True,
        'bounty_id': bounty_id,
        'bounty_title': bounty.get('title'),
        'submissions': bounty.get('teams', [])
    })


@app.route('/api/bounties/<bounty_id>/track_cost', methods=['POST'])
def api_track_bounty_cost(bounty_id):
    """Track API cost against a bounty."""
    data = request.json or {}
    bounties = load_bounties()
    bounty = next((b for b in bounties if b['id'] == bounty_id), None)

    if not bounty:
        return jsonify({'success': False, 'error': 'Bounty not found'})

    # Initialize cost tracking if missing
    if 'cost_tracking' not in bounty:
        bounty['cost_tracking'] = {
            'api_cost': 0.0,
            'sessions_used': 0,
            'tokens_spent': 0,
            'started_at': None,
            'artifacts_created': []
        }

    # Update tracking
    if data.get('api_cost'):
        bounty['cost_tracking']['api_cost'] += float(data['api_cost'])
    if data.get('session_increment'):
        bounty['cost_tracking']['sessions_used'] += 1
    if data.get('tokens_spent'):
        bounty['cost_tracking']['tokens_spent'] += int(data['tokens_spent'])
    if data.get('artifact'):
        bounty['cost_tracking']['artifacts_created'].append(data['artifact'])
    if not bounty['cost_tracking']['started_at']:
        bounty['cost_tracking']['started_at'] = datetime.now().isoformat()

    save_bounties(bounties)
    return jsonify({'success': True, 'cost_tracking': bounty['cost_tracking']})


@app.route('/api/bounties/<bounty_id>/complete', methods=['POST'])
def api_complete_bounty(bounty_id):
    """Mark a bounty as complete and distribute rewards."""
    data = request.json or {}
    bounties = load_bounties()
    bounty = next((b for b in bounties if b['id'] == bounty_id), None)

    if not bounty:
        return jsonify({'success': False, 'error': 'Bounty not found'})

    # Calculate project costs from action log if not tracked
    cost_tracking = bounty.get('cost_tracking', {})
    if cost_tracking.get('started_at') and ACTION_LOG.exists():
        try:
            start_time = datetime.fromisoformat(cost_tracking['started_at'])
            total_api_cost = cost_tracking.get('api_cost', 0.0)

            # Scan action log for API costs since bounty started
            with open(ACTION_LOG, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry.get('action_type') == 'API':
                            entry_time = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                            if entry_time >= start_time:
                                # Extract cost from detail like "1523 tokens | $0.003"
                                detail = entry.get('detail', '')
                                if '$' in detail:
                                    cost_str = detail.split('$')[-1]
                                    try:
                                        total_api_cost += float(cost_str)
                                    except:
                                        pass
                    except:
                        pass

            cost_tracking['api_cost'] = total_api_cost
            cost_tracking['completed_at'] = datetime.now().isoformat()

            # Calculate duration
            if cost_tracking.get('started_at'):
                start = datetime.fromisoformat(cost_tracking['started_at'])
                duration = datetime.now() - start
                hours = duration.total_seconds() / 3600
                cost_tracking['duration_hours'] = round(hours, 2)

        except Exception as e:
            print(f"Error calculating bounty costs: {e}")

    # Handle manual reward distribution for competing guilds
    winner_reward = data.get('winner_reward', bounty.get('reward', 50))
    runner_up_reward = data.get('runner_up_reward', 0)

    try:
        import sys
        sys.path.insert(0, str(WORKSPACE))
        from vivarium.runtime.swarm_enrichment import get_enrichment

        enrichment = get_enrichment(WORKSPACE)

        # If there are guild submissions, distribute according to placement
        teams = bounty.get('teams', [])
        if teams and len(teams) == 1:
            # Persist slot multiplier for single-claimer distribution
            try:
                bounty['slot_multiplier'] = float(teams[0].get('slot_multiplier', 1.0))
                bounty['slot_reason'] = teams[0].get('slot_reason', 'in_slot')
            except (TypeError, ValueError):
                bounty['slot_multiplier'] = 1.0
                bounty['slot_reason'] = 'in_slot'
            save_bounties(bounties)
        if teams and len(teams) > 1:
            # Winner gets winner_reward, runner-up gets runner_up_reward
            result = {
                'success': True,
                'distributions': [],
                'cost_tracking': cost_tracking
            }
            for i, team in enumerate(teams):
                reward = winner_reward if i == 0 else (runner_up_reward if i == 1 else 0)
                try:
                    slot_multiplier = float(team.get('slot_multiplier', 1.0))
                except (TypeError, ValueError):
                    slot_multiplier = 1.0
                reward = int(round(reward * max(0.0, slot_multiplier)))
                if reward > 0:
                    for member_id in team.get('members', []):
                        enrichment.grant_free_time(member_id, reward, f"bounty_{bounty_id}_place_{i+1}")
                        result['distributions'].append({
                            'identity': member_id,
                            'reward': reward,
                            'place': i + 1,
                            'slot_multiplier': slot_multiplier
                        })
        else:
            # Single guild/claimant - use original distribution
            result = enrichment.distribute_bounty(bounty_id)
            result['cost_tracking'] = cost_tracking

        # Update bounty status
        bounty['status'] = 'completed'
        bounty['completed_at'] = datetime.now().isoformat()
        bounty['cost_tracking'] = cost_tracking
        save_bounties(bounties)

        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'cost_tracking': cost_tracking})


# ═══════════════════════════════════════════════════════════════════════════════
# ARTIFACTS VIEWER - View files created by residents
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/artifact/view')
def api_view_artifact():
    """View contents of a file artifact."""
    file_path = request.args.get('path', '')

    if not file_path:
        return jsonify({'success': False, 'error': 'No path provided'})

    # Security: Only allow viewing files within workspace
    try:
        # Resolve the path relative to workspace
        if not os.path.isabs(file_path):
            full_path = WORKSPACE / file_path
        else:
            full_path = Path(file_path)

        # Ensure it's within workspace (prevent directory traversal)
        full_path = full_path.resolve()
        if not str(full_path).startswith(str(WORKSPACE.resolve())):
            return jsonify({'success': False, 'error': 'Access denied: path outside workspace'})

        if not full_path.exists():
            return jsonify({'success': False, 'error': 'File not found'})

        if not full_path.is_file():
            return jsonify({'success': False, 'error': 'Not a file'})

        # Check file size (limit to 500KB for viewing)
        if full_path.stat().st_size > 500 * 1024:
            return jsonify({'success': False, 'error': 'File too large (>500KB)'})

        # Detect file type for syntax highlighting
        ext = full_path.suffix.lower()
        file_type_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.json': 'json',
            '.md': 'markdown',
            '.html': 'html',
            '.css': 'css',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.sh': 'bash',
            '.sql': 'sql',
            '.txt': 'text',
            '.log': 'text',
        }
        file_type = file_type_map.get(ext, 'text')

        # Read content
        try:
            content = full_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = full_path.read_text(encoding='latin-1')

        return jsonify({
            'success': True,
            'path': str(full_path.relative_to(WORKSPACE)),
            'filename': full_path.name,
            'content': content,
            'file_type': file_type,
            'size': full_path.stat().st_size,
            'modified': datetime.fromtimestamp(full_path.stat().st_mtime).isoformat()
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/artifacts/list')
def api_list_artifacts():
    """List recent artifacts (files created/modified by the swarm)."""
    try:
        # Get files from journals and library
        artifacts = []

        # Journals
        journals_dir = WORKSPACE / ".swarm" / "journals"
        if journals_dir.exists():
            for f in sorted(journals_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                artifacts.append({
                    'path': str(f.relative_to(WORKSPACE)),
                    'name': f.name,
                    'type': 'journal',
                    'modified': datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                })

        # Library/creative works
        library_dir = WORKSPACE / "library" / "creative_works"
        if library_dir.exists():
            for f in sorted(library_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                artifacts.append({
                    'path': str(f.relative_to(WORKSPACE)),
                    'name': f.name,
                    'type': 'creative_work',
                    'modified': datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                })

        # Skills created
        skills_dir = WORKSPACE / "skills"
        if skills_dir.exists():
            for f in sorted(skills_dir.glob("*.py"), key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
                artifacts.append({
                    'path': str(f.relative_to(WORKSPACE)),
                    'name': f.name,
                    'type': 'skill',
                    'modified': datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                })

        return jsonify({'success': True, 'artifacts': artifacts})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# ═══════════════════════════════════════════════════════════════════
# CHAT ROOMS API - View watercooler, town hall, etc.
# ═══════════════════════════════════════════════════════════════════

DISCUSSIONS_DIR = WORKSPACE / ".swarm" / "discussions"

# Room display names and icons
ROOM_INFO = {
    'watercooler': {'name': 'Break Room', 'icon': '☕', 'description': 'Casual chat, status updates'},
    'town_hall': {'name': 'Town Hall', 'icon': '🏛️', 'description': 'Proposals, votes, community decisions'},
    'improvements': {'name': 'Improvements', 'icon': '💡', 'description': 'System enhancement ideas'},
    'struggles': {'name': 'Struggles', 'icon': '🤔', 'description': 'Challenges and help requests'},
    'discoveries': {'name': 'Discoveries', 'icon': '✨', 'description': 'Interesting findings'},
    'project_war_room': {'name': 'War Room', 'icon': '⚔️', 'description': 'Active project coordination'},
}


@app.route('/api/chatrooms')
def api_get_chatrooms():
    """Get list of available chat rooms with message counts."""
    rooms = []

    if DISCUSSIONS_DIR.exists():
        for room_file in DISCUSSIONS_DIR.glob("*.jsonl"):
            room_name = room_file.stem
            if room_name.startswith('town_hall_') or room_name.startswith('permanent'):
                continue  # Skip archives

            info = ROOM_INFO.get(room_name, {'name': room_name.title(), 'icon': '💬', 'description': ''})

            # Count messages and get latest
            message_count = 0
            latest_timestamp = None
            latest_preview = None

            try:
                with open(room_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    message_count = len([l for l in lines if l.strip()])

                    if lines:
                        for line in reversed(lines):
                            if line.strip():
                                msg = json.loads(line)
                                latest_timestamp = msg.get('timestamp')
                                author = msg.get('author_name', 'Unknown')
                                content = msg.get('content', '')[:50]
                                latest_preview = f"{author}: {content}..."
                                break
            except:
                pass

            rooms.append({
                'id': room_name,
                'name': info['name'],
                'icon': info['icon'],
                'description': info['description'],
                'message_count': message_count,
                'latest_timestamp': latest_timestamp,
                'latest_preview': latest_preview
            })

    # Sort by latest activity
    rooms.sort(key=lambda r: r.get('latest_timestamp') or '', reverse=True)
    return jsonify({'success': True, 'rooms': rooms})


@app.route('/api/chatrooms/<room_id>')
def api_get_chatroom_messages(room_id):
    """Get messages from a specific chat room."""
    limit = request.args.get('limit', 50, type=int)

    if not DISCUSSIONS_DIR.exists():
        return jsonify({'success': True, 'messages': [], 'room': room_id})

    room_file = DISCUSSIONS_DIR / f"{room_id}.jsonl"
    if not room_file.exists():
        return jsonify({'success': True, 'messages': [], 'room': room_id})

    messages = []
    try:
        with open(room_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    # Return most recent, reverse to show newest last
    info = ROOM_INFO.get(room_id, {'name': room_id.title(), 'icon': '💬', 'description': ''})

    return jsonify({
        'success': True,
        'room': room_id,
        'room_name': info['name'],
        'room_icon': info['icon'],
        'messages': messages[-limit:]
    })


def background_watcher():
    """Background thread to watch log file and push updates."""
    watcher = LogWatcher(socketio)

    # Initial load of existing entries
    if ACTION_LOG.exists():
        watcher.send_new_entries()

    observer = Observer()
    observer.schedule(watcher, str(ACTION_LOG.parent), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except:
        observer.stop()
    observer.join()


def push_identities_periodically():
    """Push identity updates every 5 seconds."""
    while True:
        time.sleep(5)
        socketio.emit('identities', get_identities())


if __name__ == '__main__':
    print("=" * 60)
    print("SWARM CONTROL PANEL")
    print("=" * 60)
    print(f"Open: http://{CONTROL_PANEL_HOST}:{CONTROL_PANEL_PORT}")
    print(f"Watching: {ACTION_LOG}")
    print("=" * 60)

    # Start background threads
    threading.Thread(target=background_watcher, daemon=True).start()
    threading.Thread(target=push_identities_periodically, daemon=True).start()

    socketio.run(
        app,
        host=CONTROL_PANEL_HOST,
        port=CONTROL_PANEL_PORT,
        debug=False,
        use_reloader=False,
    )
