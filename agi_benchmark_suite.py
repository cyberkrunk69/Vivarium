import json
import os
import datetime
from benchmarks.agi.novel_reasoning import run_novel_reasoning
from benchmarks.agi.transfer_learning import run_transfer_learning
from benchmarks.agi.planning import run_planning
from benchmarks.agi.meta_learning import run_meta_learning

RESULTS_PATH = "agi_benchmark_results.json"
REPORT_PATH = "AGI_BASELINE_REPORT.md"

def aggregate_scores():
    """
    Run all benchmark components, compute a simple aggregate score,
    and persist results to JSON.
    """
    results = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "novel_reasoning": run_novel_reasoning(),
        "transfer_learning": run_transfer_learning(),
        "planning": run_planning(),
        "meta_learning": run_meta_learning()
    }

    # Simple aggregate: average of normalized sub‑scores
    def normalize_reasoning(res):
        return sum(res.values()) / len(res)  # pass rate

    def normalize_transfer(res):
        return sum(res.values()) / len(res)  # already 0‑1

    def normalize_planning(res):
        return sum(res.values()) / (len(res) * 100)  # convert to 0‑1

    def normalize_meta(res):
        # lower steps is better; map 1‑5 to 1‑0
        return sum((5 - v) / 4 for v in res.values()) / len(res)

    agg = {
        "novel_reasoning": normalize_reasoning(results["novel_reasoning"]),
        "transfer_learning": normalize_transfer(results["transfer_learning"]),
        "planning": normalize_planning(results["planning"]),
        "meta_learning": normalize_meta(results["meta_learning"])
    }
    results["aggregate_score"] = round(sum(agg.values()) / len(agg), 3)

    # Persist
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    return results

def generate_report(results):
    """
    Produce a markdown baseline report summarizing the latest run.
    """
    lines = [
        "# AGI Benchmark Baseline Report",
        "",
        f"**Run timestamp:** {results['timestamp']}",
        "",
        "## Sub‑benchmark scores",
        ""
    ]

    # Novel reasoning
    nr_pass = sum(results["novel_reasoning"].values())
    nr_total = len(results["novel_reasoning"])
    lines.append(f"- **Novel Reasoning:** {nr_pass}/{nr_total} passed ({nr_pass/nr_total:.0%})")

    # Transfer learning
    tl_avg = sum(results["transfer_learning"].values()) / len(results["transfer_learning"])
    lines.append(f"- **Transfer Learning:** average score {tl_avg:.2f}")

    # Planning
    pl_avg = sum(results["planning"].values()) / (len(results["planning"]) * 100)
    lines.append(f"- **Planning:** average success {pl_avg:.0%}")

    # Meta‑learning
    ml_avg = sum((5 - v) / 4 for v in results["meta_learning"].values()) / len(results["meta_learning"])
    lines.append(f"- **Meta‑Learning:** adaptation efficiency {ml_avg:.0%}")

    # Aggregate
    lines.append("")
    lines.append(f"**Overall Aggregate Score:** {results['aggregate_score']:.3f}")
    lines.append("")
    lines.append("## AGI‑level Threshold")
    lines.append("")
    lines.append("- An **AGI‑achieved** system is defined as having an aggregate score ≥ **0.85**.")
    lines.append("- Current baseline is shown above; gaps are the difference to the threshold.")
    content = "\n".join(lines)

    with open(REPORT_PATH, "w") as f:
        f.write(content)

def main():
    results = aggregate_scores()
    generate_report(results)
    print(f"Benchmark completed. Aggregate score: {results['aggregate_score']:.3f}")
    print(f"Report written to {REPORT_PATH}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
AGI Benchmark Suite
Runs a collection of synthetic AGI capability tests and aggregates scores.
"""

import time
import json
from pathlib import Path

# Import benchmark modules
from benchmarks.agi.novel_reasoning import run_novel_reasoning
from benchmarks.agi.transfer_learning import run_transfer_learning
from benchmarks.agi.planning import run_planning
from benchmarks.agi.meta_learning import run_meta_learning

# Threshold for AGI‑level performance (0.0 – 1.0)
AGI_THRESHOLD = 0.90

REPORT_PATH = Path(__file__).parent / "AGI_BASELINE_REPORT.md"


def aggregate_scores(*score_dicts):
    """Combine score dictionaries, compute average."""
    all_scores = {}
    for d in score_dicts:
        all_scores.update(d)
    avg_score = sum(all_scores.values()) / len(all_scores) if all_scores else 0.0
    return all_scores, avg_score


def write_report(scores, avg_score, elapsed):
    """Write a markdown report summarising the baseline run."""
    status = "AGI Achieved ✅" if avg_score >= AGI_THRESHOLD else "AGI Not Yet Achieved ❌"
    report = f"""# AGI Benchmark Baseline Report

**Run timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Total runtime:** {elapsed:.2f} seconds  
**Average score:** {avg_score:.3f}  
**AGI threshold:** {AGI_THRESHOLD:.2f}  

**Overall status:** {status}

## Detailed Scores
| Test | Score |
|------|-------|
"""
    for name, score in scores.items():
        report += f"| {name} | {score:.3f} |\n"

    REPORT_PATH.write_text(report)
    print(f"Baseline report written to {REPORT_PATH}")


def main():
    start = time.time()

    # Run each benchmark category
    reasoning_scores = run_novel_reasoning()
    transfer_scores = run_transfer_learning()
    planning_scores = run_planning()
    meta_scores = run_meta_learning()

    # Aggregate
    all_scores, avg_score = aggregate_scores(
        reasoning_scores, transfer_scores, planning_scores, meta_scores
    )

    elapsed = time.time() - start
    write_report(all_scores, avg_score, elapsed)

    # Simple console summary
    print(f"Average score: {avg_score:.3f}")
    print(f"AGI threshold: {AGI_THRESHOLD:.2f}")
    print("AGI achieved!" if avg_score >= AGI_THRESHOLD else "AGI not yet achieved.")


if __name__ == "__main__":
    main()
import json
import time
import os
from datetime import datetime
from benchmarks.agi.novel_reasoning import run_novel_reasoning_tests
from benchmarks.agi.transfer_learning import run_transfer_learning_tests
from benchmarks.agi.planning import run_planning_tests
from benchmarks.agi.meta_learning import run_meta_learning_tests

# Directory to store benchmark history
HISTORY_FILE = "benchmark_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

class BenchmarkSuite:
    def __init__(self):
        self.results = {}
        self.start_time = None

    def _run_section(self, name, func):
        start = time.time()
        score, details = func()
        elapsed = time.time() - start
        self.results[name] = {
            "score": score,
            "details": details,
            "time_seconds": elapsed
        }

    def run_all(self):
        self.start_time = datetime.utcnow().isoformat()
        self._run_section("novel_reasoning", run_novel_reasoning_tests)
        self._run_section("transfer_learning", run_transfer_learning_tests)
        self._run_section("planning", run_planning_tests)
        self._run_section("meta_learning", run_meta_learning_tests)

        total_score = sum(r["score"] for r in self.results.values())
        self.results["total_score"] = total_score

        # Save to history for tracking
        save_history({
            "timestamp": self.start_time,
            "results": self.results
        })

        return self.results

def main():
    suite = BenchmarkSuite()
    results = suite.run_all()
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
import json
import os
import datetime
from benchmarks.agi.novel_reasoning import run_novel_reasoning
from benchmarks.agi.transfer_learning import run_transfer_learning
from benchmarks.agi.planning import run_planning
from benchmarks.agi.meta_learning import run_meta_learning

PROGRESS_FILE = "agi_progress.json"
BASELINE_REPORT = "AGI_BASELINE_REPORT.md"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"runs": []}

def save_progress(entry):
    data = load_progress()
    data["runs"].append(entry)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_report(scores, timestamp):
    lines = [
        f"# AGI Benchmark Baseline Report",
        f"**Timestamp:** {timestamp}",
        "",
        "## Scores",
        ""
    ]
    for category, result in scores.items():
        lines.append(f"### {category}")
        for test_name, value in result.items():
            lines.append(f"- **{test_name}:** {value}")
        lines.append("")
    lines.append("## AGI‑Level Threshold")
    lines.append("- A system is considered **AGI‑achieved** when the average score across all categories ≥ 90.")
    with open(BASELINE_REPORT, "w") as f:
        f.write("\n".join(lines))

def main():
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    # Run each benchmark category
    scores = {
        "Novel Reasoning": run_novel_reasoning(),
        "Transfer Learning": run_transfer_learning(),
        "Planning": run_planning(),
        "Meta‑Learning": run_meta_learning()
    }
    # Compute simple aggregate metric
    all_scores = [v for cat in scores.values() for v in cat.values()]
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
    scores["Aggregate"] = {"Average Score": round(avg_score, 2)}
    # Persist results
    save_progress({
        "timestamp": timestamp,
        "scores": scores,
        "average": round(avg_score, 2)
    })
    generate_report(scores, timestamp)
    print(f"Benchmark completed at {timestamp}. Average score: {avg_score:.2f}")

if __name__ == "__main__":
    main()
import json
import os
from benchmarks.agi.novel_reasoning import run as run_novel_reasoning
from benchmarks.agi.transfer_learning import run as run_transfer_learning
from benchmarks.agi.planning import run as run_planning
from benchmarks.agi.meta_learning import run as run_meta_learning

def run_all():
    """
    Execute all AGI benchmark components and aggregate results.
    Results are written to ``agi_progress.json`` in the repository root.
    """
    results = {
        "novel_reasoning": run_novel_reasoning(),
        "transfer_learning": run_transfer_learning(),
        "planning": run_planning(),
        "meta_learning": run_meta_learning(),
    }

    # Compute an overall score as the mean of the component overall scores
    overall = sum(comp["overall"] for comp in results.values()) / len(results)
    results["overall"] = overall

    # Persist results for dashboard / tracking
    with open("agi_progress.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == "__main__":
    # Running the suite directly prints a concise summary
    final_results = run_all()
    print("=== AGI Benchmark Suite Completed ===")
    print(json.dumps(final_results, indent=2))
#!/usr/bin/env python3
"""
AGI Benchmark Suite
Runs a collection of synthetic AGI‑style tests and produces a baseline report.

The suite is deliberately lightweight so that a full run finishes in <10 minutes
on modest hardware.
"""

import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict

# Import individual benchmark modules
from benchmarks.agi.novel_reasoning import run_novel_reasoning
from benchmarks.agi.transfer_learning import run_transfer_learning
from benchmarks.agi.planning import run_planning
from benchmarks.agi.meta_learning import run_meta_learning


@dataclass
class BenchmarkResult:
    name: str
    score: float
    details: dict


def _run_and_collect(name: str, func):
    """Execute a benchmark function and wrap its result."""
    start = time.time()
    score, details = func()
    elapsed = time.time() - start
    return BenchmarkResult(name=name, score=score, details={**details, "time_s": elapsed})


def main():
    # Run each benchmark category
    results = [
        _run_and_collect("Novel Reasoning", run_novel_reasoning),
        _run_and_collect("Transfer Learning", run_transfer_learning),
        _run_and_collect("Planning", run_planning),
        _run_and_collect("Meta‑Learning", run_meta_learning),
    ]

    # Compute overall AGI‑score as the mean of category scores
    overall_score = sum(r.score for r in results) / len(results)

    # Prepare output directories
    out_dir = Path("benchmarks/agi")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Write JSON results for the dashboard
    json_path = out_dir / "results.json"
    json_path.write_text(
        json.dumps(
            {
                "timestamp": time.time(),
                "overall_score": overall_score,
                "categories": {r.name: {"score": r.score, **r.details} for r in results},
            },
            indent=2,
        )
    )

    # Write a human‑readable markdown baseline report
    md_path = Path("AGI_BASELINE_REPORT.md")
    md_path.write_text(
        f\"\"\"# AGI Benchmark Baseline Report

**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}

| Category | Score | Time (s) |
|----------|-------|----------|
{''.join(f"| {r.name} | {r.score:.3f} | {r.details['time_s']:.2f} |\n" for r in results)}

**Overall AGI Score:** {overall_score:.3f}

*Interpretation:*  
- Scores are normalised to the interval **[0, 1]**.  
- An **AGI‑achieved** threshold is defined as **overall_score ≥ 0.90**.  

> The current baseline reflects the capabilities of the installed model at
> repository revision **{Path('.git').resolve().name if Path('.git').exists() else 'unknown'}**.

\"\"\"
    )

    print(f"✅ Benchmark completed – overall AGI score: {overall_score:.3f}")
    print(f"📝 Report written to {md_path}")
    print(f"📊 JSON results written to {json_path}")


if __name__ == "__main__":
    main()
import json
import os
import datetime
from benchmarks.agi import novel_reasoning, transfer_learning, planning, meta_learning

AGI_THRESHOLD = 0.85  # average score required to claim AGI‑level performance
PROGRESS_FILE = "agi_progress.json"

def aggregate_results(*result_dicts):
    """Combine multiple result dictionaries into one."""
    aggregated = {}
    for d in result_dicts:
        aggregated.update(d)
    return aggregated

def compute_average_score(results):
    """Return the mean of all numeric scores."""
    if not results:
        return 0.0
    return sum(results.values()) / len(results)

def log_progress(timestamp, avg_score, results):
    """Append a new entry to the progress JSON file."""
    entry = {
        "timestamp": timestamp,
        "average_score": avg_score,
        "details": results
    }
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def run_all():
    """Execute the full AGI benchmark suite and report results."""
    print("Running Novel Reasoning tests...")
    nr = novel_reasoning.run()
    print("Running Transfer Learning tests...")
    tl = transfer_learning.run()
    print("Running Planning tests...")
    pl = planning.run()
    print("Running Meta‑Learning tests...")
    ml = meta_learning.run()

    all_results = aggregate_results(nr, tl, pl, ml)
    avg_score = compute_average_score(all_results)

    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    log_progress(timestamp, avg_score, all_results)

    print("\n=== AGI Benchmark Summary ===")
    print(f"Average Score: {avg_score:.3f}")
    print(f"AGI Threshold : {AGI_THRESHOLD:.3f}")
    print(f"AGI Achieved? : {'YES' if avg_score >= AGI_THRESHOLD else 'NO'}")
    print("\nDetailed Scores:")
    for name, score in sorted(all_results.items()):
        print(f"  {name}: {score}")

    # Write a quick baseline report if it does not exist
    if not os.path.exists("AGI_BASELINE_REPORT.md"):
        with open("AGI_BASELINE_REPORT.md", "w", encoding="utf-8") as f:
            f.write(f"# AGI Baseline Report\n\n")
            f.write(f"Generated on: {timestamp}\n\n")
            f.write(f"**Average Score:** {avg_score:.3f}\n")
            f.write(f"**AGI Threshold:** {AGI_THRESHOLD:.3f}\n")
            f.write(f"**AGI Achieved:** {'YES' if avg_score >= AGI_THRESHOLD else 'NO'}\n\n")
            f.write("## Detailed Test Scores\n")
            for name, score in sorted(all_results.items()):
                f.write(f"- {name}: {score}\\n")
    return all_results

if __name__ == "__main__":
    run_all()
#!/usr/bin/env python3
"""
Unified AGI Benchmark Suite

Runs the following sub‑benchmarks:
- Novel Reasoning (10 tests)
- Cross‑Domain Transfer (5 pairs)
- Long‑Term Planning (3 scenarios)
- Meta‑Learning (adaptation speed)

The suite aggregates scores, writes a baseline report, and dumps a JSON
payload for the progress dashboard.

Execution time on a typical development machine is < 10 minutes.
"""

import json
import os
import time
from datetime import datetime

# Import benchmark components
from benchmarks.agi.novel_reasoning import NovelReasoningTest
from benchmarks.agi.transfer_learning import TransferLearningTest
from benchmarks.agi.planning import PlanningTest
from benchmarks.agi.meta_learning import MetaLearningTest

RESULTS_JSON = "agi_progress.json"
REPORT_MD = "AGI_BASELINE_REPORT.md"
AGI_THRESHOLD = 90  # average score >= 90 is considered AGI‑level for this suite


def run_all_tests() -> list:
    """Execute each benchmark and collect their results."""
    suite = [
        NovelReasoningTest(),
        TransferLearningTest(),
        PlanningTest(),
        MetaLearningTest(),
    ]

    results = []
    start = time.time()
    for test in suite:
        result = test.run()
        results.append(result)
    elapsed = time.time() - start
    print(f"All tests completed in {elapsed:.2f}s")
    return results


def aggregate_score(results: list) -> float:
    """Return the mean of all test scores."""
    if not results:
        return 0.0
    total = sum(r["score"] for r in results)
    return round(total / len(results), 2)


def write_report(results: list, avg_score: float):
    """Create or overwrite the markdown baseline report."""
    now = datetime.utcnow().isoformat() + "Z"
    agi_status = "✅ AGI‑level achieved" if avg_score >= AGI_THRESHOLD else "❌ Not yet AGI"
    lines = [
        f"# AGI Benchmark Baseline Report",
        f"*Generated:* {now}",
        "",
        "## Individual Test Scores",
        "",
    ]
    for r in results:
        lines.append(f"- **{r['test']}**: {r['score']} / 100")
    lines.extend([
        "",
        f"## Aggregate Score",
        f"- **Average:** {avg_score} / 100",
        f"- **AGI Threshold:** {AGI_THRESHOLD}",
        f"- **Status:** {agi_status}",
        "",
        "*Run `python agi_benchmark_suite.py` to reproduce.*",
    ])

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Baseline report written to {REPORT_MD}")


def dump_progress_json(results: list, avg_score: float):
    """Append the latest run to a JSON array for the dashboard."""
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "average_score": avg_score,
        "tests": results,
    }

    # Load existing data if present
    if os.path.exists(RESULTS_JSON):
        with open(RESULTS_JSON, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(entry)
    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Progress data appended to {RESULTS_JSON}")


def main():
    results = run_all_tests()
    avg = aggregate_score(results)
    write_report(results, avg)
    dump_progress_json(results, avg)


if __name__ == "__main__":
    main()
import json
import time
from pathlib import Path

# Import benchmark modules
from benchmarks.agi.novel_reasoning import run_novel_reasoning_tests
from benchmarks.agi.transfer_learning import run_transfer_learning_tests
from benchmarks.agi.planning import run_planning_tests
from benchmarks.agi.meta_learning import run_meta_learning_tests

AGI_THRESHOLD = 0.85  # Average score required to claim “AGI achieved”

def aggregate_results(*result_dicts):
    """Merge multiple result dictionaries into a single dict."""
    agg = {}
    for d in result_dicts:
        agg.update(d)
    return agg

def compute_overall_score(results):
    """Return the mean score across all tests."""
    if not results:
        return 0.0
    return round(sum(results.values()) / len(results), 3)

def run_all_benchmarks(verbose=True):
    start = time.time()
    if verbose:
        print("Running Novel Reasoning tests...")
    nr = run_novel_reasoning_tests()
    if verbose:
        print("Running Transfer Learning tests...")
    tl = run_transfer_learning_tests()
    if verbose:
        print("Running Planning tests...")
    pl = run_planning_tests()
    if verbose:
        print("Running Meta‑Learning tests...")
    ml = run_meta_learning_tests()

    all_results = aggregate_results(nr, tl, pl, ml)
    overall = compute_overall_score(all_results)

    elapsed = round(time.time() - start, 2)
    if verbose:
        print(f"\nBenchmark completed in {elapsed}s")
        print(f"Overall AGI score: {overall} (threshold: {AGI_THRESHOLD})")
    return {
        "overall_score": overall,
        "individual_scores": all_results,
        "elapsed_seconds": elapsed,
        "timestamp": time.time()
    }

def save_report(report, path=Path("AGI_BASELINE_REPORT.md")):
    """Write a human‑readable markdown report."""
    lines = [
        "# AGI Benchmark Baseline Report",
        "",
        f"- **Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **Overall Score:** {report['overall_score']}",
        f"- **Threshold for AGI:** {AGI_THRESHOLD}",
        f"- **Result:** {'✅ AGI achieved' if report['overall_score'] >= AGI_THRESHOLD else '❌ Not yet AGI'}",
        "",
        "## Individual Test Scores",
        ""
    ]
    for name, score in sorted(report["individual_scores"].items()):
        lines.append(f"- **{name}**: {score}")

    lines.append("")
    lines.append(f"*Benchmark run time: {report['elapsed_seconds']} seconds*")
    path.write_text("\n".join(lines))
    if Path("benchmark_history.json").exists():
        history = json.loads(Path("benchmark_history.json").read_text())
    else:
        history = []
    history.append({
        "timestamp": report["timestamp"],
        "overall_score": report["overall_score"],
        "individual_scores": report["individual_scores"]
    })
    Path("benchmark_history.json").write_text(json.dumps(history, indent=2))

if __name__ == "__main__":
    report = run_all_benchmarks()
    save_report(report)
"""
AGI Benchmark Suite
Runs a collection of benchmark modules and aggregates scores.
"""

import json
import time
import csv
from pathlib import Path

from benchmarks.agi.novel_reasoning import run_novel_reasoning
from benchmarks.agi.transfer_learning import run_transfer_learning
from benchmarks.agi.planning import run_planning
from benchmarks.agi.meta_learning import run_meta_learning

BENCHMARK_MODULES = {
    "Novel Reasoning": run_novel_reasoning,
    "Transfer Learning": run_transfer_learning,
    "Planning": run_planning,
    "Meta Learning": run_meta_learning,
}

def run_all():
    """Execute all benchmark modules and collect their results."""
    results = {}
    start = time.time()
    for name, func in BENCHMARK_MODULES.items():
        results[name] = func()
    duration = time.time() - start
    results["__meta__"] = {"duration_seconds": duration}
    return results

def save_report(results, path=Path("AGI_BASELINE_REPORT.md")):
    """Write a human‑readable markdown report and embed raw JSON."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("# AGI Benchmark Baseline Report\\n\\n")
        f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
        f.write("## Summary\\n\\n")
        total_score = 0.0
        count = 0
        for suite, suite_res in results.items():
            if suite.startswith("__"):
                continue
            f.write(f"### {suite}\\n")
            for test_name, score in suite_res.items():
                f.write(f"- {test_name}: {score:.2f}\\n")
                total_score += score
                count += 1
            f.write("\\n")
        overall = total_score / max(count, 1)
        f.write(f"**Overall Score:** {overall:.2f}\\n\\n")
        f.write("## Detailed Results (JSON)\\n\\n")
        f.write("```json\\n")
        f.write(json.dumps(results, indent=2))
        f.write("\\n```\\n")

def append_progress(results, path=Path("agi_progress.csv")):
    """Append the aggregated overall score with a timestamp to a CSV log."""
    total = 0.0
    cnt = 0
    for suite_res in results.values():
        if isinstance(suite_res, dict):
            for v in suite_res.values():
                if isinstance(v, (int, float)):
                    total += v
                    cnt += 1
    avg = total / max(cnt, 1)
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), f"{avg:.4f}"])

def main():
    results = run_all()
    save_report(results)
    append_progress(results)

if __name__ == "__main__":
    main()
import json
import os
import datetime
from benchmarks.agi.novel_reasoning import NovelReasoningBenchmark
from benchmarks.agi.transfer_learning import TransferLearningBenchmark
from benchmarks.agi.planning import PlanningBenchmark
from benchmarks.agi.meta_learning import MetaLearningBenchmark

RESULTS_DIR = "benchmark_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def aggregate_scores(*score_dicts):
    """Flatten nested score dictionaries into a single dict."""
    agg = {}
    for d in score_dicts:
        agg.update(d)
    return agg

def run_all():
    print("Running AGI benchmark suite...")

    nr = NovelReasoningBenchmark().run()
    tl = TransferLearningBenchmark().run()
    pl = PlanningBenchmark().run()
    ml = MetaLearningBenchmark().run()

    all_scores = {
        "novel_reasoning": nr,
        "transfer_learning": tl,
        "planning": pl,
        "meta_learning": ml
    }

    # Compute a simple overall metric (mean of all sub‑scores)
    flat = aggregate_scores(nr, tl, pl, ml)
    overall = sum(flat.values()) / len(flat) if flat else 0.0

    timestamp = datetime.datetime.utcnow().isoformat()
    report = {
        "timestamp": timestamp,
        "overall_score": overall,
        "details": all_scores
    }

    # Persist the result for tracking
    result_path = os.path.join(RESULTS_DIR, f"run_{timestamp}.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Overall AGI benchmark score: {overall:.4f}")
    print(f"Result saved to {result_path}")

if __name__ == "__main__":
    run_all()