import json
import os
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Paths to the data sources – adjust if your project stores them elsewhere
CHECKPOINT_PATH = os.path.join(os.path.dirname(__file__), "checkpoint.json")
GRIND_LOG_PATH = os.path.join(os.path.dirname(__file__), "grind_logs.json")
CHART_OUTPUT = os.path.join(os.path.dirname(__file__), "cost_breakdown.png")

def _load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _aggregate_data():
    """
    Returns a nested dict:
        data[phase][time_period][task_file] = total_cost
    Time period is month‑year (e.g., "2024‑02").
    """
    # Load both sources; they have the same schema:
    # { "task_file": "...", "phase": "...", "cost": float, "timestamp": "ISO8601" }
    entries = _load_json(CHECKPOINT_PATH) + _load_json(GRIND_LOG_PATH)

    agg = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for e in entries:
        try:
            ts = datetime.fromisoformat(e["timestamp"])
            period = ts.strftime("%Y-%m")
            phase = e.get("phase", "unknown")
            file = e.get("task_file", "unknown")
            cost = float(e.get("cost", 0))
            agg[phase][period][file] += cost
        except Exception:
            continue
    return agg

def _draw_bar_chart(agg):
    """
    Draws a simple stacked bar chart:
        X‑axis: time periods
        Stacks: phases
        Height: total cost for that period (all files)
    """
    # Gather sorted periods
    periods = sorted({p for phase in agg.values() for p in phase.keys()})
    phases = sorted(agg.keys())

    # Build matrix of costs [phase][period]
    matrix = []
    for phase in phases:
        row = [agg[phase].get(p, {}).get("", 0) for p in periods]  # placeholder for total per period
        # Actually sum across all files for that phase/period
        row = [sum(agg[phase].get(p, {}).values()) for p in periods]
        matrix.append(row)

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = [0] * len(periods)

    colors = plt.cm.tab20.colors
    for idx, (phase, costs) in enumerate(zip(phases, matrix)):
        ax.bar(periods, costs, bottom=bottom, label=phase, color=colors[idx % len(colors)])
        bottom = [b + c for b, c in zip(bottom, costs)]

    ax.set_xlabel("Time period (Month‑Year)")
    ax.set_ylabel("Cost (USD)")
    ax.set_title("Cost Breakdown by Phase Over Time")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.2f}'))
    ax.legend(title="Phase")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_OUTPUT)
    plt.close(fig)

def _draw_treemap(agg):
    """
    Draws a treemap (using squarify) that shows cost distribution
    by task file within each phase for the most recent period.
    """
    try:
        import squarify  # optional, install via pip if you want treemap support
    except ImportError:
        return  # silently skip if squarify is not available

    # Determine most recent period
    all_periods = {p for phase in agg.values() for p in phase.keys()}
    if not all_periods:
        return
    recent = max(all_periods)

    # Build data for the treemap: each entry = (size, label)
    sizes = []
    labels = []
    colors = []
    cmap = plt.cm.tab20c
    color_idx = 0

    for phase, periods in agg.items():
        files = periods.get(recent, {})
        for file, cost in files.items():
            if cost <= 0:
                continue
            sizes.append(cost)
            labels.append(f"{phase}\n{file}\n${cost:,.2f}")
            colors.append(cmap(color_idx % cmap.N))
            color_idx += 1

    if not sizes:
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8, ax=ax)
    ax.axis('off')
    plt.title(f"Cost Distribution by File (Phase) – {recent}")
    plt.tight_layout()
    treemap_path = os.path.join(os.path.dirname(__file__), f"cost_treemap_{recent}.png")
    plt.savefig(treemap_path)
    plt.close(fig)

def update_cost_chart():
    """
    Public entry point – called after each log entry is persisted.
    Generates both a stacked bar chart and, if `squarify` is installed,
    a treemap for the latest period.
    """
    agg = _aggregate_data()
    if not agg:
        return
    _draw_bar_chart(agg)
    _draw_treemap(agg)
import os
import json
import pandas as pd
import plotly.express as px
from datetime import datetime

# Paths – adjust if your project stores them elsewhere
CHECKPOINT_PATH = os.path.join(os.path.dirname(__file__), "..", "checkpoint.json")
GRIND_LOGS_PATH = os.path.join(os.path.dirname(__file__), "..", "grind_logs.csv")
OUTPUT_HTML = os.path.join(os.path.dirname(__file__), "..", "cost_chart.html")

def _load_checkpoint():
    """Load checkpoint data (expects a JSON file with a list of task dicts)."""
    if not os.path.exists(CHECKPOINT_PATH):
        return []
    with open(CHECKPOINT_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _load_grind_logs():
    """Load grind logs (expects a CSV with columns: task_file, phase, timestamp, cost)."""
    if not os.path.exists(GRIND_LOGS_PATH):
        return pd.DataFrame(columns=["task_file", "phase", "timestamp", "cost"])
    return pd.read_csv(GRIND_LOGS_PATH)

def _prepare_dataframe():
    """Combine checkpoint and grind‑log data into a single DataFrame."""
    # checkpoint may contain similar fields; we normalise them
    checkpoint_data = _load_checkpoint()
    cp_df = pd.DataFrame(checkpoint_data)

    grind_df = _load_grind_logs()

    # Ensure required columns exist
    required = {"task_file", "phase", "timestamp", "cost"}
    for df in (cp_df, grind_df):
        missing = required - set(df.columns)
        for col in missing:
            df[col] = None

    # Concatenate and clean
    df = pd.concat([cp_df, grind_df], ignore_index=True)
    df = df.dropna(subset=["task_file", "phase", "timestamp", "cost"])

    # Convert timestamp to datetime and derive a simple time period (e.g., YYYY‑MM)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df["time_period"] = df["timestamp"].dt.to_period("M").astype(str)

    # Ensure cost is numeric
    df["cost"] = pd.to_numeric(df["cost"], errors="coerce").fillna(0)

    return df

def generate_cost_chart():
    """
    Build and (re)write an HTML treemap showing cost breakdown by
    task file → phase → time period.  The function is cheap enough
    to be called after each task completes, providing a near‑real‑time
    view of spending.
    """
    df = _prepare_dataframe()
    if df.empty:
        # Nothing to plot – create a placeholder file
        with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
            f.write("<html><body><h3>No cost data available yet.</h3></body></html>")
        return

    # Treemap: hierarchical cost view
    fig = px.treemap(
        df,
        path=["task_file", "phase", "time_period"],
        values="cost",
        title="Cost Breakdown – Task File → Phase → Time Period",
        color="cost",
        color_continuous_scale="RdYlGn",
    )
    fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))

    # Write interactive HTML (overwrites previous version)
    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")