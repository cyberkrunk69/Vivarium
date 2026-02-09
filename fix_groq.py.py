import os
import re

file_path = "grind_spawner.py"

print(f"Reading {file_path}...")
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# --- FIX 1: Remove the "Hang" (Duplicate Safety Gateway) ---
print("Scanning for duplicate Safety Gateway blocks...")
safety_block_signature = 'print(f"[Session {self.session_id}] [SAFETY GATEWAY] Running comprehensive safety checks...")'

first_idx = content.find(safety_block_signature)
second_idx = content.find(safety_block_signature, first_idx + 1)

if second_idx != -1:
    print("-> Duplicate Safety Gateway block found. Removing it.")
    # Heuristic: Find the next major log statement to define the end of the block
    end_signature = 'print(f"[Session {self.session_id}] [SAFETY] Scanning prompt for network access violations...")'
    end_idx = content.find(end_signature, second_idx)
    
    if end_idx != -1:
        content = content[:second_idx] + content[end_idx:]
        print("-> Block removed successfully.")
    else:
        print("-> WARNING: Could not find end of block. Skipping safe deletion.")
else:
    print("-> No duplicate block found (clean).")

# --- FIX 2: Inject Groq/Compound Engine (Replacing Claude CLI) ---
print("Patching execution loop to use Groq API...")

# This pattern looks for the subprocess call to 'claude'
# We replace the entire try block setup for the command
regex_pattern = r'cmd\s*=\s*\[\s*"claude",[^\]]+\]\s+.*?timeout=600\s*\)'

new_execution_logic = """
                # SWAN MOD: GROQ COMPOUND EXECUTION
                from core.local_engine import get_engine
                
                # Default to Groq engine
                engine = get_engine() 
                
                # Map legacy Claude names to Groq Production Models
                if self.model in ["haiku", "sonnet", "claude-3-5-sonnet-latest"]:
                    self.model = "groq/compound"  # The Smart Router
                elif self.model in ["opus"]:
                    self.model = "llama-3.3-70b-versatile" # The Heavy Lifter

                print(f"[Session {self.session_id}] Sending to Groq LPU ({self.model})...")
                
                try:
                    # Call the local engine wrapper
                    response_text = engine.generate(current_prompt, model=self.model)
                    
                    # Create a mock object so the rest of the script thinks it ran a subprocess
                    class MockResult:
                        def __init__(self, txt):
                            self.stdout = txt
                            self.stderr = ""
                            self.returncode = 0
                    
                    result = MockResult(response_text)
                    
                except Exception as e:
                    print(f"[Session {self.session_id}] Groq API Error: {e}")
                    # Create a mock failure result
                    class MockFail:
                        def __init__(self, err):
                            self.stdout = ""
                            self.stderr = str(err)
                            self.returncode = 1
                    result = MockFail(e)
"""

# Use regex substitution to swap the logic
if re.search(regex_pattern, content, re.DOTALL):
    content = re.sub(regex_pattern, new_execution_logic, content, flags=re.DOTALL)
    print("-> Claude CLI subprocess replaced with Groq Engine calls.")
else:
    print("-> WARNING: Could not locate the subprocess block via Regex. Check indentation.")

# --- FIX 3: Update Complexity Map to use Compound ---
print("Updating complexity/model mapping...")
content = content.replace('return "opus"', 'return "llama-3.3-70b-versatile"')
content = content.replace('return "sonnet"', 'return "groq/compound"')
content = content.replace('if base_model == "haiku":', 'if base_model == "groq/compound":')

# --- FIX 4: Repair Safety Imports ---
print("Fixing Safety imports...")
content = content.replace('from safety_killswitch import KillSwitch, CircuitBreaker', 'from safety_killswitch import get_kill_switch, get_circuit_breaker')
content = content.replace('from safety_sandbox import init_sandbox', 'from safety_sandbox import initialize_sandbox')

# Write back
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Done. {file_path} patched.")