"""
Cross-Path Knowledge Transfer System
Enables real-time knowledge sharing between parallel execution paths.
"""

import json
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Discovery:
    """Represents a knowledge discovery from a path."""
    path_id: str
    discovery_type: str  # 'skill', 'pattern', 'insight', 'error_solution'
    content: Any
    timestamp: str
    quality_impact: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class SharedPathContext:
    """Thread-safe knowledge sharing between execution paths."""

    def __init__(self, storage_path: Optional[str] = None):
        self.discoveries: Dict[str, List[Discovery]] = {}
        self.lock = threading.RLock()
        self.storage_path = Path(storage_path) if storage_path else Path("path_knowledge_transfer.json")
        self.contribution_stats: Dict[str, int] = {}
        self.quality_improvements: List[Dict[str, Any]] = []
        self._load_from_disk()

    def register_discovery(
        self,
        path_id: str,
        discovery_type: str,
        content: Any,
        quality_impact: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Register a new discovery from a path.
        Thread-safe with automatic persistence.

        Args:
            path_id: Identifier of the path making the discovery
            discovery_type: Type of discovery (skill, pattern, insight, error_solution)
            content: The actual discovery content
            quality_impact: Optional quality score impact (0.0-1.0)
            metadata: Additional context about the discovery

        Returns:
            True if registered successfully
        """
        with self.lock:
            discovery = Discovery(
                path_id=path_id,
                discovery_type=discovery_type,
                content=content,
                timestamp=datetime.now().isoformat(),
                quality_impact=quality_impact,
                metadata=metadata or {}
            )

            if path_id not in self.discoveries:
                self.discoveries[path_id] = []

            self.discoveries[path_id].append(discovery)

            # Track contribution stats
            self.contribution_stats[path_id] = self.contribution_stats.get(path_id, 0) + 1

            # Persist to disk
            self._save_to_disk()

            return True

    def get_available_discoveries(
        self,
        exclude_path_id: Optional[str] = None,
        discovery_type: Optional[str] = None,
        min_quality_impact: Optional[float] = None
    ) -> List[Discovery]:
        """
        Retrieve all discoveries from other paths.

        Args:
            exclude_path_id: Exclude discoveries from this path (typically the requesting path)
            discovery_type: Filter by discovery type
            min_quality_impact: Filter by minimum quality impact

        Returns:
            List of Discovery objects matching criteria
        """
        with self.lock:
            all_discoveries = []

            for path_id, discoveries in self.discoveries.items():
                # Skip excluded path
                if exclude_path_id and path_id == exclude_path_id:
                    continue

                for discovery in discoveries:
                    # Apply filters
                    if discovery_type and discovery.discovery_type != discovery_type:
                        continue

                    if min_quality_impact is not None:
                        if discovery.quality_impact is None or discovery.quality_impact < min_quality_impact:
                            continue

                    all_discoveries.append(discovery)

            # Sort by timestamp (most recent first)
            all_discoveries.sort(key=lambda d: d.timestamp, reverse=True)

            return all_discoveries

    def get_discoveries_by_path(self, path_id: str) -> List[Discovery]:
        """Get all discoveries from a specific path."""
        with self.lock:
            return self.discoveries.get(path_id, []).copy()

    def track_quality_improvement(
        self,
        path_id: str,
        before_quality: float,
        after_quality: float,
        discoveries_used: List[str]
    ):
        """
        Track quality improvement attributed to knowledge transfer.

        Args:
            path_id: Path that benefited from the transfer
            before_quality: Quality score before applying discoveries
            after_quality: Quality score after applying discoveries
            discoveries_used: List of discovery types/IDs used
        """
        with self.lock:
            improvement = {
                'path_id': path_id,
                'before_quality': before_quality,
                'after_quality': after_quality,
                'improvement': after_quality - before_quality,
                'discoveries_used': discoveries_used,
                'timestamp': datetime.now().isoformat()
            }

            self.quality_improvements.append(improvement)
            self._save_to_disk()

    def get_contribution_stats(self) -> Dict[str, Any]:
        """Get statistics about path contributions."""
        with self.lock:
            total_discoveries = sum(len(d) for d in self.discoveries.values())

            avg_improvement = 0.0
            if self.quality_improvements:
                avg_improvement = sum(qi['improvement'] for qi in self.quality_improvements) / len(self.quality_improvements)

            return {
                'total_discoveries': total_discoveries,
                'paths_contributing': len(self.discoveries),
                'contribution_by_path': self.contribution_stats.copy(),
                'total_quality_improvements': len(self.quality_improvements),
                'avg_quality_improvement': avg_improvement,
                'discovery_types': self._count_discovery_types()
            }

    def _count_discovery_types(self) -> Dict[str, int]:
        """Count discoveries by type."""
        type_counts = {}
        for discoveries in self.discoveries.values():
            for discovery in discoveries:
                type_counts[discovery.discovery_type] = type_counts.get(discovery.discovery_type, 0) + 1
        return type_counts

    def _save_to_disk(self):
        """Persist discoveries to disk."""
        try:
            data = {
                'discoveries': {
                    path_id: [asdict(d) for d in discoveries]
                    for path_id, discoveries in self.discoveries.items()
                },
                'contribution_stats': self.contribution_stats,
                'quality_improvements': self.quality_improvements
            }

            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save knowledge transfer data: {e}")

    def _load_from_disk(self):
        """Load discoveries from disk."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Reconstruct discoveries
            self.discoveries = {
                path_id: [Discovery(**d) for d in discoveries]
                for path_id, discoveries in data.get('discoveries', {}).items()
            }

            self.contribution_stats = data.get('contribution_stats', {})
            self.quality_improvements = data.get('quality_improvements', [])

        except Exception as e:
            print(f"Warning: Failed to load knowledge transfer data: {e}")

    def clear(self):
        """Clear all discoveries (for testing/reset)."""
        with self.lock:
            self.discoveries.clear()
            self.contribution_stats.clear()
            self.quality_improvements.clear()
            self._save_to_disk()


# Global shared context instance
_global_context: Optional[SharedPathContext] = None
_context_lock = threading.Lock()


def get_shared_context() -> SharedPathContext:
    """Get or create the global shared context (singleton pattern)."""
    global _global_context

    with _context_lock:
        if _global_context is None:
            _global_context = SharedPathContext()
        return _global_context
