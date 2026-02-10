/**
 * Tree Interaction Patch
 *
 * This module ensures that tree operations (scale, collapse, drag) affect only the
 * tree instance that receives the event. It also manages z-index for drag
 * operations so that the dragged tree is brought to the front.
 *
 * Usage:
 *   import { initAllTrees } from './tree_interaction_patch.js';
 *   initAllTrees();
 */

let topZIndex = 1000; // Starting z-index for trees

/**
 * Bring the given tree element to the front by increasing its z-index.
 *
 * @param {HTMLElement} treeEl - The tree container element.
 */
function bringTreeToFront(treeEl) {
  topZIndex += 1;
  treeEl.style.zIndex = topZIndex;
}

/**
 * Initialize interaction handlers for a single tree element.
 *
 * @param {HTMLElement} treeEl - The root element of the tree.
 */
function setupTreeInteractions(treeEl) {
  // ---------- Scaling ----------
  // Scale only this tree when the user scrolls with Ctrl pressed.
  treeEl.addEventListener('wheel', (e) => {
    if (!e.ctrlKey) return;
    e.preventDefault();

    // Compute a scale factor based on wheel delta.
    const scaleFactor = Math.exp(-e.deltaY * 0.01);
    const currentScale = getCurrentScale(treeEl);
    const newScale = currentScale * scaleFactor;

    treeEl.style.transform = `scale(${newScale})`;
  });

  // Helper to read current scale from transform.
  function getCurrentScale(el) {
    const style = window.getComputedStyle(el);
    const match = style.transform.match(/scale\(([^)]+)\)/);
    return match ? parseFloat(match[1]) : 1;
  }

  // ---------- Collapse ----------
  // Collapse/expand only the targeted subtree.
  treeEl.addEventListener('click', (e) => {
    const toggle = e.target.closest('.collapse-toggle');
    if (!toggle) return;

    const node = toggle.closest('.node');
    if (!node) return;

    const childrenContainer = node.querySelector('.children');
    if (!childrenContainer) return;

    childrenContainer.classList.toggle('collapsed');
  });

  // ---------- Drag ----------
  // Drag handling is scoped to this tree only.
  let isDragging = false;
  let startX = 0;
  let startY = 0;
  let origLeft = 0;
  let origTop = 0;

  treeEl.addEventListener('mousedown', (e) => {
    // Only start dragging when the user clicks a designated handle.
    if (!e.target.matches('.drag-handle')) return;

    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;

    const rect = treeEl.getBoundingClientRect();
    origLeft = rect.left;
    origTop = rect.top;

    // Ensure the tree is positioned absolutely for moving.
    treeEl.style.position = 'absolute';
    bringTreeToFront(treeEl);

    e.preventDefault(); // Prevent text selection, etc.
  });

  // Mouse move handler attached to document to capture movement outside the tree.
  document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;

    const dx = e.clientX - startX;
    const dy = e.clientY - startY;

    treeEl.style.left = `${origLeft + dx}px`;
    treeEl.style.top = `${origTop + dy}px`;
  });

  // End drag on mouse up anywhere.
  document.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
    }
  });
}

/**
 * Initialize all trees present in the document.
 *
 * Call this after the DOM is ready (e.g., on DOMContentLoaded).
 */
export function initAllTrees() {
  const trees = document.querySelectorAll('.tree');
  trees.forEach(setupTreeInteractions);
}