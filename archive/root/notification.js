/**
 * Notification (toast) system.
 *
 * Features:
 *  - Stack to the bottom‑right corner.
 *  - Auto‑dismiss after 5 seconds.
 *  - Click to expand/collapse the toast.
 *  - Pre‑defined helpers for:
 *      * task failures
 *      * budget warnings (>80 % spent)
 *      * checkpoint saves
 *      * new task files detected
 *
 * Usage:
 *   import { notifyTaskFailure, notifyBudgetWarning, notifyCheckpoint, notifyNewTaskFile } from './notification.js';
 *
 *   notifyTaskFailure('Task XYZ failed because of …');
 *
 * The implementation is framework‑agnostic (plain JavaScript + CSS) and can be dropped into any HTML page.
 */

(() => {
    // Create a container for all toasts if it doesn't exist
    const containerId = 'toast-container';
    let container = document.getElementById(containerId);
    if (!container) {
        container = document.createElement('div');
        container.id = containerId;
        const style = document.createElement('style');
        style.textContent = `
            #${containerId} {
                position: fixed;
                bottom: 20px;
                right: 20px;
                display: flex;
                flex-direction: column-reverse;
                align-items: flex-end;
                gap: 10px;
                z-index: 9999;
                pointer-events: none; /* allow clicks only on toasts */
            }
            .toast {
                min-width: 250px;
                max-width: 350px;
                background: #333;
                color: #fff;
                padding: 12px 16px;
                border-radius: 4px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                font-family: sans-serif;
                font-size: 14px;
                line-height: 1.4;
                opacity: 0;
                transform: translateX(100%);
                transition: opacity 0.3s ease, transform 0.3s ease;
                pointer-events: auto;
                cursor: pointer;
                overflow: hidden;
                max-height: 60px; /* collapsed height */
            }
            .toast.show {
                opacity: 1;
                transform: translateX(0);
            }
            .toast.expanded {
                max-height: 500px; /* allow big messages */
            }
            .toast.error   { background:#d32f2f; }
            .toast.warning { background:#f57c00; }
            .toast.info    { background:#1976d2; }
            .toast.success { background:#388e3c; }
        `;
        document.head.appendChild(style);
        document.body.appendChild(container);
    }

    /**
     * Core toast creation.
     *
     * @param {string} type    - 'error' | 'warning' | 'info' | 'success'
     * @param {string} message - Text to display.
     */
    function createToast(type, message) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;

        // Show animation
        requestAnimationFrame(() => toast.classList.add('show'));

        // Auto‑dismiss after 5 seconds
        const autoDismiss = setTimeout(() => {
            dismissToast(toast);
        }, 5000);

        // Click toggles expand / collapse
        toast.addEventListener('click', () => {
            toast.classList.toggle('expanded');
            // Reset auto‑dismiss when expanded
            if (toast.classList.contains('expanded')) {
                clearTimeout(autoDismiss);
            } else {
                // Restart timer when collapsed again
                setTimeout(() => dismissToast(toast), 3000);
            }
        });

        container.appendChild(toast);
    }

    function dismissToast(toast) {
        toast.classList.remove('show');
        toast.addEventListener('transitionend', () => {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
        });
    }

    // Helper functions for the four required notification types
    function notifyTaskFailure(message) {
        createToast('error', `Task Failure: ${message}`);
    }

    function notifyBudgetWarning(message) {
        createToast('warning', `Budget Warning: ${message}`);
    }

    function notifyCheckpoint(message) {
        createToast('info', `Checkpoint Saved: ${message}`);
    }

    function notifyNewTaskFile(message) {
        createToast('success', `New Task File Detected: ${message}`);
    }

    // Export to global scope (or module if supported)
    const exportObj = {
        notifyTaskFailure,
        notifyBudgetWarning,
        notifyCheckpoint,
        notifyNewTaskFile,
    };

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = exportObj;
    } else {
        window.NotificationSystem = exportObj;
    }
})();