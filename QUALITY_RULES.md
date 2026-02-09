# Quality Rules

## Purpose
These rules guarantee that the swarm never produces low‑quality, unsafe, or broken code.  
Every piece of generated code must pass **all** of the checks below before it is written to disk.

## Rules
1. **No Markdown Code Fences in Code Files**  
   Generated source files must never contain literal markdown fences such as ```` ```python ```` or ```` ``` ````.  

2. **Never Overwrite a Complex File with a Simpler Version**  
   If a target file already exists, the new content must be at least as large (in bytes) and contain **all** previously existing lines unless the overwrite is explicitly approved.  

3. **No Placeholder Logic**  
   The code must not contain placeholder constructs like `random()`, `TODO()`, `pass  # TODO`, or any comment that indicates missing real logic.  

4. **Implement All TODO Comments**  
   Any comment that starts with `TODO:` must be fully implemented before the file is saved.  

5. **Validate Syntax Before Saving**  
   For Python files, the code must parse without errors (`ast.parse`). For other languages, a simple syntactic sanity check (e.g., balanced brackets) is required.  

6. **Check File Existence & Size Before Overwrite**  
   When overwriting, the existing file must be larger **and** the new content must not be a strict subset of the old content.  

7. **Strip All Markdown Formatting**  
   Any markdown formatting (code fences, headings, bullet points, etc.) must be removed from the final code that is written to disk.  

### Enforcement
All generators must call the validation layer in `groq_code_extractor.py`. If any rule fails, the operation is aborted and a detailed log entry is written explaining why.  

---
# Comprehensive Quality Rules for the Swarm

These rules are **always** applied to any code generated or modified by the swarm.  
They prevent common pitfalls and ensure that the code base remains healthy,
readable, and functional.

## 1. No Markdown Code Fences in Files
- Never write ````python``, ```` or any other markdown fence characters into
  actual source files.  
- All generated code must be raw text without surrounding back‑ticks.

## 2. Preserve Complex Files
- Do **not** overwrite an existing complex file with a simpler version unless the
  new version is verified to be a superset or an intentional refactor.
- When overwriting, compare file sizes; only replace if the new content is
  larger **or** explicitly approved.

## 3. No Placeholder Logic
- Never use placeholder functions such as `random()`, `TODO()`, or stub returns.
- All required logic must be fully implemented before the file is saved.

## 4. No Unresolved TODO Comments
- All `# TODO` comments must be resolved.  
- If a TODO is genuinely pending, it must be tracked outside of the code base,
  not left in production files.

## 5. Syntax Validation
- Every code snippet must be syntactically correct for its language before it
  is written to disk.  
- For Python, this means the code can be compiled without errors.

## 6. Safe Overwrite Checks
- Before overwriting a file, check that the target file exists **and** that the
  new content is **larger** than the existing one, unless an explicit
  override flag is provided.

## 7. Strip Markdown Formatting
- Any markdown formatting (headings, lists, bold, italics, etc.) must be stripped
  from code before it is saved to a source file.

## 8. Validation Pipeline
All file writes must pass through the **quality_validator** module, which
enforces the above rules in the following order:

1. Strip markdown formatting.  
2. Detect and reject markdown fences.  
3. Detect placeholder logic and unresolved TODOs.  
4. Verify syntax correctness.  
5. Perform safe‑overwrite size check.  

If any check fails, the operation aborts and raises a descriptive exception.

---  

*These rules are immutable and must be referenced by any new code that writes
files to the repository.*
# Quality Rules Specification

These rules are enforced by `quality_validator.py` and must be applied to **all** code
generation and file‑write operations performed by the swarm.

## 1. No Markdown Code Fences in Files
- Generated source files must never contain markdown fences such as `````python``
  or ````` ```.  Any code that will be written to disk must be plain text.

## 2. Preserve Complex Files
- Never replace an existing file with a simpler version if the existing file is
  larger (more lines or characters) unless the new content is a verified
  refactor that retains all functionality.

## 3. No Placeholder Logic
- Random or stub implementations (`random()`, `TODO`, `pass`, etc.) are forbidden.
  Real, deterministic logic must be provided.

## 4. No TODO Comments
- All `# TODO` or `TODO:` comments must be fully implemented before the file is
  saved.

## 5. Syntactic Validation
- Before writing, the content must be parsed (e.g., using `ast.parse` for Python)
  to guarantee it is syntactically correct.

## 6. Safe Overwrite Checks
- When overwriting a file, the validator must confirm that the existing file
  exists **and** is larger (by line count) than the new content. Overwrites that
  reduce size are rejected unless explicitly allowed.

## 7. Strip Markdown Formatting
- Any markdown formatting (headings, lists, bold, italics, etc.) must be stripped
  from code before it is saved.

## 8. Central Validator
- All the above checks are implemented in `quality_validator.py`. Every
  component that writes files should import and call `validate_and_write`
  instead of using raw file I/O.

---

*These rules are intended to prevent “band‑aid” fixes and ensure high‑quality,
maintainable code throughout the project.*
# Quality Rules for the Swarm

These rules are **non‑negotiable** and must be enforced by every component that writes or modifies code files.  
The goal is to prevent “band‑aid” solutions and ensure that generated code is production‑ready.

## 1. No Markdown Fences in Code Files
- **Rule**: Code files must never contain markdown code fences such as ```` ```python ```` or ```` ``` ````.
- **Enforcement**: Strip any such fences before writing to disk.

## 2. Do Not Overwrite a Complex File with a Simpler Version
- **Rule**: A file may only be overwritten if the new content is **at least as large** (in bytes) as the existing file.
- **Rationale**: Prevents accidental loss of implementation detail.

## 3. No Placeholder Logic
- **Rule**: Do **not** commit code that contains placeholder constructs like `random()`, `pass`, `...`, or any stub that does not implement real logic.
- **Detection**: Search for the patterns `random\(\)`, `pass`, `TODO`, `FIXME`, or ellipsis (`...`).

## 4. No Unimplemented TODO Comments
- **Rule**: All `# TODO` (or `# FIXME`) comments must be resolved before the file is saved.
- **Enforcement**: The validator must reject any file that still contains such comments.

## 5. Validate Syntax Before Saving
- **Rule**: Every Python file must be syntactically valid (`ast.parse`) before it is written.
- **Extension**: For other languages, appropriate parsers must be used (out of scope for the current validator).

## 6. Size Check Before Overwrite
- **Rule**: If a target file already exists, compare its size to the incoming content. Only overwrite when the incoming content’s size is **greater than or equal to** the existing size.

## 7. Strip All Markdown Formatting from Code Output
- **Rule**: Any code that originates from a markdown source must have all markdown formatting removed (code fences, bullet points, etc.) before being saved.

## 8. Central Validation API
All code‑generation modules must call the central validation API (`quality_validator.validate_and_save`) which implements the checks above. Direct file writes without this validation are prohibited.

---  

**Compliance**: Any violation should raise a `ValueError` with a clear message indicating the rule that was broken. The swarm’s orchestrator must catch these exceptions and abort the offending operation.

```
# Quality Rules for the Swarm

These rules are enforced by **quality_validator.py** and must be followed by every
component that writes or modifies source files.

## General Principles
1. **No Markdown in Code** – Never emit markdown fences (e.g., ```python) or any
   other markdown formatting inside real code files.
2. **Never Downgrade Complexity** – Do not overwrite a complex implementation
   with a simpler placeholder version.
3. **No Placeholder Logic** – Real logic must be implemented; avoid stubs such as
   `random()`, `pass`, or `# TODO` that are not later replaced.
4. **No TODO Comments** – All `TODO` comments must be resolved before the file
   is saved.
5. **Syntactic Validity** – Every file must be syntactically correct (e.g.,
   `ast.parse` succeeds for Python) before it is written to disk.
6. **Safe Overwrites** – When overwriting an existing file, ensure the existing
   file is larger *or* the new content is at least as complete. Never replace a
   larger, functional file with a smaller, incomplete one.
7. **Strip Markdown** – Any markdown formatting that accidentally makes it into
   generated code must be stripped before saving.

## Enforcement Workflow (Implemented in `quality_validator.py`)
1. **Strip Markdown** – Remove any markdown code fences and surrounding
   formatting.
2. **Check for TODOs** – Scan the text for `TODO` markers; raise an error if any
   are found.
3. **Detect Placeholder Logic** – Look for patterns such as `random\(\)`,
   `pass\s*#\s*placeholder`, or similar stubs; raise an error if present.
4. **Validate Syntax** – Parse the code with Python’s `ast` module; on failure,
   abort the write.
5. **Safe Write** – Before writing, compare the size of the existing file (if
   any) with the new content. Abort if the new content is smaller than the
   existing file.
6. **Write File** – Only after all checks pass is the file written to disk.

## Responsibility
All swarm agents must invoke `quality_validator.safe_write(path, content)` (or
the equivalent validation functions) for any file creation or modification.
Direct file writes without these checks are prohibited.

---

*These rules are immutable and must be adhered to at all times.*