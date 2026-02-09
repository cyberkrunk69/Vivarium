#!/usr/bin/env python3
"""
Fix missing /grind_logs/latest.log endpoint

Dashboard is getting 404 trying to fetch grind_logs/latest.log.
Need to add this endpoint to the dashboard server.
"""
import os
from groq_client import execute_with_groq

os.environ['GROQ_API_KEY'] = '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'

# Read current server
with open('dashboard_server.py', 'r', encoding='utf-8') as f:
    server_code = f.read()

prompt = f"""Fix 404 error in dashboard server.

## PROBLEM:
Dashboard at localhost:8420 is getting:
GET http://localhost:8420/grind_logs/latest.log 404 (NOT FOUND)

## CURRENT SERVER CODE:
```python
{server_code[:3000]}
...
```

## YOUR TASK:
Add a route to serve /grind_logs/latest.log

The endpoint should:
1. Find the most recent grind_logs/*.json file
2. Return it as text/plain or application/json
3. Handle case where no logs exist (return empty or 404)

Provide ONLY the code to add to dashboard_server.py.
Show exactly where to insert it and what to add.

Use the same framework/pattern as existing routes in the server.
"""

print("Asking swarm to fix log endpoint...")
result = execute_with_groq(prompt=prompt, model="llama-3.3-70b-versatile")

print("\n" + "="*60)
print("SWARM RESPONSE:")
print("="*60)
print(result['result'])
print()
print(f"Cost: ${result['cost']:.4f}")

with open('log_endpoint_fix.md', 'w', encoding='utf-8') as f:
    f.write("# Log Endpoint Fix\n\n")
    f.write(result['result'])

print("\nSaved to: log_endpoint_fix.md")
