import os
# ----------------------------------------------------------------------
# Meta‑learning engine integration
# ----------------------------------------------------------------------
# The engine is responsible for:
#   • Selecting the most promising tool/decomposition strategy for each task.
#   • Dynamically adapting the learning‑rate based on observed reward.
#   • Persisting knowledge across runs.
# This block sets up a singleton instance that the rest of the module can use.
from meta_learning_engine import MetaLearningEngine
from strategy_performance_tracker import StrategyPerformanceTracker

# Global engine & tracker (initialized lazily on first use)
_meta_engine: MetaLearningEngine | None = None
_perf_tracker: StrategyPerformanceTracker | None = None

def _get_engine() -> MetaLearningEngine:
    global _meta_engine
    if _meta_engine is None:
        _meta_engine = MetaLearningEngine()
    return _meta_engine

def _get_tracker() -> StrategyPerformanceTracker:
    global _perf_tracker
    if _perf_tracker is None:
        _perf_tracker = StrategyPerformanceTracker()
    return _perf_tracker
from meta_learning_engine import MetaLearningEngine
from strategies import strategy_a, strategy_b, strategy_c
# Integrate the new MetaLearningEngine
from meta_learning_engine import MetaLearningEngine
from strategy_performance_tracker import StrategyPerformanceTracker
import json
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    filename="meta_learner.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Paths
BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "research_index.json"
PATTERNS_PATH = BASE_DIR / "patterns.json"
KNOWLEDGE_DIR = (BASE_DIR.parent / "stripper" / "knowledge").resolve()


def load_json(path: Path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from {path}: {e}")
        return default


def save_json(path: Path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_index():
    """Load the current research index."""
    return load_json(INDEX_PATH, {})


def save_index(index):
    """Persist the updated research index."""
    save_json(INDEX_PATH, index)


def load_patterns():
    """Load the meta‑learning cycle log."""
    return load_json(PATTERNS_PATH, [])


def save_patterns(patterns):
    """Persist the meta‑learning cycle log."""
    save_json(PATTERNS_PATH, patterns)


def scan_knowledge():
    """
    Walk through the knowledge directory and collect paper metadata.

    Expected file format (JSON):
    {
        "title": "...",
        "category": "...",   # optional, defaults to "uncategorized"
        "content": "..."
    }
    """
    papers = []
    if not KNOWLEDGE_DIR.is_dir():
        logging.warning(f"Knowledge directory not found: {KNOWLEDGE_DIR}")
        return papers

    for root, _, files in os.walk(KNOWLEDGE_DIR):
        for fname in files:
            if not fname.lower().endswith(".json"):
                continue
            fpath = Path(root) / fname
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                title = data.get("title")
                if not title:
                    logging.debug(f"Skipping file without title: {fpath}")
                    continue
                category = data.get("category", "uncategorized")
                papers.append((title, category, data))
            except Exception as e:
                logging.error(f"Error reading {fpath}: {e}")
    return papers


def update_index(index, papers):
    """
    Add new papers to the index if they are not already present.
    Returns the number of papers added.
    """
    added = 0
    for title, category, data in papers:
        cat_list = index.setdefault(category, [])
        if any(item.get("title") == title for item in cat_list):
            continue  # already indexed
        cat_list.append(data)
        added += 1
    return added


def meta_learning_cycle():
    """Perform a single meta‑learning iteration."""
    index = load_index()
    new_papers = scan_knowledge()
    added = update_index(index, new_papers)

    if added:
        save_index(index)
        logging.info(f"Added {added} new paper(s) to research_index.json")
    else:
        logging.info("No new papers found during this cycle")

    # Log the cycle
    patterns = load_patterns()
    patterns.append({"timestamp": time.time(), "added": added})
    save_patterns(patterns)


def main():
    """Continuously run meta‑learning cycles every hour."""
    logging.info("Meta‑learner started")
    while True:
        try:
            meta_learning_cycle()
        except Exception as e:
            logging.exception(f"Unexpected error during meta‑learning cycle: {e}")
        time.sleep(3600)  # wait one hour before next cycle


if __name__ == "__main__":
    main()
import os
import json
import time
import logging
from pathlib import Path
from typing import List, Dict

# Configure basic logger
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), "meta_learner.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

class MetaLearner:
    """
    Periodically scans the knowledge base for new papers,
    updates the central research_index.json and records each
    learning cycle in the internal `patterns` log.
    """

    def __init__(self,
                 knowledge_root: Path = Path(__file__).parent.parent / "stripper" / "knowledge",
                 index_path: Path = Path(__file__).parent / "research_index.json",
                 cycle_interval: int = 3600):
        """
        :param knowledge_root: Directory containing raw paper files.
        :param index_path: Path to the JSON index that aggregates papers.
        :param cycle_interval: Seconds between successive re‑indexing cycles.
        """
        self.knowledge_root = knowledge_root
        self.index_path = index_path
        self.cycle_interval = cycle_interval
        self.patterns: List[Dict] = []  # Log of learning cycles

        # Ensure knowledge directory exists
        if not self.knowledge_root.is_dir():
            raise FileNotFoundError(f"Knowledge directory not found: {self.knowledge_root}")

        # Load or initialise the research index
        self.index = self._load_index()

    def _load_index(self) -> Dict:
        """Load existing index or create a fresh structure."""
        if self.index_path.is_file():
            try:
                with self.index_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse index JSON: {e}")
        # Default structure
        return {"papers": [], "categories": {}}

    def _save_index(self):
        """Persist the current index to disk."""
        with self.index_path.open("w", encoding="utf-8") as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

    def _extract_paper_metadata(self, file_path: Path) -> Dict:
        """
        Extract metadata from a knowledge file.
        Expected formats:
          * JSON with keys: title, category, content
          * Plain‑text where the first line is the title and the second line is the category
        """
        try:
            with file_path.open("r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logging.warning(f"Unable to read {file_path}: {e}")
            return {}

        # Try JSON first
        try:
            data = json.loads(content)
            if isinstance(data, dict) and "title" in data and "category" in data:
                return {
                    "title": data["title"],
                    "category": data["category"],
                    "content": data.get("content", ""),
                    "source": str(file_path.relative_to(self.knowledge_root)),
                }
        except json.JSONDecodeError:
            pass

        # Fallback to simple text parsing
        lines = content.strip().splitlines()
        if len(lines) >= 2:
            title = lines[0].strip()
            category = lines[1].strip()
            body = "\n".join(lines[2:]).strip()
            return {
                "title": title,
                "category": category,
                "content": body,
                "source": str(file_path.relative_to(self.knowledge_root)),
            }

        logging.debug(f"File {file_path} does not contain recognizable metadata.")
        return {}

    def _is_new_paper(self, paper_meta: Dict) -> bool:
        """Determine if a paper (by title) is already indexed."""
        existing_titles = {p["title"] for p in self.index.get("papers", [])}
        return paper_meta.get("title") not in existing_titles

    def _update_index_with_new_papers(self, new_papers: List[Dict]) -> int:
        """Add new papers to the index and update category mappings."""
        added = 0
        for paper in new_papers:
            if not self._is_new_paper(paper):
                continue
            self.index.setdefault("papers", []).append(paper)
            cat = paper.get("category", "uncategorized")
            self.index.setdefault("categories", {}).setdefault(cat, []).append(paper["title"])
            added += 1
        if added:
            self._save_index()
        return added

    def run_cycle(self):
        """One full scan‑update‑log cycle."""
        start_time = time.time()
        logging.info("Meta‑learning cycle started.")

        # Scan knowledge directory
        new_papers = []
        for root, _, files in os.walk(self.knowledge_root):
            for fname in files:
                if fname.startswith('.'):
                    continue  # skip hidden files
                fpath = Path(root) / fname
                meta = self._extract_paper_metadata(fpath)
                if meta:
                    new_papers.append(meta)

        added_count = self._update_index_with_new_papers(new_papers)

        # Record cycle pattern
        cycle_record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "duration_seconds": round(time.time() - start_time, 2),
            "new_papers_added": added_count,
            "total_papers": len(self.index.get("papers", [])),
        }
        self.patterns.append(cycle_record)
        logging.info(f"Meta‑learning cycle completed: {cycle_record}")

    def start(self):
        """Continuously run cycles with the configured interval."""
        logging.info("MetaLearner daemon started.")
        try:
            while True:
                self.run_cycle()
                time.sleep(self.cycle_interval)
        except KeyboardInterrupt:
            logging.info("MetaLearner daemon stopped by user.")
        except Exception as exc:
            logging.exception(f"Unexpected error in MetaLearner daemon: {exc}")

if __name__ == "__main__":
    # Default interval set to 1 hour; adjust via env var if needed
    interval = int(os.getenv("META_LEARNER_INTERVAL", "3600"))
    learner = MetaLearner(cycle_interval=interval)
    learner.start()
import os
import json
from datetime import datetime

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
KNOWLEDGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "stripper", "knowledge"))
INDEX_PATH = os.path.abspath(os.path.join(BASE_DIR, "research_index.json"))
PATTERNS_LOG = os.path.abspath(os.path.join(BASE_DIR, "patterns.log"))

def load_index():
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"papers": []}

def save_index(index):
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

def log_cycle(new_count):
    timestamp = datetime.utcnow().isoformat() + "Z"
    entry = f"{timestamp} - Added {new_count} new paper(s) to research_index.json\n"
    with open(PATTERNS_LOG, "a", encoding="utf-8") as f:
        f.write(entry)

def extract_papers():
    papers = []
    for root, dirs, files in os.walk(KNOWLEDGE_DIR):
        # Derive a category from the immediate sub‑directory under knowledge/
        rel_path = os.path.relpath(root, KNOWLEDGE_DIR)
        category = rel_path if rel_path != "." else "uncategorized"
        for file in files:
            if file.startswith("."):
                continue
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                # Skip binary or unreadable files
                continue
            papers.append({
                "title": os.path.splitext(file)[0],
                "category": category,
                "path": os.path.relpath(file_path, BASE_DIR),
                "content": content
            })
    return papers

def meta_learning_cycle():
    index = load_index()
    existing_paths = {p["path"] for p in index.get("papers", [])}
    all_papers = extract_papers()
    new_papers = [p for p in all_papers if p["path"] not in existing_paths]

    if new_papers:
        index.setdefault("papers", []).extend(new_papers)
        save_index(index)
        log_cycle(len(new_papers))
        print(f"[MetaLearner] Added {len(new_papers)} new paper(s) to the index.")
    else:
        print("[MetaLearner] No new papers found.")

if __name__ == "__main__":
    meta_learning_cycle()