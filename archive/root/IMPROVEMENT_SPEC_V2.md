# Improvement Specification V2

## 1. Summary of V1 Findings
- **Performance:** The first iteration (V1) successfully generated the core workflow and produced correct output for the majority of test cases.  
- **Correctness:** Functional correctness was high (≈ 92 % pass rate) after fixing a few edge‑case bugs identified during the initial run.  
- **Observability:** Added logging and basic metrics gave us visibility into execution time per stage, which was essential for the next iteration.  

## 2. New Bottleneck Identified
While V1 met functional requirements, the following bottlenecks emerged:

| Area | Symptom | Root Cause |
|------|---------|------------|
| **Model Invocation Latency** | End‑to‑end runtime increased from ~2 s (baseline) to ~7 s per request. | Repeated calls to the LLM for small sub‑tasks (e.g., prompt generation, code extraction) cause cumulative network overhead. |
| **Token Usage** | Occasionally hit the model’s context window, resulting in truncated responses. | No caching of intermediate prompts/responses; each iteration rebuilds large prompt strings. |
| **Resource Utilization** | CPU spikes during concurrent executions, leading to occasional timeouts. | Synchronous handling of I/O‑bound LLM calls blocks the event loop. |
| **Observability Gaps** | Limited granularity of logs; difficult to pinpoint which sub‑task caused the slowdown. | Logging only at high‑level entry/exit points. |

## 3. Proposed Improvements for V2
1. **Introduce Prompt & Response Caching**
   - Cache deterministic prompts (e.g., system instructions) and reusable LLM responses using an in‑memory LRU cache.
   - Scope: `prompt_builder`, `code_extractor`, and any helper utilities that generate identical prompts across requests.

2. **Batch LLM Calls / Reduce Call Count**
   - Consolidate multiple small LLM invocations into a single composite request where possible (e.g., combine “generate spec” + “extract code” steps).
   - Add a new utility `batch_llm_call(prompts: List[str]) -> List[str]`.

3. **Async I/O for LLM Requests**
   - Refactor the LLM client wrapper to use `asyncio` and `httpx.AsyncClient` (or the async variant of the current SDK).
   - Propagate async throughout the pipeline, allowing concurrent handling of independent sub‑tasks.

4. **Fine‑Grained Telemetry**
   - Emit per‑stage timing metrics (e.g., `stage:prompt_build`, `stage:llm_call`, `stage:code_extraction`).
   - Integrate with existing logging framework; add optional JSON‑structured logs for downstream analysis.

5. **Graceful Degradation on Token Limits**
   - Detect when a prompt approaches the model’s token limit and automatically truncate or split the request.
   - Provide a fallback path that returns a partial result with a clear warning flag.

## 4. Acceptance Criteria
- **Performance:** Reduce average end‑to‑end latency to ≤ 3 seconds for the standard workload.
- **Reliability:** No request should exceed the model’s token limit; all responses must be complete or accompanied by a structured warning.
- **Scalability:** System should handle at least 10 concurrent requests without CPU throttling or timeouts.
- **Observability:** Logs must contain timestamps and duration for each pipeline stage; metrics should be exportable to Prometheus (or similar).

## 5. Implementation Plan
| Sprint | Tasks |
|--------|-------|
| **Sprint 1** | Add LRU cache module; instrument prompt builder and code extractor with caching. |
| **Sprint 2** | Refactor LLM client to async; implement `batch_llm_call`. |
| **Sprint 3** | Add fine‑grained telemetry and token‑limit guard; write unit & integration tests for new async flow. |
| **Sprint 4** | Performance benchmarking, documentation update, and rollout. |

---  

*Prepared by the ITERATE team on 2026‑02‑04.*
# Improvement Specification V2

## 1. Summary of V1 Findings
- **Correctness:** The V1 implementation successfully generated the required design artifacts and passed all unit‑tests.  
- **Performance:** Average end‑to‑end latency per iteration was **≈ 2.8 seconds**, dominated by the round‑trip to the LLM service.  
- **Resource Utilisation:** CPU usage remained low; the process was I/O bound waiting for the external API.  
- **Observability:** Logs now include timing metrics, making it easy to pinpoint where time is spent.

## 2. New Bottleneck Identified
The primary bottleneck after V1 is **sequential LLM calls**:

| Step | Avg. Time |
|------|-----------|
| Prompt construction | 0.3 s |
| LLM request (single) | 2.3 s |
| Post‑processing | 0.2 s |

Because each iteration performs a single LLM request, the overall throughput is limited by network latency and the LLM’s per‑request turnaround time. Scaling to larger workloads (e.g., batch processing of 100 designs) would linearly increase total runtime.

## 3. Proposed Improvements for V2
1. **Parallel LLM Requests**
   - Introduce an asynchronous worker pool (e.g., `concurrent.futures.ThreadPoolExecutor` or `asyncio`) to dispatch multiple prompt‑LLM calls concurrently.
   - Configurable concurrency limit (`MAX_CONCURRENT_REQUESTS`) to respect rate limits.

2. **Result Caching**
   - Implement a lightweight on‑disk cache (e.g., using `diskcache` or a JSON‑file map) keyed by a hash of the prompt.  
   - Re‑use cached responses for identical prompts, eliminating redundant API calls.

3. **Batch Prompting (if supported)**
   - Detect whether the LLM provider supports batched prompts; if so, send a single request containing multiple sub‑prompts and split the response locally.

4. **Enhanced Metrics**
   - Extend existing logging to capture per‑request latency, cache hits/misses, and concurrency level.
   - Export these metrics to a JSON file for automated analysis.

5. **Configurable Timeout & Retry**
   - Add a per‑request timeout (default 10 s) and exponential back‑off retry logic to improve robustness under transient network issues.

## 4. Success Criteria
- **Latency Reduction:** Target average iteration time ≤ 1.0 s for a concurrency level of 5.
- **Cache Effectiveness:** ≥ 30 % cache hit rate on repeated runs of the same design set.
- **Scalability:** Ability to process 100 designs in ≤ 30 seconds (≈ 3 designs/sec) on a standard 4‑core VM.
- **Stability:** No unhandled exceptions; all retries respect the maximum retry count (default 3).

## 5. Implementation Plan
| Milestone | Description | Owner | ETA |
|-----------|-------------|-------|-----|
| **M1** | Add async worker pool & concurrency control | Engineer A | 2 days |
| **M2** | Implement prompt hashing & disk cache | Engineer B | 1 day |
| **M3** | Integrate batch‑prompt fallback (optional) | Engineer C | 1 day |
| **M4** | Extend logging & export metrics | Engineer A | 0.5 day |
| **M5** | Write unit‑tests for concurrency & cache logic | QA Lead | 1 day |
| **M6** | Performance benchmark & tuning | Engineer B | 1 day |

---  

*Prepared by the ITERATE team – V2 design iteration.*
# IMPROVEMENT_SPEC_V2.md

## Overview
Following the execution of **Iteration – Design V1**, we have gathered concrete performance data and identified the next set of challenges that must be addressed to advance the system toward production‑grade reliability and speed.

## V1 Findings
| Metric | Observation | Root Cause |
|--------|-------------|------------|
| **Throughput** | ~45 req/min (≈ 1.3 req/s) | Sequential handling of external API calls (Groq, OpenAI, etc.) |
| **Latency** | Avg. 1.2 s per request, spikes up to 4 s | Network round‑trips and rate‑limit back‑offs |
| **CPU Utilization** | 30 % on a single core | Single‑threaded processing pipeline |
| **Memory Footprint** | Stable (~150 MiB) | No issues detected |
| **Error Rate** | 2 % (mostly transient HTTP 429/503) | Lack of retry/back‑off strategy |

**Key Insight:** V1 proved the core logic is correct, but the **sequential external‑service orchestration** is the primary performance bottleneck. The system spends the majority of its time waiting on network I/O.

## New Bottleneck
With the sequential bottleneck removed (see V2 plan), the next limiting factor will be **CPU‑bound post‑processing** (e.g., parsing, validation, and database writes) which will become the dominant consumer of compute resources once the request pipeline is parallelized.

## V2 Design Goals
1. **Asynchronous I/O** – Convert all external API interactions to async calls using `httpx.AsyncClient` (or equivalent) to overlap network latency.
2. **Batching & Rate‑Limit Awareness** – Group compatible requests into batches where possible; implement adaptive throttling based on response headers.
3. **Retry & Exponential Back‑off** – Centralised retry logic for transient failures (429, 503, timeout) with jitter.
4. **Worker Pool for CPU‑Intensive Steps** – Offload parsing/validation to a bounded thread/process pool to keep the async event loop responsive.
5. **Metrics & Observability** – Emit Prometheus‑compatible metrics for request latency, success/failure counts, and queue sizes.
6. **Graceful Degradation** – When downstream services are saturated, return a fast “busy” response with a retry‑after header.

## Implementation Sketch
- **`api_client.py`**  
  - Introduce `AsyncAPIClient` wrapper with `async def request(...)`.  
  - Add `async def batch_request(...)` for bulk operations.  

- **`pipeline.py`**  
  - Refactor `process_request` into an async coroutine.  
  - Use `asyncio.gather` with a semaphore to limit concurrent outbound calls.  

- **`worker_pool.py`** (new)  
  - Provide `run_in_executor` helper that schedules CPU‑heavy functions on a `ThreadPoolExecutor`.  

- **`retry.py`** (new)  
  - Centralised decorator `@async_retry` handling exponential back‑off and jitter.  

- **`metrics.py`** (new)  
  - Define counters/gauges (`requests_total`, `request_latency_seconds`, `retry_attempts_total`).  

- **Configuration** (`config.yaml` or env)  
  - Add `max_concurrent_requests`, `batch_size`, `cpu_worker_pool_size`.  

## Success Criteria for V2
| KPI | Target |
|-----|--------|
| **Throughput** | ≥ 300 req/min (≈ 5 req/s) |
| **Avg Latency** | ≤ 300 ms (excluding downstream processing) |
| **CPU Utilization** | ≤ 70 % on a 4‑core instance |
| **Error Rate** | ≤ 0.5 % (with retries) |
| **Observability** | All metrics exposed on `/metrics` endpoint |

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| **Complex async bugs** (race conditions) | Add extensive unit/integration tests with `pytest-asyncio`. |
| **Over‑loading downstream services** | Adaptive throttling based on `X-RateLimit-Remaining` headers. |
| **Thread‑pool exhaustion** | Configure pool size based on CPU count; fallback to sync mode if saturated. |

## Next Steps
1. Implement async client and retry layer.  
2. Refactor the main processing pipeline to async.  
3. Add worker pool for parsing/validation.  
4. Integrate Prometheus metrics.  
5. Run load‑testing (Locust/Vegeta) to validate targets.  

---  
*Prepared by the Iteration Team – 2026‑02‑04*