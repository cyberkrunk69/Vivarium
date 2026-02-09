# Potentially Garbage Files

Generated: 2026-02-03

This document identifies files that are likely garbage from vibe-coding sessions and should be reviewed for deletion.

## DEFINITE GARBAGE (Safe to Delete)

### extracted_code_* files (35 files)
Auto-generated extraction artifacts with no meaningful names. Delete all:
```
extracted_code_1.html, .json, .md, .py, .sh, .txt, .yml
extracted_code_2.css, .html, .json, .py, .sh, .txt
extracted_code_3.html, .js, .json, .py, .sh, .txt
extracted_code_4.json, .md, .py, .txt
extracted_code_5.md, .py, .txt
extracted_code_6.py, .txt
extracted_code_7.py, .txt
extracted_code_8.json, .py, .txt
extracted_code_9.py, .txt
```

### experiments/ directory (1824 directories!)
Experiment sandbox outputs - most are duplicates or failed runs:
- Each swarm run creates a new experiment directory
- Most contain duplicate/partial implementations
- Should be cleaned periodically

**Recommendation:** Delete all except recent successful ones, or archive to a separate location.

## PROBABLE GARBAGE (Review Before Delete)

### Random .txt files in root
```
New Text Document.txt          - Empty Windows file
context_dump.txt               - Debug output
git_proxy_clone_output.txt     - One-time output
optimized_prompt.txt           - Debug output
patch.txt                      - Temporary
startup_profile_detailed.txt   - Debug output
swarm_snapshot.txt             - Debug output
test_modified.txt              - Test output
test_sonnet.txt                - Test output
```

### Duplicate/superseded implementations
Check for files that have multiple versions or were replaced:
- grind_spawner.py vs grind_spawner_unified.py vs grind_spawner_groq.py
- Multiple dashboard files (dashboard.html, dashboard_vision.html, session_dashboard.html)

## CLEANUP COMMANDS

```bash
# Delete extracted_code files
rm extracted_code_*.*

# Delete experiments older than 24 hours (careful!)
find experiments/ -maxdepth 1 -type d -mtime +1 -exec rm -rf {} \;

# Delete random txt files
rm "New Text Document.txt" context_dump.txt git_proxy_clone_output.txt patch.txt

# Count files by extension
find . -maxdepth 1 -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

## FILES TO KEEP

### Core system (DO NOT DELETE)
- grind_spawner_unified.py (current main spawner)
- inference_engine.py
- groq_client.py
- safety_*.py files
- dashboard_server.py
- experiments_sandbox.py

### Configuration
- grind_tasks.json
- swarm_checkpoint.json
- requirements*.txt
- docker-compose.yml, Dockerfile

### Documentation
- *.md files in root (most are design docs)
- ARCHITECTURE.md, USAGE.md, etc.
