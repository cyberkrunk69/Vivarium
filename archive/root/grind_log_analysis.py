#!/usr/bin/env python3
"""
Grind Log Analysis - Find patterns in mistakes/failures

Analyzes actual grind log JSON files to categorize errors and failures.
"""
import os
import json
import glob
from groq_client import execute_with_groq

if not os.environ.get("GROQ_API_KEY"):
    raise SystemExit("Set GROQ_API_KEY in environment before running grind_log_analysis.py")

# Read grind log files
log_files = glob.glob('grind_logs/*.json')
print(f"Found {len(log_files)} grind log files")

# Extract error patterns from logs
error_data = []
success_data = []

for log_file in log_files[:50]:  # Limit to first 50 files to avoid token overflow
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            log = json.load(f)

        # Extract key fields
        session_name = os.path.basename(log_file)
        returncode = log.get('returncode', 0)
        error = log.get('error')
        result = log.get('result', '')
        cost = log.get('cost', 0)

        if returncode != 0 or error:
            error_data.append({
                'file': session_name,
                'error': error if error else 'Non-zero returncode',
                'returncode': returncode,
                'result_preview': result[:300] if result else ''
            })
        else:
            success_data.append({
                'file': session_name,
                'cost': cost
            })

        print(f"[OK] Parsed {session_name}")
    except Exception as e:
        print(f"[SKIP] Could not parse {log_file}: {e}")

# Build analysis prompt
prompt = f"""You are analyzing real grind log data from an autonomous AI swarm system.

## Dataset Summary
- Total log files analyzed: {len(log_files)}
- Failed/Error sessions: {len(error_data)}
- Successful sessions: {len(success_data)}

## Error Examples (first 20):

"""

for i, err in enumerate(error_data[:20], 1):
    prompt += f"\n### Error {i}: {err['file']}\n"
    prompt += f"Returncode: {err['returncode']}\n"
    prompt += f"Error: {err['error']}\n"
    prompt += f"Result Preview: {err['result_preview']}\n"

prompt += """

## Your Mission: Failure Taxonomy

Analyze these real errors and create:

### 1. Error Categories
Group errors by root cause:
- API/Model errors
- Code generation failures
- File operation errors
- Timeout/resource errors
- Logic/reasoning failures
- Hallucination/fabrication
- Other categories you identify

### 2. Pattern Analysis
For each category:
- How many occurrences
- Common triggers
- Example error messages
- Severity (1-10)

### 3. Stupid Mistakes
Specifically identify:
- Cases where the AI clearly misunderstood the task
- Hallucinated data instead of reading real files
- Used wrong tools/flags
- Broke working code
- Forgot basic facts about the system

### 4. Actionable Insights
What patterns suggest systemic issues vs one-off mistakes?

Be brutally honest. This is for learning, not ego protection.
"""

print("\n" + "="*60)
print("GRIND LOG ANALYSIS INITIATED")
print("="*60)
print(f"Analyzing {len(error_data)} errors from {len(log_files)} sessions")
print(f"Prompt size: ~{len(prompt)} characters")
print("Budget: $0.10")
print()

result = execute_with_groq(prompt=prompt, model="llama-3.3-70b-versatile")

print("="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print()
print(f"Cost: ${result['cost']:.4f}")
print(f"Tokens: {result['input_tokens']} in, {result['output_tokens']} out")
print()

# Save to file
with open('GRIND_LOG_ANALYSIS.md', 'w', encoding='utf-8') as f:
    f.write("# Grind Log Failure Analysis\n\n")
    f.write(f"**Date:** {result['timestamp']}\n")
    f.write(f"**Model:** {result['model_display']}\n")
    f.write(f"**Cost:** ${result['cost']:.4f}\n")
    f.write(f"**Files Analyzed:** {len(log_files)} grind logs\n")
    f.write(f"**Errors Found:** {len(error_data)}\n\n")
    f.write("---\n\n")
    f.write(result['result'])

print("Saved to: GRIND_LOG_ANALYSIS.md")
print()
print(result['result'])
