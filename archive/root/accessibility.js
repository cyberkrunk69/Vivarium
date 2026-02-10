/**
 * accessibility.js
 *
 * Adds title attributes, tooltips, and ARIA labels to UI control buttons:
 *   - collapse
 *   - expand
 *   - drag
 *   - minimize
 *
 * This script runs after the DOM is ready and enhances existing buttons
 * without modifying core files.
 */

(function () {
    // Mapping of button identifiers to human‑readable labels
    const buttonMap = {
        // Adjust selectors as needed for your UI framework
        '.btn-collapse':   { title: 'Collapse panel',   aria: 'Collapse panel' },
        '.btn-expand':     { title: 'Expand panel',     aria: 'Expand panel' },
        '.btn-drag':       { title: 'Drag panel',       aria: 'Drag panel' },
        '.btn-minimize':   { title: 'Minimize panel',   aria: 'Minimize panel' }
    };

    /**
     * Apply title and aria-label attributes to a collection of elements.
     *
     * @param {NodeListOf<Element>} elements - Elements to enhance.
     * @param {string} title - Text for the title attribute (tooltip).
     * @param {string} ariaLabel - Text for the aria-label attribute.
     */
    function enhanceButtons(elements, title, ariaLabel) {
        elements.forEach(el => {
            // Only set if not already present to avoid overwriting custom values
            if (!el.hasAttribute('title')) {
                el.setAttribute('title', title);
            }
            if (!el.hasAttribute('aria-label')) {
                el.setAttribute('aria-label', ariaLabel);
            }
            // Ensure the element is focusable for screen readers
            if (!el.hasAttribute('tabindex')) {
                el.setAttribute('tabindex', '0');
            }
        });
    }

    // Wait for DOMContentLoaded to ensure all buttons exist
    document.addEventListener('DOMContentLoaded', () => {
        Object.entries(buttonMap).forEach(([selector, {title, aria}]) => {
            const elems = document.querySelectorAll(selector);
            if (elems.length) {
                enhanceButtons(elems, title, aria);
            }
        });
    });
})();