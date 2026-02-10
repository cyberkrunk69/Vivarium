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
    SOLUTION_PATH = "SOLUTION_PATH"


class EdgeType(Enum):
    """Edge types in the knowledge graph."""
    RELATES_TO = "RELATES_TO"
    IMPLEMENTS = "IMPLEMENTS"
    USES = "USES"
    DEPENDS_ON = "DEPENDS_ON"
    CONTAINS = "CONTAINS"
    EXPLORED_BY = "EXPLORED_BY"
    RECOMMENDED_FOR = "RECOMMENDED_FOR"


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

    def __init__(self, filepath: str = 'knowledge_graph.json'):
        """Initialize knowledge graph, loading from file if it exists."""
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: List[KnowledgeEdge] = []
        self.adjacency: Dict[str, List[Tuple[str, EdgeType]]] = defaultdict(list)
        self.filepath = filepath

        # Auto-load from file if it exists
        if os.path.exists(self.filepath):
            try:
                self.load_from_file(self.filepath)
            except Exception as e:
                print(f"Warning: Could not load knowledge graph from {self.filepath}: {e}")

    def add_node(self, node: KnowledgeNode) -> None:
        """Add a node to the graph."""
        self.nodes[node.id] = node
        self._auto_save()

    def add_typed_node(self, name: str, node_type: NodeType, metadata: Dict = None) -> str:
        """
        Add a typed node to the graph with metadata.

        Args:
            name: Name/label of the node
            node_type: NodeType enum value (CONCEPT, FILE, FUNCTION, LESSON, SKILL)
            metadata: Optional dictionary of properties

        Returns:
            The generated node ID
        """
        if metadata is None:
            metadata = {}

        # Generate ID based on type and name
        node_id = f"{node_type.value.lower()}:{name.lower().replace(' ', '_')}"

        node = KnowledgeNode(
            id=node_id,
            label=name,
            type=node_type,
            properties=metadata
        )
        self.add_node(node)
        return node_id

    def add_edge(self, edge: KnowledgeEdge) -> None:
        """Add an edge to the graph."""
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise ValueError(f"Source or target node not found in graph")
        self.edges.append(edge)
        self.adjacency[edge.source].append((edge.target, edge.relation))
        self._auto_save()

    def add_typed_edge(self, from_id: str, to_id: str, edge_type: EdgeType) -> None:
        """
        Add a typed edge between two nodes.

        Args:
            from_id: Source node ID
            to_id: Target node ID
            edge_type: EdgeType enum value (IMPLEMENTS, USES, RELATES_TO, LEARNED_FROM)
        """
        edge = KnowledgeEdge(
            source=from_id,
            target=to_id,
            relation=edge_type
        )
        self.add_edge(edge)

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

    def get_related_concepts(self, task: str, max_results: int = 5) -> List[str]:
        """
        Get related concepts from the knowledge graph based on a task description.

        Args:
            task: Task description string
            max_results: Maximum number of related concepts to return

        Returns:
            List of related concept labels
        """
        task_lower = task.lower()
        related_concepts = []

        # Find nodes whose labels match keywords in the task
        for node_id, node in self.nodes.items():
            node_label_lower = node.label.lower()
            # Match if task contains node label or node label contains task words
            task_words = [w for w in task_lower.split() if len(w) > 3]
            if any(word in node_label_lower for word in task_words):
                related_concepts.append(node.label)
                if len(related_concepts) >= max_results:
                    break

        return related_concepts

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

    def _auto_save(self) -> None:
        """Internal method to auto-save after modifications."""
        try:
            self.save_to_file(self.filepath)
        except Exception as e:
            print(f"Warning: Could not auto-save knowledge graph: {e}")

    def save_to_file(self, filepath: str = 'knowledge_graph.json') -> None:
        """Save the knowledge graph to a JSON file."""
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def load_from_file(self, filepath: str = 'knowledge_graph.json') -> None:
        """Load the knowledge graph from a JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)

        # Clear existing graph
        self.nodes.clear()
        self.edges.clear()
        self.adjacency.clear()

        # Load nodes
        for node_data in data.get("nodes", {}).values():
            node = KnowledgeNode(
                id=node_data["id"],
                label=node_data["label"],
                type=NodeType[node_data["type"]],
                properties=node_data.get("properties", {})
            )
            # Add without triggering auto-save during load
            self.nodes[node.id] = node

        # Load edges
        for edge_data in data.get("edges", []):
            edge = KnowledgeEdge(
                source=edge_data["source"],
                target=edge_data["target"],
                relation=EdgeType[edge_data["relation"]]
            )
            # Add without triggering auto-save during load
            if edge.source in self.nodes and edge.target in self.nodes:
                self.edges.append(edge)
                self.adjacency[edge.source].append((edge.target, edge.relation))

    # Keep legacy method names for backward compatibility
    def save_json(self, filepath: str) -> None:
        """Save the knowledge graph to a JSON file (legacy method)."""
        self.save_to_file(filepath)

    def load_json(self, filepath: str) -> None:
        """Load the knowledge graph from a JSON file (legacy method)."""
        self.load_from_file(filepath)

    def add_lesson_node(self, lesson_dict: Dict) -> str:
        """
        Add a lesson as a LESSON node to the knowledge graph.

        Args:
            lesson_dict: Dictionary containing lesson data (from learned_lessons.json)

        Returns:
            The lesson node ID
        """
        lesson_id = lesson_dict.get("id", f"lesson_{len(self.nodes)}")

        lesson_node = KnowledgeNode(
            id=lesson_id,
            label=lesson_dict.get("lesson", "Unknown lesson")[:50],
            type=NodeType.LESSON,
            properties={
                "task_category": lesson_dict.get("task_category", ""),
                "timestamp": lesson_dict.get("timestamp", ""),
                "importance": lesson_dict.get("importance", 5),
                "source": lesson_dict.get("source", ""),
                "full_lesson": lesson_dict.get("lesson", "")
            }
        )

        self.add_node(lesson_node)
        return lesson_id

    def link_lesson_to_concepts(self, lesson_id: str, concepts: List[str]) -> None:
        """
        Link a lesson node to concept nodes (creating concepts if they don't exist).

        Args:
            lesson_id: The lesson node ID
            concepts: List of concept strings to link to
        """
        if lesson_id not in self.nodes:
            raise ValueError(f"Lesson node {lesson_id} not found in graph")

        for concept in concepts:
            # Create or find concept node
            concept_id = f"concept:{concept.lower().replace(' ', '_')}"

            if concept_id not in self.nodes:
                concept_node = KnowledgeNode(
                    id=concept_id,
                    label=concept,
                    type=NodeType.CONCEPT,
                    properties={"name": concept}
                )
                self.add_node(concept_node)

            # Create edge from lesson to concept
            edge = KnowledgeEdge(
                source=lesson_id,
                target=concept_id,
                relation=EdgeType.RELATES_TO
            )
            self.add_edge(edge)

    def extract_concepts_from_lesson(self, lesson_text: str) -> List[str]:
        """
        Extract key concepts from lesson text automatically.
        Simple extraction based on common patterns and keywords.

        Args:
            lesson_text: The lesson text to extract concepts from

        Returns:
            List of extracted concept strings
        """
        concepts = []

        # Common technical concepts to extract
        concept_keywords = [
            "CAMEL", "DSPy", "Voyager", "TextGrad", "LATS",
            "role decomposition", "prompt optimization", "skill injection",
            "knowledge graph", "reflection", "self-verification",
            "error categorization", "complexity adaptation", "critic feedback",
            "online learning", "memory synthesis", "demonstration",
            "few-shot", "chain-of-thought", "quality assurance",
            "performance tracking", "message pool", "lesson recording"
        ]

        lesson_lower = lesson_text.lower()

        # Extract matching concepts
        for keyword in concept_keywords:
            if keyword.lower() in lesson_lower:
                concepts.append(keyword)

        # Extract arXiv references as concepts
        if "arxiv" in lesson_lower:
            import re
            arxiv_matches = re.findall(r'arXiv:\d+\.\d+', lesson_text)
            concepts.extend(arxiv_matches)

        return list(set(concepts))  # Remove duplicates

    def extract_concepts(self, text: str) -> List[str]:
        """
        Auto-extract concepts from task descriptions or any text using:
        - Noun phrase extraction (simple regex)
        - Technical term detection
        - Code pattern recognition (function names, class names, etc.)

        Args:
            text: Text to extract concepts from (task description, etc.)

        Returns:
            List of concept strings extracted from the text
        """
        import re

        concepts = []

        # 1. Extract noun phrases (capitalized words and multi-word technical terms)
        # Pattern: Capitalized words or sequences like "knowledge graph", "API endpoint"
        noun_phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z]?[a-z]+)*\b', text)
        concepts.extend(noun_phrases)

        # 2. Technical term detection - common programming/AI concepts
        technical_terms = [
            'API', 'database', 'function', 'class', 'method', 'endpoint',
            'query', 'node', 'edge', 'graph', 'algorithm', 'optimization',
            'model', 'agent', 'task', 'prompt', 'context', 'embeddings',
            'vector', 'semantic', 'retrieval', 'search', 'index',
            'config', 'logging', 'error', 'exception', 'validation',
            'authentication', 'authorization', 'token', 'session',
            'cache', 'performance', 'metrics', 'monitoring',
            'deployment', 'testing', 'debugging', 'refactor'
        ]

        text_lower = text.lower()
        for term in technical_terms:
            if term.lower() in text_lower:
                concepts.append(term)

        # 3. Code pattern recognition
        # Extract function/method names (snake_case or camelCase)
        function_patterns = re.findall(r'\b[a-z_][a-z0-9_]*\(\)', text)
        concepts.extend([p.replace('()', '') for p in function_patterns])

        # Extract class names (PascalCase)
        class_patterns = re.findall(r'\b[A-Z][a-zA-Z0-9]*(?:\.[A-Z][a-zA-Z0-9]*)*\b', text)
        concepts.extend(class_patterns)

        # Extract Python identifiers (variables, modules)
        identifier_patterns = re.findall(r'\b[a-z_][a-z0-9_]{2,}\b', text)
        # Filter out common stop words
        stop_words = {'the', 'and', 'for', 'with', 'from', 'that', 'this', 'have', 'has', 'was', 'are', 'been'}
        concepts.extend([p for p in identifier_patterns if p not in stop_words])

        # 4. Extract quoted strings (often contain important concepts)
        quoted_strings = re.findall(r'"([^"]+)"', text) + re.findall(r"'([^']+)'", text)
        concepts.extend(quoted_strings)

        # 5. Extract file paths/extensions
        file_patterns = re.findall(r'\b[\w/]+\.(py|json|js|ts|md|txt|yaml|yml)\b', text)
        concepts.extend(file_patterns)

        # 6. Extract arXiv references
        arxiv_patterns = re.findall(r'arXiv:\d+\.\d+', text)
        concepts.extend(arxiv_patterns)

        # Deduplicate and filter out very short or common words
        concepts = list(set(concepts))
        concepts = [c for c in concepts if len(c) > 2 and c.lower() not in stop_words]

        return concepts

    def auto_link_concepts_to_task(self, task_id: str, task_description: str) -> List[str]:
        """
        Auto-extract concepts from a task description and link them to the task node.
        Creates concept nodes if they don't exist and establishes RELATES_TO edges.

        Args:
            task_id: The task node ID to link concepts to
            task_description: The task description text to extract concepts from

        Returns:
            List of concept IDs that were linked
        """
        if task_id not in self.nodes:
            raise ValueError(f"Task node {task_id} not found in graph")

        # Extract concepts from task description
        extracted_concepts = self.extract_concepts(task_description)

        linked_concept_ids = []

        for concept in extracted_concepts:
            # Create or find concept node
            concept_id = f"concept:{concept.lower().replace(' ', '_').replace('.', '_').replace('/', '_')}"

            if concept_id not in self.nodes:
                concept_node = KnowledgeNode(
                    id=concept_id,
                    label=concept,
                    type=NodeType.CONCEPT,
                    properties={"name": concept, "auto_extracted": True}
                )
                self.add_node(concept_node)

            # Create edge from task to concept (if not already exists)
            edge_exists = any(
                e.source == task_id and e.target == concept_id
                for e in self.edges
            )

            if not edge_exists:
                edge = KnowledgeEdge(
                    source=task_id,
                    target=concept_id,
                    relation=EdgeType.RELATES_TO
                )
                self.add_edge(edge)
                linked_concept_ids.append(concept_id)

        return linked_concept_ids

    def link_path_to_outcomes(self, path_id: str, quality: float, task_type: str) -> None:
        """
        Link a solution path to its outcomes (quality score and task type).
        Creates EXPLORED_BY edges to concepts and stores quality/task metadata.

        Args:
            path_id: The SOLUTION_PATH node ID
            quality: Quality score of the path (0.0-1.0)
            task_type: Type of task this path solved
        """
        if path_id not in self.nodes:
            raise ValueError(f"Path node {path_id} not found in graph")

        # Update path properties with outcome data
        path_node = self.nodes[path_id]
        path_node.properties['quality'] = quality
        path_node.properties['task_type'] = task_type

        # Find concepts explored by this path (via RELATES_TO edges)
        for edge in self.edges:
            if edge.source == path_id and edge.relation == EdgeType.RELATES_TO:
                concept_id = edge.target
                # Create EXPLORED_BY edge from concept to path
                explored_edge = KnowledgeEdge(
                    source=concept_id,
                    target=path_id,
                    relation=EdgeType.EXPLORED_BY
                )
                # Check if edge already exists
                if not any(e.source == concept_id and e.target == path_id and e.relation == EdgeType.EXPLORED_BY for e in self.edges):
                    self.add_edge(explored_edge)

        self._auto_save()

    def get_paths_for_concept(self, concept: str) -> List[Dict]:
        """
        Get all solution paths that explored a given concept.

        Args:
            concept: Concept name or ID to query

        Returns:
            List of path dictionaries with id, quality, and task_type
        """
        # Normalize concept to ID format
        if not concept.startswith("concept:"):
            concept_id = f"concept:{concept.lower().replace(' ', '_').replace('.', '_').replace('/', '_')}"
        else:
            concept_id = concept

        if concept_id not in self.nodes:
            return []

        paths = []
        # Find all paths connected via EXPLORED_BY edges
        for edge in self.edges:
            if edge.source == concept_id and edge.relation == EdgeType.EXPLORED_BY:
                path_id = edge.target
                path_node = self.nodes.get(path_id)
                if path_node and path_node.type == NodeType.SOLUTION_PATH:
                    paths.append({
                        'id': path_id,
                        'quality': path_node.properties.get('quality', 0.0),
                        'task_type': path_node.properties.get('task_type', 'unknown'),
                        'label': path_node.label
                    })

        # Sort by quality descending
        paths.sort(key=lambda p: p['quality'], reverse=True)
        return paths

    def get_recommended_path_for_task_type(self, task_type: str) -> Optional[Dict]:
        """
        Get the highest quality path for a given task type.

        Args:
            task_type: Type of task to find recommended path for

        Returns:
            Dictionary with path info or None if no paths found
        """
        # Find all SOLUTION_PATH nodes matching this task type
        matching_paths = []
        for node_id, node in self.nodes.items():
            if node.type == NodeType.SOLUTION_PATH:
                if node.properties.get('task_type') == task_type:
                    matching_paths.append({
                        'id': node_id,
                        'quality': node.properties.get('quality', 0.0),
                        'task_type': task_type,
                        'label': node.label,
                        'properties': node.properties
                    })

        if not matching_paths:
            return None

        # Return highest quality path
        best_path = max(matching_paths, key=lambda p: p['quality'])
        return best_path
