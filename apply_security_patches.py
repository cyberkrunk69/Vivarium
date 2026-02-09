#!/usr/bin/env python3
"""
Apply Security Patches - LOCKED DOWN EXECUTION

CONSTRAINTS:
- Apply ONLY the patches from SECURITY_PATCHES.md
- No modifications, no improvements, no creativity
- Exact implementation of what was proposed
- Create files exactly as specified
"""
import os
from groq_client import execute_with_groq

# Set API key
os.environ['GROQ_API_KEY'] = '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'

# Read the approved patches
with open('SECURITY_PATCHES.md', 'r', encoding='utf-8') as f:
    patches = f.read()

prompt = f"""You are applying pre-approved security patches.

CRITICAL CONSTRAINTS:
- Apply ONLY what is specified in the patches below
- NO modifications, NO improvements, NO additions
- Create files EXACTLY as specified
- Do NOT edit any files not mentioned in the patches
- Do NOT add features or "helpful" extras

## APPROVED PATCHES:
{patches}

## YOUR TASK:

1. Create `secure_config.py` with the EXACT code from Patch 1
2. Note the changes needed for `safety_gateway.py` from Patch 2 (you will NOT apply these - they require manual integration)
3. Create `integrity_checker.py` with the EXACT code from Patch 3

## OUTPUT FORMAT:

Return ONLY the code blocks in this exact format:

```python
# === FILE: secure_config.py ===
[EXACT CODE FROM PATCH 1 - NO CHANGES]
```

```python
# === FILE: integrity_checker.py ===
[EXACT CODE FROM PATCH 3 - NO CHANGES]
```

```text
# === MANUAL INTEGRATION NEEDED: safety_gateway.py ===
[DESCRIPTION OF PATCH 2 CHANGES - FOR HUMAN TO APPLY]
```

Do NOT add:
- Extra comments
- Improvements
- Error handling beyond what's specified
- Additional features
- Your own ideas

Just transcribe the patches exactly as approved.
"""

print("="*60)
print("APPLYING SECURITY PATCHES (LOCKED DOWN)")
print("="*60)
print("Budget: $0.05")
print()

result = execute_with_groq(prompt=prompt, model="llama-3.1-8b-instant")  # Using faster model for simple task

print("="*60)
print("PATCH APPLICATION COMPLETE")
print("="*60)
print()
print(f"Cost: ${result['cost']:.4f}")
print(f"Tokens: {result['input_tokens']} in, {result['output_tokens']} out")
print()

# Parse and save the files
response = result['result']

# Extract code blocks
import re

# Find secure_config.py
secure_config_match = re.search(r'```python\n# === FILE: secure_config\.py ===\n(.*?)\n```', response, re.DOTALL)
if secure_config_match:
    with open('secure_config.py', 'w', encoding='utf-8') as f:
        f.write(secure_config_match.group(1))
    print("[CREATED] secure_config.py")
else:
    print("[SKIP] Could not extract secure_config.py")

# Find integrity_checker.py
integrity_match = re.search(r'```python\n# === FILE: integrity_checker\.py ===\n(.*?)\n```', response, re.DOTALL)
if integrity_match:
    with open('integrity_checker.py', 'w', encoding='utf-8') as f:
        f.write(integrity_match.group(1))
    print("[CREATED] integrity_checker.py")
else:
    print("[SKIP] Could not extract integrity_checker.py")

# Save manual integration notes
manual_match = re.search(r'```text\n# === MANUAL INTEGRATION NEEDED: safety_gateway\.py ===\n(.*?)\n```', response, re.DOTALL)
if manual_match:
    with open('MANUAL_INTEGRATION_NOTES.txt', 'w', encoding='utf-8') as f:
        f.write("SAFETY_GATEWAY.PY CHANGES (APPLY MANUALLY):\n\n")
        f.write(manual_match.group(1))
    print("[CREATED] MANUAL_INTEGRATION_NOTES.txt")

print()
print("Files created. Review before using in production.")
print()
print(result['result'])
