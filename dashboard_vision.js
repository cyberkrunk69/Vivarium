/**
 * BLACK SWARM - Living Dashboard JavaScript
 * Implements the UX Motion Vision from UX_MOTION_SPEC.md
 */

// ============================================
// STATE
// ============================================
const state = {
    nodes: [],
    quests: [],
    activeWorkers: 0,
    completedTasks: 0,
    totalCost: 0,
    eventSource: null
};

// Completion quips
const QUIPS = [
    "got 'er done",
    "finally",
    "that was rough",
    "nailed it",
    "ez",
    "ship it"
];

// ============================================
// DOM ELEMENTS
// ============================================
const elements = {
    nodesContainer: document.getElementById('nodes-container'),
    questList: document.getElementById('quest-list'),
    activeWorkers: document.getElementById('active-workers'),
    completedTasks: document.getElementById('completed-tasks'),
    totalCost: document.getElementById('total-cost'),
    chatInput: document.getElementById('chat-input'),
    sendBtn: document.getElementById('send-btn'),
    collapseHistory: document.getElementById('collapse-history'),
    historyDashboard: document.getElementById('history-dashboard')
};

// ============================================
// NODE MANAGEMENT
// ============================================
let nodeIdCounter = 0;

function createNode(type, title, parentId = null) {
    const node = {
        id: `node-${nodeIdCounter++}`,
        type: type, // understanding, worker, helper, expert
        title: title,
        status: 'pending',
        progress: 0,
        parentId: parentId,
        spawnTime: Date.now(),
        depth: parentId ? (getNode(parentId)?.depth || 0) + 1 : 0,
        element: null
    };

    const el = document.createElement('div');
    el.className = `node ${type} spawning`;
    el.id = node.id;
    el.innerHTML = `
        <div class="node-header">
            <span class="node-type">${type}</span>
        </div>
        <div class="node-title">${title}</div>
        <div class="node-status">Pending...</div>
        <div class="node-progress">
            <div class="node-progress-fill"></div>
        </div>
    `;

    node.element = el;
    state.nodes.push(node);
    elements.nodesContainer.appendChild(el);

    // Remove spawn animation class after it completes
    setTimeout(() => el.classList.remove('spawning'), 350);

    // Draw connection line if has parent
    if (parentId) {
        drawConnectionLine(parentId, node.id);
    }

    return node;
}

function getNode(id) {
    return state.nodes.find(n => n.id === id);
}

function updateNode(id, updates) {
    const node = getNode(id);
    if (!node) return;

    Object.assign(node, updates);

    if (updates.status) {
        node.element.querySelector('.node-status').textContent =
            updates.status === 'running' ? 'Working...' :
            updates.status === 'completed' ? 'Done!' :
            updates.status === 'failed' ? 'Failed' : 'Pending...';

        if (updates.status === 'running') {
            node.element.classList.add('running');
        } else {
            node.element.classList.remove('running');
        }
    }

    if (updates.progress !== undefined) {
        node.element.querySelector('.node-progress-fill').style.width =
            `${updates.progress * 100}%`;
    }
}

function drawConnectionLine(parentId, childId) {
    const parent = document.getElementById(parentId);
    const child = document.getElementById(childId);
    if (!parent || !child) return;

    const line = document.createElement('div');
    line.className = 'connection-line active';
    line.dataset.from = parentId;
    line.dataset.to = childId;

    // Position will be updated by updateConnectionLines()
    elements.nodesContainer.appendChild(line);
    updateConnectionLines();
}

function updateConnectionLines() {
    const lines = elements.nodesContainer.querySelectorAll('.connection-line');
    lines.forEach(line => {
        const parent = document.getElementById(line.dataset.from);
        const child = document.getElementById(line.dataset.to);
        if (!parent || !child) return;

        const parentRect = parent.getBoundingClientRect();
        const childRect = child.getBoundingClientRect();
        const containerRect = elements.nodesContainer.getBoundingClientRect();

        const startX = parentRect.right - containerRect.left;
        const startY = parentRect.top + parentRect.height / 2 - containerRect.top;
        const endX = childRect.left - containerRect.left;
        const length = endX - startX;

        line.style.left = `${startX}px`;
        line.style.top = `${startY}px`;
        line.style.width = `${Math.max(0, length)}px`;
    });
}

// ============================================
// COLLAPSE SEQUENCE (Thunk Thunk Thunk)
// ============================================
async function collapseSequence(nodes) {
    const THUNK_DELAY = 120;
    const COLLAPSE_DURATION = 250;

    // Sort: deepest/last-spawned first (LIFO)
    const orderedNodes = [...nodes].sort((a, b) =>
        b.depth - a.depth || b.spawnTime - a.spawnTime
    );

    // Show completion quip on the last node before collapse
    if (orderedNodes.length > 0) {
        const primaryNode = orderedNodes[orderedNodes.length - 1];
        showQuip(primaryNode.element, QUIPS[Math.floor(Math.random() * QUIPS.length)]);
        await sleep(300);
    }

    for (const node of orderedNodes) {
        const parent = node.parentId ? getNode(node.parentId) : null;
        const targetX = parent ? -100 : -200; // Collapse toward parent or dashboard
        const targetY = 0;

        node.element.style.setProperty('--collapse-x', `${targetX}px`);
        node.element.style.setProperty('--collapse-y', `${targetY}px`);
        node.element.classList.add('collapsing');

        // Retract connection line
        const line = elements.nodesContainer.querySelector(
            `.connection-line[data-to="${node.id}"]`
        );
        if (line) {
            line.classList.add('retracting');
        }

        await sleep(THUNK_DELAY);
    }

    // Wait for last animation to complete
    await sleep(COLLAPSE_DURATION);

    // Clean up DOM
    orderedNodes.forEach(node => {
        node.element.remove();
        const line = elements.nodesContainer.querySelector(
            `.connection-line[data-to="${node.id}"]`
        );
        if (line) line.remove();
    });

    // Remove from state
    state.nodes = state.nodes.filter(n => !orderedNodes.includes(n));

    // Add to history
    addToHistory(orderedNodes[orderedNodes.length - 1]?.title || 'Task');
}

function showQuip(element, text) {
    const quip = document.createElement('div');
    quip.className = 'completion-quip';
    quip.textContent = text;
    element.appendChild(quip);
}

function addToHistory(title) {
    const quest = document.createElement('div');
    quest.className = 'quest-item';
    quest.innerHTML = `
        <div class="quest-title">${title}</div>
        <div class="quest-time">${new Date().toLocaleTimeString()}</div>
    `;
    elements.questList.insertBefore(quest, elements.questList.firstChild);
    state.completedTasks++;
    updateStats();
}

// ============================================
// SSE CONNECTION
// ============================================
function connectSSE() {
    const eventSource = new EventSource('/events');
    state.eventSource = eventSource;

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleEvent(data);
    };

    eventSource.onerror = () => {
        console.log('SSE disconnected, retrying...');
        setTimeout(connectSSE, 3000);
    };
}

function handleEvent(event) {
    switch (event.type) {
        case 'task_started':
            const node = createNode(
                event.nodeType || 'worker',
                event.title,
                event.parentId
            );
            updateNode(node.id, { status: 'running' });
            state.activeWorkers++;
            updateStats();
            break;

        case 'task_progress':
            updateNode(event.nodeId, { progress: event.progress });
            break;

        case 'task_completed':
            updateNode(event.nodeId, { status: 'completed', progress: 1 });
            state.activeWorkers = Math.max(0, state.activeWorkers - 1);
            state.totalCost += event.cost || 0;
            updateStats();

            // Trigger collapse after brief pause
            setTimeout(() => {
                const node = getNode(event.nodeId);
                if (node) {
                    const childNodes = state.nodes.filter(n => n.parentId === node.id);
                    collapseSequence([...childNodes, node]);
                }
            }, 500);
            break;

        case 'task_failed':
            updateNode(event.nodeId, { status: 'failed' });
            state.activeWorkers = Math.max(0, state.activeWorkers - 1);
            updateStats();
            break;

        case 'stats_update':
            state.activeWorkers = event.activeWorkers || state.activeWorkers;
            state.completedTasks = event.completedTasks || state.completedTasks;
            state.totalCost = event.totalCost || state.totalCost;
            updateStats();
            break;
    }
}

// ============================================
// STATS
// ============================================
function updateStats() {
    elements.activeWorkers.textContent = state.activeWorkers;
    elements.completedTasks.textContent = state.completedTasks;
    elements.totalCost.textContent = `$${state.totalCost.toFixed(2)}`;
}

// ============================================
// UI INTERACTIONS
// ============================================
function setupEventListeners() {
    // Send button
    elements.sendBtn.addEventListener('click', sendMessage);
    elements.chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Collapse history
    elements.collapseHistory.addEventListener('click', () => {
        elements.historyDashboard.classList.toggle('collapsed');
    });

    // Window resize - update connection lines
    window.addEventListener('resize', updateConnectionLines);
}

async function sendMessage() {
    const input = elements.chatInput.value.trim();
    if (!input) return;

    elements.chatInput.value = '';

    // Create understanding node
    const node = createNode('understanding', input);
    updateNode(node.id, { status: 'running' });
    state.activeWorkers++;
    updateStats();

    // Send to backend
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: input })
        });
        // Server will send events via SSE
    } catch (error) {
        console.error('Send error:', error);
        updateNode(node.id, { status: 'failed' });
    }
}

// ============================================
// UTILITIES
// ============================================
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================
// DEMO MODE (for testing without backend)
// ============================================
async function runDemo() {
    // Create understanding node
    const understanding = createNode('understanding', 'Build a task scheduler');
    await sleep(500);
    updateNode(understanding.id, { status: 'running', progress: 0.2 });

    await sleep(800);

    // Spawn workers
    const worker1 = createNode('worker', 'Design architecture', understanding.id);
    const worker2 = createNode('worker', 'Write tests', understanding.id);
    updateNode(worker1.id, { status: 'running', progress: 0.1 });
    updateNode(worker2.id, { status: 'running', progress: 0.1 });

    state.activeWorkers = 3;
    updateStats();

    await sleep(600);

    // Spawn helper
    const helper = createNode('helper', 'Generate types', worker1.id);
    updateNode(helper.id, { status: 'running', progress: 0.3 });

    await sleep(1000);

    // Progress updates
    updateNode(understanding.id, { progress: 0.5 });
    updateNode(worker1.id, { progress: 0.6 });
    updateNode(worker2.id, { progress: 0.4 });
    updateNode(helper.id, { progress: 0.8 });

    await sleep(1200);

    // Complete helper
    updateNode(helper.id, { status: 'completed', progress: 1 });

    await sleep(500);

    // Complete workers
    updateNode(worker1.id, { status: 'completed', progress: 1 });
    updateNode(worker2.id, { status: 'completed', progress: 1 });
    updateNode(understanding.id, { progress: 0.9 });

    await sleep(800);

    // Complete understanding
    updateNode(understanding.id, { status: 'completed', progress: 1 });

    await sleep(500);

    // Collapse sequence!
    await collapseSequence([helper, worker1, worker2, understanding]);
}

// ============================================
// INIT
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    updateConnectionLines();

    // Try to connect SSE, fall back to demo
    try {
        connectSSE();
    } catch (e) {
        console.log('SSE not available, running demo mode');
    }

    // Run demo after 2 seconds if no events received
    setTimeout(() => {
        if (state.nodes.length === 0) {
            runDemo();
        }
    }, 2000);
});
