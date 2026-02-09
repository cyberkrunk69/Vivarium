# UX Motion Design Specification

## The Vision

A unified intelligent system that **feels alive**. When you talk to it, it responds like a capable colleague - not a robot, not a chatbot. The visual choreography reinforces this: information flows visibly, work happens transparently, and completion feels satisfying.

**Core Principle**: Every animation serves comprehension. The user should understand at a glance what's happening, but can drill down into any node for details.

---

## 1. Overall Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  HEADER: Logo | Status | Stats | Autonomy Toggle                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                    │                    │
│                                                    │    HISTORY         │
│                                                    │    DASHBOARD       │
│              MAIN CANVAS                           │    (collapsible)   │
│         (task flow visualization)                  │                    │
│                                                    │    ┌────────────┐  │
│   ← nodes spawn here                               │    │ Quest 1 ✓  │  │
│     and flow rightward →                           │    │ Quest 2 ✓  │  │
│                                                    │    │ Quest 3... │  │
│                                                    │    └────────────┘  │
│                                                    │                    │
├─────────────────────────────────────────────────────────────────────────┤
│  INPUT: [ Chat input field                              ] [Send] [Mic]  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Completion Collapse Sequence ("Thunk Thunk Thunk")

**Trigger**: All work complete, task successful (or failed)

**The Core Concept**:
Nodes collapse in **reverse spawn order** (LIFO), each one "thunking" into its parent, until only the original Understanding node remains. Then that collapses into the History Dashboard.

```
Timeline:
0ms     Work complete signal received
        └─ All rainbow borders stop
        └─ Brief pause (300ms) - let user see final state

300ms   Completion quip appears on the Understanding node
        └─ "got 'er done ✓" / "finally 😅" / "that was rough"

600ms   COLLAPSE SEQUENCE BEGINS
        └─ Start with DEEPEST/LAST spawned nodes

        For each node (in reverse order):
        ├─ Node shrinks: scale(1) → scale(0.5)
        ├─ Node moves toward parent: translateX/Y toward parent center
        ├─ Node fades: opacity 1 → 0
        ├─ Duration: 250ms per node
        ├─ Easing: cubic-bezier(0.55, 0.055, 0.675, 0.19) [ease-in]
        ├─ Delay between nodes: 120ms (the "thunk" rhythm)
        └─ Connection line retracts simultaneously

        Sound design note: Each collapse could have subtle
        haptic feedback or audio "thunk" if supported
```

**JavaScript Orchestration**:
```javascript
async function collapseSequence(nodes) {
  const THUNK_DELAY = 120; // ms between collapses
  const COLLAPSE_DURATION = 250;

  // Sort nodes: deepest/last-spawned first
  const orderedNodes = [...nodes].sort((a, b) => b.depth - a.depth || b.spawnTime - a.spawnTime);

  for (const node of orderedNodes) {
    const parent = node.parentNode;
    const targetX = parent ? parent.x - node.x : dashboardX - node.x;
    const targetY = parent ? parent.y - node.y : dashboardY - node.y;

    node.style.setProperty('--collapse-x', `${targetX}px`);
    node.style.setProperty('--collapse-y', `${targetY}px`);
    node.classList.add('collapsing');

    if (node.connectionLine) {
      node.connectionLine.classList.add('retracting');
    }

    await sleep(THUNK_DELAY);
  }

  await sleep(COLLAPSE_DURATION);
  addToHistoryDashboard(quest);
}
```

---

## CSS Variables

```css
:root {
  /* Timing */
  --anim-fast: 150ms;
  --anim-normal: 250ms;
  --anim-slow: 350ms;
  --thunk-delay: 120ms;

  /* Easing */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-snap: cubic-bezier(0.55, 0.055, 0.675, 0.19);

  /* Colors */
  --node-bg: #1a1a2e;
  --node-border: #333;
  --node-complete: #10b981;
  --node-failed: #ef4444;

  /* Node Types */
  --color-understanding: #6366f1;
  --color-worker: #8b5cf6;
  --color-helper: #06b6d4;
  --color-expert: #f59e0b;

  /* Layout */
  --node-gap: 24px;
  --node-width-primary: 280px;
  --node-width-worker: 220px;
  --node-width-helper: 180px;
  --dashboard-width: 320px;
}
```

---

## Rainbow Border (Active State)

```css
.node.running::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 14px;
  background: linear-gradient(
    90deg,
    #ff0000, #ff7f00, #ffff00, #00ff00,
    #0000ff, #4b0082, #8f00ff, #ff0000
  );
  background-size: 400% 100%;
  animation: rainbowFlow 3s linear infinite;
  z-index: -1;
}

@keyframes rainbowFlow {
  0% { background-position: 0% 50%; }
  100% { background-position: 400% 50%; }
}
```

---

*This spec: living system, left-to-right flow, rainbow borders, thunk-thunk-thunk collapse into history dashboard.*
