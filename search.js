/**
 * Task Filtering & Search Module
 *
 * Adds a search box that filters visible tasks by:
 *   - id
 *   - description text
 *   - status
 *   - phase
 *
 * Features:
 *   - Supports regular expressions (fallback to plain text if regex invalid)
 *   - Highlights matching substrings
 *   - Persists current filter in URL hash for easy sharing
 *
 * Expected HTML structure:
 *   <div class="task" data-id="123" data-status="open" data-phase="planning">
 *       <span class="description">Fix login bug</span>
 *   </div>
 *
 * Include this script at the end of your page (or after the task list) and ensure
 * the CSS from `search.css` is loaded.
 */

(() => {
    const HASH_KEY = 'filter';
    const HIGHLIGHT_CLASS = 'search-highlight';

    // Utility: Escape HTML to avoid injection when highlighting
    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Parse the hash for the persisted filter string
    function getPersistedFilter() {
        const hash = location.hash.slice(1); // remove '#'
        const params = new URLSearchParams(hash);
        return params.get(HASH_KEY) || '';
    }

    // Persist the filter string in the URL hash
    function setPersistedFilter(value) {
        const params = new URLSearchParams(location.hash.slice(1));
        if (value) {
            params.set(HASH_KEY, value);
        } else {
            params.delete(HASH_KEY);
        }
        const newHash = params.toString();
        history.replaceState(null, '', newHash ? `#${newHash}` : location.pathname + location.search);
    }

    // Create the search input UI
    function createSearchBox(initialValue) {
        const container = document.createElement('div');
        container.className = 'search-container';
        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Search tasks (id, description, status, phase)...';
        input.value = initialValue;
        input.className = 'search-input';
        container.appendChild(input);
        // Insert at top of body (or adjust as needed)
        document.body.insertBefore(container, document.body.firstChild);
        return input;
    }

    // Highlight matches in a given text using a RegExp
    function highlightMatches(text, regex) {
        if (!regex) return escapeHtml(text);
        const parts = [];
        let lastIndex = 0;
        let match;
        while ((match = regex.exec(text)) !== null) {
            const start = match.index;
            const end = regex.lastIndex;
            // push non‑matched segment
            if (start > lastIndex) {
                parts.push(escapeHtml(text.slice(lastIndex, start)));
            }
            // push matched segment wrapped in <mark>
            const matchedText = escapeHtml(text.slice(start, end));
            parts.push(`<mark class="${HIGHLIGHT_CLASS}">${matchedText}</mark>`);
            lastIndex = end;
            // Prevent zero‑length infinite loops
            if (match[0].length === 0) regex.lastIndex++;
        }
        // remaining tail
        if (lastIndex < text.length) {
            parts.push(escapeHtml(text.slice(lastIndex)));
        }
        return parts.join('');
    }

    // Apply filter to all task elements
    function applyFilter(filterStr) {
        let regex = null;
        if (filterStr) {
            try {
                regex = new RegExp(filterStr, 'i');
            } catch (e) {
                // Invalid regex – treat as plain text search
                const escaped = filterStr.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                regex = new RegExp(escaped, 'i');
            }
        }

        const tasks = document.querySelectorAll('.task');
        tasks.forEach(task => {
            const id = task.dataset.id || '';
            const status = task.dataset.status || '';
            const phase = task.dataset.phase || '';
            const descElem = task.querySelector('.description');
            const description = descElem ? descElem.textContent : '';

            const searchable = `${id} ${description} ${status} ${phase}`;

            const isMatch = !regex || regex.test(searchable);
            task.style.display = isMatch ? '' : 'none';

            // Highlight matches only when visible
            if (descElem) {
                if (isMatch && regex) {
                    descElem.innerHTML = highlightMatches(description, regex);
                } else {
                    // Reset to plain text when no match or no filter
                    descElem.textContent = description;
                }
            }
        });
    }

    // Main init
    document.addEventListener('DOMContentLoaded', () => {
        const initialFilter = getPersistedFilter();
        const searchInput = createSearchBox(initialFilter);

        // Initial filter application
        applyFilter(initialFilter);

        // Debounce helper
        let debounceTimer = null;
        const DEBOUNCE_MS = 300;

        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const value = searchInput.value.trim();
                setPersistedFilter(value);
                applyFilter(value);
            }, DEBOUNCE_MS);
        });

        // Listen to hash changes (e.g., back/forward navigation)
        window.addEventListener('hashchange', () => {
            const newFilter = getPersistedFilter();
            if (newFilter !== searchInput.value) {
                searchInput.value = newFilter;
                applyFilter(newFilter);
            }
        });
    });
})();