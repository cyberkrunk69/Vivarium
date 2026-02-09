# NEXT_EVOLUTION_ROADMAP.md

## Objective
Allocate the next **$1** of compute to initiatives that will deliver the highest incremental impact on model performance, data quality, and operational robustness for the unified session experiment.

## Prioritized Spend Plan

| Rank | Initiative | Description | Expected Impact | Approx. Compute Cost |
|------|------------|-------------|-----------------|----------------------|
| 1 | **Targeted Data Augmentation Pipeline** | Build a lightweight, on‑the‑fly augmentation service that generates synthetic variations (noise injection, paraphrasing, style transfer) for the most error‑prone data slices identified in the last evaluation. | ↑ +3–5% F1 on low‑resource domains; improves generalization with minimal data collection overhead. | ~0.25 USD |
| 2 | **Curriculum Learning Scheduler** | Implement a dynamic curriculum that prioritizes training on high‑loss examples first, then gradually introduces easier samples. Uses a simple loss‑based sampler without extra model passes. | ↑ +2% overall accuracy; faster convergence, reducing future compute waste. | ~0.20 USD |
| 3 | **Lightweight Knowledge Distillation** | Distill the current large model into a 2‑3× smaller student using a single‑epoch teacher‑student pass on a curated subset (≈10 % of the corpus). | ↓ inference latency 30 %; enables larger batch sizes for downstream tasks. | ~0.18 USD |
| 4 | **Automated Prompt Engineering Loop** | Deploy a small LLM (e.g., GPT‑2‑small) to generate and evaluate prompt variants on a validation set, selecting top‑k prompts automatically. | ↑ +1–2% task‑specific performance; reduces manual prompt tuning time. | ~0.15 USD |
| 5 | **Robustness Evaluation Suite** | Run a focused adversarial test suite (perturbations, out‑of‑distribution samples) to surface hidden failure modes before the next training cycle. | Early bug detection → saves >$0.5 in future re‑training. | ~0.12 USD |

### Rationale
1. **Data augmentation** provides the highest ROI because it directly expands the effective training set without costly data collection.
2. **Curriculum learning** leverages existing loss signals to make each training step more informative, accelerating convergence.
3. **Distillation** prepares the model for production scaling, ensuring the $1 spend also yields downstream cost savings.
4. **Prompt engineering automation** reduces human effort and uncovers prompt patterns that may be missed manually.
5. **Robustness evaluation** is a preventative measure that protects earlier investments from hidden defects.

### Execution Steps
1. **Set up a temporary compute sandbox** (e.g., a low‑cost spot instance) with the current codebase.
2. **Implement the augmentation pipeline** using existing `nlpaug` utilities; log augmentation statistics.
3. **Integrate the curriculum scheduler** into the training loop; monitor loss distribution.
4. **Run a single distillation pass** on a sampled dataset; validate student performance.
5. **Launch the prompt generation script**, capture top prompts, and benchmark them.
6. **Execute the robustness suite**, collect failure reports, and feed them back into the augmentation step.

### Monitoring & Metrics
- Track **F1 / Accuracy improvements** per initiative.
- Log **compute usage** to ensure the total stays ≤ $1.
- Record **latency / model size** after distillation.
- Capture **prompt performance variance** across tasks.
- Document **failure modes** identified by the robustness suite.

---

*Prepared for experiment `exp_20260204_033659_unified_session_14` on 2026‑02‑04.*