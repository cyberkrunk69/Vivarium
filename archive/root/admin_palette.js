/**
 * Admin Command Palette
 * ---------------------
 * Press Ctrl+K to open a modal overlay.
 * Type to fuzzy-search available admin commands.
 * Selecting a command triggers an API call to the backend.
 *
 * Commands:
 *   - restart swarm
 *   - clear logs
 *   - export stats
 *   - pause workers
 *
 * The implementation is framework‑agnostic and can be dropped into any
 * front‑end that runs in the browser.
 */

(() => {
  // ----- Configuration -----
  const COMMANDS = [
    { name: "restart swarm", endpoint: "/api/admin/restart-swarm" },
    { name: "clear logs", endpoint: "/api/admin/clear-logs" },
    { name: "export stats", endpoint: "/api/admin/export-stats" },
    { name: "pause workers", endpoint: "/api/admin/pause-workers" },
  ];

  // ----- Utility: simple fuzzy matcher -----
  function fuzzyMatch(query, target) {
    query = query.toLowerCase();
    target = target.toLowerCase();
    let qIdx = 0;
    for (let tIdx = 0; tIdx < target.length && qIdx < query.length; tIdx++) {
      if (query[qIdx] === target[tIdx]) qIdx++;
    }
    return qIdx === query.length;
  }

  // ----- Create DOM elements -----
  const overlay = document.createElement("div");
  overlay.style.cssText = `
    position: fixed; inset: 0; background: rgba(0,0,0,0.4);
    display: flex; align-items: flex-start; justify-content: center;
    padding-top: 10vh; z-index: 9999; visibility: hidden;
  `;

  const container = document.createElement("div");
  container.style.cssText = `
    background: #1e1e1e; color: #fff; width: 400px; border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3); font-family: sans-serif;
  `;

  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "Admin command...";
  input.style.cssText = `
    width: 100%; box-sizing: border-box; padding: 12px 16px;
    border: none; outline: none; background: #2d2d2d; color: #fff;
    font-size: 16px; border-top-left-radius: 6px; border-top-right-radius: 6px;
  `;

  const list = document.createElement("ul");
  list.style.cssText = `
    list-style: none; margin: 0; padding: 0; max-height: 200px; overflow-y: auto;
  `;

  container.appendChild(input);
  container.appendChild(list);
  overlay.appendChild(container);
  document.body.appendChild(overlay);

  // ----- Render command list -----
  function renderList(filter = "") {
    list.innerHTML = "";
    const filtered = COMMANDS.filter(c => fuzzyMatch(filter, c.name));
    filtered.forEach((cmd, idx) => {
      const li = document.createElement("li");
      li.textContent = cmd.name;
      li.dataset.idx = idx;
      li.style.cssText = `
        padding: 10px 16px; cursor: pointer;
      `;
      li.addEventListener("mouseenter", () => {
        li.style.background = "#3a3a3a";
      });
      li.addEventListener("mouseleave", () => {
        li.style.background = "transparent";
      });
      li.addEventListener("click", () => executeCommand(cmd));
      list.appendChild(li);
    });
  }

  // ----- Execute selected command -----
  async function executeCommand(cmd) {
    hidePalette();
    try {
      const resp = await fetch(cmd.endpoint, { method: "POST" });
      if (!resp.ok) throw new Error(`Error ${resp.status}`);
      const data = await resp.json();
      console.log(`Admin command "${cmd.name}" executed:`, data);
    } catch (e) {
      console.error(`Failed to execute "${cmd.name}":`, e);
    }
  }

  // ----- Show / Hide palette -----
  function showPalette() {
    overlay.style.visibility = "visible";
    input.value = "";
    renderList();
    input.focus();
  }

  function hidePalette() {
    overlay.style.visibility = "hidden";
  }

  // ----- Keyboard handling -----
  document.addEventListener("keydown", (e) => {
    // Ctrl+K opens the palette (avoid conflict with browser shortcuts)
    if (e.ctrlKey && e.key.toLowerCase() === "k") {
      e.preventDefault();
      showPalette();
    } else if (e.key === "Escape") {
      hidePalette();
    }
  });

  input.addEventListener("input", (e) => {
    renderList(e.target.value);
  });

  // Allow navigation via Arrow keys and Enter
  input.addEventListener("keydown", (e) => {
    const items = Array.from(list.children);
    const active = document.activeElement;
    let currentIdx = items.findIndex(li => li === active);
    if (e.key === "ArrowDown") {
      e.preventDefault();
      const nextIdx = (currentIdx + 1) % items.length;
      items[nextIdx].focus();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      const prevIdx = (currentIdx - 1 + items.length) % items.length;
      items[prevIdx].focus();
    } else if (e.key === "Enter") {
      e.preventDefault();
      const selected = items.find(li => li === document.activeElement);
      if (selected) {
        const idx = parseInt(selected.dataset.idx, 10);
        executeCommand(COMMANDS.filter(c => fuzzyMatch(input.value, c.name))[idx]);
      }
    }
  });
})();