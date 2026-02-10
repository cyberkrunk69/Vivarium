/**
 * Keyboard shortcuts for the dashboard.
 *
 * Shortcuts:
 *   - g : Switch to Grid view
 *   - l : Switch to Log view
 *   - t : Switch to Tree view
 *   - Space : Pause/Resume auto‑refresh
 *   - r : Force refresh
 *   - ? : Show help overlay
 *
 * The current mode is displayed in the header element with id="dashboard-header-mode".
 *
 * This module should be imported once (e.g., in the main dashboard entry point).
 */

(() => {
    // Mapping of shortcut keys to actions
    const shortcuts = {
        g: () => switchView('grid'),
        l: () => switchView('log'),
        t: () => switchView('tree'),
        ' ': () => toggleAutoRefresh(),
        r: () => forceRefresh(),
        '?': () => toggleHelpOverlay(),
    };

    // Helper to dispatch custom events that the existing dashboard can listen to.
    function dispatchDashboardEvent(name, detail = {}) {
        const event = new CustomEvent(name, { detail });
        window.dispatchEvent(event);
    }

    // View switching
    function switchView(view) {
        dispatchDashboardEvent('dashboard:view:switch', { view });
        updateHeaderMode(view);
    }

    // Auto‑refresh control
    let autoRefreshPaused = false;
    function toggleAutoRefresh() {
        autoRefreshPaused = !autoRefreshPaused;
        dispatchDashboardEvent('dashboard:autoRefresh:toggle', { paused: autoRefreshPaused });
        updateHeaderMode(autoRefreshPaused ? 'paused' : 'running');
    }

    // Force refresh
    function forceRefresh() {
        dispatchDashboardEvent('dashboard:refresh:force');
    }

    // Help overlay
    let helpOverlayVisible = false;
    function toggleHelpOverlay() {
        helpOverlayVisible = !helpOverlayVisible;
        dispatchDashboardEvent('dashboard:help:toggle', { visible: helpOverlayVisible });
    }

    // Header mode display
    function updateHeaderMode(mode) {
        const headerEl = document.getElementById('dashboard-header-mode');
        if (headerEl) {
            headerEl.textContent = mode.charAt(0).toUpperCase() + mode.slice(1);
        }
    }

    // Keydown listener
    window.addEventListener('keydown', (e) => {
        // Ignore if focus is on an input/textarea/select element
        const targetTag = e.target.tagName.toLowerCase();
        if (['input', 'textarea', 'select'].includes(targetTag)) return;

        const key = e.key.toLowerCase();
        if (shortcuts[key]) {
            e.preventDefault();
            shortcuts[key]();
        }
    });

    // Initial mode display (default to grid view)
    document.addEventListener('DOMContentLoaded', () => {
        updateHeaderMode('grid');
    });
})();