/**
 * Thunk‑collapse helper – applies LIFO (deepest‑first) staggered collapse
 * to nodes and their connections.
 *
 * Usage:
 *   const root = document.querySelector('#thunk-root');
 *   initThunkCollapse(root);
 */
function initThunkCollapse(root) {
  if (!root) return;

  // Collect all nodes with a depth attribute (or compute depth via DOM)
  const nodes = Array.from(root.querySelectorAll('.thunk-node'))
    .map(node => ({
      el: node,
      depth: parseInt(node.dataset.depth, 10) || 0
    }))
    // Sort deepest first (LIFO)
    .sort((a, b) => b.depth - a.depth);

  const STAGGER = 80; // ms

  nodes.forEach((item, index) => {
    const delay = index * STAGGER;
    item.el.style.setProperty('--thunk-depth', item.depth);
    item.el.style.setProperty('--thunk-delay', `${delay}ms`);
    item.el.classList.add('collapse');

    // Collapse associated connections (assumes they have data-parent-id linking to node id)
    const connections = root.querySelectorAll(`.thunk-connection[data-parent-id="${item.el.id}"]`);
    connections.forEach(conn => {
      conn.style.setProperty('--thunk-delay', `${delay}ms`);
      conn.classList.add('collapse');
    });
  });
}

// Export for module environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = initThunkCollapse;
}