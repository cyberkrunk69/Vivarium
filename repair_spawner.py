import os
import re

file_path = "grind_spawner.py"

print(f"Reading {file_path}...")
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# --- FIX: Replace the Broken Subprocess Block with Groq Logic ---
print("Locating broken subprocess block...")

# We look for the start of the try block inside run_once
# and replace everything down to the end of the subprocess call
# This regex targets the specific commented-out mess and the subprocess.run call
pattern = r'while attempt <= max_retries:\s+try:\s+# Build claude command.*?result = subprocess\.run\(.*?timeout=600.*?\)'

new_logic = """        while attempt <= max_retries:
            try:
                # SWAN MOD: GROQ DIRECT EXECUTION
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
                    result = MockFail(e)"""

# Perform the replacement using DOTALL so . matches newlines
match = re.search(pattern, content, re.DOTALL)
if match:
    print("-> Found broken block. Replacing with Groq Engine logic...")
    content = content.replace(match.group(0), new_logic)
else:
    print("-> WARNING: Could not find exact block match. Attempting fallback patch...")
    # Fallback: Find the specific commented out lines causing the error
    broken_code_start = '# cmd = [\n                    # "claude",'
    if broken_code_start in content:
        # We find the start, and look for the end of the subprocess call
        start_idx = content.find(broken_code_start)
        end_marker = "timeout=600  # 10 minute timeout per session\n                )"
        end_idx = content.find(end_marker, start_idx) + len(end_marker)
        
        # We need to preserve the "while attempt <= max_retries:\n            try:" part which is above
        # So we reconstruct just the inner part
        
        inner_logic = """
                # SWAN MOD: GROQ DIRECT EXECUTION
                from core.local_engine import get_engine
                engine = get_engine() 
                
                # Map legacy Claude names
                if self.model in ["haiku", "sonnet"]: self.model = "groq/compound"
                elif self.model in ["opus"]: self.model = "llama-3.3-70b-versatile"

                print(f"[Session {self.session_id}] Sending to Groq LPU ({self.model})...")
                
                try:
                    response_text = engine.generate(current_prompt, model=self.model)
                    class MockResult:
                        def __init__(self, txt):
                            self.stdout = txt
                            self.stderr = ""
                            self.returncode = 0
                    result = MockResult(response_text)
                except Exception as e:
                    print(f"[Session {self.session_id}] Groq API Error: {e}")
                    class MockFail:
                        def __init__(self, err):
                            self.stdout = ""
                            self.stderr = str(err)
                            self.returncode = 1
                    result = MockFail(e)
"""
        # Find the line "while attempt <= max_retries:"
        loop_start = content.rfind("while attempt <= max_retries:", 0, start_idx)
        try_start = content.find("try:", loop_start)
        
        # Replace from after "try:" to end_idx
        content = content[:try_start + 4] + inner_logic + content[end_idx:]
        print("-> Fallback patch applied.")

# Write back
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Done. {file_path} repaired.")