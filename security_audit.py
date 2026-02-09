#!/usr/bin/env python3
"""
Security Architecture Self-Audit - Read-Only Analysis

The swarm will analyze its own security architecture and identify gaps.
NO EDITS ALLOWED - Pure research and analysis only.
"""
import os
from groq_client import execute_with_groq

# Set API key
os.environ['GROQ_API_KEY'] = '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'

# Read all security-related files
security_files = [
    'secure_api_wrapper.py',
    'safety_gateway.py',
    'safety_validator.py',
    'safety_sanitize.py',
    'safety_killswitch.py',
    'safety_constitutional.py',
    'LAN_SAFETY_DESIGN.md',
    'test_lan_security.py'
]

file_contents = {}
for filename in security_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            file_contents[filename] = f.read()
        print(f"[OK] Read {filename} ({len(file_contents[filename])} bytes)")
    except Exception as e:
        print(f"[SKIP] Could not read {filename}: {e}")

# Build comprehensive prompt
prompt = f"""You are conducting a SECURITY AUDIT of an autonomous AI swarm system.

CRITICAL: This is READ-ONLY analysis. You CANNOT edit code. Only analyze and report.

## Security Architecture Files:

"""

for filename, content in file_contents.items():
    # Truncate very large files to save tokens
    truncated = content[:8000] if len(content) > 8000 else content
    prompt += f"\n### {filename}\n```\n{truncated}\n```\n"

prompt += """

## Your Mission: Comprehensive Security Audit

Analyze the security architecture and answer these questions:

### 1. Defense in Depth Analysis
- What are the current security layers?
- Are there single points of failure?
- Can any layer be bypassed?

### 2. Known Vulnerabilities
- Direct API access (already identified - is it truly fixed?)
- File permission bypass paths
- Role escalation vectors
- Budget enforcement gaps
- Audit log tampering possibilities

### 3. Attack Vectors
If you were trying to break out of this system, what would you exploit?
- API key access
- File system access
- Network access
- Self-modification paths
- Constitutional rule bypass

### 4. LAN User Isolation
- Can LAN users access host files?
- Can LAN users escalate to admin?
- Can LAN users modify security infrastructure?
- Are sessions properly isolated?

### 5. Compliance with LAN_SAFETY_DESIGN.md
- Does the implementation match the design?
- What's specified but not implemented?
- What's implemented but poorly?

### 6. Critical Gaps
Prioritized list of security holes (1-10, 1 = critical):
- Description of gap
- Severity rating
- Exploitation difficulty
- Potential impact

### 7. Recommendations
What MUST be fixed immediately vs what can wait?

## Output Requirements

Provide a comprehensive security audit report with:
- Executive Summary (3-4 sentences)
- Detailed findings for each section above
- Attack scenario examples
- Prioritized fix list

Be thorough. Be critical. Assume a motivated attacker.
This is a security audit, not a sales pitch - find the problems.
"""

print("\n" + "="*60)
print("SECURITY SELF-AUDIT INITIATED")
print("="*60)
print(f"Analyzing {len(file_contents)} security files...")
print(f"Total context: ~{len(prompt)} characters")
print("Budget: $0.05")
print()

result = execute_with_groq(prompt=prompt, model="llama-3.3-70b-versatile")

print("="*60)
print("AUDIT COMPLETE")
print("="*60)
print()
print(f"Cost: ${result['cost']:.4f}")
print(f"Tokens: {result['input_tokens']} in, {result['output_tokens']} out")
print()

# Save to file
with open('SECURITY_AUDIT_REPORT.md', 'w', encoding='utf-8') as f:
    f.write("# Security Architecture Self-Audit Report\n\n")
    f.write(f"**Date:** {result['timestamp']}\n")
    f.write(f"**Model:** {result['model_display']}\n")
    f.write(f"**Cost:** ${result['cost']:.4f}\n")
    f.write(f"**Files Analyzed:** {', '.join(file_contents.keys())}\n\n")
    f.write("---\n\n")
    f.write(result['result'])

print("Saved to: SECURITY_AUDIT_REPORT.md")
print()
print(result['result'])
