#!/usr/bin/env python3
"""
Build Modern Dashboard - From Scratch

Current dashboard is unfixable (HTML inside JS, duplicate vars, malformed structure).
Build a new one using UIUX knowledge base.

Requirements:
- Real-time progress monitoring (/progress-stream SSE)
- Node status display
- Engine/model usage tracking
- Error handling
- Loading states
- Modern, responsive design
- NO syntax errors
"""
import os
from groq_client import execute_with_groq

os.environ['GROQ_API_KEY'] = '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'

prompt = """You are building a modern dashboard for an autonomous AI swarm orchestration system.

## VISION SPECIFICATIONS:

**Node Visualization:**
- Understanding nodes (indigo #6366f1) - primary tasks
- Worker nodes (purple #8b5cf6) - spawned tasks
- Helper nodes (cyan #06b6d4) - subtasks
- Expert nodes (amber #f59e0b) - specialized work
- Nodes connected by animated SVG lines

**Rainbow Border Animation:**
- Active/running nodes get animated rainbow border
- CSS: linear-gradient with 400% background-size
- 3s infinite animation cycling through spectrum

**Thunk-Thunk-Thunk Collapse Animation:**
- When work completes, nodes collapse in LIFO order (deepest first)
- Each node shrinks, moves toward parent, fades out
- 120ms stagger between nodes (the 'thunk' rhythm)
- Completion quips: "got er done", "finally", etc.
- Final node collapses into History Dashboard

**Interactive Features:**
1. **Draggable Nodes** - Click drag handle (⋯) to reposition
2. **Auto-Scaling Trees** - Trees scale down as they grow (30-100% scale)
3. **Floating Chat Module** - Draggable, minimizable, position persistence
4. **Collapsible Trees** - One-click mini mode showing completion ratio
5. **Multi-Tree Workspace** - Support multiple parallel task trees

**Engine/Model Visibility:**
- Engine badges: CLAUDE (blue #1e90ff), GROQ (orange #ff8c00)
- Model name display (e.g., "claude-sonnet-4", "llama-3.3-70b")
- Selection reason tooltip
- Real-time cost and token tracking
- Summary panel with engine split and cost breakdown

**Technical Requirements:**
- SSE endpoint: `/events` for real-time updates
- localStorage for position persistence
- NO mixed HTML/JS/CSS (proper separation)
- NO duplicate variables or undefined references
- CSS Variables:
  - --anim-fast: 150ms, --anim-normal: 250ms, --anim-slow: 350ms
  - --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1)
  - --ease-snap: cubic-bezier(0.55, 0.055, 0.675, 0.19)
  - --node-gap: 24px

**SSE Payload Structure:**
```json
{
  "type": "node_update",
  "node_id": "worker-7",
  "status": "running",
  "engine": "CLAUDE",
  "model": "claude-sonnet-4",
  "reason": "Complex task",
  "tokens_used": 1245,
  "cost": 0.018
}
```

## GENERATE:

Complete, working HTML file implementing ALL vision specs above.
Proper HTML5/CSS3/JavaScript separation.
Production quality, no syntax errors.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Swarm Vision Dashboard</title>
    <style>
        /* CSS implementing all visual specs */
    </style>
</head>
<body>
    <!-- HTML structure with all interactive elements -->
    <script>
        // JavaScript implementing all interactions and SSE
    </script>
</body>
</html>
```

Make it worthy of a "beyond state-of-the-art black swarm" system.
"""

print("="*60)
print("BUILDING MODERN DASHBOARD FROM SCRATCH")
print("="*60)
print("Using: UIUX knowledge base")
print("Target: Production-quality dashboard")
print("Budget: $0.50")
print()

result = execute_with_groq(prompt=prompt, model="llama-3.3-70b-versatile")

print("="*60)
print("DASHBOARD GENERATED")
print("="*60)
print()
print(f"Cost: ${result['cost']:.4f}")
print(f"Tokens: {result['input_tokens']} in, {result['output_tokens']} out")
print()

# Extract HTML from result
html_content = result['result']

# Save new dashboard
with open('dashboard_modern.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Saved to: dashboard_modern.html")
print()
print("Next steps:")
print("1. Review dashboard_modern.html")
print("2. Test with your progress server")
print("3. Replace old dashboard.html if satisfied")
