/**
 * Theme Toggle Module
 * - Reads/writes user preference to localStorage ('theme')
 * - Applies CSS class to <html> element
 * - Respects system preference via prefers-color-scheme
 */

const THEME_KEY = 'theme';
const LIGHT_CLASS = 'light-theme';
const DARK_CLASS = 'dark-theme';

/**
 * Apply the given theme class to the document element.
 * @param {string} theme - 'light' | 'dark'
 */
function applyTheme(theme) {
  const root = document.documentElement;
  root.classList.remove(LIGHT_CLASS, DARK_CLASS);
  if (theme === 'light') {
    root.classList.add(LIGHT_CLASS);
  } else {
    root.classList.add(DARK_CLASS);
  }
}

/**
 * Determine the initial theme:
 * 1. Check localStorage.
 * 2. If not set, check system preference.
 * 3. Default to dark.
 */
function getInitialTheme() {
  const stored = localStorage.getItem(THEME_KEY);
  if (stored === 'light' || stored === 'dark') {
    return stored;
  }

  // System preference
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
    return 'light';
  }

  // Default
  return 'dark';
}

/**
 * Toggle between light and dark themes.
 */
function toggleTheme() {
  const current = document.documentElement.classList.contains(LIGHT_CLASS) ? 'light' : 'dark';
  const next = current === 'light' ? 'dark' : 'light';
  applyTheme(next);
  localStorage.setItem(THEME_KEY, next);
}

/**
 * Initialize theme on page load.
 */
function initTheme() {
  const theme = getInitialTheme();
  applyTheme(theme);
}

/* Expose toggle function globally for UI hooks */
window.toggleTheme = toggleTheme;

/* Run initialization */
document.addEventListener('DOMContentLoaded', initTheme);