/**
 * Task Filtering & Search Module
 *
 * This script adds a search box to the task list UI, filters visible tasks by
 * ID, description, status, or phase using regular expressions, highlights the
 * matching substrings, and persists the current filter in the URL hash for
 * easy sharing.
 *
 * Expected global environment:
 *   - `window.tasks` : Array of task objects with at least the following fields:
 *       { id: string|number, description: string, status: string, phase: string }
 *   - A container element with id="task-list" where each task is rendered as
 *     a <div class="task-item" data-id="...">...</div>
 *
 * Integration:
 *   Include this script after the task list markup, e.g.:
 *     <script src="experiments/exp_20260204_032115_unified_session_7/task_filter.js"></script>
 */

(() => {
  // Utility: escape HTML to avoid XSS when injecting highlighted text
  const escapeHTML = (str) =>
    str.replace(/[&<>"'`=\/]/g, (s) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
      '`': '&#x60;',
      '=': '&#x3D;',
      '/': '&#x2F;',
    }[s]));

  // Insert search UI
  const insertSearchBox = () => {
    const container = document.createElement('div');
    container.id = 'task-filter-container';
    container.style.marginBottom = '1rem';
    container.innerHTML = `
      <input type="text" id="task-filter-input" placeholder="Search tasks (regex supported)" style="width:100%;padding:0.5rem;font-size:1rem;">
    `;
    const taskList = document.getElementById('task-list');
    if (taskList && taskList.parentNode) {
      taskList.parentNode.insertBefore(container, taskList);
    }
  };

  // Parse filter from URL hash (e.g., #filter=regex)
  const getFilterFromHash = () => {
    const hash = window.location.hash.substring(1); // strip '#'
    const params = new URLSearchParams(hash);
    return params.get('filter') || '';
  };

  // Update URL hash with current filter (without causing page jump)
  const updateHash = (filter) => {
    const params = new URLSearchParams();
    if (filter) params.set('filter', filter);
    const newHash = params.toString();
    history.replaceState(null, '', newHash ? `#${newHash}` : window.location.pathname);
  };

  // Highlight matches within a string using <mark>
  const highlightMatches = (text, regex) => {
    if (!regex) return escapeHTML(text);
    return escapeHTML(text).replace(regex, (match) => `<mark>${match}</mark>`);
  };

  // Render filtered tasks
  const renderTasks = (filter) => {
    const taskListEl = document.getElementById('task-list');
    if (!taskListEl) return;

    // Build regex; if invalid, treat as plain text
    let regex = null;
    if (filter) {
      try {
        regex = new RegExp(filter, 'gi');
      } catch (e) {
        // invalid regex – ignore filtering
        regex = null;
      }
    }

    // Clear existing content
    taskListEl.innerHTML = '';

    // Filter and render
    const filtered = window.tasks.filter((task) => {
      if (!regex) return true; // no filter => all tasks
      const combined = `${task.id} ${task.description} ${task.status} ${task.phase}`;
      return regex.test(combined);
    });

    filtered.forEach((task) => {
      const taskDiv = document.createElement('div');
      taskDiv.className = 'task-item';
      taskDiv.dataset.id = task.id;

      // Build inner HTML with highlights
      const idHTML = highlightMatches(String(task.id), regex);
      const descHTML = highlightMatches(task.description, regex);
      const statusHTML = highlightMatches(task.status, regex);
      const phaseHTML = highlightMatches(task.phase, regex);

      taskDiv.innerHTML = `
        <strong>ID:</strong> ${idHTML}<br>
        <strong>Description:</strong> ${descHTML}<br>
        <strong>Status:</strong> ${statusHTML}<br>
        <strong>Phase:</strong> ${phaseHTML}
      `;
      taskListEl.appendChild(taskDiv);
    });
  };

  // Initialize
  const init = () => {
    if (!Array.isArray(window.tasks)) {
      console.warn('task_filter.js: window.tasks is not defined or not an array.');
      return;
    }

    insertSearchBox();

    const input = document.getElementById('task-filter-input');
    if (!input) return;

    // Load filter from hash
    const initialFilter = getFilterFromHash();
    input.value = initialFilter;
    renderTasks(initialFilter);

    // Debounce input handling
    let timeout = null;
    input.addEventListener('input', () => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        const filterVal = input.value.trim();
        updateHash(filterVal);
        renderTasks(filterVal);
      }, 250);
    });

    // React to hash changes (e.g., back/forward navigation)
    window.addEventListener('hashchange', () => {
      const newFilter = getFilterFromHash();
      input.value = newFilter;
      renderTasks(newFilter);
    });
  };

  // Run after DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();