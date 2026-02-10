/**
 * Dashboard script – modern ES module, no HTML inside JS.
 * Handles:
 *   • Tree generation & auto‑scaling
 *   • Drag‑and‑drop of nodes
 *   • LIFO collapse animation (120 ms stagger)
 *   • SSE connection to /events
 *   • Floating chat UI
 */

const treeContainer = document.getElementById('tree-container');
const chatToggle = document.getElementById('chat-toggle');
const chatBox = document.getElementById('floating-chat');
const chatClose = document.getElementById('chat-close');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');

/* ---------- 1. SAMPLE TREE DATA ---------- */
const sampleTree = {
    id: 'root',
    label: 'Root',
    children: [
        { id: 'a', label: 'Node A', children: [] },
        {
            id: 'b',
            label: 'Node B',
            children: [
                { id: 'b1', label: 'Node B1', children: [] },
                { id: 'b2', label: 'Node B2', children: [] }
            ]
        },
        { id: 'c', label: 'Node C', children: [] }
    ]
};

/* ---------- 2. RENDER TREE ---------- */
function renderNode(node, depth = 0, parentPos = {x: 20, y: 20}) {
    const el = document.createElement('div');
    el.className = 'node';
    el.dataset.id = node.id;
    el.textContent = node.label;
    el.style.left = `${parentPos.x + depth * 150}px`;
    el.style.top = `${parentPos.y}px`;

    // store children positions for later rendering
    treeContainer.appendChild(el);

    // attach collapse toggle
    el.addEventListener('dblclick', () => toggleCollapse(node.id));

    // make draggable
    makeDraggable(el);

    // Render children recursively
    const childYStart = parentPos.y + 80;
    node.children.forEach((child, idx) => {
        renderNode(child, depth + 1, {
            x: parentPos.x,
            y: childYStart + idx * 80
        });
    });
}

/* ---------- 3. DRAG‑AND‑DROP ---------- */
function makeDraggable(nodeEl) {
    let offsetX = 0;
    let offsetY = 0;
    let isDragging = false;

    const onMouseDown = (e) => {
        isDragging = true;
        nodeEl.classList.add('dragging');
        const rect = nodeEl.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    };

    const onMouseMove = (e) => {
        if (!isDragging) return;
        const containerRect = treeContainer.getBoundingClientRect();
        let left = e.clientX - containerRect.left - offsetX;
        let top  = e.clientY - containerRect.top - offsetY;
        // constrain within container
        left = Math.max(0, Math.min(left, containerRect.width - nodeEl.offsetWidth));
        top  = Math.max(0, Math.min(top, containerRect.height - nodeEl.offsetHeight));
        nodeEl.style.left = `${left}px`;
        nodeEl.style.top  = `${top}px`;
    };

    const onMouseUp = () => {
        isDragging = false;
        nodeEl.classList.remove('dragging');
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    };

    nodeEl.addEventListener('mousedown', onMouseDown);
}

/* ---------- 4. COLLAPSE / EXPAND ---------- */
function toggleCollapse(nodeId) {
    // Find all descendant nodes (simple BFS)
    const queue = [nodeId];
    const nodesToToggle = [];

    while (queue.length) {
        const currentId = queue.shift();
        const el = document.querySelector(`.node[data-id="${currentId}"]`);
        if (el) nodesToToggle.push(el);
        // Find children in the sampleTree structure
        const dataNode = findNodeById(sampleTree, currentId);
        if (dataNode && dataNode.children) {
            dataNode.children.forEach(child => queue.push(child.id));
        }
    }

    // LIFO collapse: reverse order, stagger 120ms
    nodesToToggle.reverse().forEach((el, idx) => {
        setTimeout(() => {
            el.classList.toggle('collapsed');
        }, idx * 120);
    });
}

/* Helper to locate node in sampleTree */
function findNodeById(root, id) {
    if (root.id === id) return root;
    for (const child of root.children || []) {
        const found = findNodeById(child, id);
        if (found) return found;
    }
    return null;
}

/* ---------- 5. AUTO‑SCALING (simple responsive) ---------- */
function autoScale() {
    const width = treeContainer.scrollWidth;
    const height = treeContainer.scrollHeight;
    treeContainer.style.minWidth = `${width}px`;
    treeContainer.style.minHeight = `${height}px`;
}
window.addEventListener('resize', autoScale);

/* ---------- 6. SERVER‑SENT EVENTS ---------- */
function initSSE() {
    const evtSource = new EventSource('/events');

    evtSource.addEventListener('progress', (e) => {
        const data = JSON.parse(e.data);
        // Example: update a progress bar (placeholder)
        console.log('Progress event:', data);
    });

    evtSource.onerror = (err) => {
        console.error('SSE error', err);
        evtSource.close();
    };
}

/* ---------- 7. FLOATING CHAT ---------- */
chatToggle.addEventListener('click', () => {
    chatBox.classList.toggle('hidden');
});

chatClose.addEventListener('click', () => {
    chatBox.classList.add('hidden');
});

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && chatInput.value.trim()) {
        const msg = chatInput.value.trim();
        const div = document.createElement('div');
        div.textContent = `You: ${msg}`;
        chatMessages.appendChild(div);
        chatInput.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight;
        // Echo back as placeholder
        setTimeout(() => {
            const echo = document.createElement('div');
            echo.textContent = `Bot: Received "${msg}"`;
            chatMessages.appendChild(echo);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 500);
    }
});

/* ---------- 8. INITIALISE ---------- */
function init() {
    renderNode(sampleTree);
    autoScale();
    initSSE();
}
init();