import json
import os
import ast
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict, deque


class NodeType(Enum):
    """Node types in the knowledge graph."""
    CONCEPT = "CONCEPT"
    SKILL = "SKILL"
    LESSON = "LESSON"
    FILE = "FILE"
    FUNCTION = "FUNCTION"


class EdgeType(Enum):
    """Edge types in the knowledge graph."""
    RELATES_TO = "RELATES_TO"
    IMPLEMENTS = "IMPLEMENTS"
    USES = "USES"
    DEPENDS_ON = "DEPENDS_ON"
    CONTAINS = "CONTAINS"


@dataclass
class KnowledgeNode:
    """Represents a node in the knowledge graph."""
    id: str
    label: str
    type: NodeType
    properties: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "label": self.label,
            "type": self.type.value,
            "properties": self.properties
        }


@dataclass
class KnowledgeEdge:
    """Represents an edge in the knowledge graph."""
    source: str
    target: str
    relation: EdgeType

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation.value
        }


class KnowledgeGraph:
    """A knowledge graph for storing and querying relationships between concepts."""

    def __init__(self):
        """Initialize an empty knowledge graph."""
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: List[KnowledgeEdge] = []
        self.adjacency: Dict[str, List[Tuple[str, EdgeType]]] = defaultdict(list)

    def add_node(self, node: KnowledgeNode) -> None:
        """Add a node to the graph."""
        self.nodes[node.id] = node

    def add_edge(self, edge: KnowledgeEdge) -> None:
        """Add an edge to the graph."""
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise ValueError(f"Source or target node not found in graph")
        self.edges.append(edge)
        self.adjacency[edge.source].append((edge.target, edge.relation))

    def query(self, node_id: str) -> Optional[KnowledgeNode]:
        """Query a node by its ID."""
        return self.nodes.get(node_id)

    def query_related(self, node_id: str, depth: int = 2) -> Dict:
        """Query all related nodes within a given depth (subgraph)."""
        if node_id not in self.nodes:
            return {"nodes": {}, "edges": []}

        visited_nodes: Set[str] = set()
        visited_edges: List[KnowledgeEdge] = []
        queue: deque = deque([(node_id, 0)])

        while queue:
            current_id, current_depth = queue.popleft()

            if current_id in visited_nodes or current_depth > depth:
                continue

            visited_nodes.add(current_id)

            # Explore neighbors
            if current_depth < depth:
                for target_id, relation in self.adjacency[current_id]:
                    if target_id not in visited_nodes:
                        queue.append((target_id, current_depth + 1))
                        # Find and add the edge
                        for edge in self.edges:
                            if edge.source == current_id and edge.target == target_id:
                                visited_edges.append(edge)
                                break

        # Build subgraph
        subgraph_nodes = {nid: self.nodes[nid].to_dict() for nid in visited_nodes}
        subgraph_edges = [e.to_dict() for e in visited_edges]

        return {
            "root_node": node_id,
            "nodes": subgraph_nodes,
            "edges": subgraph_edges,
            "depth": depth
        }

    def populate_from_codebase(self, root_path: str = ".") -> None:
        """
        Scan Python files in the codebase and populate the graph with FILE and FUNCTION nodes.
        Creates CONTAINS edges linking files to their functions.
        """
        root = Path(root_path)

        # Scan for Python files
        py_files = list(root.glob("**/*.py"))

        for py_file in py_files:
            # Skip common directories
            if any(part in py_file.parts for part in ["__pycache__", ".git", "venv", ".venv"]):
                continue

            try:
                # Create FILE node
                file_id = f"file:{py_file.relative_to(root)}"
                file_node = KnowledgeNode(
                    id=file_id,
                    label=str(py_file.name),
                    type=NodeType.FILE,
                    properties={"path": str(py_file.relative_to(root))}
                )
                self.add_node(file_node)

                # Parse file and extract functions/classes
                with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                try:
                    tree = ast.parse(content)
                except SyntaxError:
                    continue

                # Extract function and class definitions
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_id = f"func:{py_file.relative_to(root)}:{node.name}"
                        func_node = KnowledgeNode(
                            id=func_id,
                            label=node.name,
                            type=NodeType.FUNCTION,
                            properties={
                                "lineno": node.lineno,
                                "file": str(py_file.relative_to(root))
                            }
                        )
                        self.add_node(func_node)

                        # Create CONTAINS edge from file to function
                        edge = KnowledgeEdge(
                            source=file_id,
                            target=func_id,
                            relation=EdgeType.CONTAINS
                        )
                        self.add_edge(edge)

                    elif isinstance(node, ast.ClassDef):
                        class_id = f"class:{py_file.relative_to(root)}:{node.name}"
                        class_node = KnowledgeNode(
                            id=class_id,
                            label=node.name,
                            type=NodeType.SKILL,  # Using SKILL for classes
                            properties={
                                "lineno": node.lineno,
                                "file": str(py_file.relative_to(root))
                            }
                        )
                        self.add_node(class_node)

                        # Create CONTAINS edge from file to class
                        edge = KnowledgeEdge(
                            source=file_id,
                            target=class_id,
                            relation=EdgeType.CONTAINS
                        )
                        self.add_edge(edge)

            except Exception as e:
                print(f"Error processing {py_file}: {e}")

    def to_dict(self) -> Dict:
        """Convert the entire graph to a dictionary for JSON serialization."""
        return {
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
            "edges": [edge.to_dict() for edge in self.edges]
        }

    def save_json(self, filepath: str) -> None:
        """Save the knowledge graph to a JSON file."""
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def load_json(self, filepath: str) -> None:
        """Load the knowledge graph from a JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)

        # Load nodes
        for node_data in data.get("nodes", {}).values():
            node = KnowledgeNode(
                id=node_data["id"],
                label=node_data["label"],
                type=NodeType[node_data["type"]],
                properties=node_data.get("properties", {})
            )
            self.add_node(node)

        # Load edges
        for edge_data in data.get("edges", []):
            edge = KnowledgeEdge(
                source=edge_data["source"],
                target=edge_data["target"],
                relation=EdgeType[edge_data["relation"]]
            )
            self.add_edge(edge)
