/**
 * Dashboard Keyboard Shortcuts
 *
 * This module registers global keyboard shortcuts for the dashboard UI:
 *   - g : switch to Grid view
 *   - l : switch to Log view
 *   - t : switch to Tree view
 *   - Space : pause / resume auto‑refresh
 *   - r : force immediate refresh
 *   - ? : toggle the help overlay
 *
 * It also updates the header to display the current view mode.
 *
 * Integration:
 *   1. Include this script in the dashboard page (e.g. <script src=".../dashboard_shortcuts.js"></script>).
 *   2. Ensure the dashboard object exposes the following API:
 *        dashboard.setView(mode)            // mode = 'grid' | 'log' | 'tree'
 *        dashboard.toggleAutoRefresh()
 *        dashboard.refresh()
 *        dashboard.toggleHelpOverlay()
 *   3. The header element that shows the current mode must have the id `dashboard-header-mode`.
 *
 * The script is deliberately defensive – it checks for the existence of the required
 * dashboard methods and UI elements before acting, preventing runtime errors if the
 * surrounding code changes.
 */

(function () {
    // Mapping from key to view mode
    const viewKeyMap = {
        'g': 'grid',
        'l': 'log',
        't': 'tree'
    };

    // State tracking for auto‑refresh
    let autoRefreshPaused = false;

    // Helper: update the mode indicator in the header
    function updateHeader(mode) {
        const headerEl = document.getElementById('dashboard-header-mode');
        if (headerEl) {
            headerEl.textContent = `Mode: ${mode.charAt(0).toUpperCase() + mode.slice(1)}`;
        }
    }

    // Main keydown handler
    function onKeyDown(event) {
        // Ignore events from input/textarea/select elements to avoid interfering with typing
        const targetTag = event.target.tagName.toLowerCase();
        if (['input', 'textarea', 'select'].includes(targetTag)) {
            return;
        }

        const key = event.key.toLowerCase();

        // Help overlay
        if (key === '?') {
            if (typeof dashboard?.toggleHelpOverlay === 'function') {
                dashboard.toggleHelpOverlay();
            }
            event.preventDefault();
            return;
        }

        // View switching
        if (viewKeyMap[key]) {
            const mode = viewKeyMap[key];
            if (typeof dashboard?.setView === 'function') {
                dashboard.setView(mode);
                updateHeader(mode);
            }
            event.preventDefault();
            return;
        }

        // Space – pause/resume auto‑refresh
        if (key === ' ') {
            if (typeof dashboard?.toggleAutoRefresh === 'function') {
                dashboard.toggleAutoRefresh();
                autoRefreshPaused = !autoRefreshPaused;
                // Optionally reflect pause state in header
                const headerEl = document.getElementById('dashboard-header-mode');
                if (headerEl) {
                    const suffix = autoRefreshPaused ? ' (paused)' : '';
                    headerEl.textContent = headerEl.textContent.replace(/ \(paused\)$/, '') + suffix;
                }
            }
            event.preventDefault();
            return;
        }

        // Force refresh
        if (key === 'r') {
            if (typeof dashboard?.refresh === 'function') {
                dashboard.refresh();
            }
            event.preventDefault();
            return;
        }
    }

    // Register the listener once the DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            document.addEventListener('keydown', onKeyDown);
        });
    } else {
        document.addEventListener('keydown', onKeyDown);
    }

    // Export for testing / external use (optional)
    window.dashboardShortcuts = {
        onKeyDown,
        updateHeader,
        viewKeyMap
    };
})();