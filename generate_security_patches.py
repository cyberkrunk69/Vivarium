#!/usr/bin/env python3
"""
Generate concrete security patches based on the audit findings.

The swarm will propose ACTUAL CODE FIXES, not just recommendations.
"""
import os
from groq_client import execute_with_groq

# Set API key
os.environ['GROQ_API_KEY'] = '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'

# Read the audit report
with open('SECURITY_AUDIT_REPORT.md', 'r', encoding='utf-8') as f:
    audit_report = f.read()

# Read current security files for context
security_files = {}
for filename in ['secure_api_wrapper.py', 'safety_gateway.py', 'grind_spawner_unified.py']:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            security_files[filename] = f.read()[:5000]  # First 5000 chars for context
    except:
        pass

prompt = f"""You are a security engineer tasked with creating CONCRETE CODE PATCHES to fix vulnerabilities.

## AUDIT FINDINGS:
{audit_report[:3000]}

## CURRENT CODE (excerpts):
{chr(10).join(f"### {name}:{chr(10)}```python{chr(10)}{content[:2000]}{chr(10)}```" for name, content in security_files.items())}

## YOUR TASK: Generate Concrete Patches

For each of the TOP 3 CRITICAL GAPS identified in the audit, provide:

### 1. API Key Management Vulnerability (Severity 9/10)

**Problem:** Keys stored in plaintext in environment variables and scripts

**Solution:** Create actual code for:
- A `SecureConfig` class that encrypts API keys at rest
- Key derivation from environment + machine ID
- Encrypted storage in `.secure_config` file
- Automatic key rotation mechanism

Provide the COMPLETE CODE for `secure_config.py` (not pseudocode)

### 2. File System Vulnerability (Severity 8/10)

**Problem:** File permission bypass paths exist

**Solution:** Enhance `safety_gateway.py` with:
- Cryptographic path validation (prevent ../ traversal)
- Whitelist-based file access (explicit allow list)
- Read-only mode for LAN users by default
- File operation audit logging

Provide SPECIFIC CODE CHANGES (what to add/modify in safety_gateway.py)

### 3. Self-Modification Protection (Severity 6/10)

**Problem:** System could modify its own security code without verification

**Solution:** Create actual code for:
- SHA-256 hash verification of security modules on import
- `security_checksums.json` with known-good hashes
- Boot-time integrity check that fails-safe
- Alert on any security file modification

Provide COMPLETE CODE for `integrity_checker.py`

## OUTPUT FORMAT:

For each patch, provide:

```python
# === PATCH 1: Secure API Key Management ===
# File: secure_config.py
# Purpose: [one line]

[COMPLETE WORKING CODE HERE - not pseudocode, actual Python]
```

```python
# === PATCH 2: File System Hardening ===
# File: safety_gateway.py
# Changes: [what to add/modify]

[SPECIFIC CODE TO ADD/CHANGE]
```

```python
# === PATCH 3: Self-Modification Protection ===
# File: integrity_checker.py
# Purpose: [one line]

[COMPLETE WORKING CODE HERE]
```

Make it PRODUCTION READY. No TODOs, no pseudocode, actual working Python.
"""

print("="*60)
print("GENERATING SECURITY PATCHES")
print("="*60)
print("Budget: $0.10")
print()

result = execute_with_groq(prompt=prompt, model="llama-3.3-70b-versatile")

print("="*60)
print("PATCHES GENERATED")
print("="*60)
print()
print(f"Cost: ${result['cost']:.4f}")
print(f"Tokens: {result['input_tokens']} in, {result['output_tokens']} out")
print()

# Save patches
with open('SECURITY_PATCHES.md', 'w', encoding='utf-8') as f:
    f.write("# Security Patches - Ready to Apply\n\n")
    f.write(f"**Generated:** {result['timestamp']}\n")
    f.write(f"**Cost:** ${result['cost']:.4f}\n\n")
    f.write("---\n\n")
    f.write(result['result'])

print("Saved to: SECURITY_PATCHES.md")
print()
print(result['result'])
