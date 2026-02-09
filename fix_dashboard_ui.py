#!/usr/bin/env python3
"""
Fix Dashboard UI - Use UIUX Knowledge Base

The swarm has access to comprehensive UI/UX knowledge from 500+ sources.
Yet the dashboard is still HTML 1.0 quality with console errors.

Console Errors to Fix:
1. (index):131  Uncaught SyntaxError: Unexpected token '<'
2. (index):224  Uncaught ReferenceError: evtSource is not defined
3. (index):430  Uncaught SyntaxError: Unexpected token '<'
4. (index):562  Uncaught SyntaxError: Identifier 'summary' has already been declared
5. :8420/progress:1   Failed to load resource: 404 (NOT FOUND)
6. :8420/progress-stream:1   Failed to load resource: 404 (NOT FOUND)
7. Uncaught Error: async response channel closed before response received

Task: Make this dashboard worthy of a "baby AGI" system.
"""
import os
import json
from groq_client import execute_with_groq

# Set API key
os.environ['GROQ_API_KEY'] = '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'

# Read current dashboard
with open('dashboard.html', 'r', encoding='utf-8') as f:
    current_dashboard = f.read()

# Load UIUX knowledge index
with open('knowledge/uiux/index.json', 'r', encoding='utf-8') as f:
    uiux_index = json.load(f)

prompt = f"""You are fixing a dashboard UI that has critical console errors.

## CONTEXT:

You have access to comprehensive UI/UX knowledge scraped from 500+ sources:
- Design systems (Google Material, Apple HIG, etc.)
- Component libraries (React, Vue, etc.)
- Accessibility standards (WCAG, ARIA)
- Modern CSS and animations
- Data visualization best practices
- Framework-specific patterns

Available knowledge categories: {', '.join(uiux_index.get('categories', []))}

## CURRENT DASHBOARD PROBLEMS:

**Console Errors:**
1. Line 131: Uncaught SyntaxError: Unexpected token '<'
2. Line 224: Uncaught ReferenceError: evtSource is not defined
3. Line 430: Uncaught SyntaxError: Unexpected token '<'
4. Line 562: Identifier 'summary' has already been declared
5. Missing endpoint: /progress (404)
6. Missing endpoint: /progress-stream (404)
7. Async message channel error

**Current State:** HTML 1.0 quality
**Expected State:** Modern, professional UI worthy of advanced AI system

## YOUR TASK:

Analyze the dashboard code below and provide:

1. **Root Cause Analysis** - What's causing each error?
2. **Fix Strategy** - How to resolve each issue
3. **Modern UI Recommendations** - Using your UIUX knowledge:
   - Proper component structure
   - Error handling patterns
   - Loading states
   - Real-time data display
   - Responsive design
   - Accessibility

4. **Code Fixes** - Specific code changes needed

## CURRENT DASHBOARD CODE:

```html
{current_dashboard[:15000]}
... (truncated, full file is {len(current_dashboard)} chars)
```

Focus on the areas with errors (lines 131, 224, 430, 562) and the missing endpoints.

Provide actionable fixes that can be implemented immediately.
"""

print("="*60)
print("DASHBOARD UI FIX - USING UIUX KNOWLEDGE BASE")
print("="*60)
print(f"Current dashboard: {len(current_dashboard):,} characters")
print(f"UIUX knowledge: {uiux_index.get('total_sources', 0)} sources")
print(f"Budget: $0.50")
print()

result = execute_with_groq(prompt=prompt, model="llama-3.3-70b-versatile")

print("="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print()
print(f"Cost: ${result['cost']:.4f}")
print(f"Tokens: {result['input_tokens']} in, {result['output_tokens']} out")
print()

# Save analysis
with open('dashboard_fix_analysis.md', 'w', encoding='utf-8') as f:
    f.write("# Dashboard UI Fix Analysis\n\n")
    f.write(f"**Generated:** {result['timestamp']}\n")
    f.write(f"**Cost:** ${result['cost']:.4f}\n")
    f.write(f"**UIUX Knowledge Sources:** {uiux_index.get('total_sources', 0)}\n\n")
    f.write("---\n\n")
    f.write(result['result'])

print(result['result'])
print()
print("Saved to: dashboard_fix_analysis.md")
