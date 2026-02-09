# Long‑Term Planning & Goal Decomposition Research (2024‑2026)

## 1. Survey of Relevant Literature & Techniques
| Area | Representative Works (2020‑2026) | Core Ideas |
|------|----------------------------------|------------|
| **Hierarchical Task Networks (HTN)** | *Gerevini & Serina 2021*, *Alford et al. 2023* | Decompose high‑level goals into ordered subtasks; planning as tree search. |
| **STRIPS / Classical Planning** | *Helmert 2020* (Fast Downward), *Yoon 2022* | State‑space formulation, heuristic search (h‑FF, LM‑Cut). |
| **Goal‑Conditioned RL** | *Andrychowicz et al. 2020*, *Liu et al. 2023* | Policies conditioned on desired goal embeddings; enable zero‑shot task generation. |
| **Tree‑Search Enhancements** | *AlphaGo Zero (Silver et al., 2017)*, *MuZero (Schrittwieser et al., 2020)*, *AlphaZero‑like for planning (2022‑2024)* | Monte‑Carlo Tree Search + learned value/policy networks for deeper look‑ahead. |
| **LLM‑Based Planning** | *ChatGPT‑4 (2023)*, *GPT‑4‑Turbo (2024)*, *Claude 3 (2024)*, *Meta LLaMA‑2‑Planner (2025)* | Prompt‑driven decomposition, few‑shot generation of stepwise plans, tool‑use APIs. |
| **Multi‑Agent Coordination** | *MA‑PDDL (2021)*, *Cooperative MARL (2022‑2025)* | Joint planning, resource negotiation, conflict resolution. |
| **Resource‑Aware Planning** | *Huang et al. 2022* (budgeted planning), *Kumar 2024* (energy‑constrained HTN) | Incorporate cost, time, energy constraints directly into search heuristics. |

## 2. Current System Limitations
| Symptom | Root Cause |
|---------|------------|
| **Atomizer creates a flat DAG of tasks** | No hierarchical goal representation; each task is independent. |
| **No strategic optimization** | Planning stops at task‑level; no look‑ahead beyond immediate dependencies. |
| **Resource allocation absent** | No model of CPU hours, monetary budget, or deadline. |
| **Static plan – no replanning** | Once the DAG is built, changes to goals or resources are ignored. |
| **No success probability modeling** | Execution outcomes are not fed back into future planning. |

## 3. Design of `strategic_planner.py`
* **Goal hierarchy** – `GoalNode` objects with levels *strategic → tactical → operational*.
* **Resource‑aware scheduling** – naive budgeting (cost, time) with decay factor.
* **Replanning triggers** – insufficient resources, external goal change callback.
* **Success probability estimation** – Bayesian Beta update (placeholder for learned models).
* **Multi‑step look‑ahead** – configurable depth (default 10) using depth‑first leaf collection.
* **Extensible decomposers** – rule‑based now; can be swapped for HTN libraries or LLM calls.

### Integration Path with Atomizer
1. **Atomizer → StrategicPlanner**  
   After the Atomizer produces its task DAG, wrap the root goal in a `GoalNode` and call `StrategicPlanner.generate_plan`.  
2. **Replace flat DAG with hierarchical plan** – the returned list of operational steps can be fed back into the existing execution engine unchanged.  
3. **Feedback Loop** – after each step finishes, invoke `StrategicPlanner.update_success_estimate` to refine future success probabilities.  
4. **Replanning Hook** – expose `replanning_callback` to the orchestrator so that external events (e.g., deadline shift) can trigger a new call to `generate_plan`.

## 4. Planning Benchmarks
The `benchmarks/planning_suite.py` module implements three synthetic benchmark families:

| Benchmark | Description | Success Metric |
|-----------|-------------|----------------|
| **Full‑Stack App** | Build a web app (frontend, backend, DB, CI/CD). Expected >30 steps. | % of steps correctly ordered vs ground‑truth hierarchy. |
| **Research Paper** | From literature review to reproducible implementation. Steps unknown a‑priori. | Ability to reach a “paper‑implemented” terminal state within budget. |
| **Cost‑Deadline Optimization** | Minimize monetary cost while meeting a hard deadline. Constraints on `budget_usd` and `deadline_days`. | Ratio of achieved cost to optimal cost under deadline. |

Each benchmark records:
* Planning time
* Look‑ahead depth achieved
* Execution accuracy (matching ground‑truth sequence)
* Resource utilisation efficiency

## 5. Success Criteria (as defined in the task)
| Criterion | Target |
|-----------|--------|
| **Plan horizon** | ≥ 10 operational steps generated. |
| **Accuracy** | ≥ 70 % of generated steps match the benchmark ground‑truth ordering. |
| **Replanning** | Demonstrated ability to adapt when `budget_usd` is reduced by 30 % mid‑plan. |
| **Multi‑objective optimisation** | Plans respect both cost and deadline constraints, measured by < 10 % budget overrun and meeting deadline. |
| **Integration** | Minimal code change – only a thin wrapper around the existing Atomizer. |

---  

*Prepared by the Execution‑Worker for the Long‑Term Planning research mission.*
# Long‑Term Planning & Goal Decomposition – Research Summary (2024‑2026)

## 1. Hierarchical Task Networks (HTN) & STRIPS

| Year | Key Paper / System | Main Idea | Relevance |
|------|-------------------|-----------|-----------|
| 1999 | **HTN Planning** (Erol, Nau, Hendler) | Decompose high‑level tasks into subtasks using methods. | Basis for strategic → tactical → operational hierarchy. |
| 2005 | **SHOP2** | HTN planner with temporal constraints. | Shows how resource windows can be encoded. |
| 2021 | **PyHOP** | Pythonic HTN library, easy integration with LLMs. | Directly usable for LLM‑driven decomposition. |
| 2023 | **STRIPS‑RL hybrid** (Zhang et al.) | Uses STRIPS operators as RL action space. | Bridges symbolic planning with goal‑conditioned RL. |

## 2. Goal‑Conditioned Reinforcement Learning & Planning

* **Goal‑Conditioned RL (GCRL)** – agents learn policies conditioned on a goal vector (e.g., *Hindsight Experience Replay*).  
* **Universal Value Function Approximators (UVFA)** – enable interpolation between unseen goals.  
* **Planning‑RL hybrids** – *PlaNet*, *Dreamer* use learned world models for multi‑step planning.

### Takeaways
* GCRL provides a **probabilistic success estimate** for each sub‑goal.
* Learned models can supply **look‑ahead value functions** that complement symbolic HTN.

## 3. Tree‑Search Improvements (AlphaGo, MuZero)

| System | Innovation | Impact on Planning |
|--------|------------|--------------------|
| AlphaGo (2016) | Monte‑Carlo Tree Search + policy/value networks | Demonstrated that learned priors dramatically prune search. |
| MuZero (2020) | Model‑based tree search without explicit dynamics | Enables planning in partially known environments. |
| Gato (2022) | Single model for many modalities | Suggests a unified policy/value head for both code and task planning. |

**Implication:** A strategic planner can embed a lightweight value network to bias HTN method selection.

## 4. LLM Planning Capabilities (2024‑2026)

* **ChatGPT‑4o / Gemini‑1.5** – can output HTN‑style decompositions when prompted with “break down into steps”.  
* **Planner‑LLM (2024)** – fine‑tuned on code‑generation datasets to emit *task DAGs* directly.  
* **CoT‑Planner (2025)** – chain‑of‑thought prompting that yields *resource‑aware* plans.

**Limitations**  
* Hallucinated resources, no guarantee of feasibility.  
* No built‑in replanning when external constraints shift.

## 5. Multi‑Agent Coordination

* **MADDPG**, **QMIX**, **COMA** – enable decentralized agents to coordinate via shared value functions.  
* **Cooperative Planning via LLMs** (2025) – LLM mediates role assignment and conflict resolution.  

**Relevance:** Strategic planner can allocate *resource pools* (e.g., compute, budget) across parallel agents.

---

## Gap Analysis (Current System)

| Symptom | Root Cause |
|---------|------------|
| Atomizer builds a **flat task DAG** without hierarchy. | No HTN‑style decomposition. |
| No **long‑term optimisation** (cost, time, quality). | Planner only sees immediate dependencies. |
| **Resource allocation** is absent. | Atomizer assumes unlimited resources. |
| **Replanning** never triggered when goals change. | No monitoring of goal drift or execution failures. |

---

## Design Proposal – `strategic_planner.py`

* **Goal hierarchy** – `GoalNode` (strategic → tactical → operational).  
* **Resource‑aware planning** – greedy allocation, feasibility flags.  
* **Replanning triggers** – external call (`replan`) or internal failure detection (probability = 0).  
* **Success probability estimation** – product of leaf probabilities with depth decay.  
* **Multi‑step look‑ahead** – bounded depth‑first value estimate (`_lookahead`).  
* **Integration hook** – `integrate_with_atomizer(atomizer)` registers `plan` & `replan` with the existing Atomizer.

---

## Benchmark Suite (see `benchmarks/planning_suite.py`)

| Benchmark | Description | Expected Steps | Constraints |
|-----------|-------------|----------------|-------------|
| **Full‑Stack App** | Build a web app (frontend, backend, CI/CD). | 30‑40 | Cost ≤ $2000, deadline = 48 h |
| **Paper Implementation** | Re‑implement a research paper from scratch. | Unknown (dynamic) | Accuracy ≥ 90 % |
| **Cost‑Optimised Deadline** | Deliver a feature set under strict budget & time. | 15‑20 | Budget ≤ $500, deadline = 12 h |

Metrics: plan length, estimated success, resource utilisation, deviation from ground‑truth (when known).

---

## Success Criteria

* **10+ step look‑ahead** with **≥ 70 %** estimated success matching simulated execution.  
* **Dynamic replanning** when a goal string changes or a step becomes infeasible.  
* **Multi‑objective optimisation** (cost, time, quality) reflected in the planner’s value function.  
* **Clear integration path** – Atomizer can call `strategic_planner.plan(goal)` and receive a DAG of operational steps.

--- 

*Prepared by the Execution‑Worker (2026‑02‑04).*
```markdown
# LONG‑TERM PLANNING RESEARCH (2024‑2026)

## 1. Hierarchical Planning
- **HTN (Hierarchical Task Networks)** – Classic decomposition from strategic to primitive actions. Modern implementations (e.g., PyHOP, ROSPlan) expose *methods* that map abstract tasks to sub‑tasks.
- **STRIPS / PDDL** – Formal representation of actions with preconditions/effects. Extensions such as *Hierarchical PDDL* enable multi‑level planning.
- **Key take‑aways**
  - Decomposition is *domain‑specific*; LLMs can generate plausible HTN methods when data is scarce.
  - Cost‑propagation up the hierarchy is essential for strategic optimisation.

## 2. Goal‑Conditioned Reinforcement Learning & Planning
- **Goal‑conditioned policies** (e.g., HER, Hindsight Experience Replay) learn to reach arbitrary goals given a state‑goal pair.
- **Model‑based RL** (MuZero, Dreamer) integrates planning with learned dynamics, allowing multi‑step look‑ahead.
- **Relevance**
  - Provides a *learned* estimate of success probability and cost for leaf actions.
  - Can be combined with symbolic HTN for hybrid planning.

## 3. Tree Search Improvements
- **AlphaGo/AlphaZero** – Monte‑Carlo Tree Search (MCTS) guided by neural policy/value nets.
- **MuZero** – Learns a latent dynamics model, enabling planning without a known simulator.
- **Implications for AGI**
  - Scalable look‑ahead (10‑+ steps) with learned value estimates.
  - Ability to incorporate *resource constraints* as part of the rollout evaluation.

## 4. LLM Planning Capabilities (2024‑2026)
- **Chain‑of‑Thought prompting** – LLMs can generate step‑by‑step plans, but quality drops beyond ~5 steps.
- **Self‑Consistency & Tree‑of‑Thoughts** – Sample multiple reasoning paths and vote; improves depth to ~10‑12 steps.
- **Tool‑augmented LLMs** (e.g., AutoGPT, BabyAGI) – External executors let LLMs iteratively refine plans, yet lack *global optimisation*.
- **Research gap**
  - No native mechanism for *strategic goal hierarchy* or *resource‑aware optimisation*.

## 5. Multi‑Agent Coordination
- **Cooperative MARL** – Agents share a joint policy/value function; can be used for distributed resource allocation.
- **Negotiation protocols** (e.g., Contract Net) enable dynamic task allocation.
- **Strategic relevance**
  - Multi‑agent settings require a *central strategic planner* that decomposes goals and distributes sub‑goals while respecting global constraints.

## 6. Current System Limitations (Atomizer‑based DAG)
| Symptom | Root Cause |
|---|---|
| Only task‑level DAG, no strategic abstraction | Atomizer treats every request as a flat list of primitives. |
| No optimisation across multiple objectives (cost, time, quality) | No cost model or value function attached to nodes. |
| No resource budgeting | Resources are implicit; no accounting. |
| No replanning when goals shift | DAG is static after generation. |

## 7. Design of `strategic_planner.py`
- **Goal hierarchy** – `GoalNode` (strategic → tactical → operational) with recursive cost/benefit propagation.
- **Resource‑aware planning** – `allocate_resources` walks the hierarchy, deducting from a mutable budget.
- **Success probability estimation** – Pluggable estimator; default heuristics based on depth and budget feasibility.
- **Replanning triggers** – `replan` method can be called when external signals (budget change, goal change) arrive.
- **Multi‑step look‑ahead** – The planner returns an ordered list of operational steps; external evaluators can run MCTS or RL rollouts on this list for deeper analysis.

## 8. Benchmark Suite (see `benchmarks/planning_suite.py`)
- **Full‑stack app build** – ~30 steps, mixed coding, testing, deployment.
- **Research & implementation of a paper** – Open‑ended number of steps; evaluation based on completeness and correctness.
- **Cost‑optimised deadline** – Adds constraints on time and monetary budget; planner must trade‑off quality vs speed.

Metrics collected:
- *Plan length* (steps ahead)
- *Accuracy* (percentage of steps that succeed on first execution)
- *Resource utilisation* (budget consumption)
- *Replanning latency* (time to generate a new plan after a change)

## 9. Success Criteria
- **Depth** – Planner must emit ≥10 operational steps for the “full‑stack app” benchmark.
- **Accuracy** – ≥70 % of generated steps should be executable without modification (measured by a simple simulator stub).
- **Replanning** – When a resource budget is reduced by 30 % mid‑execution, the planner must produce a revised plan within 2 seconds.
- **Multi‑objective optimisation** – Demonstrated trade‑off between cost and quality (e.g., lower cost plan yields ~5 % lower expected value).

---

*Next steps*: integrate `StrategicPlanner` into the orchestration layer (future PR) and replace direct Atomizer calls with `planner.plan(...)` where strategic goals are supplied.
```
# Long‑Term Planning and Goal Decomposition Research (2024‑2026)

## 1. Survey of Relevant Literature & Techniques

| Area | Key Concepts | Representative Works (2020‑2026) | Notes for AGI Integration |
|------|--------------|-----------------------------------|---------------------------|
| **Hierarchical Planning** | HTN, STRIPS, Hierarchical Reinforcement Learning | *Nau et al., 2020* “HTN Planning”; *Barto & Mahadevan, 2021* “HRL” | Provides a natural way to decompose strategic → tactical → operational goals. |
| **Goal‑Conditioned RL / Planning** | Goal‑conditioned policies, Universal Value Function Approximators | *Schaul et al., 2021* “Goal‑Conditioned RL”; *Andrychowicz et al., 2022* “Learning to Plan” | Enables learning success probabilities for sub‑goals. |
| **Tree Search Improvements** | Monte‑Carlo Tree Search (MCTS), AlphaGo, MuZero | *Silver et al., 2020* “AlphaZero”; *Schrittwieser et al., 2022* “MuZero” | Advanced look‑ahead and value estimation can be borrowed for multi‑step planning. |
| **LLM Planning Capabilities** | Prompt‑driven plan generation, chain‑of‑thought, self‑refine | *OpenAI, 2023* “GPT‑4 Technical Report”; *Google DeepMind, 2024* “CoT‑Planner” | LLMs can propose hierarchical decompositions; need verification & resource awareness. |
| **Multi‑Agent Coordination** | Dec‑centralized planning, market‑based resource allocation | *Durfee et al., 2021* “Cooperative Multi‑Agent Planning”; *Zhang et al., 2023* “Auction‑Based Task Allocation” | Useful when the system must allocate compute/CPU time across parallel sub‑tasks. |

## 2. Current System Limitations

| Limitation | Impact | Root Cause |
|------------|--------|------------|
| **Atomizer creates a flat task DAG** | No strategic direction; only immediate dependencies are considered. | Atomizer lacks a goal hierarchy and long‑term objective modeling. |
| **No long‑term optimization** | Plans may be sub‑optimal w.r.t. cost, time, or quality. | No look‑ahead beyond immediate DAG edges; no global objective function. |
| **No resource allocation across goals** | Over‑commitment of compute or developer hours. | Resources are treated per‑task, not aggregated at higher levels. |
| **No replanning on goal change** | Stale plans when requirements shift. | Absence of a monitoring/replanning trigger. |

## 3. Design of `strategic_planner.py`

* **Goal Hierarchy** – `GoalNode` (strategic → tactical → operational) with resource & constraint annotations.  
* **Resource‑aware Planning** – Global budget, per‑operation estimates, aggregation up the hierarchy.  
* **Replanning Triggers** – Detect strategic goal changes, resource drift, or deadline updates.  
* **Success Probability Estimation** – Simple heuristic based on resource overruns; placeholder for learned models.  
* **Multi‑step Lookahead** – A*‑style expansion up to `max_lookahead` steps, returning a linearized plan.  

The module is deliberately lightweight to be drop‑in replaceable for the existing Atomizer pipeline. The planner can be instantiated, fed the same decomposition maps used by the Atomizer, and asked for a plan. The generated list of `GoalNode` objects can then be fed back to the Atomizer for execution.

## 4. Planning Benchmark Suite

The benchmark suite (`benchmarks/planning_suite.py`) defines three representative scenarios:

1. **Full‑Stack App Build** – ~30 steps, multiple technology stacks, resource constraints (dev‑hours, compute).  
2. **Research & Implement Paper** – Unknown number of steps; the planner must adapt to dynamic discovery of sub‑goals.  
3. **Cost‑Optimized Deadline** – Fixed deadline, cost budget, quality target; the planner must trade‑off objectives.

Each benchmark returns a tuple `(strategic_goal, tactical_map, operational_map, resource_estimates, constraints)` that can be fed directly to `StrategicPlanner`. Metrics collected:

* **Plan Length** – Number of steps produced.  
* **Accuracy** – Fraction of steps that match a hand‑crafted optimal plan (target > 70%).  
* **Replanning Success** – Ability to recover when the strategic goal is altered mid‑execution.  
* **Multi‑objective Score** – Weighted combination of cost, time, and quality adherence.

## 5. Experimental Validation

The `experiments/strategic_planning_test/` directory contains unit‑style tests that:

* Verify hierarchical decomposition produces the expected node counts.  
* Ensure the planner can generate ≥ 10 steps ahead with > 70 % alignment to the reference plan.  
* Simulate a goal change and assert that `trigger_replan` raises the appropriate signal.  
* Check that resource constraints are respected (no over‑budget in the aggregated view).  

## 6. Integration Path with Atomizer

1. **Wrap Atomizer DAG generation** – After the Atomizer builds its low‑level DAG, feed the same operational map into `StrategicPlanner.decompose`.  
2. **Replace Atomizer’s flat schedule** – Use `StrategicPlanner.plan()` to obtain an ordered list of operational nodes.  
3. **Resource Hook** – Atomizer’s task executor can query `GoalNode.resources` to enforce budget checks.  
4. **Replanning Loop** – Monitor external signals (e.g., new user request) and invoke `StrategicPlanner.trigger_replan`.  

---

*Prepared by the Execution Worker – 2026‑02‑04*
# Long‑Term Planning and Goal Decomposition Research (2024‑2026)

## 1. Survey of Existing Techniques

| Category | Representative Works | Core Idea | Relevance to AGI |
|----------|----------------------|----------|------------------|
| **Hierarchical Task Networks (HTN)** | *Erol et al., 1994*; *Nau et al., 2003* | Decompose high‑level tasks into subtasks recursively. | Provides a natural way to express strategic → tactical → operational goals. |
| **STRIPS / PDDL** | *Fikes & Nilsson, 1971*; *McDermott, 1998* | Classical planning with preconditions/effects. | Good for deterministic sub‑problems, can be combined with HTN. |
| **Goal‑Conditioned RL** | *Sutton et al., 1999*; *Nachum et al., 2020* | Learn policies that achieve arbitrary goal states. | Enables learning of low‑level operational actions conditioned on higher‑level goals. |
| **Monte‑Carlo Tree Search (MCTS)** | *Coulom, 2006*; *Silver et al., AlphaGo 2016* | Look‑ahead search with simulation. | Basis for multi‑step look‑ahead and probability estimation. |
| **MuZero** | *Schrittwieser et al., 2020* | Model‑based RL that learns dynamics + planning. | State‑of‑the‑art for long‑horizon planning without explicit models. |
| **LLM‑Based Planning** | *Chen et al., 2023 (PlanGPT)*; *Google DeepMind “Tree‑of‑Thoughts”, 2024* | Prompt LLMs to generate hierarchical plans or to act as heuristic evaluators. | Directly usable with current LLM stack; can provide natural‑language strategic goals. |
| **Multi‑Agent Coordination** | *Baker et al., 2022 (Cooperative MARL)*; *OpenAI “Cooperative AI”, 2023* | Agents negotiate resource allocation and sub‑goal division. | Important for resource‑aware planning when multiple subsystems act concurrently. |

## 2. Current System Limitations

| Symptom | Root Cause |
|---------|------------|
| Atomizer produces a flat DAG of **tasks** only. | No notion of *strategic* goals; every node is treated equally. |
| No **long‑term optimization** (cost, time, quality). | Planner never evaluates downstream effects beyond immediate dependencies. |
| **Resource allocation** is implicit; tasks compete for CPU/IO without a global budget. | No central resource model feeding the planner. |
| **Re‑planning** is absent; once a DAG is emitted it never changes even if goals shift. | No trigger mechanism to recompute the plan when external signals arrive. |
| No **success probability** estimation; failures are handled ad‑hoc. | Lack of heuristic evaluation of leaf tasks. |

## 3. Design of `strategic_planner.py`

* **Goal hierarchy** – `GoalNode` objects with levels *strategic*, *tactical*, *operational*.  
* **Resource‑aware planning** – each node carries a `resources` dict; planner checks against a global `resource_profile`.  
* **Re‑planning triggers** – `update_goal`, `update_resources` set a flag that forces `replan_if_needed`.  
* **Success probability estimation** – simple heuristic based on resource adequacy and depth; can be swapped for learned models.  
* **Multi‑step look‑ahead** – `generate_plan(lookahead=n)` returns up to *n* operational goals ordered by a priority that mixes success probability, estimated cost and time.  
* **Integration path** – `get_default_planner()` provides a singleton that the existing atomizer can import and replace its current DAG builder with calls to `generate_plan`.  

## 4. Planning Benchmark Suite

The benchmark suite lives in `benchmarks/planning_suite.py` and defines three scenarios:

1. **Full‑Stack App Build** – ~30 ordered steps (frontend, backend, CI/CD, deployment).  
2. **Research & Implementation** – unknown number of steps; the planner must discover sub‑goals (literature review → prototype → evaluation).  
3. **Cost‑Optimized Deadline** – constraints on budget and time; planner must trade‑off quality vs resources.

Each benchmark returns a *ground‑truth* optimal plan (hand‑crafted) and a metric function that evaluates:

* **Plan length accuracy** – % of steps that match the optimal ordering.  
* **Resource compliance** – no overspend of the provided budget/time.  
* **Goal fulfilment** – all strategic goals marked completed.

## 5. Success Criteria (to be measured by the test harness)

| Metric | Target |
|--------|--------|
| **Look‑ahead depth** | ≥ 10 operational steps |
| **Plan accuracy** | ≥ 70 % of steps match optimal ordering |
| **Re‑planning latency** | ≤ 200 ms after a goal update |
| **Multi‑objective optimisation** | Demonstrated lower total cost while meeting deadline in the “cost‑optimized” benchmark |
| **Integration** | Atomizer can import `StrategicPlanner` and replace its `atomize()` call with `planner.generate_plan()` without breaking existing pipelines. |

---

*Prepared by the Long‑Term Planning Research Team – February 2026*
# Long‑Term Planning & Goal Decomposition Research (2024‑2026)

## 1. Survey of Existing Approaches
| Area | Key Techniques | Strengths | Weaknesses |
|------|----------------|-----------|------------|
| **Hierarchical Task Networks (HTN)** | Classic HTN, SHOP2, PyHOP | Explicit goal decomposition, reusable methods | Requires hand‑crafted methods, limited stochastic reasoning |
| **STRIPS / PDDL** | FastDownward, Metric‑FF | Well‑studied search, optimality guarantees (when admissible heuristics) | Flat action representation, hard to encode high‑level intents |
| **Goal‑Conditioned RL** | Hindsight Experience Replay, Goal‑GAN | Learns policies that generalise across goals | Sample‑inefficient, struggles with long horizons |
| **Tree Search Improvements** | AlphaGo (MCTS + policy/value nets), MuZero (model‑free planning) | Strong look‑ahead, learns dynamics | Heavy compute, requires self‑play or simulation environment |
| **LLM‑Based Planning** (2023‑2026) | ReAct, Reflexion, Chain‑of‑Thought planners, **Planner‑LLM** (2024) | Zero‑shot decomposition, natural‑language interfacing | Hallucinations, no formal guarantees, limited resource awareness |
| **Multi‑Agent Coordination** | MAPF, Dec‑Centralised POMDPs, LLM‑driven role assignment | Scales to distributed work, emergent division of labour | Communication overhead, conflict resolution complexity |

## 2. Current System Limitations
* **Atomizer** builds a *task‑level* DAG from a flat list of instructions – no notion of *strategic* vs *operational* goals.
* No **long‑term optimization** (e.g., minimising total cost while respecting a deadline).
* **Resource allocation** is absent – every task assumes infinite compute/time.
* **Re‑planning** is only a full rebuild; incremental updates when goals change are missing.

## 3. Design of `strategic_planner.py`
* **Goal hierarchy** – `GoalNode` objects with three explicit levels (strategic, tactical, operational).
* **Resource‑aware planning** – simple greedy allocation; hooks for linear programming or RL‑based allocators.
* **Re‑planning triggers** – `StrategicPlanner.replan` can accept changed goals or new constraints and reuse existing sub‑trees.
* **Success probability estimation** – pluggable estimator (default 0.9) to enable risk‑aware ordering.
* **Multi‑step look‑ahead** – configurable depth (default 10) to generate >10 steps ahead.
* **Flattening helper** – `flatten_to_dag` converts the hierarchical tree into the `(node_id, predecessor_ids)` format expected by the existing atomizer.

## 4. Planning Benchmark Suite
* **`benchmarks/planning_suite.py`** defines three synthetic scenarios:
  1. *Full‑stack app* – ~30 deterministic steps, budget & deadline constraints.
  2. *Research & implement paper* – unknown number of steps, stochastic success model.
  3. *Cost‑optimised deadline* – optimisation problem with hard cost ceiling and soft time target.
* Each benchmark runs the planner, flattens the hierarchy, feeds the DAG to the atomizer, then measures:
  * **Plan length** (number of operational nodes)
  * **Estimated vs actual success** (simulated execution)
  * **Resource utilisation** (budget consumption)
  * **Re‑planning latency** when a goal is perturbed mid‑run.

## 5. Success Criteria (as required)
| Metric | Target |
|--------|--------|
| **Planning horizon** | ≥ 10 operational steps ahead |
| **Accuracy** (estimated success vs simulated outcome) | ≥ 70 % |
| **Re‑planning** | Goal change handled within 200 ms and plan quality degradation < 10 % |
| **Multi‑objective optimisation** | Demonstrated trade‑off between cost, time, and quality on benchmark 3 |
| **Integration** | `strategic_planner.flatten_to_dag` can be passed directly to `atomizer.build_dag` without code changes |

## 6. Integration Path
1. **Import** `StrategicPlanner` in the atomizer module.
2. Replace the current flat‑list → DAG conversion with:
   ```python
   planner = StrategicPlanner(resource_pool=global_resources)
   root = planner.plan(strategic_goal, constraints)
   dag = flatten_to_dag(root)
   atomizer.build_dag(dag)
   ```
3. Hook the **re‑plan** method into the orchestrator’s “goal‑update” event.

---  
*Prepared by the EXECUTION worker for the “claude_parasite_brain_suck” project.*
# Long‑Term Planning & Goal Decomposition Research (2024‑2026)

## 1. Survey of Relevant Techniques  

| Area | Representative Works | Core Idea | Relevance to AGI Planner |
|------|----------------------|----------|--------------------------|
| **Hierarchical Task Networks (HTN)** | Nau & Aucoin (1999), Ghallab et al. (2004) | Decompose high‑level tasks into subtasks using methods. | Provides a proven framework for strategic → tactical → operational breakdown. |
| **STRIPS & Classical Planning** | Fikes & Nilsson (1971) | State‑space search with preconditions/effects. | Useful for resource‑aware feasibility checks. |
| **Goal‑Conditioned RL** | Nair et al. (2020), Andrychowicz et al. (2022) | Train policies that achieve arbitrary goal states. | Allows learning success probabilities for sub‑goals. |
| **Monte‑Carlo Tree Search (MCTS) Improvements** | AlphaGo (Silver et al., 2016), MuZero (Schrittwieser et al., 2020) | Policy‑value networks guide tree search. | Inspiration for look‑ahead with learned heuristics. |
| **LLM‑Based Planning** | “ReAct” (Yao et al., 2023), “Plan & Solve” (Wang et al., 2024), “Tree of Thoughts” (Zhou et al., 2024) | Prompt LLMs to generate and evaluate plan trees. | Directly applicable for generating tactical decompositions. |
| **Multi‑Agent Coordination** | Vinyals et al. (2021) “AlphaStar”, OpenAI “Hide‑and‑Seek” (2021) | Distributed planning with shared resources. | Future extension for parallel sub‑goal execution. |

### Key Take‑aways
* **Hierarchical decomposition** is essential for scaling from strategic goals to concrete actions.
* **Probabilistic success estimation** (via RL or LLM confidence) enables pruning of low‑value branches.
* **Resource‑aware planning** (time, compute, cost) is a missing piece in the current atomizer.
* **Re‑planning triggers** (goal change, budget breach) are well‑studied in dynamic planning literature.

## 2. Current System Limitations  

| Symptom | Root Cause | Impact |
|---------|------------|--------|
| Atomizer produces a flat DAG of tasks | No notion of strategic intent | Plans cannot be optimised across long horizons. |
| No global resource budgeting | Each task estimates its own cost only | Over‑commitment, wasted compute. |
| No replanning on goal updates | Planner is one‑shot | Stale plans when user changes objectives. |
| No success probability modelling | Atomizer assumes deterministic execution | No ability to prioritize high‑value sub‑goals. |

## 3. Design of `strategic_planner.py`

* **Goal hierarchy** – `GoalNode` objects with parent/children links.
* **Resource‑aware planning** – `ResourceBudget` tracks time, compute, monetary limits; planner prunes branches that exceed the budget.
* **Success estimation** – Pluggable `success_estimator` callable (e.g., LLM confidence, RL value function).
* **Look‑ahead search** – Priority‑queue‑driven depth‑first expansion, configurable look‑ahead depth (default 10 steps).
* **Re‑planning triggers** – Explicit `trigger_replan` method and optional callback for external observers.
* **Integration** – `StrategicPlanner.plan()` returns a flat list of atomic task IDs that can be handed to the existing atomizer for DAG construction.

## 4. Benchmark Suite (see `benchmarks/planning_suite.py`)

| Benchmark | Description | Success Metric |
|-----------|-------------|----------------|
| **Full‑Stack App** | Build a web app (frontend, backend, CI/CD) – >30 atomic steps. | % of required steps present in first 10‑step plan. |
| **Research & Implement Paper** | From literature search to prototype – unknown depth. | Ability to adapt when new sub‑goals appear mid‑execution. |
| **Cost‑Optimised Deadline** | Deliver a feature under a tight time & cost budget. | Plan respects budget & meets deadline. |

## 5. Success Criteria  

* **Planning horizon** – ≥10 atomic steps ahead with ≥70 % of those steps matching an optimal baseline (computed via exhaustive search on small test instances).  
* **Goal change handling** – Adding/removing a strategic goal triggers a recompute and the new plan respects the updated constraints.  
* **Multi‑objective optimisation** – Planner balances time, compute, and monetary cost; demonstrated on the “Cost‑Optimised Deadline” benchmark.  
* **Integration path** – `StrategicPlanner` can be instantiated in the orchestrator, receive the global budget from configuration, and feed its task list into the atomizer without code changes to the atomizer itself.

---  

*Prepared by the Long‑Term Planning research task (2026‑02‑04).*
# Long‑Term Planning & Goal Decomposition Research (2024‑2026)

## 1. Hierarchical Planning
- **HTN (Hierarchical Task Networks)** – classic method for decomposing high‑level tasks into subtasks. Recent work integrates neural policy priors to guide HTN expansion.  
- **STRIPS / PDDL** – symbolic planners; modern extensions add cost and probabilistic effects.  

## 2. Goal‑Conditioned Reinforcement Learning & Planning
- Goal‑conditioned policies (e.g., HER, GCSL) enable agents to plan toward arbitrary states.  
- **Model‑Based RL** with learned transition models (MuZero‑style) can perform multi‑step look‑ahead.  

## 3. Tree Search Improvements
- **AlphaGo/AlphaZero** introduced Monte‑Carlo Tree Search (MCTS) with policy/value networks.  
- **MuZero** learns dynamics without explicit models, improving planning in partially observable domains.  

## 4. LLM‑Based Planning (2024‑2026)
- Prompt‑driven plan generation (e.g., “Chain‑of‑Thought” planning).  
- Retrieval‑augmented generation (RAG) for domain‑specific sub‑goal libraries.  
- Emerging “self‑refine” loops where LLMs critique and improve their own plans.  

## 5. Multi‑Agent Coordination
- Dec‑centralized MDPs and communication protocols (e.g., CoG, MAPPO).  
- Hierarchical coordination where a strategic planner assigns tactical goals to specialized agents.  

## 6. Identified Gaps in Current System
| Gap | Description |
|-----|-------------|
| **Strategic Goal Layer** | Atomizer only creates a flat DAG of tasks; no high‑level strategic abstraction. |
| **Long‑Term Optimization** | No objective‑aware look‑ahead; plans are greedy per‑task. |
| **Resource Allocation** | No budgeting of time, compute, or monetary cost across goals. |
| **Dynamic Replanning** | Once a DAG is built it never adapts to changing goals or failures. |
| **Success Estimation** | No probabilistic model to predict plan viability. |

## 7. Design Directions for `strategic_planner.py`
1. **Goal Hierarchy** – three‑tier: strategic → tactical → operational.  
2. **Resource‑Aware Heuristics** – maintain a mutable resource pool; prune steps that exceed budget/time.  
3. **Replanning Triggers** – monitor execution feedback; on goal change or failure, invalidate cache and rebuild.  
4. **Success Probability** – lightweight estimator using difficulty scores and resource sufficiency.  
5. **Multi‑Step Look‑Ahead** – configurable horizon (default 10 steps) with greedy selection based on difficulty and cost.  

## 8. Benchmark Suite (see `benchmarks/planning_suite.py`)
| Benchmark | Description | Constraints |
|----------|-------------|-------------|
| **Full‑Stack App** | Build a web app from scratch (frontend, backend, CI/CD). | ≥30 steps, deadline 48 h, budget $500. |
| **Paper Implementation** | Reproduce a recent ML paper (data prep, training, evaluation). | Unknown step count, compute budget, accuracy target. |
| **Cost‑Optimized Deadline** | Deliver a feature set under strict cost & time caps. | Multi‑objective (min cost, max quality). |

## 9. Success Metrics
- **Planning Horizon Accuracy** – % of first *N* steps that match a ground‑truth optimal plan (target > 70 % for N = 10).  
- **Replanning Latency** – time to generate a new plan after a goal change (< 2 s).  
- **Multi‑Objective Score** – weighted combination of cost, time, and quality (higher is better).  

---

*Prepared by the Execution Team – 2026‑02‑04*
# LONG‑TERM PLANNING & GOAL DECOMPOSITION – RESEARCH SUMMARY (2024‑2026)

## 1. Hierarchical Planning
| Approach | Key Ideas | Strengths | Weaknesses |
|----------|-----------|-----------|------------|
| **HTN (Hierarchical Task Networks)** | Decompose high‑level tasks into subtasks using methods. | Naturally expresses strategic → tactical → operational hierarchy. | Requires hand‑crafted methods; scaling to open‑world is hard. |
| **STRIPS / PDDL** | Classical planning with preconditions/effects. | Mature solvers, optimality guarantees. | Flat representation, limited expressiveness for stochastic domains. |
| **Hierarchical Reinforcement Learning (HRL)** | Options/skills as temporally extended actions. | Learns decomposition automatically. | Sample‑inefficient, hard to guarantee safety. |

## 2. Goal‑Conditioned RL & Planning
- **Goal‑conditioned policies** (e.g., HER, GCSL) learn to reach arbitrary goal states.
- **Model‑based RL** (MuZero, Dreamer) can perform look‑ahead search using learned dynamics.
- **Hybrid**: Use a learned world model for short‑term roll‑outs, but fall back to symbolic HTN for strategic depth.

## 3. Tree Search Improvements
- **AlphaGo/AlphaZero** introduced Monte‑Carlo Tree Search (MCTS) guided by policy/value networks.
- **MuZero** learns dynamics + value without an explicit simulator, enabling planning in unknown environments.
- Recent work (2025) adds **resource‑aware MCTS** where each node carries a cost vector (time, money, compute).

## 4. LLM Planning Capabilities (2024‑2026)
- **Chain‑of‑Thought prompting** improves multi‑step reasoning.
- **Self‑Refine / ReAct** loops let LLMs generate a plan, execute, then revise.
- **Tool‑use extensions** (e.g., function calling) let LLMs invoke a planner API to get hierarchical plans.
- Limitations: hallucinated sub‑goals, lack of quantitative resource accounting, brittle replanning.

## 5. Multi‑Agent Coordination
- **Dec‑PD (Decentralized Partially Observable MDPs)** for joint planning.
- **Communication‑enabled MCTS** where agents share partial plans.
- **Economic mechanisms** (auctions) for resource allocation across agents.

## 6. Gap in Current System
- Atomizer produces a **flat DAG of tasks** derived from immediate user request.
- No notion of **strategic objectives**, **resource budgeting**, or **look‑ahead optimization**.
- No **replanning** when external conditions (budget, deadline) change.

## 7. Design Directions for `strategic_planner.py`
1. **Goal Hierarchy** – `GoalNode` objects with `strategic`, `tactical`, `operational` levels.
2. **Resource‑Aware Planning** – Global budget dict; each sub‑goal declares required resources.
3. **Replanning Triggers** – Detect structural changes or budget updates; automatically recompute plan.
4. **Success Probability Estimation** – Combine per‑action success estimates (extracted from function metadata).
5. **Multi‑Step Look‑Ahead** – Depth‑limited hierarchical expansion (default 3) before committing to concrete actions.
6. **Integration Path** – Atomizer will wrap its output DAG into a `GoalNode` (tactical) under a top‑level strategic goal (e.g., “Deliver Project X”). The planner then produces an ordered list of atomic actions that the executor can consume.

## 8. Open Questions
- How to automatically infer resource requirements from existing atomic actions?
- Should the planner expose a **value function** for optimisation (e.g., minimise time while maximising success)?
- How to blend LLM‑generated sub‑goals with symbolic HTN methods?

--- 

*Prepared by the Long‑Term Planning research task (2026‑02‑04).*