# META LESSONS LEARNED  
*Experiment: exp_20260204_033700_unified_session_15*  

## 1. Prompt Clarity Drives Output Quality  
- Explicitly state the required output format (e.g., artifact tags, file paths).  
- Include concrete constraints (read‑only files, default directories) to avoid accidental modifications.  

## 2. Modular Artifact Generation  
- Create one file per logical unit; keep each artifact self‑contained.  
- Use consistent naming conventions (`META_LESSONS_LEARNED.md`) and store under the experiment’s folder to simplify downstream retrieval.  

## 3. Iterative Refinement Over One‑Shot Solutions  
- Break complex tasks into smaller, testable steps (e.g., first draft, then add bullet points).  
- Validate assumptions (e.g., directory existence) before writing to avoid runtime errors.  

## 4. Emphasize Reusability  
- Write lessons in a generic, future‑proof style—avoid references to specific code that may change.  
- Highlight patterns (prompt design, logging, version control) that are applicable across swarm runs.  

## 5. Documentation Consistency  
- Begin every meta‑doc with a header that includes the experiment ID and date.  
- Use markdown headings and bullet lists for quick scanning by automated tools.  

## 6. Safety & Permissions Awareness  
- Respect the “read‑only core system files” rule; always target the `experiments/` subtree for new artifacts.  
- Include a brief note on any deviations from the rule (none required here).  

## 7. Speed vs. Completeness Trade‑off  
- Prioritize concise, actionable insights when the instruction emphasizes “be FAST”.  
- Reserve deep technical analysis for dedicated follow‑up tasks.  

---  

*These lessons should be referenced at the start of future swarm runs to accelerate onboarding, reduce errors, and improve overall productivity.*