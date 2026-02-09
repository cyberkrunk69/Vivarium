/**
 * Live Log Stream
 * Tails the last 50 lines from grind_logs/ in real‑time.
 * Color‑codes by log level:
 *   START → blue, DONE → green, FAIL → red, SKIP → gray
 * Auto‑scrolls unless the user hovers over the panel (pause on hover).
 */

(() => {
    const LOG_PANEL_ID = 'log-panel';
    const POLL_INTERVAL_MS = 1000; // 1 second
    const LOG_ENDPOINT = '/grind_logs/tail?lines=50'; // Adjust if needed

    const panel = document.getElementById(LOG_PANEL_ID);
    if (!panel) return;

    let polling = true;
    let lastFetched = ''; // simple deduplication

    const levelClass = (level) => `log-${level}`;

    const renderLines = (lines) => {
        panel.innerHTML = ''; // clear old content
        lines.forEach(line => {
            const trimmed = line.trim();
            // Expected format: LEVEL: message
            const match = trimmed.match(/^(\w+):\s*(.*)$/);
            let level = 'INFO';
            let message = trimmed;
            if (match) {
                level = match[1];
                message = match[2];
            }
            const span = document.createElement('div');
            span.className = `log-line ${levelClass(level)}`;
            span.textContent = line;
            panel.appendChild(span);
        });
        // Auto‑scroll to bottom
        panel.scrollTop = panel.scrollHeight;
    };

    const fetchLog = async () => {
        try {
            const resp = await fetch(LOG_ENDPOINT, { cache: 'no-store' });
            if (!resp.ok) return;
            const text = await resp.text();
            if (text === lastFetched) return; // no change
            lastFetched = text;
            const lines = text.split('\n').filter(l => l.length);
            renderLines(lines);
        } catch (e) {
            console.error('Log fetch error:', e);
        }
    };

    // Pause on hover
    panel.addEventListener('mouseenter', () => { polling = false; });
    panel.addEventListener('mouseleave', () => { polling = true; });

    // Poll loop
    setInterval(() => {
        if (polling) fetchLog();
    }, POLL_INTERVAL_MS);

    // Initial load
    fetchLog();
})();