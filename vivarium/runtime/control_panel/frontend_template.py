CONTROL_PANEL_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swarm Control Panel</title>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js" crossorigin="anonymous"></script>
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
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, "Helvetica Neue", Arial, sans-serif;
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
            position: relative;
            z-index: 110;
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

        .control-btn.stop.engaged {
            background: var(--green);
            color: var(--bg-dark);
            box-shadow: 0 0 15px rgba(68, 255, 68, 0.3);
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

        .spawner-status .start-hint {
            margin-left: 0.5rem;
            font-size: 0.75rem;
            color: var(--text-dim);
            max-width: 42em;
        }
        .spawner-status .start-hint code {
            background: var(--bg-dark);
            padding: 0.15rem 0.35rem;
            border-radius: 4px;
            font-size: 0.7rem;
        }

        .add-task-bar {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
        }
        .add-task-input {
            padding: 0.4rem 0.6rem;
            border: 1px solid var(--border);
            border-radius: 4px;
            background: var(--bg-dark);
            color: var(--text);
            font-size: 0.85rem;
        }
        .add-task-input::placeholder { color: var(--text-dim); }
        .add-task-input.add-task-instruction { flex: 1; min-width: 12rem; }
        .add-task-bar .add-task-btn {
            flex-shrink: 0;
            padding: 0.4rem 0.8rem;
            background: var(--teal);
            color: var(--bg-dark);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
        }
        .add-task-bar .add-task-btn:hover { filter: brightness(1.1); }
.resident-count-control {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    margin-right: 0.5rem;
    color: var(--text-dim);
    font-size: 0.75rem;
}
.resident-count-control input {
    width: 54px;
    padding: 0.25rem 0.35rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--bg-dark);
    color: var(--text);
    font-size: 0.8rem;
}

        .queue-panel {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.6rem;
            padding: 0.6rem 1rem;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
        }
        .queue-column {
            background: var(--bg-hover);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.55rem 0.7rem;
            min-height: 120px;
        }
        .queue-column h4 {
            margin: 0 0 0.4rem 0;
            font-size: 0.75rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .queue-list {
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            font-size: 0.78rem;
            max-height: 180px;
            overflow: auto;
        }
        .queue-item {
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.35rem 0.45rem;
            background: var(--bg-dark);
        }
        .queue-item .qid {
            color: var(--teal);
            font-weight: 600;
        }
        .queue-item .qprompt {
            margin-top: 0.2rem;
            line-height: 1.35;
        }
        .queue-item .qactions {
            display: flex;
            gap: 0.3rem;
            margin-top: 0.3rem;
        }
        .queue-item .qbtn {
            padding: 0.16rem 0.4rem;
            border-radius: 4px;
            border: 1px solid var(--border);
            background: var(--bg-hover);
            color: var(--text);
            font-size: 0.68rem;
            cursor: pointer;
        }
        .queue-item .qbtn.delete {
            background: rgba(255, 68, 68, 0.12);
            border-color: rgba(255, 68, 68, 0.4);
            color: #ff7d7d;
        }
        .queue-empty {
            color: var(--text-dim);
            font-size: 0.75rem;
        }

        .insights-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(170px, 1fr));
            gap: 0.6rem;
            padding: 0.75rem 1rem;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
        }

        .insights-collapsible {
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
        }

        .insights-summary {
            cursor: pointer;
            padding: 0.55rem 1rem;
            list-style: none;
            color: var(--text-dim);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }

        .insights-summary::after {
            content: '▼';
            font-size: 0.65rem;
            transition: transform 0.2s;
        }

        .insights-collapsible[open] .insights-summary::after {
            transform: rotate(180deg);
        }

        .insight-card {
            background: var(--bg-hover);
            border: 1px solid var(--border);
            border-radius: 8px;
            min-height: 64px;
        }

        .insight-label {
            color: var(--text-dim);
            font-size: 0.65rem;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        .insight-value {
            color: var(--text);
            font-size: 1.05rem;
            font-weight: 700;
            line-height: 1.2;
        }

        .insight-sub {
            color: var(--text-dim);
            font-size: 0.7rem;
            margin-top: 0.15rem;
        }

        .insight-value.good { color: var(--green); }
        .insight-value.warn { color: var(--yellow); }
        .insight-value.bad { color: var(--red); }
        .insight-value.teal { color: var(--teal); }

        .insight-card summary {
            list-style: none;
            cursor: pointer;
            padding: 0.55rem 0.7rem;
        }
        .insight-card summary::-webkit-details-marker {
            display: none;
        }
        .insight-card summary::after {
            content: '+';
            float: right;
            color: var(--text-dim);
            font-weight: 700;
        }
        .insight-card[open] summary::after {
            content: '−';
        }
        .insight-detail {
            border-top: 1px solid var(--border);
            padding: 0.45rem 0.7rem 0.6rem;
            font-size: 0.72rem;
            color: var(--text-dim);
            line-height: 1.35;
            white-space: pre-line;
        }

        @media (max-width: 1200px) {
            .insights-strip {
                grid-template-columns: repeat(2, minmax(160px, 1fr));
            }
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
            min-height: 0;
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
        .log-empty {
            color: var(--text-dim);
            padding: 0.8rem 0.2rem;
            font-size: 0.8rem;
            font-style: italic;
        }

        .log-time {
            color: var(--text-dim);
            min-width: 80px;
        }

        .log-day {
            color: var(--purple);
            min-width: 64px;
            cursor: help;
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

        .log-task {
            color: var(--purple);
            min-width: 130px;
            font-size: 0.78rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .log-hat {
            color: var(--teal);
            min-width: 120px;
            font-size: 0.78rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .log-usage {
            color: var(--yellow);
            min-width: 110px;
            font-size: 0.78rem;
            white-space: nowrap;
        }

        .log-detail {
            flex: 1;
            color: var(--text);
        }

        /* Log type colors */
        .type-TOOL { color: var(--teal); }
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

        .slideout-toggle.identities-toggle {
            top: 36%;
            background: #182235;
            color: var(--teal);
        }

        .slideout-toggle.identities-toggle:hover {
            background: #1f2b41;
            color: #9bf7ee;
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

        .slideout-panel.identities-panel {
            right: -420px;
            width: 420px;
            z-index: 210;
        }

        .slideout-panel.identities-panel.open {
            right: 0;
        }

        .slideout-overlay.identities-overlay {
            z-index: 205;
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

        .chat-room-card {
            background: var(--bg-hover);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.55rem;
            margin-bottom: 0.5rem;
        }

        .chat-room-card-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .chat-room-open-btn {
            background: var(--teal);
            color: var(--bg-dark);
            border: none;
            border-radius: 6px;
            padding: 0.25rem 0.55rem;
            cursor: pointer;
            font-size: 0.72rem;
            font-weight: 700;
        }

        .chatroom-modal {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.82);
            z-index: 1200;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }

        .chatroom-modal.open {
            display: flex;
        }

        .chatroom-modal-panel {
            width: min(1100px, 96vw);
            height: min(840px, 88vh);
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chatroom-modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.8rem 1rem;
            border-bottom: 1px solid var(--border);
        }

        .chatroom-modal-meta {
            font-size: 0.75rem;
            color: var(--text-dim);
            padding: 0.4rem 1rem;
            border-bottom: 1px solid var(--border);
        }

        .chatroom-modal-messages {
            flex: 1;
            overflow-y: auto;
            padding: 0.8rem 1rem;
        }

        .chat-msg {
            background: var(--bg-hover);
            border-radius: 8px;
            padding: 0.6rem;
            margin-bottom: 0.55rem;
            border-left: 3px solid var(--teal);
        }

        .mailbox-launcher {
            background: var(--bg-hover);
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.35rem 0.65rem;
            cursor: pointer;
            font-size: 0.78rem;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }

        .mailbox-badge {
            min-width: 1.1rem;
            height: 1.1rem;
            border-radius: 999px;
            background: var(--red);
            color: #fff;
            font-size: 0.65rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0 0.25rem;
            opacity: 0;
            transform: scale(0.9);
            transition: opacity 120ms ease, transform 120ms ease;
        }

        .mailbox-badge.show {
            opacity: 1;
            transform: scale(1);
            animation: mailboxPulse 1.2s ease-in-out infinite;
        }

        @keyframes mailboxPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.12); }
            100% { transform: scale(1); }
        }

        .mailbox-modal {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.82);
            z-index: 1300;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }

        .mailbox-modal.open {
            display: flex;
        }

        .mailbox-phone {
            width: min(460px, 96vw);
            height: min(840px, 90vh);
            background: linear-gradient(180deg, #151a20 0%, #0f1318 100%);
            border: 1px solid var(--border);
            border-radius: 18px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .mailbox-head {
            padding: 0.7rem 0.85rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .mailbox-threads {
            padding: 0.6rem 0.75rem;
            border-bottom: 1px solid var(--border);
            max-height: 190px;
            overflow-y: auto;
        }

        .mailbox-thread-item {
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--bg-card);
            padding: 0.45rem 0.5rem;
            cursor: pointer;
            margin-bottom: 0.35rem;
        }

        .mailbox-thread-item.active {
            border-color: var(--teal);
            background: rgba(3, 218, 198, 0.09);
        }

        .mailbox-messages {
            flex: 1;
            overflow-y: auto;
            padding: 0.7rem 0.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
        }

        .mailbox-msg {
            max-width: 88%;
            border-radius: 10px;
            padding: 0.45rem 0.55rem;
            font-size: 0.82rem;
            line-height: 1.35;
            border: 1px solid var(--border);
        }

        .mailbox-msg.in {
            align-self: flex-start;
            background: var(--bg-card);
        }

        .mailbox-msg.out {
            align-self: flex-end;
            background: rgba(3, 218, 198, 0.12);
            border-color: rgba(3, 218, 198, 0.35);
        }

        .mailbox-compose {
            border-top: 1px solid var(--border);
            padding: 0.65rem 0.75rem;
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
            <div class="dot" id="workerDot"></div>
            <span id="workerStatus">Residents: —</span>
        </div>
        <div class="control-buttons">
            <label class="resident-count-control" title="How many residents run in parallel">
                Active residents
                <input type="number" id="residentCount" min="1" max="16" step="1" value="1" onchange="persistUiSettings()">
            </label>
            <button class="mailbox-launcher" id="mailboxLauncher" onclick="openMailboxModal()" title="Open communication mailbox">
                <span>📬</span>
                <span>Mailbox</span>
                <span id="mailboxUnreadBadge" class="mailbox-badge">0</span>
            </button>
            <button class="control-btn start" id="workerStartBtn" onclick="startWorker()" title="Start resident runtime (worker daemon)">Start residents</button>
            <button class="control-btn stop" id="workerStopBtn" onclick="stopWorker()" style="display:none;" title="Pause resident runtime">Pause residents</button>
            <button class="control-btn pause" id="pauseBtn" onclick="togglePause()" disabled style="display:none;">DISABLED</button>
            <button class="control-btn stop" id="stopBtn" onclick="toggleStop()">HALT</button>
        </div>
    </div>

    <div class="add-task-bar">
        <input type="text" id="addTaskId" placeholder="Task ID (e.g. task-001)" class="add-task-input" />
        <input type="text" id="addTaskInstruction" placeholder="Instruction (e.g. Draft a docs improvement proposal)" class="add-task-input add-task-instruction" />
        <button type="button" class="control-btn add-task-btn" onclick="addTaskFromUI()">Add task</button>
    </div>

    <div class="queue-panel">
        <div class="queue-column">
            <h4>Open Queue</h4>
            <div id="queueOpenList" class="queue-list"><div class="queue-empty">No open tasks</div></div>
        </div>
        <div class="queue-column">
            <h4>Pending your approval</h4>
            <div id="queuePendingReviewList" class="queue-list"><div class="queue-empty">None</div></div>
        </div>
        <div class="queue-column">
            <h4>Recent Completed</h4>
            <div id="queueCompletedList" class="queue-list"><div class="queue-empty">No completed tasks yet</div></div>
        </div>
        <div class="queue-column">
            <h4>Recent Failed</h4>
            <div id="queueFailedList" class="queue-list"><div class="queue-empty">No failed tasks</div></div>
        </div>
    </div>

    <details class="insights-collapsible" id="oneTimeTasksSection" open>
        <summary class="insights-summary">One-time tasks (per identity) — create / manage</summary>
        <div style="padding: 0.5rem 0;">
            <p style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.5rem;">Each resident can complete each task once for a bonus. Residents see only tasks they have not completed. New tasks are locked to identities that exist on disk at creation (identity records in .swarm/identities). You can swap which identity is active; eligibility is per identity on disk, not who is currently inhabited.</p>
            <div id="oneTimeTasksList" class="queue-list" style="margin-bottom: 0.75rem;"><div class="queue-empty">Loading…</div></div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: flex-end;">
                <input type="text" id="oneTimeTaskId" placeholder="Task (e.g. one_time_my_task)" style="width: 14rem; padding: 0.3rem; font-size: 0.8rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 5px;" />
                <input type="number" id="oneTimeTaskBonus" placeholder="Bonus" min="0" step="1" value="25" style="width: 4rem; padding: 0.3rem; font-size: 0.8rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 5px;" title="Bonus tokens" />
                <textarea id="oneTimeTaskPrompt" placeholder="Prompt for residents…" rows="2" style="width: 20rem; padding: 0.3rem; font-size: 0.8rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 5px; resize: vertical;"></textarea>
                <button type="button" class="control-btn" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;" onclick="addOneTimeTaskFromUI()">Add one-time task</button>
            </div>
        </div>
    </details>

    <details class="insights-collapsible">
        <summary class="insights-summary">Stats</summary>
        <div class="insights-strip" id="insightCards">
            <details class="insight-card" open>
                <summary>
                    <div class="insight-label">Loading</div>
                    <div class="insight-value">--</div>
                    <div class="insight-sub">Fetching metrics…</div>
                </summary>
                <div class="insight-detail">Insights API is loading.</div>
            </details>
        </div>
    </details>

    <!-- Identities slide-out toggle (cards show token wallet per identity) -->
    <div class="slideout-toggle identities-toggle" onclick="toggleIdentitiesSlideout()" title="Identities and token wallet balances">
        Identities
    </div>

    <!-- Identities slide-out overlay -->
    <div class="slideout-overlay identities-overlay" id="identitiesSlideoutOverlay" onclick="toggleIdentitiesSlideout()"></div>

    <!-- Identities slide-out panel -->
    <div class="slideout-panel identities-panel" id="identitiesSlideoutPanel">
        <div class="slideout-header">
            <h3>Identities <span id="identityDrawerCount" style="font-size:0.8rem; color: var(--text-dim);"></span></h3>
            <button class="slideout-close" onclick="toggleIdentitiesSlideout()">&times;</button>
        </div>
        <div class="slideout-content" id="identitiesDrawerContainer">
            <p style="color: var(--text-dim);">No identities yet</p>
        </div>
    </div>

    <!-- Completed requests slide-out toggle button -->
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
            <!-- Legacy inline identities list (hidden; right drawer is canonical) -->
            <h3 style="display: none; align-items: center; justify-content: space-between;">
                <span>Identities</span>
                <span id="identityCount" style="font-size: 0.7rem; color: var(--text-dim); font-weight: normal;"></span>
            </h3>
            <div id="identities" style="display:none;">
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
                        <label style="font-size: 0.7rem; color: var(--text-dim); display: block; margin-bottom: 0.25rem;">
                            Human username (shown to residents)
                        </label>
                        <input type="text" id="humanUsername" value="human" maxlength="48" onchange="persistUiSettings()"
                            placeholder="human"
                            style="width: 100%; padding: 0.35rem; margin-bottom: 0.35rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.78rem;">
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

            <!-- Collapsible: Spend, Model & Pace (speed control here) -->
            <details class="sidebar-section" open>
                <summary>Spend, Model & Pace</summary>
                <div class="sidebar-section-content">
            <div class="identity-card">
                <div class="identity-stat">
                    <span>Spent (24h)</span>
                    <span class="stat-value" id="spent24h">--</span>
                </div>
                <div class="identity-stat">
                    <span>Total Spent</span>
                    <span class="stat-value" id="totalSpent">--</span>
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

                <!-- Runtime pace -->
                <div id="manualScaleControls" style="margin-top: 0.75rem;">
                    <label style="font-size: 0.8rem; color: var(--text-dim);">Audit Pace (seconds): <span id="sessionCount" style="color: var(--teal);">2</span>s</label>
                    <input type="range" id="sessionSlider" min="0" max="120" value="2" step="1"
                           oninput="updateSessionCount(this.value)"
                           style="width: 100%; margin-top: 0.3rem; accent-color: var(--teal);">
                    <p style="font-size: 0.7rem; color: var(--text-dim); margin-top: 0.3rem;">
                        Wait between queue checks in the worker loop (human-auditable pace)
                    </p>
                </div>

                <!-- Task spend defaults -->
                <div id="autoScaleControls" style="display: block; margin-top: 0.75rem;">
                    <div style="font-size: 0.8rem; color: var(--text-dim); margin-bottom: 0.25rem;">
                        New Task Spend Defaults
                    </div>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                        <label style="font-size: 0.75rem; color: var(--text-dim);">
                            Min $
                            <input type="number" id="taskMinBudget" value="0.05"
                                   step="0.01" min="0.00" onchange="updateBudgetLimit(this.value)"
                                   style="width: 70px; padding: 0.2rem; background: var(--bg-dark);
                                          border: 1px solid var(--border); color: var(--yellow);
                                          border-radius: 4px; font-size: 0.85rem;">
                        </label>
                        <label style="font-size: 0.75rem; color: var(--text-dim);">
                            Max $
                            <input type="number" id="taskMaxBudget" value="0.10"
                                   step="0.01" min="0.00" onchange="updateBudgetLimit(this.value)"
                                   style="width: 70px; padding: 0.2rem; background: var(--bg-dark);
                                          border: 1px solid var(--border); color: var(--yellow);
                                          border-radius: 4px; font-size: 0.85rem;">
                        </label>
                    </div>
                    <p style="font-size: 0.7rem; color: var(--text-dim); margin-top: 0.3rem;">
                        Applied automatically to tasks created from Add Task and Collaboration Request.
                    </p>
                </div>

                <button onclick="saveRuntimeSpeed()"
                    style="margin-top: 0.75rem; width: 100%; padding: 0.3rem; background: var(--bg-hover);
                           border: 1px solid var(--border); color: var(--text); border-radius: 4px;
                           cursor: pointer; font-size: 0.75rem;">
                    Save Runtime + Budget Defaults
                </button>
                <div id="runtimeSpeedStatus" style="font-size: 0.65rem; color: var(--green); margin-top: 0.3rem; text-align: center;"></div>
            </div>
                </div>
            </details>

            <!-- Collapsible: Groq API Key -->
            <details class="sidebar-section">
                <summary>
                    Groq API
                    <span id="groqKeyBadge" style="font-size: 0.65rem; color: var(--text-dim);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div class="identity-card">
                        <div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.4rem;">
                            Attach your own Groq key for live LLM calls.
                        </div>
                        <input type="password" id="groqApiKeyInput" placeholder="gsk_..."
                            style="width: 100%; padding: 0.35rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px;
                                   font-size: 0.8rem; margin-bottom: 0.35rem;">
                        <div style="display: flex; gap: 0.35rem;">
                            <button onclick="saveGroqApiKey()"
                                style="flex: 1; padding: 0.3rem; background: var(--teal); border: none;
                                       color: var(--bg-dark); border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600;">
                                Save Key
                            </button>
                            <button onclick="clearGroqApiKey()"
                                style="padding: 0.3rem 0.5rem; background: var(--bg-hover); border: 1px solid var(--border);
                                       color: var(--text); border-radius: 4px; cursor: pointer; font-size: 0.72rem;">
                                Clear
                            </button>
                        </div>
                        <div id="groqKeyStatus" style="font-size: 0.65rem; margin-top: 0.35rem; color: var(--text-dim);"></div>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Time Rollback -->
            <details class="sidebar-section">
                <summary>
                    Time Rollback
                    <span id="rollbackBadge" style="font-size: 0.65rem; color: var(--orange);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div class="identity-card">
                        <div style="font-size: 0.68rem; color: var(--text-dim); margin-bottom: 0.35rem;">
                            Rewind mutable world state to a checkpoint from N day(s) ago.
                            This affects queue/artifacts/state under mutable scope.
                        </div>
                        <div style="display: flex; gap: 0.35rem; align-items: center; margin-bottom: 0.35rem;">
                            <input type="number" id="rollbackDays" min="1" max="180" value="1"
                                style="width: 86px; padding: 0.28rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.78rem;">
                            <button onclick="previewRollbackByDays()"
                                style="flex: 1; padding: 0.28rem; background: var(--bg-hover); border: 1px solid var(--border);
                                       color: var(--text); border-radius: 4px; cursor: pointer; font-size: 0.75rem;">
                                Preview
                            </button>
                            <button onclick="runRollbackByDays()"
                                style="padding: 0.28rem 0.45rem; background: var(--red); border: none;
                                       color: white; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600;">
                                Rollback
                            </button>
                        </div>
                        <div id="rollbackStatus" style="font-size: 0.65rem; color: var(--text-dim); margin-bottom: 0.3rem;"></div>
                        <div id="rollbackPreview" style="max-height: 140px; overflow-y: auto; font-size: 0.7rem; color: var(--text-dim);"></div>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Fresh Reset -->
            <details class="sidebar-section">
                <summary>Fresh Reset</summary>
                <div class="sidebar-section-content">
                    <div class="identity-card">
                        <div style="font-size: 0.68rem; color: var(--text-dim); margin-bottom: 0.35rem;">
                            Wipe stale runtime state (queue/logs/generated artifacts/transient swarm files) and reset to a clean slate.
                        </div>
                        <button onclick="runFreshStateReset()"
                            style="width: 100%; padding: 0.32rem; background: var(--red); border: none;
                                   color: white; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600;">
                            Wipe stale runtime state
                        </button>
                        <div id="freshResetStatus" style="font-size: 0.65rem; color: var(--text-dim); margin-top: 0.35rem;"></div>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Identity Forge -->
            <details class="sidebar-section">
                <summary>Identity Forge</summary>
                <div class="sidebar-section-content">
                    <div class="identity-card">
                        <div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.35rem;">
                            Resident-driven identity creation. No preset names.
                            Inspiration is fine; exact copying of examples/other identities is not.
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.35rem; margin-bottom: 0.3rem;">
                            <span style="font-size: 0.68rem; color: var(--text-dim);">Fresh creativity seed:</span>
                            <code id="creativeSeedValue" style="font-size: 0.75rem; color: var(--yellow); background: var(--bg-dark); padding: 0.12rem 0.35rem; border-radius: 4px;">--</code>
                            <button type="button" onclick="refreshCreativeSeed()"
                                style="margin-left: auto; padding: 0.2rem 0.45rem; background: var(--bg-hover); border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.7rem; cursor: pointer;">
                                New
                            </button>
                        </div>
                        <select id="identityCreatorSelect"
                            style="width: 100%; padding: 0.32rem; margin-bottom: 0.3rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.78rem;">
                            <option value="">Creator identity (optional)</option>
                        </select>
                        <input type="text" id="newIdentityName" placeholder="Name (self-chosen)"
                            style="width: 100%; padding: 0.35rem; margin-bottom: 0.3rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.8rem;">
                        <textarea id="newIdentitySummary" placeholder="Creative identity spark / summary"
                            style="width: 100%; height: 56px; margin-bottom: 0.3rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px;
                                   padding: 0.35rem; font-size: 0.78rem; resize: vertical;"></textarea>
                        <input type="text" id="newIdentityTraits" placeholder="Traits (comma-separated)"
                            style="width: 100%; padding: 0.35rem; margin-bottom: 0.25rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.75rem;">
                        <input type="text" id="newIdentityValues" placeholder="Values (comma-separated)"
                            style="width: 100%; padding: 0.35rem; margin-bottom: 0.25rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.75rem;">
                        <input type="text" id="newIdentityActivities" placeholder="Preferred activities (comma-separated)"
                            style="width: 100%; padding: 0.35rem; margin-bottom: 0.3rem; background: var(--bg-dark);
                                   border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.75rem;">
                        <button onclick="createResidentIdentity()"
                            style="width: 100%; padding: 0.3rem; background: var(--purple); border: none;
                                   color: white; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600;">
                            Create Identity
                        </button>
                        <div id="identityCreateStatus" style="font-size: 0.65rem; margin-top: 0.35rem; color: var(--text-dim);"></div>
                    </div>
                </div>
            </details>

            <!-- Legacy: Messages (hidden; mailbox is canonical) -->
            <details class="sidebar-section" style="display:none;">
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

            <!-- Legacy: Direct Messages (hidden; mailbox is canonical) -->
            <details class="sidebar-section" style="display:none;">
                <summary>
                    Direct Messages
                    <span id="dmThreadCount" style="font-size: 0.65rem; color: var(--purple);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div class="identity-card" style="margin-bottom: 0.5rem;">
                        <div style="display: flex; gap: 0.35rem; margin-bottom: 0.3rem;">
                            <select id="dmFromIdentity"
                                style="flex: 1; padding: 0.32rem; background: var(--bg-dark);
                                       border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.75rem;"
                                onchange="loadDmThreads()">
                                <option value="">From identity</option>
                            </select>
                            <select id="dmToIdentity"
                                style="flex: 1; padding: 0.32rem; background: var(--bg-dark);
                                       border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.75rem;">
                                <option value="">To identity</option>
                            </select>
                        </div>
                        <textarea id="dmMessageInput" placeholder="Private message..."
                            style="width: 100%; height: 52px; background: var(--bg-dark); border: 1px solid var(--border);
                                   color: var(--text); padding: 0.35rem; border-radius: 4px; font-size: 0.75rem; resize: vertical;"></textarea>
                        <button onclick="sendDirectMessage()"
                            style="margin-top: 0.35rem; width: 100%; padding: 0.3rem; background: var(--purple); border: none;
                                   color: white; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600;">
                            Send DM
                        </button>
                        <div id="dmStatus" style="font-size: 0.65rem; margin-top: 0.35rem; color: var(--text-dim);"></div>
                    </div>
                    <div id="dmThreadsContainer" style="max-height: 170px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.72rem;">No DM threads yet</p>
                    </div>
                    <div id="dmConversationContainer" style="max-height: 220px; overflow-y: auto; margin-top: 0.35rem;">
                        <p style="color: var(--text-dim); font-size: 0.72rem;">Select a DM thread to view messages</p>
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
                    <div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.35rem;">
                        Open any room in a large popout for easier monitoring.
                    </div>
                    <div id="chatRoomsContainer" style="max-height: 300px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.75rem;">Loading rooms...</p>
                    </div>
                </div>
            </details>

            <!-- Collapsible: Recent Artifacts -->
            <details class="sidebar-section">
                <summary>
                    Artifacts
                    <span id="artifactCount" style="font-size: 0.65rem; color: var(--purple);"></span>
                </summary>
                <div class="sidebar-section-content">
                    <div id="artifactsContainer" style="max-height: 220px; overflow-y: auto;">
                        <p style="color: var(--text-dim); font-size: 0.75rem;">No artifacts yet</p>
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
                    <button class="filter-btn" data-filter="JOURNAL">Journal</button>
                    <button class="filter-btn" data-filter="IDENTITY">Identity</button>
                    <button type="button" class="filter-btn" onclick="openFullLogModal()" style="margin-left: auto;" title="Load full log (up to 5000 entries, optionally by resident day)">Full log</button>
                </div>
            </div>
            <div style="padding: 0.4rem 1rem; background: var(--bg-dark); border-bottom: 2px solid var(--border); display: flex; gap: 1rem; font-size: 0.7rem; font-weight: 600; color: var(--text-dim);">
                <span style="min-width: 80px;">Time</span>
                <span style="min-width: 64px;">Day</span>
                <span style="min-width: 100px;">Actor</span>
                <span style="min-width: 70px;">Type</span>
                <span style="min-width: 100px;">Action</span>
                <span style="min-width: 130px;">Task</span>
                <span style="min-width: 120px;">Hat</span>
                <span style="min-width: 110px;">Usage</span>
                <span style="min-width: 80px;">Model</span>
                <span style="flex: 1;">Detail</span>
            </div>
            <div class="log-container" id="logContainer">
                <div id="logEmptyState" class="log-empty">Waiting for log entries...</div>
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

    <div id="chatRoomModal" class="chatroom-modal" onclick="handleChatRoomModalBackdrop(event)">
        <div class="chatroom-modal-panel">
            <div class="chatroom-modal-header">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span id="chatRoomModalIcon" style="font-size: 1.2rem;">💬</span>
                    <div>
                        <div id="chatRoomModalTitle" style="font-size: 1rem; font-weight: 700; color: var(--teal);">Chat Room</div>
                        <div id="chatRoomModalSubtitle" style="font-size: 0.72rem; color: var(--text-dim);">Live room feed</div>
                    </div>
                </div>
                <button class="chat-room-open-btn" style="background: var(--red); color: white;" onclick="closeChatRoomModal()">Close</button>
            </div>
            <div id="chatRoomModalMeta" class="chatroom-modal-meta">Loading room…</div>
            <div id="chatRoomModalMessages" class="chatroom-modal-messages">
                <p style="color: var(--text-dim); font-size: 0.8rem;">Loading messages...</p>
            </div>
        </div>
    </div>

    <div id="fullLogModal" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 999; flex-direction: column; padding: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <label style="font-size: 0.8rem; color: var(--text-dim);"><input type="checkbox" id="fullLogGroupByDay" onchange="renderFullLogContent()"> Group by resident day</label>
            <button type="button" class="control-btn" onclick="closeFullLogModal()">Close</button>
        </div>
        <div id="fullLogModalContent" style="flex: 1; overflow: auto; background: var(--bg-dark); border: 1px solid var(--border); border-radius: 8px; padding: 0.5rem; font-size: 0.72rem; font-family: monospace;">
            Loading…
        </div>
    </div>

    <div id="mailboxModal" class="mailbox-modal" onclick="handleMailboxBackdrop(event)">
        <div class="mailbox-phone">
            <div class="mailbox-head">
                <div>
                    <div style="font-size: 0.95rem; color: var(--teal); font-weight: 700;">Communication Mailbox</div>
                    <div id="mailboxSubhead" style="font-size: 0.68rem; color: var(--text-dim);">Phone-style async chat</div>
                </div>
                <button class="chat-room-open-btn" style="background: var(--red); color: white;" onclick="closeMailboxModal()">Close</button>
            </div>
            <div id="mailboxThreads" class="mailbox-threads">
                <p style="color: var(--text-dim); font-size: 0.75rem;">Loading threads...</p>
            </div>
            <div id="mailboxMessages" class="mailbox-messages">
                <p style="color: var(--text-dim); font-size: 0.75rem;">Select a thread to start chatting.</p>
            </div>
            <div class="mailbox-compose">
                <div style="display: flex; gap: 0.4rem; margin-bottom: 0.35rem;">
                    <select id="mailboxTarget" style="flex: 1; padding: 0.32rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 5px; font-size: 0.74rem;">
                        <option value="">Target resident (optional)</option>
                    </select>
                    <button class="chat-room-open-btn" onclick="sendMailboxMessage()">Send</button>
                </div>
                <textarea id="mailboxComposer" placeholder="Send message to a resident (or broadcast if target is blank)..."
                    style="width: 100%; height: 72px; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); padding: 0.45rem; border-radius: 6px; font-size: 0.78rem; resize: vertical;"></textarea>
                <div style="margin-top: 0.55rem; padding-top: 0.55rem; border-top: 1px dashed var(--border);">
                    <div style="font-size: 0.72rem; color: var(--yellow); margin-bottom: 0.25rem;">Assign Quest</div>
                    <input id="questTitleInput" type="text" placeholder="Quest title"
                        style="width: 100%; margin-bottom: 0.25rem; padding: 0.34rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 5px; font-size: 0.73rem;">
                    <textarea id="questPromptInput" placeholder="Quest objective for selected resident..."
                        style="width: 100%; height: 60px; margin-bottom: 0.3rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); padding: 0.4rem; border-radius: 6px; font-size: 0.75rem; resize: vertical;"></textarea>
                    <div style="display:flex; gap:0.35rem; margin-bottom:0.15rem;">
                        <label for="questBudgetInput" style="width:33%; font-size:0.65rem; color:var(--text-dim);">Budget ($)</label>
                        <label for="questTipInput" style="width:33%; font-size:0.65rem; color:var(--text-dim);">Upfront tip</label>
                        <label for="questRewardInput" style="width:34%; font-size:0.65rem; color:var(--text-dim);">Completion reward</label>
                    </div>
                    <div style="display:flex; gap:0.35rem; margin-bottom:0.3rem;">
                        <input id="questBudgetInput" type="number" min="0.01" step="0.01" value="0.20"
                            title="Quest token budget ($)" style="width:33%; padding:0.32rem; background:var(--bg-dark); border:1px solid var(--border); color:var(--text); border-radius:5px; font-size:0.72rem;">
                        <input id="questTipInput" type="number" min="0" step="1" value="10"
                            title="Upfront free-time tip tokens" style="width:33%; padding:0.32rem; background:var(--bg-dark); border:1px solid var(--border); color:var(--text); border-radius:5px; font-size:0.72rem;">
                        <input id="questRewardInput" type="number" min="0" step="1" value="30"
                            title="Completion reward tokens (manual approval)" style="width:34%; padding:0.32rem; background:var(--bg-dark); border:1px solid var(--border); color:var(--text); border-radius:5px; font-size:0.72rem;">
                    </div>
                    <button class="chat-room-open-btn" style="width:100%;" onclick="createMailboxQuest()">Assign Quest</button>
                    <div id="questStatus" style="font-size: 0.68rem; color: var(--text-dim); margin-top: 0.25rem;"></div>
                    <div id="questProgressContainer" style="max-height: 150px; overflow-y: auto; margin-top: 0.4rem;"></div>
                </div>
                <div id="mailboxStatus" style="font-size: 0.68rem; color: var(--text-dim); margin-top: 0.3rem;"></div>
            </div>
        </div>
    </div>

    <script>
        const socket = (typeof io === 'function') ? io() : null;
        let entryCount = 0;
        let isStopped = false;
        let connectedAt = Date.now();
        let currentFilter = 'all';
        const seenLogKeys = new Set();
        const LOG_DAY_TOOLTIP = 'Compressed timescale "day" for residents. Helps them roleplay as people and helps you conceptualize their timescale.';
        let liveLogBaselineCycle = null;
        let currentRuntimeCycleId = null;
        let dayVibeBaselineCycle = null;
        let mailboxData = { threads: [], thread_messages: {}, identities: [], unread_count: 0 };
        const DRAFT_STORAGE_KEY = 'vivarium_ui_drafts';
        let draftSaveTimer = null;

        function restoreDraftInputs() {
            try {
                const raw = localStorage.getItem(DRAFT_STORAGE_KEY);
                if (!raw) return;
                const drafts = JSON.parse(raw);
                const set = (id, val) => { const el = document.getElementById(id); if (el && val != null && val !== '') el.value = val; };
                set('humanRequest', drafts.humanRequest);
                set('addTaskId', drafts.addTaskId);
                set('addTaskInstruction', drafts.addTaskInstruction);
                set('oneTimeTaskId', drafts.oneTimeTaskId);
                set('oneTimeTaskPrompt', drafts.oneTimeTaskPrompt);
                if (drafts.oneTimeTaskBonus != null) set('oneTimeTaskBonus', String(drafts.oneTimeTaskBonus));
            } catch (e) {}
        }
        function persistDraftInputs(immediate) {
            const save = () => {
                try {
                    const get = (id) => { const el = document.getElementById(id); return el ? (el.value || '').trim() : ''; };
                    const drafts = {
                        humanRequest: get('humanRequest'),
                        addTaskId: get('addTaskId'),
                        addTaskInstruction: get('addTaskInstruction'),
                        oneTimeTaskId: get('oneTimeTaskId'),
                        oneTimeTaskPrompt: get('oneTimeTaskPrompt'),
                        oneTimeTaskBonus: get('oneTimeTaskBonus'),
                    };
                    localStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify(drafts));
                } catch (e) {}
                draftSaveTimer = null;
            };
            if (draftSaveTimer) clearTimeout(draftSaveTimer);
            draftSaveTimer = null;
            if (immediate) save();
            else draftSaveTimer = setTimeout(save, 300);
        }
        function bindDraftInputs() {
            ['humanRequest', 'addTaskId', 'addTaskInstruction', 'oneTimeTaskId', 'oneTimeTaskPrompt', 'oneTimeTaskBonus'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.addEventListener('input', persistDraftInputs);
            });
        }

        function showToast(message, tone = 'success') {
            const existing = document.getElementById('globalToast');
            if (existing) existing.remove();
            const toast = document.createElement('div');
            toast.id = 'globalToast';
            toast.style.cssText = 'position: fixed; bottom: 1rem; right: 1rem; padding: 0.5rem 1rem; border-radius: 6px; z-index: 9999; font-size: 0.8rem; color: var(--bg-dark); box-shadow: 0 2px 8px rgba(0,0,0,0.3);';
            toast.style.background = tone === 'error' ? 'var(--red)' : (tone === 'info' ? 'var(--teal)' : 'var(--green)');
            toast.textContent = message;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }
        let activeMailboxThreadId = null;
        let mailboxPoller = null;
        let mailboxQuests = [];

        function parseTimestampMillis(timestamp) {
            const millis = Date.parse(timestamp || '');
            return Number.isFinite(millis) ? millis : null;
        }

        function parseTokenUsage(detail) {
            const text = String(detail || '');
            const m = text.match(/(\d+)\s*tokens?\b/i);
            if (!m) return null;
            const n = Number(m[1]);
            return Number.isFinite(n) ? n : null;
        }

        function parseUsdCost(detail) {
            const text = String(detail || '');
            const matches = Array.from(text.matchAll(/\$([0-9]+(?:\.[0-9]+)?)/g));
            if (!matches.length) return null;
            const n = Number(matches[matches.length - 1][1]);
            return Number.isFinite(n) ? n : null;
        }

        function tsToResidentCycle(timestamp, cycleSeconds) {
            const millis = parseTimestampMillis(timestamp);
            if (millis == null) return null;
            const cycleSec = Math.max(1, Number(cycleSeconds || 10));
            return Math.floor((millis / 1000) / cycleSec);
        }

        function cycleToDisplayDay(cycleId, baselineCycle) {
            if (cycleId == null) return null;
            if (baselineCycle == null) return 1;
            const value = (cycleId - baselineCycle) + 1;
            return Number.isFinite(value) ? Math.max(1, value) : null;
        }

        // Update connected time
        setInterval(() => {
            const secs = Math.floor((Date.now() - connectedAt) / 1000);
            document.getElementById('connectedTime').textContent = `${secs}s`;
        }, 1000);

        // Socket events (optional; page still works without CDN socket.io)
        if (socket) {
            socket.on('connect', () => {
                console.log('Connected to control panel');
                loadRecentLogs();
                loadWorkerStatus();
                loadStopStatus();
                loadRuntimeSpeed();
                loadGroqKeyStatus();
                loadSwarmInsights();
                loadMailboxData();
            });

            socket.on('disconnect', () => {
                console.log('Disconnected');
                const dot = document.getElementById('workerDot');
                if (dot) dot.classList.add('stopped');
            });

            socket.on('log_entry', (entry) => {
                addLogEntry(entry);
            });

            socket.on('identities', (data) => {
                updateIdentities(data);
            });

            socket.on('spawner_started', () => { refreshWorkerStatus(); });
            socket.on('spawner_paused', () => { refreshWorkerStatus(); });
            socket.on('spawner_resumed', () => { refreshWorkerStatus(); });
            socket.on('spawner_killed', () => { refreshWorkerStatus(); });

            socket.on('stop_status', (data) => {
                isStopped = !!(data && data.stopped);
                updateKillSwitchUI();
            });
        } else {
            console.warn('socket.io unavailable; using polling-only UI mode');
        }

        function addLogEntry(entry) {
            const entryKey = [
                entry.timestamp || '',
                entry.actor || '',
                entry.action_type || '',
                entry.action || '',
                entry.detail || '',
            ].join('|');
            if (seenLogKeys.has(entryKey)) {
                return;
            }
            seenLogKeys.add(entryKey);

            const container = document.getElementById('logContainer');
            const emptyEl = document.getElementById('logEmptyState');
            if (emptyEl) emptyEl.style.display = 'none';
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

            // Parse timestamp; "day" = resident (machine) cycle day, not human weekday
            let timeStr = '--:--:--';
            let dayStr = '---';
            const timestampMs = parseTimestampMillis(entry.timestamp);
            const residentCycle = tsToResidentCycle(entry.timestamp, logCycleSeconds);
            if (timestampMs != null) {
                const dt = new Date(timestampMs);
                timeStr = dt.toTimeString().split(' ')[0];
            }
            if (residentCycle != null) {
                if (liveLogBaselineCycle == null || residentCycle < liveLogBaselineCycle) {
                    liveLogBaselineCycle = residentCycle;
                }
                const displayDay = cycleToDisplayDay(residentCycle, liveLogBaselineCycle);
                dayStr = displayDay != null ? ('Day ' + displayDay) : '---';
            }
            const calendarDay = timestampMs != null
                ? new Date(timestampMs).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
                : '';
            const cycleHint = residentCycle != null ? ` Resident cycle id: ${residentCycle}.` : '';
            const dayTitle = calendarDay ? `${LOG_DAY_TOOLTIP} Calendar day: ${calendarDay}.${cycleHint}` : `${LOG_DAY_TOOLTIP}${cycleHint}`;
            const dayTitleHtml = dayTitle.replace(/"/g, '&quot;');

            // Make file paths clickable in detail
            const linkedDetail = linkifyFilePaths(entry.detail || '');
            const modelStr = entry.model || (entry.metadata && entry.metadata.model) ? (entry.model || entry.metadata.model || '') : '';
            const modelSpan = modelStr ? `<span class="log-model" style="font-size:0.65rem; color:var(--yellow);" title="Model">${modelStr}</span>` : '';
            const taskId = (entry.metadata && entry.metadata.task_id) || entry.task_id || '';
            const taskSpan = taskId ? `<span class="log-task" title="Task ID">${taskId}</span>` : `<span class="log-task">-</span>`;
            const hatName = (entry.metadata && entry.metadata.hat_name) || entry.hat_name || '';
            const hatSpan = hatName ? `<span class="log-hat" title="Hat overlay">${hatName}</span>` : `<span class="log-hat">-</span>`;
            const tokenCount = (entry.metadata && Number.isFinite(Number(entry.metadata.total_tokens)))
                ? Number(entry.metadata.total_tokens)
                : parseTokenUsage(entry.detail);
            const usdCost = (entry.metadata && Number.isFinite(Number(entry.metadata.usd_cost)))
                ? Number(entry.metadata.usd_cost)
                : parseUsdCost(entry.detail);
            const usageParts = [];
            if (tokenCount != null) usageParts.push(`${tokenCount}t`);
            if (usdCost != null) usageParts.push(`$${usdCost.toFixed(6)}`);
            const usageSpan = `<span class="log-usage" title="Token/API cost">${usageParts.length ? usageParts.join(' | ') : '-'}</span>`;

            div.innerHTML = `
                <span class="log-time">${timeStr}</span>
                <span class="log-day" title="${dayTitleHtml}">${dayStr}</span>
                <span class="log-actor">${entry.actor || 'UNKNOWN'}</span>
                <span class="log-type type-${entry.action_type}">${entry.action_type}</span>
                <span class="log-action">${entry.action}</span>
                ${taskSpan}
                ${hatSpan}
                ${usageSpan}
                ${modelSpan}
                <span class="log-detail">${linkedDetail}</span>
            `;

            // Apply filter
            if (currentFilter !== 'all' && entry.action_type !== currentFilter) {
                div.style.display = 'none';
            }

            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
            applyLogFilter();
            updateLogEmptyState();

            entryCount++;
            document.getElementById('entryCount').textContent = entryCount;
            document.getElementById('lastUpdate').textContent = timeStr;
        }

        function loadRecentLogs() {
            fetch('/api/logs/recent?limit=500')
                .then(r => r.json())
                .then(data => {
                    if (!data || !data.success) return;
                    const entries = Array.isArray(data.entries) ? data.entries : [];
                    if (entries.length) {
                        const cycles = entries
                            .map(e => tsToResidentCycle(e.timestamp, logCycleSeconds))
                            .filter(c => c != null);
                        if (cycles.length) {
                            liveLogBaselineCycle = Math.min(...cycles);
                        }
                    }
                    entries.forEach(entry => addLogEntry(entry));
                    applyLogFilter();
                    updateLogEmptyState();
                })
                .catch(() => {});
        }

        let fullLogEntries = [];
        let fullLogCycleSeconds = 10;
        let fullLogMeta = { limit: 5000, returned: 0, available: 0, is_truncated: false };
        function openFullLogModal() {
            const modal = document.getElementById('fullLogModal');
            const content = document.getElementById('fullLogModalContent');
            if (!modal || !content) return;
            modal.style.display = 'flex';
            content.textContent = 'Loading…';
            Promise.all([
                fetch('/api/runtime_speed').then(r => r.json()),
                fetch('/api/logs/recent?limit=5000').then(r => r.json()),
            ]).then(([speedData, logData]) => {
                fullLogCycleSeconds = Number(speedData.cycle_seconds) || 10;
                fullLogEntries = Array.isArray(logData.entries) ? logData.entries : [];
                fullLogMeta = {
                    limit: Number(logData.limit || 5000) || 5000,
                    returned: Number(logData.returned || fullLogEntries.length) || fullLogEntries.length,
                    available: Number(logData.available || fullLogEntries.length) || fullLogEntries.length,
                    is_truncated: !!logData.is_truncated,
                };
                renderFullLogContent();
            }).catch(() => { content.textContent = 'Failed to load log.'; });
        }
        function renderFullLogContent() {
            const content = document.getElementById('fullLogModalContent');
            const groupByDay = document.getElementById('fullLogGroupByDay') && document.getElementById('fullLogGroupByDay').checked;
            if (!content) return;
            const cycleSec = Math.max(1, fullLogCycleSeconds);
            const escapeHtml = (s) => {
                const d = document.createElement('div');
                d.textContent = s == null ? '' : s;
                return d.innerHTML;
            };
            const tsToCycle = (ts) => tsToResidentCycle(ts, cycleSec);
            const allCycles = fullLogEntries
                .map(e => tsToCycle(e.timestamp))
                .filter(c => c != null);
            const baselineCycle = allCycles.length ? Math.min(...allCycles) : null;
            const summaryLine = fullLogMeta.is_truncated
                ? `Showing last ${fullLogMeta.returned} of ${fullLogMeta.available} deduplicated entries.`
                : `Showing ${fullLogMeta.returned} deduplicated entries.`;
            const rawLinks = `<div style="margin-top:0.2rem;"><a href="/api/logs/raw?kind=action" target="_blank" rel="noopener" style="color:var(--teal);">Open raw action_log.jsonl</a> · <a href="/api/logs/raw?kind=execution" target="_blank" rel="noopener" style="color:var(--teal);">Open raw execution_log.jsonl</a></div>`;
            const summaryBlock = `<div style="margin-bottom:0.55rem; color:var(--text-dim); font-size:0.74rem;">${escapeHtml(summaryLine)}${rawLinks}</div>`;
            const headerRow = `<div style="display:grid; grid-template-columns: 4rem 6rem 5rem 5rem 7rem 9rem 8rem 8rem 8rem 1fr; gap:0.25rem; padding:0.3rem 0; border-bottom:2px solid var(--border); font-size:0.7rem; font-weight:600; color:var(--text-dim); position:sticky; top:0; background:var(--bg-dark); z-index:1;">
                <span>Time</span>
                <span>Day</span>
                <span>Actor</span>
                <span>Type</span>
                <span>Action</span>
                <span>Task</span>
                <span>Hat</span>
                <span>Usage</span>
                <span>Model</span>
                <span>Detail</span>
            </div>`;
            const formatRow = (e) => {
                const timestampMs = parseTimestampMillis(e.timestamp);
                const dt = timestampMs != null ? new Date(timestampMs) : null;
                const timeStr = dt ? dt.toTimeString().split(' ')[0] : '--:--:--';
                const residentCycle = dt ? tsToCycle(e.timestamp) : null;
                const residentDay = cycleToDisplayDay(residentCycle, baselineCycle);
                const dayStr = residentDay != null ? 'Day ' + residentDay : '---';
                const calendarDay = dt ? dt.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }) : '';
                const cycleHint = residentCycle != null ? ` Resident cycle id: ${residentCycle}.` : '';
                const dayTitle = calendarDay ? `${LOG_DAY_TOOLTIP} Calendar day: ${calendarDay}.${cycleHint}` : `${LOG_DAY_TOOLTIP}${cycleHint}`;
                const detail = e.detail || '';
                const model = e.model || (e.metadata && e.metadata.model) ? escapeHtml(e.model || e.metadata.model || '') : '';
                const taskId = escapeHtml((e.metadata && e.metadata.task_id) || e.task_id || '');
                const hatName = escapeHtml((e.metadata && e.metadata.hat_name) || e.hat_name || '');
                const tokenCount = (e.metadata && Number.isFinite(Number(e.metadata.total_tokens)))
                    ? Number(e.metadata.total_tokens)
                    : parseTokenUsage(detail);
                const usdCost = (e.metadata && Number.isFinite(Number(e.metadata.usd_cost)))
                    ? Number(e.metadata.usd_cost)
                    : parseUsdCost(detail);
                const usageText = [
                    tokenCount != null ? `${tokenCount}t` : '',
                    usdCost != null ? `$${usdCost.toFixed(6)}` : '',
                ].filter(Boolean).join(' | ');
                return `<div style="display:grid; grid-template-columns: 4rem 6rem 5rem 5rem 7rem 9rem 8rem 8rem 8rem 1fr; gap:0.25rem; padding:0.2rem 0; border-bottom:1px solid var(--border); font-size:0.7rem;">` +
                    `<span style="color:var(--text-dim);" title="Clock time">${escapeHtml(timeStr)}</span>` +
                    `<span style="color:var(--text-dim); cursor:help;" title="${escapeHtml(dayTitle)}">${escapeHtml(dayStr)}</span>` +
                    `<span style="color:var(--teal);">${escapeHtml(e.actor || '')}</span>` +
                    `<span class="type-${e.action_type || ''}">${escapeHtml(e.action_type || '')}</span>` +
                    `<span style="color:var(--text-dim);">${escapeHtml(e.action || '')}</span>` +
                    `<span style="color:var(--purple); overflow:hidden; text-overflow:ellipsis;" title="${taskId || ''}">${taskId || '-'}</span>` +
                    `<span style="color:var(--teal); overflow:hidden; text-overflow:ellipsis;" title="${hatName || ''}">${hatName || '-'}</span>` +
                    `<span style="color:var(--yellow);" title="Token/API cost">${escapeHtml(usageText || '-')}</span>` +
                    (model ? `<span style="color:var(--yellow); font-size:0.65rem; overflow:hidden; text-overflow:ellipsis;">${model}</span>` : '<span></span>') +
                    `<span style="word-wrap:break-word; overflow-wrap:break-word; max-height: 8rem; overflow-y: auto; display: block;">${escapeHtml(detail)}</span>` +
                    `</div>`;
            };
            if (groupByDay) {
                const byDay = {};
                fullLogEntries.forEach(e => {
                    const c = tsToCycle(e.timestamp);
                    if (c == null) return;
                    const d = cycleToDisplayDay(c, baselineCycle);
                    if (d == null) return;
                    if (!byDay[d]) byDay[d] = [];
                    byDay[d].push(e);
                });
                const days = Object.keys(byDay).map(Number).sort((a, b) => a - b);
                const groupedHtml = days.map(d => {
                    const rows = byDay[d].map(formatRow).join('');
                    return `<div style="margin-bottom:0.75rem;"><div style="font-weight:700; color:var(--teal); margin-bottom:0.25rem;">Resident day ${d}</div>${headerRow}${rows}</div>`;
                }).join('');
                content.innerHTML = summaryBlock + groupedHtml;
            } else {
                const rowsHtml = fullLogEntries.length ? fullLogEntries.map(formatRow).join('') : '<div style="color:var(--text-dim);">No entries.</div>';
                content.innerHTML = summaryBlock + headerRow + rowsHtml;
            }
        }
        function closeFullLogModal() {
            const modal = document.getElementById('fullLogModal');
            if (modal) modal.style.display = 'none';
        }

        let profileActivityLogEntries = [];
        let profileActivityLogCycles = [];
        let profileActivityLogBaselineCycle = null;
        function loadProfileActivityLog(identityId) {
            const content = document.getElementById('profileActivityLogContent');
            const daySelect = document.getElementById('profileActivityLogDay');
            const countEl = document.getElementById('profileActivityLogCount');
            if (!content || !identityId) return;
            content.innerHTML = 'Loading activity log…';
            fetch('/api/identity/' + encodeURIComponent(identityId) + '/log?limit=5000')
                .then(r => r.json())
                .then(data => {
                    if (!data.success || !Array.isArray(data.entries)) {
                        content.innerHTML = '<span style="color: var(--text-dim);">No log entries for this identity.</span>';
                        return;
                    }
                    profileActivityLogEntries = data.entries;
                    profileActivityLogCycles = data.cycles_with_data || [];
                    const cycleCandidates = profileActivityLogCycles.length
                        ? profileActivityLogCycles
                        : profileActivityLogEntries.map(e => Number(e.cycle_id)).filter(c => Number.isFinite(c));
                    profileActivityLogBaselineCycle = cycleCandidates.length ? Math.min(...cycleCandidates) : null;
                    if (daySelect) {
                        daySelect.innerHTML = '<option value="">All days</option>' +
                            profileActivityLogCycles.map(c => {
                                const display = cycleToDisplayDay(Number(c), profileActivityLogBaselineCycle) || 1;
                                return '<option value="' + c + '">Day ' + display + '</option>';
                            }).join('');
                    }
                    filterProfileActivityLogByDay();
                })
                .catch(() => {
                    if (content) content.innerHTML = '<span style="color: var(--red);">Failed to load log.</span>';
                });
        }
        function filterProfileActivityLogByDay() {
            const content = document.getElementById('profileActivityLogContent');
            const daySelect = document.getElementById('profileActivityLogDay');
            const countEl = document.getElementById('profileActivityLogCount');
            if (!content) return;
            const cycleFilter = daySelect && daySelect.value !== '' ? parseInt(daySelect.value, 10) : null;
            const entries = cycleFilter != null
                ? profileActivityLogEntries.filter(e => e.cycle_id === cycleFilter)
                : profileActivityLogEntries;
            const escapeHtml = (s) => {
                const d = document.createElement('div');
                d.textContent = s == null ? '' : s;
                return d.innerHTML;
            };
            if (countEl) countEl.textContent = entries.length + ' entries';
            if (!entries.length) {
                content.innerHTML = '<span style="color: var(--text-dim);">No entries for this selection.</span>';
                return;
            }
            content.innerHTML = entries.map(e => {
                const dt = e.timestamp ? new Date(e.timestamp) : null;
                const timeStr = dt ? dt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) : '--:--:--';
                const typeColor = e.action_type === 'EXECUTION' ? 'var(--teal)' : e.action_type === 'SAFETY' ? 'var(--orange)' : 'var(--purple)';
                const detail = (e.detail || '').substring(0, 300);
                const modelPart = e.model ? ' <span style="color:var(--yellow); font-size:0.65rem;">[' + escapeHtml(e.model) + ']</span>' : '';
                return '<div style="padding:0.35rem 0; border-bottom:1px solid var(--border);">' +
                    '<span style="color:var(--text-dim);">' + escapeHtml(timeStr) + '</span> ' +
                    '<span style="color:' + typeColor + '; font-weight:600;">' + escapeHtml(e.action_type || '') + '</span> ' +
                    '<span style="color:var(--text);">' + escapeHtml(e.action || '') + '</span>' + modelPart +
                    (detail ? '<div style="margin-top:0.2rem; color:var(--text-dim); font-size:0.68rem;">' + escapeHtml(detail) + '</div>' : '') +
                    '</div>';
            }).join('');
        }

        function updateLogEmptyState() {
            const container = document.getElementById('logContainer');
            const emptyEl = document.getElementById('logEmptyState');
            if (!container || !emptyEl) return;
            const visibleEntries = Array.from(container.querySelectorAll('.log-entry'))
                .filter(el => el.style.display !== 'none');
            if (visibleEntries.length > 0) {
                emptyEl.style.display = 'none';
                return;
            }
            const labels = {
                all: 'No log entries yet.',
                TOOL: 'No TOOL log entries yet.',
                API: 'No API log entries yet.',
                SAFETY: 'No SAFETY log entries yet.',
                SOCIAL: 'No SOCIAL log entries yet.',
                JOURNAL: 'No JOURNAL log entries yet.',
                IDENTITY: 'No IDENTITY log entries yet.',
            };
            emptyEl.textContent = labels[currentFilter] || `No ${currentFilter} log entries yet.`;
            emptyEl.style.display = '';
        }

        function applyLogFilter() {
            document.querySelectorAll('.log-entry').forEach(entry => {
                if (currentFilter === 'all' || entry.dataset.type === currentFilter) {
                    entry.style.display = '';
                } else {
                    entry.style.display = 'none';
                }
            });
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
            const drawerContainer = document.getElementById('identitiesDrawerContainer');
            const countEl = document.getElementById('identityCount');
            const drawerCountEl = document.getElementById('identityDrawerCount');
            if (countEl) countEl.textContent = `(${identities.length})`;
            if (drawerCountEl) drawerCountEl.textContent = `(${identities.length})`;
            populateIdentityCreatorOptions(identities);
            populateDmIdentityOptions(identities);

            // Sort by level (highest first), then by sessions
            identities.sort((a, b) => {
                const levelA = Number.isFinite(Number(a.level)) ? Number(a.level) : -1;
                const levelB = Number.isFinite(Number(b.level)) ? Number(b.level) : -1;
                const levelDiff = levelB - levelA;
                if (levelDiff !== 0) return levelDiff;
                const sessionsA = Number.isFinite(Number(a.sessions)) ? Number(a.sessions) : -1;
                const sessionsB = Number.isFinite(Number(b.sessions)) ? Number(b.sessions) : -1;
                return sessionsB - sessionsA;
            });

            const cardsHtml = identities.map(id => {
                const level = Number.isFinite(Number(id.level)) ? Math.max(0, Math.trunc(Number(id.level))) : null;
                const sessions = Number.isFinite(Number(id.sessions)) ? Math.max(0, Math.trunc(Number(id.sessions))) : null;
                const respecCost = Number.isFinite(Number(id.respec_cost)) ? Math.max(0, Math.trunc(Number(id.respec_cost))) : null;
                const levelLabel = level == null ? 'Lv.--' : `Lv.${level}`;
                const sessionsLabel = sessions == null ? '--' : String(sessions);
                const respecLabel = respecCost == null ? '--' : String(respecCost);
                return `
                <div class="identity-card" style="cursor: pointer;" onclick="showProfile('${id.id}')">
                    ${id.profile_thumbnail_html ? `<div style="margin-bottom: 0.35rem; background: var(--bg-dark); border: 1px solid var(--border); border-radius: 6px; padding: 0.35rem; overflow: hidden;">
                        <style scoped>${id.profile_thumbnail_css || ''}</style>
                        ${id.profile_thumbnail_html}
                    </div>` : ''}
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div class="identity-name">${id.name}</div>
                        <span style="font-size: 0.7rem; color: var(--yellow); background: rgba(255,193,7,0.15);
                                     padding: 0.15rem 0.4rem; border-radius: 4px; font-weight: 600;">
                            ${levelLabel}
                        </span>
                    </div>
                    ${id.profile_display ? `<div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.3rem; font-style: italic;">${id.profile_display.substring(0, 50)}${id.profile_display.length > 50 ? '...' : ''}</div>` : ''}
                    ${id.traits && id.traits.length ? `<div style="font-size: 0.7rem; color: var(--purple); margin-bottom: 0.3rem;">${id.traits.slice(0,3).join(' | ')}</div>` : ''}
                    <div class="identity-stat">
                        <span>Wallet</span>
                        <span class="token-count">${(id.tokens != null ? id.tokens : 0) + (id.journal_tokens != null ? id.journal_tokens : 0)}</span>
                    </div>
                    <div class="identity-stat">
                        <span>Sessions</span>
                        <span>${sessionsLabel}</span>
                    </div>
                    <div class="identity-stat">
                        <span>Respec Cost</span>
                        <span style="color: var(--orange);">${respecLabel}</span>
                    </div>
                </div>
            `;
            }).join('');
            if (container) container.innerHTML = cardsHtml;
            if (drawerContainer) {
                drawerContainer.innerHTML = cardsHtml || '<p style="color: var(--text-dim);">No identities yet</p>';
            }
        }

        function populateIdentityCreatorOptions(identities) {
            const select = document.getElementById('identityCreatorSelect');
            if (!select) return;
            const previous = select.value;
            const options = ['<option value="">Creator identity (optional)</option>'];
            identities.forEach((identity) => {
                options.push(
                    `<option value="${identity.id}">${identity.name} (${identity.id})</option>`
                );
            });
            select.innerHTML = options.join('');
            if (previous && identities.some((identity) => identity.id === previous)) {
                select.value = previous;
            }
        }

        function populateDmIdentityOptions(identities) {
            const fromSelect = document.getElementById('dmFromIdentity');
            const toSelect = document.getElementById('dmToIdentity');
            if (!fromSelect || !toSelect) return;
            const prevFrom = fromSelect.value;
            const prevTo = toSelect.value;
            const options = ['<option value="">Select identity</option>'];
            identities.forEach((identity) => {
                options.push(`<option value="${identity.id}">${identity.name} (${identity.id})</option>`);
            });
            fromSelect.innerHTML = options.join('');
            toSelect.innerHTML = options.join('');
            if (prevFrom && identities.some((i) => i.id === prevFrom)) fromSelect.value = prevFrom;
            if (prevTo && identities.some((i) => i.id === prevTo)) toSelect.value = prevTo;
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
                    const escapeHtml = (value) => {
                        const div = document.createElement('div');
                        div.textContent = value == null ? '' : String(value);
                        return div.innerHTML;
                    };

                    const createdAt = data.created_at ? new Date(data.created_at) : null;
                    const createdDisplay = createdAt && !Number.isNaN(createdAt.getTime())
                        ? createdAt.toLocaleDateString() : 'n/a';
                    const levelValue = Number.isFinite(Number(data.level)) ? Math.max(0, Math.trunc(Number(data.level))) : null;
                    const sessionsValue = Number.isFinite(Number(data.sessions)) ? Math.max(0, Math.trunc(Number(data.sessions))) : null;
                    const tasksCompletedValue = Number.isFinite(Number(data.tasks_completed)) ? Math.max(0, Math.trunc(Number(data.tasks_completed))) : null;
                    const successRateValue = Number.isFinite(Number(data.task_success_rate))
                        ? Math.max(0, Math.min(100, Number(data.task_success_rate))) : null;
                    const respecCostValue = Number.isFinite(Number(data.respec_cost))
                        ? Math.max(0, Math.trunc(Number(data.respec_cost))) : null;

                    let content = `<h2 style="color: var(--teal); margin-bottom: 0.5rem;">${data.name}</h2>`;
                    content += `<div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 1rem;">Created: ${createdDisplay}</div>`;

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

                    // Stats bar (row 1) — Level, Days, Tasks, Success, Wallet
                    const freeTime = data.tokens != null ? data.tokens : 0;
                    const journalTokens = data.journal_tokens != null ? data.journal_tokens : 0;
                    const totalWallet = freeTime + journalTokens;
                    const successColor = successRateValue == null
                        ? 'var(--text-dim)'
                        : (successRateValue >= 80 ? 'var(--green)' : successRateValue >= 50 ? 'var(--yellow)' : 'var(--red)');
                    const successLabel = successRateValue == null ? '--' : `${successRateValue}%`;
                    content += `<div style="display: flex; gap: 1rem; margin-bottom: 0.5rem; padding: 0.75rem; background: var(--bg-dark); border-radius: 8px; flex-wrap: wrap;">
                        <div style="text-align: center; flex: 1; min-width: 3rem;"><div style="font-size: 1.5rem; color: var(--yellow);">${levelValue == null ? '--' : levelValue}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Level</div></div>
                        <div style="text-align: center; flex: 1; min-width: 3rem;"><div style="font-size: 1.5rem; color: var(--teal);">${sessionsValue == null ? '--' : sessionsValue}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Days</div></div>
                        <div style="text-align: center; flex: 1; min-width: 3rem;"><div style="font-size: 1.5rem; color: var(--green);">${tasksCompletedValue == null ? '--' : tasksCompletedValue}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Tasks</div></div>
                        <div style="text-align: center; flex: 1; min-width: 3rem;"><div style="font-size: 1.5rem; color: ${successColor}">${successLabel}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Success</div></div>
                        <div style="text-align: center; flex: 1; min-width: 3rem;"><div style="font-size: 1.5rem; color: var(--yellow);">${totalWallet}</div><div style="font-size: 0.7rem; color: var(--text-dim);">Wallet</div><div style="font-size: 0.65rem; color: var(--text-dim);">${freeTime} free + ${journalTokens} journal</div></div>
                    </div>`;
                    // Stats bar (row 2 - respec info)
                    content += `<div style="display: flex; gap: 1rem; margin-bottom: 1rem; padding: 0.5rem 0.75rem; background: var(--bg-dark); border-radius: 8px; font-size: 0.8rem;">
                        <div style="flex: 1; color: var(--text-dim);">Respec Cost: <span style="color: var(--orange); font-weight: 600;">${respecCostValue == null ? 'n/a' : `${respecCostValue} tokens`}</span></div>
                        <div style="color: var(--text-dim); font-size: 0.7rem;">Level formula: sqrt(days) | Respec: 10 + (days × 3)</div>
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
                    if (mutable.current_focus) {
                        content += `<div style="margin-bottom: 0.5rem; font-size: 0.85rem;"><span style="color: var(--text-dim);">Focus:</span> ${mutable.current_focus}</div>`;
                    }

                    const identityDoc = data.identity_document || {};
                    content += `<details style="margin-top: 0.5rem;"><summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">Full Identity JSON</summary>
                        <pre style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem; max-height: 360px; overflow: auto; font-size: 0.7rem; line-height: 1.35;">${escapeHtml(JSON.stringify(identityDoc, null, 2))}</pre>
                    </details>`;

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
                            <div style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem; max-height: 520px; overflow-y: auto;">
                                ${data.journals.map(j => `<div style="margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);">
                                    <div style="font-size: 0.7rem; color: var(--purple);">${j.filename}</div>
                                    <div style="font-size: 0.75rem; color: var(--text); white-space: pre-wrap;">${j.content || ''}</div>
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

                    // Activity log (My Space) — full filtered log with daily pagination
                    content += `<details style="margin-top: 0.5rem;" id="profileActivityLogDetails" data-identity-id="${(data.identity_id || '').replace(/"/g, '&quot;')}" ontoggle="if(this.open && !this.dataset.loaded){ this.dataset.loaded='1'; loadProfileActivityLog(this.getAttribute('data-identity-id')); }">
                        <summary style="cursor: pointer; color: var(--teal); font-size: 0.9rem;">Activity log (My Space)</summary>
                        <div style="margin-top: 0.5rem;">
                            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; flex-wrap: wrap;">
                                <label style="font-size: 0.75rem; color: var(--text-dim);">Resident day:</label>
                                <select id="profileActivityLogDay" style="padding: 0.25rem 0.5rem; font-size: 0.75rem; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text); border-radius: 4px;" onchange="filterProfileActivityLogByDay()">
                                    <option value="">All days</option>
                                </select>
                                <span id="profileActivityLogCount" style="font-size: 0.7rem; color: var(--text-dim);"></span>
                            </div>
                            <div id="profileActivityLogContent" style="background: var(--bg-dark); padding: 0.75rem; border-radius: 8px; max-height: 400px; overflow-y: auto; font-size: 0.72rem;">
                                Loading…
                            </div>
                        </div>
                    </details>`;

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
        const GOLDEN_PATH_NOTICE = 'Golden path enforced: run tasks via queue + vivarium.runtime.worker_runtime only.';

        function updateKillSwitchUI() {
            const stopBtn = document.getElementById('stopBtn');
            if (!stopBtn) return;

            stopBtn.disabled = false;
            stopBtn.classList.toggle('engaged', isStopped);
            stopBtn.textContent = isStopped ? 'RESUME' : 'HALT';
        }

        function loadStopStatus() {
            fetch('/api/stop_status')
                .then(r => r.json())
                .then(data => {
                    isStopped = !!(data && data.stopped);
                    updateKillSwitchUI();
                });
        }

        function toggleStop() {
            fetch('/api/toggle_stop', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    isStopped = !!(data && data.stopped);
                    updateKillSwitchUI();
                });
        }

        function getRollbackDays() {
            const raw = document.getElementById('rollbackDays')?.value;
            const parsed = parseInt(raw || '1', 10);
            return Math.max(1, Math.min(180, Number.isFinite(parsed) ? parsed : 1));
        }

        function previewRollbackByDays() {
            const days = getRollbackDays();
            const statusEl = document.getElementById('rollbackStatus');
            const previewEl = document.getElementById('rollbackPreview');
            const badgeEl = document.getElementById('rollbackBadge');
            if (statusEl) {
                statusEl.textContent = 'Loading rollback preview...';
                statusEl.style.color = 'var(--text-dim)';
            }
            fetch('/api/rollback/preview?days=' + encodeURIComponent(String(days)))
                .then(r => r.json().then(data => ({status: r.status, data})))
                .then(({status, data}) => {
                    if (!data.success || status >= 400) {
                        if (statusEl) {
                            statusEl.textContent = data.error || 'Rollback preview unavailable';
                            statusEl.style.color = 'var(--red)';
                        }
                        if (previewEl) previewEl.innerHTML = '';
                        if (badgeEl) badgeEl.textContent = '';
                        return;
                    }
                    const target = data.target || {};
                    const since = Number(data.checkpoints_since_target || 0);
                    const task = target.task_id ? `task ${target.task_id}` : 'checkpoint';
                    if (statusEl) {
                        statusEl.textContent = `Target: ${target.day_tag || 'unknown day'} (${task}), rewinds ~${since} checkpoint(s).`;
                        statusEl.style.color = 'var(--orange)';
                    }
                    if (badgeEl) badgeEl.textContent = `${since} to rewind`;
                    const affected = Array.isArray(data.affected_preview) ? data.affected_preview : [];
                    if (previewEl) {
                        if (!affected.length) {
                            previewEl.innerHTML = '<div>No newer checkpoints than target.</div>';
                        } else {
                            previewEl.innerHTML = affected.reverse().map(item => {
                                const summary = (item.summary || '').replace(/</g, '&lt;');
                                const day = item.day_tag || '';
                                const tid = item.task_id || 'unknown';
                                return `<div style="margin-bottom: 0.25rem; border-bottom: 1px solid var(--border); padding-bottom: 0.2rem;"><span style="color: var(--text);">${day}</span> - <span style="color: var(--teal);">${tid}</span><br>${summary}</div>`;
                            }).join('');
                        }
                    }
                })
                .catch(() => {
                    if (statusEl) {
                        statusEl.textContent = 'Failed to load rollback preview';
                        statusEl.style.color = 'var(--red)';
                    }
                });
        }

        function runRollbackByDays() {
            const days = getRollbackDays();
            if (!confirm(`Rollback mutable world by ${days} day(s)? Stop swarm first. This cannot be undone from UI.`)) {
                return;
            }
            const statusEl = document.getElementById('rollbackStatus');
            if (statusEl) {
                statusEl.textContent = 'Applying rollback...';
                statusEl.style.color = 'var(--orange)';
            }
            fetch('/api/rollback/by_days', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    days: days,
                    reason: 'Human rollback from control panel',
                    force_stop: true,
                }),
            })
            .then(r => r.json().then(data => ({status: r.status, data})))
            .then(({status, data}) => {
                if (!data.success || status >= 400) {
                    if (statusEl) {
                        statusEl.textContent = data.error || 'Rollback failed';
                        statusEl.style.color = 'var(--red)';
                    }
                    return;
                }
                if (statusEl) {
                    statusEl.textContent = `Rollback complete -> ${data.target?.day_tag || 'target checkpoint'}`;
                    statusEl.style.color = 'var(--green)';
                }
                loadQueueView();
                loadSwarmInsights();
                previewRollbackByDays();
            })
            .catch(() => {
                if (statusEl) {
                    statusEl.textContent = 'Rollback request failed';
                    statusEl.style.color = 'var(--red)';
                }
            });
        }

        function runFreshStateReset() {
            if (!confirm('Wipe stale runtime state now? This clears queue, logs, generated artifacts, and transient swarm files.')) {
                return;
            }
            const statusEl = document.getElementById('freshResetStatus');
            if (statusEl) {
                statusEl.textContent = 'Resetting...';
                statusEl.style.color = 'var(--orange)';
            }
            fetch('/api/system/fresh_reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ force_stop: true }),
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status, data }) => {
                if (status >= 400 || !data.success) {
                    if (statusEl) {
                        statusEl.textContent = data.error || 'Fresh reset failed';
                        statusEl.style.color = 'var(--red)';
                    }
                    return;
                }
                if (statusEl) {
                    statusEl.textContent = 'Fresh reset complete';
                    statusEl.style.color = 'var(--green)';
                }
                loadQueueView();
                loadSwarmInsights();
                loadArtifacts();
                updateLogEmptyState();
                const logContainer = document.getElementById('logContainer');
                if (logContainer) {
                    logContainer.innerHTML = '<div id="logEmptyState" class="log-empty">Waiting for log entries...</div>';
                }
                const entryCount = document.getElementById('entryCount');
                if (entryCount) entryCount.textContent = '0';
            })
            .catch(() => {
                if (statusEl) {
                    statusEl.textContent = 'Fresh reset request failed';
                    statusEl.style.color = 'var(--red)';
                }
            });
        }

        function addTaskFromUI() {
            const taskIdEl = document.getElementById('addTaskId');
            const instructionEl = document.getElementById('addTaskInstruction');
            const taskId = (taskIdEl && taskIdEl.value || '').trim();
            const instruction = (instructionEl && instructionEl.value || '').trim();
            if (!instruction) { alert('Enter an instruction for the task.'); return; }
            fetch('/api/queue/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_id: taskId, instruction: instruction })
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status, data }) => {
                if (data.success) {
                    if (instructionEl) instructionEl.value = '';
                    if (taskIdEl) taskIdEl.value = '';
                    if (typeof persistDraftInputs === 'function') persistDraftInputs(true);
                    if (typeof refreshInsights === 'function') refreshInsights();
                    if (typeof loadQueueView === 'function') loadQueueView();
                    alert('Task "' + (data.task_id || taskId || 'new task') + '" added. Start residents to process it.');
                } else {
                    alert(data.error || 'Failed to add task');
                }
            })
            .catch(() => alert('Failed to add task'));
        }

        function editQueueTask(taskId) {
            const nextId = prompt('New task ID (leave unchanged for same ID):', taskId || '');
            if (nextId === null) return;
            const nextInstruction = prompt('Updated task instruction/prompt:');
            if (nextInstruction === null) return;
            if (!String(nextInstruction || '').trim()) {
                alert('Task prompt cannot be empty.');
                return;
            }
            fetch('/api/queue/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    task_id: taskId,
                    new_task_id: String(nextId || '').trim(),
                    instruction: String(nextInstruction || '').trim(),
                }),
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status, data }) => {
                if (status >= 400 || !data.success) {
                    showToast(data.error || 'Failed to update task', 'error');
                    return;
                }
                loadQueueView();
                showToast('Task updated');
            })
            .catch(() => showToast('Failed to update task', 'error'));
        }

        function deleteQueueTask(taskId) {
            if (!confirm('Delete task "' + taskId + '" from queue?')) return;
            fetch('/api/queue/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_id: taskId }),
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status, data }) => {
                if (status >= 400 || !data.success) {
                    showToast(data.error || 'Failed to delete task', 'error');
                    return;
                }
                loadQueueView();
                showToast('Task removed');
            })
            .catch(() => showToast('Failed to delete task', 'error'));
        }

        function renderQueueList(containerId, items, emptyText, mode='readonly') {
            const container = document.getElementById(containerId);
            if (!container) return;
            if (!Array.isArray(items) || items.length === 0) {
                container.innerHTML = '<div class="queue-empty">' + emptyText + '</div>';
                return;
            }
            container.innerHTML = items.map(item => {
                const id = (item && item.id) ? String(item.id) : '(no-id)';
                const prompt = (item && item.prompt) ? String(item.prompt) : '';
                const shortPrompt = prompt.length > 120 ? prompt.slice(0, 120) + '…' : prompt;
                const editBtn = mode === 'open'
                    ? '<button class="qbtn" onclick="editQueueTask(\\'' + id.replace(/'/g, "\\'") + '\\')">Edit</button>'
                    : '';
                const deleteBtn = mode !== 'readonly'
                    ? '<button class="qbtn delete" onclick="deleteQueueTask(\\'' + id.replace(/'/g, "\\'") + '\\')">Delete</button>'
                    : '';
                return '<div class="queue-item"><div class="qid">' + escapeHtml(id) + '</div><div class="qprompt">' + escapeHtml(shortPrompt) + '</div><div class="qactions">' + editBtn + deleteBtn + '</div></div>';
            }).join('');
        }

        function loadQueueView() {
            fetch('/api/queue/state')
                .then(r => r.json())
                .then(data => {
                    renderQueueList('queueOpenList', data.open || [], 'No open tasks', 'open');
                    renderPendingReviewList(data.pending_review || []);
                    renderQueueList('queueCompletedList', data.completed || [], 'No completed tasks yet', 'history');
                    renderQueueList('queueFailedList', data.failed || [], 'No failed tasks', 'history');
                })
                .catch(() => {
                    const openEl = document.getElementById('queueOpenList');
                    if (openEl) openEl.innerHTML = '<div class="queue-empty">Queue API unavailable</div>';
                });
        }

        function loadOneTimeTasks() {
            const el = document.getElementById('oneTimeTasksList');
            if (!el) return;
            fetch('/api/one_time_tasks')
                .then(r => r.json())
                .then(data => {
                    if (data.success && Array.isArray(data.tasks)) {
                        renderOneTimeTasksList(data.tasks);
                    } else {
                        el.innerHTML = '<div class="queue-empty">No one-time tasks</div>';
                    }
                })
                .catch(() => { el.innerHTML = '<div class="queue-empty">Failed to load</div>'; });
        }
        function renderOneTimeTasksList(tasks) {
            const el = document.getElementById('oneTimeTasksList');
            if (!el) return;
            if (!tasks.length) {
                el.innerHTML = '<div class="queue-empty">No one-time tasks. Add one below.</div>';
                return;
            }
            el.innerHTML = tasks.map((t) => {
                const id = (t.id || '').replace(/[^a-zA-Z0-9_-]/g, '_');
                const promptText = escapeHtml((t.prompt || t.title || t.id || ''));
                const bonus = Math.max(0, parseInt(t.bonus_tokens, 10) || 0);
                return '<div class="queue-item" style="flex-direction:column; align-items:stretch; gap:0.2rem;">' +
                    '<div class="qprompt">' + promptText + '</div>' +
                    '<div style="font-size:0.68rem; color:var(--text-dim); display:flex; flex-wrap:wrap; align-items:center; gap:0.35rem;">' +
                    '<span>' + escapeHtml(t.id) + ' · ' + (t.completions_count || 0) + ' completed</span>' +
                    '<span style="display:inline-flex; align-items:center; gap:0.2rem;">Reward: <input type="number" id="oneTimeBonus_' + id + '" min="0" step="1" value="' + bonus + '" style="width:3.5rem; padding:0.15rem 0.25rem; font-size:0.68rem; background:var(--bg-dark); border:1px solid var(--border); color:var(--text); border-radius:4px;" /> tokens</span>' +
                    '<button type="button" class="qbtn" style="padding:0.15rem 0.35rem; font-size:0.68rem;" data-one-time-id="' + escapeHtml(t.id) + '" onclick="updateOneTimeTaskReward(this)">Update</button>' +
                    '</div>' +
                    '<div class="qactions"><button type="button" class="qbtn delete" data-one-time-id="' + escapeHtml(t.id) + '" onclick="deleteOneTimeTaskFromUI(this)">Remove</button></div></div>';
            }).join('');
        }
        function addOneTimeTaskFromUI() {
            const idEl = document.getElementById('oneTimeTaskId');
            const promptEl = document.getElementById('oneTimeTaskPrompt');
            const bonusEl = document.getElementById('oneTimeTaskBonus');
            const id = (idEl && idEl.value || '').trim();
            const prompt = (promptEl && promptEl.value || '').trim();
            const bonus = Math.max(0, parseInt(bonusEl && bonusEl.value, 10) || 0);
            if (!id) { alert('Task identifier is required'); return; }
            fetch('/api/one_time_tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: id, prompt: prompt, bonus_tokens: bonus }),
            })
                .then(r => r.json())
                .then((data) => {
                    if (data.success) {
                        if (idEl) idEl.value = ''; if (promptEl) promptEl.value = '';
                        if (typeof persistDraftInputs === 'function') persistDraftInputs(true);
                        loadOneTimeTasks();
                        alert('One-time task "' + id + '" added.');
                    } else {
                        alert(data.error || 'Failed to add task');
                    }
                })
                .catch(() => alert('Request failed'));
        }
        function updateOneTimeTaskReward(btn) {
            const taskId = (btn && btn.getAttribute && btn.getAttribute('data-one-time-id')) || '';
            if (!taskId) return;
            const idSafe = taskId.replace(/[^a-zA-Z0-9_-]/g, '_');
            const inputEl = document.getElementById('oneTimeBonus_' + idSafe);
            const bonus = inputEl ? Math.max(0, parseInt(inputEl.value, 10) || 0) : 0;
            fetch('/api/one_time_tasks/' + encodeURIComponent(taskId), {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ bonus_tokens: bonus }),
            })
                .then(r => r.json())
                .then((data) => {
                    if (data.success) {
                        loadOneTimeTasks();
                        showToast('Reward updated to ' + bonus + ' tokens');
                    } else {
                        showToast(data.error || 'Update failed', 'error');
                    }
                })
                .catch(() => showToast('Request failed', 'error'));
        }
        function deleteOneTimeTaskFromUI(btn) {
            const taskId = (btn && btn.getAttribute && btn.getAttribute('data-one-time-id')) || '';
            if (!taskId || !confirm('Remove one-time task "' + taskId + '"? Residents will no longer see it.')) return;
            fetch('/api/one_time_tasks/' + encodeURIComponent(taskId), { method: 'DELETE' })
                .then(function(r) {
                    return r.json().then(function(data) {
                        if (data.success) {
                            loadOneTimeTasks();
                            showToast('One-time task removed');
                        } else {
                            showToast(data.error || 'Delete failed', 'error');
                        }
                    }).catch(function() { showToast(r.ok ? 'Delete failed' : 'Server error', 'error'); });
                })
                .catch(function() { showToast('Request failed', 'error'); });
        }

        function renderPendingReviewList(items) {
            const el = document.getElementById('queuePendingReviewList');
            if (!el) return;
            if (!items.length) {
                el.innerHTML = '<div class="queue-empty">None</div>';
                return;
            }
            el.innerHTML = items.map((t) => {
                const taskId = String(t.id || '');
                const shortPrompt = String(t.prompt || t.id || '').slice(0, 60);
                const who = t.identity_id || 'resident';
                const verdict = t.review_verdict || '—';
                const tipId = 'pendingTip_' + taskId.replace(/[^a-zA-Z0-9_-]/g, '_');
                const feedbackId = 'pendingFeedback_' + taskId.replace(/[^a-zA-Z0-9_-]/g, '_');
                const taskIdAttr = escapeHtml(taskId);
                return '<div class="queue-item" style="flex-direction:column; align-items:stretch; gap:0.35rem;">' +
                    '<div class="qid">' + escapeHtml(t.id) + '</div>' +
                    '<div class="qprompt">' + escapeHtml(shortPrompt) + '</div>' +
                    '<div style="font-size:0.68rem; color:var(--text-dim);">' + escapeHtml(who) + ' · ' + escapeHtml(verdict) + '</div>' +
                    '<div style="display:flex; gap:0.25rem; align-items:center;"><label style="font-size:0.68rem; color:var(--text-dim);">Tip (tokens):</label><input type="number" id="' + tipId + '" min="0" step="1" value="0" style="width:4rem; padding:0.2rem; font-size:0.7rem; background:var(--bg-dark); border:1px solid var(--border); color:var(--text); border-radius:4px;"></div>' +
                    '<div><label style="font-size:0.68rem; color:var(--text-dim);">Feedback (optional):</label><textarea id="' + feedbackId + '" placeholder="Reinforce excellence or give guidance..." rows="2" style="width:100%; margin-top:0.15rem; padding:0.25rem; font-size:0.7rem; background:var(--bg-dark); border:1px solid var(--border); color:var(--text); border-radius:4px; resize:vertical;"></textarea></div>' +
                    '<div class="qactions" style="flex-wrap:wrap; gap:0.25rem;">' +
                    '<button class="chat-room-open-btn" style="padding:0.2rem 0.4rem; font-size:0.7rem; background:var(--green); color:#0f1318;" data-queue-task-id="' + taskIdAttr + '" data-tip-id="' + tipId + '" data-feedback-id="' + feedbackId + '" onclick="approveQueueTaskFromBtn(this)">Approve</button>' +
                    '<button class="chat-room-open-btn" style="padding:0.2rem 0.4rem; font-size:0.7rem; background:var(--orange); color:#0f1318;" data-queue-task-id="' + taskIdAttr + '" onclick="requeueQueueTaskFromBtn(this)">Try again</button>' +
                    '<button class="chat-room-open-btn" style="padding:0.2rem 0.4rem; font-size:0.7rem; background:var(--red); color:#fff;" data-queue-task-id="' + taskIdAttr + '" onclick="removeQueueTaskFromBtn(this)">Remove task</button>' +
                    '</div></div>';
            }).join('');
        }

        function approveQueueTaskFromBtn(btn) {
            const taskId = btn.getAttribute('data-queue-task-id') || '';
            const tipId = btn.getAttribute('data-tip-id') || '';
            const feedbackId = btn.getAttribute('data-feedback-id') || '';
            approveQueueTask(taskId, tipId, feedbackId);
        }
        function approveQueueTaskFromMailbox(btn) {
            const taskId = (btn && btn.getAttribute ? btn.getAttribute('data-mailbox-task-id') : '') || '';
            if (!taskId) return;
            approveQueueTask(taskId, '', '');
        }
        function requeueQueueTaskFromBtn(btn) {
            requeueQueueTask(btn.getAttribute('data-queue-task-id') || '');
        }
        function removeQueueTaskFromBtn(btn) {
            removeQueueTask(btn.getAttribute('data-queue-task-id') || '');
        }
        function approveQueueTask(taskId, tipInputId, feedbackInputId) {
            let tip = 0;
            let feedback = '';
            if (tipInputId) {
                const tipEl = document.getElementById(tipInputId);
                if (tipEl) tip = Math.max(0, parseInt(tipEl.value, 10) || 0);
            }
            if (feedbackInputId) {
                const fbEl = document.getElementById(feedbackInputId);
                if (fbEl) feedback = (fbEl.value || '').trim();
            }
            if (!confirm('Approve this task and grant the completion reward to the resident?' + (tip > 0 ? ' A tip of ' + tip + ' tokens will be added.' : ''))) return;
            fetch('/api/queue/task/approve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_id: taskId, tip_tokens: tip, feedback: feedback }),
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        let msg = data.reward_applied ? 'Approved. ' + (data.tokens_awarded || 0) + ' tokens awarded.' : 'Approved.';
                        if (data.tip_awarded) msg += ' Tip: ' + data.tip_awarded + ' tokens.';
                        showToast(msg);
                        loadQueueView();
                    } else {
                        showToast('Approve failed: ' + (data.error || 'Unknown'), 'error');
                    }
                })
                .catch(() => { showToast('Approve request failed', 'error'); });
        }

        function requeueQueueTask(taskId) {
            if (!confirm('Send this task back to the queue for another attempt? The resident will not receive completion reward.')) return;
            fetch('/api/queue/task/requeue', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_id: taskId }),
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) { loadQueueView(); if (typeof alert === 'function') alert('Task requeued for try again.'); }
                    else { if (typeof alert === 'function') alert('Requeue failed: ' + (data.error || 'Unknown')); }
                })
                .catch(() => { if (typeof alert === 'function') alert('Requeue request failed'); });
        }

        function removeQueueTask(taskId) {
            if (!confirm('Remove this task from the queue? It will be marked as failed and the resident will not receive completion reward.')) return;
            fetch('/api/queue/task/remove', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_id: taskId }),
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) { loadQueueView(); if (typeof alert === 'function') alert('Task removed.'); }
                    else { if (typeof alert === 'function') alert('Remove failed: ' + (data.error || 'Unknown')); }
                })
                .catch(() => { if (typeof alert === 'function') alert('Remove request failed'); });
        }

        function showGoldenPathOnlyNotice() {
            alert(GOLDEN_PATH_NOTICE);
        }

        function updateWorkerUI(running, runningCount = 0, targetCount = 1, runningSource = 'none') {
            const dot = document.getElementById('workerDot');
            const statusEl = document.getElementById('workerStatus');
            const startBtn = document.getElementById('workerStartBtn');
            const stopBtn = document.getElementById('workerStopBtn');
            if (!dot || !statusEl) return;
            dot.className = 'dot';
            if (running) {
                dot.classList.add('running');
                const count = Number.isFinite(Number(runningCount)) ? Number(runningCount) : 1;
                const sourceLabel = runningSource === 'unmanaged' ? ' external' : '';
                statusEl.textContent = `Residents: active (${count}${sourceLabel})`;
                if (startBtn) startBtn.style.display = 'none';
                if (stopBtn) stopBtn.style.display = '';
            } else {
                dot.classList.add('stopped');
                const target = Number.isFinite(Number(targetCount)) ? Number(targetCount) : 1;
                statusEl.textContent = `Worker stopped — Start to run ${target} resident${target !== 1 ? 's' : ''}`;
                if (startBtn) startBtn.style.display = '';
                if (stopBtn) stopBtn.style.display = 'none';
            }
        }

        function refreshWorkerStatus() {
            fetch('/api/worker/status')
                .then(r => r.json())
                .then(data => { updateWorkerUI(!!data.running, data.running_count || 0, data.target_count || 1, data.running_source || 'none'); })
                .catch(() => updateWorkerUI(false, 0, 1));
        }

        function startWorker() {
            const residentCountEl = document.getElementById('residentCount');
            const residentCount = Math.max(1, Math.min(16, parseInt(residentCountEl?.value || '1', 10) || 1));
            fetch('/api/worker/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resident_count: residentCount }),
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        updateWorkerUI(true, data.running_count || residentCount, data.target_count || residentCount, data.running_source || 'managed');
                        setTimeout(loadRecentLogs, 800);  // Refresh log soon after worker starts writing
                        if (data.message && data.message !== 'Worker already running') {
                            const started = data.running_count || residentCount;
                            alert(`Residents started (${started} active).`);
                        }
                    } else {
                        alert('Failed to start residents: ' + (data.error || 'Unknown error'));
                    }
                })
                .catch(() => alert('Failed to start residents'));
        }

        function stopWorker() {
            fetch('/api/worker/stop', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    updateWorkerUI(false);
                    if (data.message && data.message !== 'Worker not running') {
                        alert('Residents paused.');
                    }
                })
                .catch(() => updateWorkerUI(false));
        }

        function togglePause() { /* unused: worker has no pause */ }

        function emergencyStop() {
            if (!confirm('Pause resident runtime? Queue execution will stop until restarted.')) return;
            stopWorker();
        }

        // Scaling controls
        function toggleScaleMode() {
            // Legacy autoscale toggle removed in golden-path UI; keep both sections visible.
            const manual = document.getElementById('manualScaleControls');
            const budget = document.getElementById('autoScaleControls');
            if (manual) manual.style.display = 'block';
            if (budget) budget.style.display = 'block';
            persistUiSettings();
        }

        function updateSessionCount(value) {
            const numeric = parseFloat(value);
            const display = Number.isFinite(numeric) ? numeric.toFixed(0) : value;
            document.getElementById('sessionCount').textContent = display;
        }

        let logCycleSeconds = 10;  // Resident (machine) cycle length in seconds; used for log "day" column
        function loadRuntimeSpeed() {
            fetch('/api/runtime_speed')
                .then(r => r.json())
                .then(data => {
                    const cycleSec = Number(data.cycle_seconds ?? 10);
                    if (Number.isFinite(cycleSec) && cycleSec >= 1) logCycleSeconds = cycleSec;
                    const currentCycle = Number(data.current_cycle_id);
                    if (Number.isFinite(currentCycle)) currentRuntimeCycleId = currentCycle;
                    const slider = document.getElementById('sessionSlider');
                    const waitSeconds = Number(data.wait_seconds ?? 2);
                    if (slider && Number.isFinite(waitSeconds)) {
                        slider.value = String(waitSeconds);
                        updateSessionCount(waitSeconds);
                    }
                });
        }

        function saveRuntimeSpeed() {
            const slider = document.getElementById('sessionSlider');
            const status = document.getElementById('runtimeSpeedStatus');
            const waitSeconds = Number(slider ? slider.value : 2);
            fetch('/api/runtime_speed', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({wait_seconds: waitSeconds})
            })
            .then(r => r.json())
            .then(data => {
                if (!data.success) {
                    if (status) {
                        status.textContent = data.error || 'Failed to save pace';
                        status.style.color = 'var(--red)';
                    }
                    showToast(data.error || 'Failed to save pace', 'error');
                    return;
                }
                updateSessionCount(data.wait_seconds);
                persistUiSettings();
                if (status) {
                    status.textContent = `Saved: ${Number(data.wait_seconds).toFixed(0)}s idle wait`;
                    status.style.color = 'var(--green)';
                    setTimeout(() => { status.textContent = ''; }, 2500);
                }
                showToast('Pace saved');
            })
            .catch(() => {
                if (status) { status.textContent = 'Request failed'; status.style.color = 'var(--red)'; }
                showToast('Failed to save pace', 'error');
            });
        }

        function loadGroqKeyStatus() {
            fetch('/api/groq_key')
                .then(r => r.json())
                .then(data => {
                    const badge = document.getElementById('groqKeyBadge');
                    const status = document.getElementById('groqKeyStatus');
                    if (badge) {
                        badge.textContent = data.configured ? 'CONFIGURED' : 'NOT SET';
                        badge.style.color = data.configured ? 'var(--green)' : 'var(--text-dim)';
                    }
                    if (status) {
                        if (data.configured) {
                            status.textContent = `Active key: ${data.masked_key || 'configured'} (${data.source || 'runtime'})`;
                            status.style.color = 'var(--green)';
                        } else {
                            status.textContent = 'No key configured yet';
                            status.style.color = 'var(--text-dim)';
                        }
                    }
                });
        }

        function saveGroqApiKey() {
            const input = document.getElementById('groqApiKeyInput');
            const status = document.getElementById('groqKeyStatus');
            const raw = input ? input.value.trim() : '';
            if (!raw) {
                if (status) {
                    status.textContent = 'Enter a key first';
                    status.style.color = 'var(--red)';
                }
                return;
            }
            fetch('/api/groq_key', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({api_key: raw})
            })
            .then(r => r.json())
            .then(data => {
                if (!data.success) {
                    if (status) {
                        status.textContent = data.error || 'Failed to save key';
                        status.style.color = 'var(--red)';
                    }
                    showToast(data.error || 'Failed to save key', 'error');
                    return;
                }
                if (input) input.value = '';
                loadGroqKeyStatus();
                showToast('API key saved');
            })
            .catch(() => {
                if (status) { status.textContent = 'Request failed'; status.style.color = 'var(--red)'; }
                showToast('Failed to save key', 'error');
            });
        }

        function clearGroqApiKey() {
            fetch('/api/groq_key', {method: 'DELETE'})
                .then(r => r.json())
                .then(data => {
                    const status = document.getElementById('groqKeyStatus');
                    if (!data.success) {
                        if (status) {
                            status.textContent = data.error || 'Failed to clear key';
                            status.style.color = 'var(--red)';
                        }
                        showToast(data.error || 'Failed to clear key', 'error');
                        return;
                    }
                    loadGroqKeyStatus();
                    showToast('API key cleared');
                })
                .catch(() => showToast('Failed to clear key', 'error'));
        }

        function refreshCreativeSeed() {
            fetch('/api/creative_seed')
                .then(r => r.json())
                .then(data => {
                    const el = document.getElementById('creativeSeedValue');
                    if (!el) return;
                    if (data && data.success && data.seed) {
                        el.textContent = String(data.seed);
                        el.style.color = 'var(--yellow)';
                        showToast('New seed: ' + data.seed);
                    } else {
                        el.textContent = '--';
                        el.style.color = 'var(--text-dim)';
                        showToast('No seed available', 'info');
                    }
                })
                .catch(() => {
                    const el = document.getElementById('creativeSeedValue');
                    if (el) {
                        el.textContent = '--';
                        el.style.color = 'var(--text-dim)';
                    }
                    showToast('Failed to load seed', 'error');
                });
        }

        function createResidentIdentity() {
            const creator = document.getElementById('identityCreatorSelect');
            const name = document.getElementById('newIdentityName');
            const summary = document.getElementById('newIdentitySummary');
            const traits = document.getElementById('newIdentityTraits');
            const values = document.getElementById('newIdentityValues');
            const activities = document.getElementById('newIdentityActivities');
            const seedEl = document.getElementById('creativeSeedValue');
            const status = document.getElementById('identityCreateStatus');

            const payload = {
                creator_identity_id: creator ? creator.value : '',
                name: name ? name.value : '',
                summary: summary ? summary.value : '',
                traits_csv: traits ? traits.value : '',
                values_csv: values ? values.value : '',
                activities_csv: activities ? activities.value : '',
                creativity_seed: seedEl ? String(seedEl.textContent || '').trim() : '',
            };

            fetch('/api/identities/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload),
            })
            .then(r => r.json())
            .then(data => {
                if (!data.success) {
                    if (status) {
                        status.textContent = data.error || 'Identity creation failed';
                        status.style.color = 'var(--red)';
                    }
                    return;
                }
                if (status) {
                    status.textContent = `Created ${data.identity?.name || 'identity'} (${data.identity?.id || ''}) with seed ${data.identity?.creativity_seed || 'n/a'}`;
                    status.style.color = 'var(--green)';
                }
                if (name) name.value = '';
                if (summary) summary.value = '';
                if (traits) traits.value = '';
                if (values) values.value = '';
                if (activities) activities.value = '';
                refreshCreativeSeed();
                fetch('/api/identities').then(r => r.json()).then(updateIdentities);
            });
        }

        function updateBudgetLimit(value) {
            const minEl = document.getElementById('taskMinBudget');
            const maxEl = document.getElementById('taskMaxBudget');
            const minV = Number(minEl ? minEl.value : 0.05);
            const maxV = Number(maxEl ? maxEl.value : 0.10);
            if (Number.isFinite(minV) && Number.isFinite(maxV) && maxV < minV && maxEl) {
                maxEl.value = String(minV.toFixed(2));
            }
            persistUiSettings();
        }

        function updateModel(model) {
            // Model selection - saved with config
            updateModelDescription(model);
            persistUiSettings();
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
            persistUiSettings();
        }

        function persistUiSettings() {
            const override = !!document.getElementById('overrideModelToggle')?.checked;
            const selector = document.getElementById('modelSelector');
            const minBudgetRaw = document.getElementById('taskMinBudget')?.value;
            const maxBudgetRaw = document.getElementById('taskMaxBudget')?.value;
            const residentCountRaw = document.getElementById('residentCount')?.value;
            const humanUsernameRaw = document.getElementById('humanUsername')?.value || 'human';
            const humanUsername = String(humanUsernameRaw).trim().replace(/[^a-zA-Z0-9 _.\-]/g, '').slice(0, 48) || 'human';
            const taskMinBudget = Number.isFinite(Number(minBudgetRaw)) ? Number(minBudgetRaw) : 0.05;
            const taskMaxBudget = Number.isFinite(Number(maxBudgetRaw)) ? Number(maxBudgetRaw) : Math.max(0.10, taskMinBudget);
            const residentCount = Number.isFinite(Number(residentCountRaw)) ? Number(residentCountRaw) : 1;
            const model = override ? (selector?.value || 'auto') : 'auto';
            fetch('/api/ui_settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    override_model: override,
                    model: model,
                    auto_scale: false,
                    budget_limit: taskMaxBudget,
                    task_min_budget: taskMinBudget,
                    task_max_budget: Math.max(taskMinBudget, taskMaxBudget),
                    resident_count: Math.max(1, Math.min(16, residentCount)),
                    human_username: humanUsername,
                }),
            }).catch(() => {});
        }

        function loadUiSettings() {
            fetch('/api/ui_settings')
                .then(r => r.json())
                .then(data => {
                    if (!data || data.success === false) return;
                    const override = !!data.override_model;
                    const model = String(data.model || 'auto');
                    const taskMinBudget = Number(data.task_min_budget ?? 0.05);
                    const taskMaxBudget = Number(data.task_max_budget ?? data.budget_limit ?? 0.10);
                    const residentCount = Number(data.resident_count ?? 1);
                    const humanUsername = String(data.human_username || 'human');

                    const overrideEl = document.getElementById('overrideModelToggle');
                    const modelEl = document.getElementById('modelSelector');
                    const minEl = document.getElementById('taskMinBudget');
                    const maxEl = document.getElementById('taskMaxBudget');
                    const residentCountEl = document.getElementById('residentCount');
                    const humanUsernameEl = document.getElementById('humanUsername');

                    if (overrideEl) overrideEl.checked = override;
                    if (modelEl) modelEl.value = override ? model : 'auto';
                    if (minEl && Number.isFinite(taskMinBudget)) minEl.value = taskMinBudget.toFixed(2);
                    if (maxEl && Number.isFinite(taskMaxBudget)) maxEl.value = taskMaxBudget.toFixed(2);
                    if (residentCountEl && Number.isFinite(residentCount)) residentCountEl.value = String(Math.max(1, Math.min(16, Math.trunc(residentCount))));
                    if (humanUsernameEl) humanUsernameEl.value = humanUsername;

                    toggleModelOverride();
                    toggleScaleMode();
                    if (modelEl) updateModelDescription(modelEl.value);
                })
                .catch(() => {});
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
        }

        function loadWorkerStatus() {
            refreshWorkerStatus();
        }

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                applyLogFilter();
                updateLogEmptyState();
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
        function setRequestStatus(message, tone = 'info', holdMs = 3000) {
            const status = document.getElementById('requestStatus');
            if (!status) return;
            const colorMap = {
                success: 'var(--green)',
                error: 'var(--red)',
                info: 'var(--teal)',
            };
            status.textContent = message || '';
            status.style.color = colorMap[tone] || 'var(--text-dim)';
            if (holdMs > 0) {
                setTimeout(() => {
                    status.textContent = '';
                    status.style.color = '';
                }, holdMs);
            }
        }

        function saveRequest() {
            const request = document.getElementById('humanRequest').value;
            setRequestStatus('Saving...', 'info', 0);
            fetch('/api/human_request', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({request: request})
            })
            .then(async (r) => {
                const data = await r.json().catch(() => ({}));
                if (!r.ok || data.success === false) {
                    const detail = data.error || `request failed (${r.status})`;
                    throw new Error(detail);
                }
                return data;
            })
            .then(data => {
                setRequestStatus(
                    data.task_id ? `Saved + queued (${data.task_id})` : 'Saved!',
                    'success',
                    3000
                );
                updateRequestIndicator(request.trim().length > 0);
                if (typeof loadQueueView === 'function') loadQueueView();
            })
            .catch((err) => {
                const detail = (err && err.message) ? err.message : 'unknown error';
                setRequestStatus(`Save failed: ${detail}`, 'error', 6000);
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
                    updateMailboxUnreadBadge(unread);

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
                        const humanName = (msg.response && msg.response.responder_name) || msg.human_username || 'human';
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
                                        <span style="color: var(--green); font-size: 0.75rem;">${humanName} replied:</span>
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
                    loadMessages();
                    loadMailboxData(true);
                    showToast('Reply sent');
                } else {
                    showToast(data.error || 'Failed to send reply', 'error');
                }
            })
            .catch(() => showToast('Failed to send reply', 'error'));
        }

        function updateMailboxUnreadBadge(unreadCount) {
            const badge = document.getElementById('mailboxUnreadBadge');
            if (!badge) return;
            const safe = Math.max(0, Number(unreadCount || 0));
            if (safe <= 0) {
                badge.textContent = '0';
                badge.classList.remove('show');
                return;
            }
            badge.textContent = safe > 99 ? '99+' : String(safe);
            badge.classList.add('show');
        }

        function renderMailboxTargetOptions(identities) {
            const target = document.getElementById('mailboxTarget');
            if (!target) return;
            const previous = target.value;
            const opts = ['<option value="">Broadcast (all residents)</option>'];
            (Array.isArray(identities) ? identities : []).forEach((identity) => {
                const id = String(identity.id || '').trim();
                if (!id) return;
                const name = String(identity.name || id);
                opts.push(`<option value="${id}">${escapeHtml(name)} (${escapeHtml(id)})</option>`);
            });
            target.innerHTML = opts.join('');
            if (previous && (identities || []).some((i) => i.id === previous)) {
                target.value = previous;
            }
        }

        function renderMailboxThreads() {
            const container = document.getElementById('mailboxThreads');
            if (!container) return;
            const threads = Array.isArray(mailboxData.threads) ? mailboxData.threads : [];
            if (!threads.length) {
                container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem;">No threads yet. Residents will appear here when they message you.</p>';
                return;
            }
            container.innerHTML = threads.map((thread) => {
                const activeClass = String(activeMailboxThreadId || '') === String(thread.id || '') ? ' active' : '';
                const unread = Number(thread.unread || 0);
                const preview = escapeHtml(thread.last_preview || 'No messages yet');
                const idEsc = String(thread.id || '').replace(/'/g, "\\'");
                const ts = thread.last_at ? new Date(thread.last_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '--:--';
                return `
                    <div class="mailbox-thread-item${activeClass}" onclick="openMailboxThread('${idEsc}')">
                        <div style="display:flex; justify-content:space-between; align-items:center; gap:0.4rem;">
                            <span style="font-size:0.78rem; color:var(--teal); font-weight:650;">${escapeHtml(thread.name || thread.id || 'Resident')}</span>
                            <span style="font-size:0.66rem; color:var(--text-dim);">${ts}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; gap:0.4rem; margin-top:0.2rem; max-height: 4rem; overflow-y: auto; word-wrap: break-word;">
                            <span style="font-size:0.72rem; color:var(--text-dim); word-wrap:break-word;">${preview}</span>
                            ${unread > 0 ? `<span class="mailbox-badge show" style="animation:none; min-width:0.95rem; height:0.95rem; font-size:0.62rem;">${unread}</span>` : ''}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function openMailboxThread(threadId) {
            activeMailboxThreadId = threadId;
            const threads = Array.isArray(mailboxData.threads) ? mailboxData.threads : [];
            const selected = threads.find((t) => String(t.id || '') === String(threadId || ''));
            const target = document.getElementById('mailboxTarget');
            if (target && selected && selected.id && selected.id !== '__broadcast__') {
                target.value = String(selected.id);
            }
            renderMailboxThreads();
            renderMailboxMessages();
        }

        function renderMailboxMessages() {
            const container = document.getElementById('mailboxMessages');
            if (!container) return;
            if (!activeMailboxThreadId) {
                container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem;">Select a thread to start chatting.</p>';
                return;
            }
            const all = mailboxData.thread_messages || {};
            const messages = Array.isArray(all[activeMailboxThreadId]) ? all[activeMailboxThreadId] : [];
            if (!messages.length) {
                container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem;">No messages yet in this thread.</p>';
                return;
            }
            container.innerHTML = messages.map((msg) => {
                const direction = msg.direction === 'out' ? 'out' : 'in';
                const stamp = msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '';
                const responded = msg.direction === 'in' && msg.responded ? '<span style="font-size:0.62rem; color: var(--green); margin-left:0.35rem;">replied</span>' : '';
                const isApproval = msg.type === 'task_pending_approval' && msg.task_id;
                const taskIdAttr = isApproval ? escapeHtml(String(msg.task_id)).replace(/"/g, '&quot;') : '';
                const approveBtn = isApproval ? `<button class="chat-room-open-btn" style="margin-top:0.4rem; padding:0.2rem 0.4rem; font-size:0.7rem; background:var(--green); color:#0f1318;" data-mailbox-task-id="${taskIdAttr}" onclick="approveQueueTaskFromMailbox(this)">Approve task</button>` : '';
                return `
                    <div class="mailbox-msg ${direction}">
                        <div style="font-size:0.64rem; color: var(--text-dim); margin-bottom:0.2rem;">
                            ${escapeHtml(msg.author_name || '')} • ${stamp}${responded}
                        </div>
                        <div>${escapeHtml(msg.content || '')}</div>
                        ${approveBtn}
                    </div>
                `;
            }).join('');
            container.scrollTop = container.scrollHeight;
        }

        function loadMailboxData(forceOpenThread=false) {
            fetch('/api/messages/mailbox')
                .then(r => r.json())
                .then(data => {
                    if (!data || !data.success) return;
                    mailboxData = data;
                    updateMailboxUnreadBadge(data.unread_count || 0);
                    renderMailboxTargetOptions(data.identities || []);
                    const subhead = document.getElementById('mailboxSubhead');
                    if (subhead) {
                        const human = data.human_name || 'human';
                        subhead.textContent = `Async phone chat as ${human}`;
                    }
                    const threadIds = new Set((data.threads || []).map((t) => String(t.id || '')));
                    if (!activeMailboxThreadId || !threadIds.has(String(activeMailboxThreadId))) {
                        activeMailboxThreadId = (data.threads && data.threads.length) ? String(data.threads[0].id || '') : null;
                    }
                    if (forceOpenThread && data.threads && data.threads.length && !activeMailboxThreadId) {
                        activeMailboxThreadId = String(data.threads[0].id || '');
                    }
                    renderMailboxThreads();
                    renderMailboxMessages();
                })
                .catch(() => {});
        }

        function openMailboxModal() {
            const modal = document.getElementById('mailboxModal');
            if (!modal) return;
            modal.classList.add('open');
            loadMailboxData(true);
            loadQuestProgress();
            if (mailboxPoller) clearInterval(mailboxPoller);
            mailboxPoller = setInterval(() => {
                loadMailboxData(false);
                loadQuestProgress();
            }, 4000);
        }

        function closeMailboxModal() {
            const modal = document.getElementById('mailboxModal');
            if (modal) modal.classList.remove('open');
            if (mailboxPoller) {
                clearInterval(mailboxPoller);
                mailboxPoller = null;
            }
        }

        function handleMailboxBackdrop(event) {
            if (event && event.target && event.target.id === 'mailboxModal') {
                closeMailboxModal();
            }
        }

        function sendMailboxMessage() {
            const input = document.getElementById('mailboxComposer');
            const target = document.getElementById('mailboxTarget');
            const status = document.getElementById('mailboxStatus');
            const content = String(input ? input.value : '').trim();
            const toId = String(target ? target.value : '').trim();
            if (!content) {
                if (status) { status.textContent = 'Message is empty.'; status.style.color = 'var(--red)'; }
                return;
            }
            const toName = toId ? ((mailboxData.identities || []).find((i) => String(i.id) === toId)?.name || toId) : '';
            fetch('/api/messages/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({to_id: toId, to_name: toName, content: content})
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status: httpStatus, data }) => {
                if (httpStatus >= 400 || !data.success) {
                    if (status) { status.textContent = data.error || 'Failed to send'; status.style.color = 'var(--red)'; }
                    return;
                }
                if (input) input.value = '';
                if (status) { status.textContent = toId ? 'Message sent to resident.' : 'Broadcast sent.'; status.style.color = 'var(--green)'; }
                showToast(toId ? 'Message sent' : 'Broadcast sent');
                loadMailboxData(true);
                loadMessages(true);
            })
            .catch(() => {
                if (status) { status.textContent = 'Failed to send'; status.style.color = 'var(--red)'; }
                showToast('Failed to send', 'error');
            });
        }

        function renderQuestProgress() {
            const container = document.getElementById('questProgressContainer');
            if (!container) return;
            const quests = Array.isArray(mailboxQuests) ? mailboxQuests : [];
            if (!quests.length) {
                container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.7rem;">No quests yet.</p>';
                return;
            }
            container.innerHTML = quests.slice(0, 16).map((q) => {
                const qid = String(q.id || '').replace(/'/g, "\\'");
                const status = q.status || 'active';
                const tone = status === 'completed' ? 'var(--green)'
                    : status === 'failed' ? 'var(--red)'
                    : status === 'paused' ? 'var(--orange)'
                    : status === 'awaiting_approval' ? 'var(--yellow)'
                    : 'var(--teal)';
                const detail = q.last_event?.result_summary || q.last_event?.errors || '';
                const canApprove = status === 'awaiting_approval';
                const questBudget = Number.isFinite(Number(q.budget))
                    ? `$${Number(q.budget).toFixed(2)}` : 'n/a';
                const questTip = Number.isFinite(Number(q.upfront_tip))
                    ? String(Math.max(0, Math.trunc(Number(q.upfront_tip)))) : 'n/a';
                const questReward = Number.isFinite(Number(q.completion_reward))
                    ? String(Math.max(0, Math.trunc(Number(q.completion_reward)))) : 'n/a';
                const pauseBtn = q.manual_paused
                    ? `<button class="chat-room-open-btn" style="padding:0.2rem 0.35rem; font-size:0.66rem;" onclick="resumeQuest('${qid}')">Resume</button>`
                    : `<button class="chat-room-open-btn" style="padding:0.2rem 0.35rem; font-size:0.66rem; background: var(--orange); color: #111;" onclick="pauseQuest('${qid}')">Pause</button>`;
                return `
                    <div style="border:1px solid var(--border); border-radius:7px; padding:0.35rem; margin-bottom:0.3rem; background:var(--bg-dark);">
                        <div style="display:flex; justify-content:space-between; gap:0.35rem;">
                            <span style="font-size:0.72rem; color:var(--teal); font-weight:650;">${escapeHtml(q.identity_name || q.identity_id || 'resident')}</span>
                            <span style="font-size:0.66rem; color:${tone}; text-transform:uppercase;">${escapeHtml(status)}</span>
                        </div>
                        <div style="font-size:0.7rem; margin-top:0.15rem;">${escapeHtml(q.title || 'Quest')}</div>
                        <div style="font-size:0.65rem; color:var(--text-dim); margin-top:0.15rem;">Budget ${questBudget} • Upfront ${questTip} • Reward ${questReward}</div>
                        ${detail ? `<div style="font-size:0.64rem; color:var(--text-dim); margin-top:0.15rem;">${escapeHtml(String(detail).slice(0, 150))}</div>` : ''}
                        <div style="display:flex; gap:0.25rem; margin-top:0.28rem;">
                            <button class="chat-room-open-btn" style="padding:0.2rem 0.35rem; font-size:0.66rem;" onclick="tipQuest('${qid}', 10)">Tip +10</button>
                            ${pauseBtn}
                            ${canApprove ? `<button class="chat-room-open-btn" style="padding:0.2rem 0.35rem; font-size:0.66rem; background: var(--green); color:#0f1318;" onclick="approveQuest('${qid}')">Approve + Reward</button>` : ''}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function loadQuestProgress() {
            fetch('/api/quests/status')
                .then(r => r.json())
                .then(data => {
                    if (!data || !data.success) return;
                    mailboxQuests = Array.isArray(data.quests) ? data.quests : [];
                    renderQuestProgress();
                })
                .catch(() => {});
        }

        function createMailboxQuest() {
            const target = document.getElementById('mailboxTarget');
            const titleEl = document.getElementById('questTitleInput');
            const promptEl = document.getElementById('questPromptInput');
            const budgetEl = document.getElementById('questBudgetInput');
            const tipEl = document.getElementById('questTipInput');
            const rewardEl = document.getElementById('questRewardInput');
            const status = document.getElementById('questStatus');

            const identityId = String(target ? target.value : '').trim();
            const prompt = String(promptEl ? promptEl.value : '').trim();
            const title = String(titleEl ? titleEl.value : '').trim();
            const budget = Number(budgetEl ? budgetEl.value : 0.20);
            const upfrontTip = Number(tipEl ? tipEl.value : 10);
            const completionReward = Number(rewardEl ? rewardEl.value : 30);
            if (!identityId) {
                if (status) { status.textContent = 'Choose a target resident first.'; status.style.color = 'var(--red)'; }
                return;
            }
            if (!prompt) {
                if (status) { status.textContent = 'Quest objective is empty.'; status.style.color = 'var(--red)'; }
                return;
            }
            fetch('/api/quests/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    identity_id: identityId,
                    title: title,
                    prompt: prompt,
                    budget: budget,
                    upfront_tip: upfrontTip,
                    completion_reward: completionReward,
                })
            })
            .then(r => r.json().then(data => ({ status: r.status, data })))
            .then(({ status: httpStatus, data }) => {
                if (httpStatus >= 400 || !data.success) {
                    if (status) { status.textContent = data.error || 'Failed to create quest'; status.style.color = 'var(--red)'; }
                    return;
                }
                if (promptEl) promptEl.value = '';
                if (titleEl) titleEl.value = '';
                if (status) { status.textContent = `Quest started (${data.task_id || 'queued'}).`; status.style.color = 'var(--green)'; }
                showToast('Quest assigned');
                loadQuestProgress();
                loadQueueView();
            })
            .catch(() => {
                if (status) { status.textContent = 'Failed to create quest'; status.style.color = 'var(--red)'; }
                showToast('Failed to create quest', 'error');
            });
        }

        function tipQuest(questId, tokens) {
            fetch('/api/quests/tip', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ quest_id: questId, tokens: tokens }),
            })
            .then(r => r.json())
            .then(data => {
                const status = document.getElementById('questStatus');
                if (!data.success) {
                    if (status) { status.textContent = data.error || 'Tip failed'; status.style.color = 'var(--red)'; }
                    showToast(data.error || 'Tip failed', 'error');
                    return;
                }
                if (status) { status.textContent = `Tipped ${tokens} tokens.`; status.style.color = 'var(--green)'; }
                showToast(`Tipped ${tokens} tokens`);
                loadQuestProgress();
            })
            .catch(() => showToast('Tip request failed', 'error'));
        }

        function approveQuest(questId) {
            fetch('/api/quests/approve', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ quest_id: questId }),
            })
            .then(r => r.json())
            .then(data => {
                const status = document.getElementById('questStatus');
                if (!data.success) {
                    if (status) { status.textContent = data.error || 'Approval failed'; status.style.color = 'var(--red)'; }
                    showToast(data.error || 'Approval failed', 'error');
                    return;
                }
                if (status) { status.textContent = `Quest approved. Reward: ${data.reward || 0} tokens.`; status.style.color = 'var(--green)'; }
                showToast('Quest approved');
                loadQuestProgress();
            })
            .catch(() => showToast('Approval request failed', 'error'));
        }

        function pauseQuest(questId) {
            fetch('/api/quests/pause', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ quest_id: questId }),
            })
            .then(r => r.json())
            .then(data => {
                const status = document.getElementById('questStatus');
                if (!data.success) {
                    if (status) { status.textContent = data.error || 'Pause failed'; status.style.color = 'var(--red)'; }
                    showToast(data.error || 'Pause failed', 'error');
                    return;
                }
                if (status) { status.textContent = 'Quest pause requested.'; status.style.color = 'var(--orange)'; }
                showToast('Quest paused');
                loadQuestProgress();
                loadQueueView();
            })
            .catch(() => showToast('Pause request failed', 'error'));
        }

        function resumeQuest(questId) {
            fetch('/api/quests/resume', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ quest_id: questId }),
            })
            .then(r => r.json())
            .then(data => {
                const status = document.getElementById('questStatus');
                if (!data.success) {
                    if (status) { status.textContent = data.error || 'Resume failed'; status.style.color = 'var(--red)'; }
                    showToast(data.error || 'Resume failed', 'error');
                    return;
                }
                if (status) { status.textContent = 'Quest resumed.'; status.style.color = 'var(--green)'; }
                showToast('Quest resumed');
                loadQuestProgress();
                loadQueueView();
            })
            .catch(() => showToast('Resume request failed', 'error'));
        }

        function loadDmThreads() {
            const fromId = document.getElementById('dmFromIdentity')?.value || '';
            const threadsContainer = document.getElementById('dmThreadsContainer');
            const threadCountEl = document.getElementById('dmThreadCount');
            if (!threadsContainer || !fromId) {
                if (threadsContainer) threadsContainer.innerHTML = '<p style="color: var(--text-dim); font-size: 0.72rem;">Select a sender identity to view DM threads</p>';
                if (threadCountEl) threadCountEl.textContent = '';
                return;
            }
            fetch('/api/dm/threads/' + encodeURIComponent(fromId))
                .then(r => r.json())
                .then(data => {
                    const threads = Array.isArray(data.threads) ? data.threads : [];
                    if (threadCountEl) threadCountEl.textContent = threads.length ? `(${threads.length})` : '';
                    if (!threads.length) {
                        threadsContainer.innerHTML = '<p style="color: var(--text-dim); font-size: 0.72rem;">No DM threads yet</p>';
                        return;
                    }
                    threadsContainer.innerHTML = threads.map(t => {
                        const name = t.peer_name || t.peer_id || 'unknown';
                        const preview = t.latest_preview || '';
                        const count = Number(t.message_count || 0);
                        return `<button onclick="loadDmConversation('${t.peer_id}')" style="display:block;width:100%;text-align:left;margin-bottom:0.25rem;padding:0.35rem;background:var(--bg-dark);border:1px solid var(--border);color:var(--text);border-radius:4px;cursor:pointer;">
                            <div style="font-size:0.75rem;color:var(--teal);">${name} (${count})</div>
                            <div style="font-size:0.68rem;color:var(--text-dim);">${preview}</div>
                        </button>`;
                    }).join('');
                })
                .catch(() => {
                    threadsContainer.innerHTML = '<p style="color: var(--red); font-size: 0.72rem;">Failed to load DM threads</p>';
                });
        }

        function loadDmConversation(peerId) {
            const fromId = document.getElementById('dmFromIdentity')?.value || '';
            const container = document.getElementById('dmConversationContainer');
            if (!container || !fromId || !peerId) return;
            fetch('/api/dm/messages?identity_id=' + encodeURIComponent(fromId) + '&peer_id=' + encodeURIComponent(peerId) + '&limit=100')
                .then(r => r.json())
                .then(data => {
                    const messages = Array.isArray(data.messages) ? data.messages : [];
                    if (!messages.length) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.72rem;">No DM messages yet</p>';
                        return;
                    }
                    container.innerHTML = messages.map(m => {
                        const mine = String(m.author_id || '') === String(fromId);
                        const author = m.author_name || m.author_id || 'Unknown';
                        const content = m.content || '';
                        return `<div style="margin-bottom:0.35rem;padding:0.35rem;border:1px solid var(--border);border-radius:6px;background:${mine ? 'rgba(3,218,198,0.08)' : 'var(--bg-dark)'};">
                            <div style="font-size:0.68rem;color:${mine ? 'var(--teal)' : 'var(--text-dim)'};">${author}</div>
                            <div style="font-size:0.78rem;">${content}</div>
                        </div>`;
                    }).join('');
                    container.scrollTop = container.scrollHeight;
                    const toEl = document.getElementById('dmToIdentity');
                    if (toEl) toEl.value = peerId;
                })
                .catch(() => {
                    container.innerHTML = '<p style="color: var(--red); font-size: 0.72rem;">Failed to load DM conversation</p>';
                });
        }

        function sendDirectMessage() {
            const fromEl = document.getElementById('dmFromIdentity');
            const toEl = document.getElementById('dmToIdentity');
            const msgEl = document.getElementById('dmMessageInput');
            const statusEl = document.getElementById('dmStatus');
            const fromId = fromEl ? fromEl.value : '';
            const toId = toEl ? toEl.value : '';
            const content = (msgEl ? msgEl.value : '').trim();
            if (!fromId || !toId) {
                if (statusEl) { statusEl.textContent = 'Pick both sender and recipient.'; statusEl.style.color = 'var(--red)'; }
                return;
            }
            if (fromId === toId) {
                if (statusEl) { statusEl.textContent = 'Sender and recipient must be different.'; statusEl.style.color = 'var(--red)'; }
                return;
            }
            if (!content) {
                if (statusEl) { statusEl.textContent = 'Message is empty.'; statusEl.style.color = 'var(--red)'; }
                return;
            }
            fetch('/api/dm/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({from_id: fromId, to_id: toId, content: content}),
            })
            .then(r => r.json())
            .then(data => {
                if (!data.success) {
                    if (statusEl) { statusEl.textContent = data.error || 'Failed to send DM'; statusEl.style.color = 'var(--red)'; }
                    return;
                }
                if (msgEl) msgEl.value = '';
                if (statusEl) { statusEl.textContent = 'DM sent.'; statusEl.style.color = 'var(--green)'; }
                loadDmThreads();
                loadDmConversation(toId);
            })
            .catch(() => {
                if (statusEl) { statusEl.textContent = 'Failed to send DM'; statusEl.style.color = 'var(--red)'; }
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
                    document.querySelector('[style*="position: fixed"]').remove();
                    showProfile(identityId);
                    showToast('Reply sent');
                } else {
                    showToast(data.error || 'Failed to send reply', 'error');
                }
            })
            .catch(() => showToast('Failed to send reply', 'error'));
        }

        // Refresh messages periodically
        // Legacy messages polling disabled (mailbox is canonical).

        // Day vibe setup
        function setupDayVibe() {
            const cycleSec = Math.max(1, Number(logCycleSeconds || 10));
            const nowSec = Date.now() / 1000;
            const cycleId = Math.floor(nowSec / cycleSec);
            const day = ((cycleId % 7) + 7) % 7;
            const phase = (nowSec % cycleSec) / cycleSec;
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

            // Phase overrides are tied to resident-cycle progress, not wall-clock time.
            let vibe = vibes[day];
            if (phase < 0.2) vibe = { ...vibe, text: vibe.text + ' - Dawn' };
            else if (phase > 0.85) vibe = { ...vibe, text: vibe.text + ' - Wind Down' };

            vibeEl.className = 'day-vibe ' + vibe.class;
            iconEl.textContent = vibe.icon;
            if (dayVibeBaselineCycle == null) {
                dayVibeBaselineCycle = Number.isFinite(currentRuntimeCycleId) ? currentRuntimeCycleId : cycleId;
            }
            const displayDay = cycleToDisplayDay(cycleId, dayVibeBaselineCycle);
            textEl.textContent = `Resident Day ${displayDay || 1} (${vibe.text})`;
            vibeEl.title = 'Resident machine-day reference (derived from runtime cycle length)';
        }

        // Slideout panel
        function toggleSlideout() {
            const panel = document.getElementById('slideoutPanel');
            const overlay = document.getElementById('slideoutOverlay');
            const isOpen = panel.classList.contains('open');
            const identitiesPanel = document.getElementById('identitiesSlideoutPanel');
            const identitiesOverlay = document.getElementById('identitiesSlideoutOverlay');

            if (isOpen) {
                panel.classList.remove('open');
                overlay.classList.remove('open');
            } else {
                if (identitiesPanel) identitiesPanel.classList.remove('open');
                if (identitiesOverlay) identitiesOverlay.classList.remove('open');
                panel.classList.add('open');
                overlay.classList.add('open');
                loadCompletedRequests();
            }
        }

        function toggleIdentitiesSlideout() {
            const panel = document.getElementById('identitiesSlideoutPanel');
            const overlay = document.getElementById('identitiesSlideoutOverlay');
            if (!panel || !overlay) return;
            const isOpen = panel.classList.contains('open');
            const requestsPanel = document.getElementById('slideoutPanel');
            const requestsOverlay = document.getElementById('slideoutOverlay');

            if (isOpen) {
                panel.classList.remove('open');
                overlay.classList.remove('open');
            } else {
                if (requestsPanel) requestsPanel.classList.remove('open');
                if (requestsOverlay) requestsOverlay.classList.remove('open');
                panel.classList.add('open');
                overlay.classList.add('open');
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
                        persistDraftInputs(true);
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
                    showToast('Bounty created');
                } else {
                    showToast(data.error || 'Failed to create bounty', 'error');
                }
            })
            .catch(() => showToast('Failed to create bounty', 'error'));
        }

        function loadBounties() {
            fetch('/api/bounties')
                .then(r => r.json())
                .then(data => {
                    const bounties = data.bounties ?? data;
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
                    if (data.success) {
                        loadBounties();
                        showToast('Bounty cancelled');
                    } else {
                        showToast(data.error || 'Failed to delete bounty', 'error');
                    }
                })
                .catch(() => showToast('Failed to delete bounty', 'error'));
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
                                                ${Array.from(new Set(s.artifacts)).map(a => `<a href="#" onclick="viewArtifact('${a}'); return false;" style="color: var(--purple); margin-right: 0.5rem;">${a.split('/').pop()}</a>`).join('')}
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
        let latestChatRooms = [];
        let currentChatModalRoomId = null;
        let chatRoomModalPoller = null;

        function loadChatRooms() {
            fetch('/api/chatrooms')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('chatRoomsContainer');
                    const countEl = document.getElementById('chatRoomsCount');

                    if (!data.success || !data.rooms || data.rooms.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.8rem;">No chat rooms yet. Rooms appear when residents start chatting!</p>';
                        countEl.textContent = '';
                        latestChatRooms = [];
                        return;
                    }

                    latestChatRooms = data.rooms;
                    const totalMessages = data.rooms.reduce((sum, r) => sum + (r.message_count || 0), 0);
                    countEl.textContent = `(${totalMessages} messages)`;

                    container.innerHTML = data.rooms.map(room => `
                        <div class="chat-room-card">
                            <div class="chat-room-card-header">
                                <span style="font-size: 1.05rem;">${room.icon || '💬'}</span>
                                <span style="flex: 1;">
                                    <span style="font-weight: 650; color: var(--teal);">${escapeHtml(room.name || room.id)}</span>
                                    <span style="font-size: 0.7rem; color: var(--text-dim); margin-left: 0.3rem;">(${room.message_count || 0})</span>
                                </span>
                                <span style="font-size: 0.65rem; color: var(--text-dim);">
                                    ${room.latest_timestamp ? new Date(room.latest_timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '--:--'}
                                </span>
                                <button class="chat-room-open-btn" onclick="openChatRoomModalById('${encodeURIComponent(room.id)}')">Popout</button>
                            </div>
                            <div style="margin-top: 0.45rem; font-size: 0.73rem; color: var(--text-dim);">
                                ${escapeHtml(room.description || 'No description')}
                            </div>
                            <div style="margin-top: 0.35rem; font-size: 0.75rem; color: var(--text); line-height: 1.35;">
                                ${escapeHtml(room.latest_preview || 'No messages yet.')}
                            </div>
                        </div>
                    `).join('');
                });
        }

        function openChatRoomModalById(encodedRoomId) {
            const roomId = decodeURIComponent(encodedRoomId || '');
            const room = latestChatRooms.find(r => r.id === roomId) || { id: roomId, name: roomId, icon: '💬' };
            openChatRoomModal(room.id, room.name, room.icon);
        }

        function openChatRoomModal(roomId, roomName, roomIcon) {
            currentChatModalRoomId = roomId;
            const modal = document.getElementById('chatRoomModal');
            document.getElementById('chatRoomModalTitle').textContent = roomName || roomId || 'Chat Room';
            document.getElementById('chatRoomModalSubtitle').textContent = roomId || '';
            document.getElementById('chatRoomModalIcon').textContent = roomIcon || '💬';
            modal.classList.add('open');
            loadChatRoomModalMessages();
            if (chatRoomModalPoller) clearInterval(chatRoomModalPoller);
            chatRoomModalPoller = setInterval(() => {
                if (currentChatModalRoomId) loadChatRoomModalMessages(false);
            }, 4000);
        }

        function closeChatRoomModal() {
            currentChatModalRoomId = null;
            const modal = document.getElementById('chatRoomModal');
            if (modal) modal.classList.remove('open');
            if (chatRoomModalPoller) {
                clearInterval(chatRoomModalPoller);
                chatRoomModalPoller = null;
            }
        }

        function handleChatRoomModalBackdrop(event) {
            if (event && event.target && event.target.id === 'chatRoomModal') {
                closeChatRoomModal();
            }
        }

        function escapeHtml(value) {
            const div = document.createElement('div');
            div.textContent = String(value || '');
            return div.innerHTML;
        }

        function loadChatRoomModalMessages(scrollToBottom=true) {
            if (!currentChatModalRoomId) return;
            const container = document.getElementById('chatRoomModalMessages');
            const meta = document.getElementById('chatRoomModalMeta');
            if (!container || !meta) return;

            const nearBottom = (container.scrollHeight - container.scrollTop - container.clientHeight) < 40;

            fetch('/api/chatrooms/' + encodeURIComponent(currentChatModalRoomId))
                .then(r => r.json())
                .then(data => {
                    if (!data.success || !data.messages || data.messages.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.8rem; font-style: italic;">No messages in this room yet.</p>';
                        meta.textContent = '0 messages';
                        return;
                    }

                    meta.textContent = `${data.messages.length} recent messages`;
                    container.innerHTML = data.messages.map(msg => {
                        const time = msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '';
                        const mood = msg.mood ? ` <span style="opacity: 0.6;">(${msg.mood})</span>` : '';
                        const replyTo = msg.reply_to ? `<div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.2rem;">↳ replying to ${escapeHtml(String(msg.reply_to).slice(0, 24))}</div>` : '';
                        const linkedContent = linkifyFilePaths(msg.content || '');

                        return `
                            <div class="chat-msg">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                                    <span style="font-weight: 600; color: var(--teal); font-size: 0.84rem;">${escapeHtml(msg.author_name || 'Unknown')}${mood}</span>
                                    <span style="font-size: 0.68rem; color: var(--text-dim);">${time}</span>
                                </div>
                                ${replyTo}
                                <div style="font-size: 0.9rem; color: var(--text); line-height: 1.45;">${linkedContent}</div>
                            </div>
                        `;
                    }).join('');

                    if (scrollToBottom || nearBottom) {
                        container.scrollTop = container.scrollHeight;
                    }
                });
        }

        function loadArtifacts() {
            fetch('/api/artifacts/list')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('artifactsContainer');
                    const countEl = document.getElementById('artifactCount');

                    if (!data.success || !data.artifacts || data.artifacts.length === 0) {
                        container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.75rem;">No artifacts yet</p>';
                        countEl.textContent = '';
                        return;
                    }

                    const artifacts = data.artifacts.slice(0, 20);
                    countEl.textContent = `(${artifacts.length})`;
                    container.innerHTML = artifacts.map(artifact => {
                        const safePath = String(artifact.path || '').replace(/'/g, "\\'");
                        const iconByType = {
                            journal: 'J',
                            creative_work: 'W',
                            community_doc: 'D',
                            skill: 'S',
                        };
                        const icon = iconByType[artifact.type] || 'F';
                        const modified = artifact.modified
                            ? new Date(artifact.modified).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
                            : '';

                        return `
                            <div class="identity-card" style="margin-bottom: 0.4rem; padding: 0.5rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center; gap: 0.5rem;">
                                    <span style="color: var(--purple); font-size: 0.75rem; font-weight: 600;">${icon}</span>
                                    <a href="#" onclick="viewArtifact('${safePath}'); return false;"
                                       style="flex: 1; color: var(--teal); text-decoration: underline; font-size: 0.75rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                                        ${artifact.name}
                                    </a>
                                    <span style="color: var(--text-dim); font-size: 0.65rem;">${modified}</span>
                                </div>
                                <div style="margin-top: 0.2rem; color: var(--text-dim); font-size: 0.65rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                                    ${artifact.path}
                                </div>
                            </div>
                        `;
                    }).join('');
                });
        }

        function renderInsightCards(cards) {
            const container = document.getElementById('insightCards');
            if (!container) return;
            if (!Array.isArray(cards) || cards.length === 0) {
                container.innerHTML = `
                    <details class="insight-card" open>
                        <summary>
                            <div class="insight-label">Stats</div>
                            <div class="insight-value">--</div>
                            <div class="insight-sub">No metrics available</div>
                        </summary>
                        <div class="insight-detail">Insights API returned no cards.</div>
                    </details>
                `;
                return;
            }
            container.innerHTML = cards.map(card => {
                const tone = card.tone ? String(card.tone) : '';
                const details = Array.isArray(card.details) ? card.details.join('\\n') : '';
                return `
                    <details class="insight-card">
                        <summary>
                            <div class="insight-label">${escapeHtml(card.label || 'Metric')}</div>
                            <div class="insight-value ${escapeHtml(tone)}">${escapeHtml(card.headline || '--')}</div>
                            <div class="insight-sub">${escapeHtml(card.subline || '')}</div>
                        </summary>
                        <div class="insight-detail">${escapeHtml(details)}</div>
                    </details>
                `;
            }).join('');
        }

        function loadSwarmInsights() {
            fetch('/api/insights')
                .then(r => r.json())
                .then(data => {
                    if (!data.success) return;
                    renderInsightCards(data.metric_cards || []);
                    const formatUsdDisplay = (value) => {
                        const n = Number(value);
                        if (!Number.isFinite(n)) return '--';
                        const abs = Math.abs(n);
                        if (abs === 0) return '$0.00';
                        if (abs < 0.01) return '$' + n.toFixed(4);
                        if (abs < 1) return '$' + n.toFixed(3);
                        return '$' + n.toFixed(2);
                    };
                    const apiCost24h = data.ops && Number.isFinite(Number(data.ops.api_cost_24h))
                        ? Number(data.ops.api_cost_24h) : 0;
                    const apiCost = data.ops && Number.isFinite(Number(data.ops.api_cost_all_time))
                        ? Number(data.ops.api_cost_all_time) : 0;
                    const spent24hEl = document.getElementById('spent24h');
                    if (spent24hEl) spent24hEl.textContent = formatUsdDisplay(apiCost24h);
                    const totalSpentEl = document.getElementById('totalSpent');
                    if (totalSpentEl) totalSpentEl.textContent = formatUsdDisplay(apiCost);
                })
                .catch(() => {
                    const spent24hEl = document.getElementById('spent24h');
                    if (spent24hEl) spent24hEl.textContent = '--';
                    const totalSpentEl = document.getElementById('totalSpent');
                    if (totalSpentEl) totalSpentEl.textContent = '--';
                    renderInsightCards([
                        {
                            label: 'Stats',
                            headline: 'OFFLINE',
                            subline: 'Insights API unavailable',
                            tone: 'bad',
                            details: ['Unable to load stats right now.'],
                        },
                    ]);
                });
        }

        // Initial load
        setupDayVibe();
        setInterval(setupDayVibe, 5000); // Keep up with short resident cycles.
        fetch('/api/identities').then(r => r.json()).then(updateIdentities);
        loadWorkerStatus();
        loadRequest();
        // Legacy messages/DM panels are hidden; mailbox is the active communication UI.
        restoreDraftInputs();
        bindDraftInputs();
        loadBounties();
        loadChatRooms();
        loadArtifacts();
        loadStopStatus();
        loadRuntimeSpeed();
        loadUiSettings();
        refreshCreativeSeed();
        loadGroqKeyStatus();
        loadSwarmInsights();
        loadQueueView();
        loadOneTimeTasks();
        loadMailboxData();
        loadQuestProgress();
        updateLogEmptyState();

        // Refresh bounties, spawner status, and chat rooms periodically
        setInterval(loadBounties, 10000);
        setInterval(loadWorkerStatus, 5000);
        setInterval(loadRecentLogs, 2000);  // Fallback so logs update if socket misses events
        loadRecentLogs();  // Initial load so log isn't empty on first open
        // Legacy DM polling disabled (mailbox replaces it).
        setInterval(loadChatRooms, 15000);  // Refresh chat rooms every 15 seconds
        setInterval(loadArtifacts, 15000);
        setInterval(loadStopStatus, 5000);
        setInterval(loadRuntimeSpeed, 15000);
        setInterval(loadGroqKeyStatus, 30000);
        setInterval(loadSwarmInsights, 10000);
        setInterval(loadQueueView, 5000);
        setInterval(loadOneTimeTasks, 15000);
        setInterval(loadMailboxData, 5000);
        setInterval(loadQuestProgress, 5000);
    </script>
</body>
</html>
'''
