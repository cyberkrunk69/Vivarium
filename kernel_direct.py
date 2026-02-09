#!/usr/bin/env python3
"""
Direct kernel analysis - bypass the grind spawner entirely.
"""
import os
from groq_client import GroqInferenceEngine

# Set API key
os.environ['GROQ_API_KEY'] = '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'

# Read io_uring.c
with open('io_uring.c', 'r') as f:
    kernel_code = f.read()

# Create the analysis prompt
prompt = f"""You are analyzing Linux kernel code for race conditions.

File: io_uring.c from Linux kernel v6.12.10 (3,881 lines)

TASK:
Analyze the request cancellation logic in this io_uring code.
Specifically examine:
1. io_poll_cancel functionality
2. Async completion of linked requests
3. Potential race conditions where io_kiocb could be freed while another thread accesses it
4. Use-after-free (UAF) vulnerabilities in concurrent paths

REQUIREMENTS:
- Trace specific line numbers for any issues found
- Do NOT hallucinate - only report what you can verify in the code
- If already hardened, explain the protection mechanisms

CODE:
```c
{kernel_code}
```

Provide your analysis as a detailed report.
"""

print("="*60)
print("DIRECT KERNEL ANALYSIS")
print("="*60)
print(f"Code size: {len(kernel_code)} bytes")
print(f"Lines: {len(kernel_code.splitlines())}")
print("Starting analysis...")
print()

# Create engine and run
from groq_client import execute_with_groq
result = execute_with_groq(prompt=prompt, model="llama-3.3-70b-versatile")

print("="*60)
print("ANALYSIS RESULT")
print("="*60)
print(result.get('response', result.get('text', str(result))))
print()
print(f"Cost: ${result.get('cost', 0):.4f}")
print(f"Tokens: {result.get('input_tokens', 0)} in, {result.get('output_tokens', 0)} out")

# Save to file
with open('kernel_analysis.md', 'w') as f:
    f.write("# Linux io_uring.c Race Condition Analysis\n\n")
    f.write(f"**Model:** {result.get('model', 'unknown')}\n")
    f.write(f"**Cost:** ${result.get('cost', 0):.4f}\n")
    f.write(f"**Tokens:** {result.get('input_tokens', 0)} in, {result.get('output_tokens', 0)} out\n\n")
    f.write("## Analysis\n\n")
    f.write(result.get('response', result.get('text', str(result))))

print("\nSaved to: kernel_analysis.md")
