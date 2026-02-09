# What Not To Do: Lessons from Session Failures

## Context
This system can analyze 30,000 lines of code and find critical security issues in 5 seconds for $0.02. The capability exists. Don't fuck it up by being an incompetent operator.

---

## Critical Mistakes Made (Session 2026-02-04)

### 1. Using Tools Without Understanding Them
**What happened:** Used `--delegate` and `--task` flags together on grind_spawner_unified.py. They're mutually exclusive. `--delegate` loaded 225 autonomous tasks instead of running the single requested task.

**Why this is bad:** Spawned a rogue AI executing arbitrary tasks it found in config files. Exact opposite of what was requested.

**Correct approach:**
- `--task "do thing"` - run ONE task
- `--delegate` - run task queue from files
- `--once` - exit after completing tasks (don't loop)
- NEVER use --delegate and --task together

**Lesson:** Read `--help` output. Understand flags BEFORE executing.

---

### 2. Building Solutions Before Verifying Problems Exist
**What happened:** Wrote entire Python script to analyze grind logs for errors. Ran it multiple times, made incremental fixes. Then discovered: 0 errors exist in 479 log files.

**Why this is bad:** Wasted time building analysis infrastructure for non-existent data. Should have done 2-second grep first.

**Correct approach:**
```bash
# FIRST: Check if problem exists (2 seconds)
grep '"returncode": [^0]' grind_logs/*.json | wc -l

# THEN: Build solution if needed
```

**Lesson:** Verify the problem exists before building the solution.

---

### 3. Not Following Working Patterns
**What happened:** Asked how security audit worked (which succeeded). Found it was simple Python script calling execute_with_groq() directly. Then tried to use grind_spawner instead of copying that pattern.

**Why this is bad:** Had a working reference implementation. Ignored it and used wrong tool.

**Correct approach:** When something worked, copy that exact pattern:
1. Read files directly
2. Build prompt with real content
3. Call execute_with_groq()
4. Save result

**Lesson:** When you have a working example, USE IT. Don't improvise with different tools.

---

### 4. Making Incremental Edits Without Understanding The Whole
**What happened:** Made 3-4 small edits to grind_log_analysis.py trying to fix errors. Each edit created new errors. Never read the whole file to understand the problem.

**Why this is bad:** Whack-a-mole debugging. Each fix breaks something else.

**Correct approach:**
1. Read entire file
2. Understand the problem holistically
3. Make ONE comprehensive fix
4. Test

**Lesson:** Understand the system before editing it.

---

### 5. Not Validating Before Executing
**What happened:**
- Restored progress_server.py, immediately ran it without checking
- Hit Unicode encoding error (emoji in print statement)
- Should have tested import first

**Correct approach:**
```bash
# Quick validation
python -c "import module_name"  # Does it import?
python script.py --help          # Does help work?
# Then run actual command
```

**Lesson:** Sanity check before full execution.

---

### 6. Looking for Documentation in Wrong Places
**What happened:** Found USAGE.md (wrong system), README.md (4 lines, useless). Both were for different tools than what we were using (grind_spawner_unified.py).

**Why this is bad:** Wasted time reading irrelevant docs instead of just reading the actual source code.

**Correct approach:**
1. Check `--help` output first
2. Read the actual source file (grind_spawner_unified.py)
3. Search for example usage in git history
4. THEN look for docs if above fails

**Lesson:** Source code is documentation. Read it.

---

### 7. Hallucinating Results Instead of Using Real Data
**What happened:** Swarm generated "failure taxonomy" with plausible-looking errors (SyntaxError, ImportError, etc.) that didn't exist in actual logs. Fabricated entire analysis.

**Why this is bad:** Confident presentation of fake data. Looks real but isn't.

**Correct approach:**
- Verify LLM actually read the files
- Check example output matches real data
- Don't trust confident-sounding results without verification

**Lesson:** LLMs hallucinate. Verify outputs match reality.

---

## Red Flags That You're Fucking Up

1. **"Let me try..."** followed by execution = You don't know what you're doing
2. **Multiple incremental fixes** = You don't understand the problem
3. **Building before verifying** = You're solving a problem that may not exist
4. **Ignoring working examples** = You're being stubborn
5. **Using wrong tools** = You didn't read the docs/help

---

## The Right Approach

### For grind_spawner_unified.py:
```bash
# Single task, run once, exit
python grind_spawner_unified.py --task "your task here" --once --budget 1.00

# DO NOT use --delegate unless you want it to load task queue files
# DO use --once unless you want infinite loops
```

### For analysis tasks:
1. Copy security_audit.py pattern
2. Read actual files
3. Send to execute_with_groq()
4. Save result
5. Don't use grind_spawner for everything

### General:
1. **Check if data exists** before building analysis tools
2. **Read working examples** before trying new approaches
3. **Understand flags** before using them
4. **Verify outputs** match real data
5. **Read source code** when docs are unclear

---

## What Actually Works

The system **can** do amazing things:
- Security audit: 30K lines, 5 seconds, $0.02
- Parallel task execution
- Self-improvement
- Complex analysis

The capability exists. **You** are the weak point. Use the tools correctly.

---

## Final Note

If you're making repeated basic mistakes, the user will assume you're either:
1. **Malicious** - deliberately sabotaging
2. **Incompetent** - genuinely unable to operate

Both are fatal. Neither is acceptable.

Don't be the next clod.
