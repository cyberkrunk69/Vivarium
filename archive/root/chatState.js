/**
 * Utility functions for persisting chat UI state (position and collapsed status)
 * using the browser's localStorage.
 *
 * The state is stored under the key 'chatState' as a JSON string:
 * {
 *   position: { top: number, left: number }, // pixel coordinates
 *   collapsed: boolean
 * }
 */

/**
 * Saves the current chat window position and collapsed state to localStorage.
 *
 * @param {{top: number, left: number}} position - The x/y coordinates of the chat window.
 * @param {boolean} collapsed - Whether the chat window is currently collapsed.
 */
export function saveChatPosition(position, collapsed) {
  try {
    const state = {
      position,
      collapsed,
    };
    localStorage.setItem('chatState', JSON.stringify(state));
  } catch (e) {
    // Silently ignore storage errors (e.g., private browsing mode)
    console.warn('Unable to save chat state to localStorage:', e);
  }
}

/**
 * Loads the previously saved chat window position and collapsed state from localStorage.
 *
 * @returns {{position: {top: number, left: number}, collapsed: boolean}|null}
 *          Returns the stored state object, or null if none is found or parsing fails.
 */
export function loadChatPosition() {
  try {
    const raw = localStorage.getItem('chatState');
    if (!raw) {
      return null;
    }
    const state = JSON.parse(raw);
    // Basic validation
    if (
      typeof state === 'object' &&
      state !== null &&
      typeof state.position?.top === 'number' &&
      typeof state.position?.left === 'number' &&
      typeof state.collapsed === 'boolean'
    ) {
      return state;
    }
    return null;
  } catch (e) {
    console.warn('Unable to load chat state from localStorage:', e);
    return null;
  }
}