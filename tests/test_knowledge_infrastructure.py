"""
Knowledge Infrastructure Tests

Tests for embedding similarity, KG persistence, concept extraction,
context building, and query expansion.
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_graph import (
    KnowledgeGraph, KnowledgeNode, KnowledgeEdge,
    NodeType, EdgeType
)
from context_builder import ContextBuilder, build_context
from query_expander import expand_query, get_expansion_log


class TestEmbeddingSimilarity(unittest.TestCase):
    """Test embedding-based similarity search for skills."""

    def setUp(self):
        """Set up test environment."""
        self.workspace = Path(__file__).parent.parent

    def test_skill_registry_similarity_search(self):
        """Test that skill registry can find similar skills."""
        # Import here to avoid dependencies during setup
        from skills.skill_registry import _registry as skill_registry

        # Ensure registry has skills loaded
        if not skill_registry.skills:
            skill_registry.load_from_directory(self.workspace / "skills")

        # Test similarity search
        query = "implement error handling"
        results = skill_registry.find_similar_skills(query, top_k=3)

        # Verify results structure
        self.assertIsInstance(results, list)
        if results:  # If there are skills loaded
            self.assertLessEqual(len(results), 3)
            for skill_name, score in results:
                self.assertIsInstance(skill_name, str)
                self.assertIsInstance(score, (int, float))
                self.assertGreaterEqual(score, 0.0)
                self.assertLessEqual(score, 1.0)

    def test_embedding_similarity_calculation(self):
        """Test that embeddings produce meaningful similarity scores."""
        from skills.skill_registry import _registry as skill_registry

        # Load skills if not already loaded
        if not skill_registry.skills:
            skill_registry.load_from_directory(self.workspace / "skills")

        if not skill_registry.skills:
            self.skipTest("No skills loaded for testing")

        # Test that same query twice yields same results
        query = "error handling function"
        results1 = skill_registry.find_similar_skills(query, top_k=2)
        results2 = skill_registry.find_similar_skills(query, top_k=2)

        self.assertEqual(results1, results2, "Similarity search should be deterministic")

    def test_embedding_file_persistence(self):
        """Test that skill embeddings are persisted to disk."""
        embedding_file = self.workspace / "skill_embeddings.json"

        # Check if embeddings file exists
        from skills.skill_registry import _registry as skill_registry

        if not skill_registry.skills:
            skill_registry.load_from_directory(self.workspace / "skills")

        # If skills exist and embeddings are generated, they should be persisted
        if skill_registry.skills:
            # Embeddings are auto-generated and saved during similarity search
            query = "test query"
            skill_registry.find_similar_skills(query, top_k=1)
            # After similarity search, embeddings file should exist
            self.assertTrue(embedding_file.exists() or len(skill_registry.skills) == 0,
                          "Embeddings should be saved to disk after similarity search")


class TestKGPersistence(unittest.TestCase):
    """Test knowledge graph save/load functionality."""

    def setUp(self):
        """Create temporary file for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.kg_path = self.temp_file.name

    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.kg_path):
            os.remove(self.kg_path)

    def test_kg_save_and_load(self):
        """Test that KG can save to file and load correctly."""
        # Create KG with test data
        kg1 = KnowledgeGraph(self.kg_path)

        # Add test nodes
        node1 = KnowledgeNode(
            id="test:node1",
            label="Test Node 1",
            type=NodeType.CONCEPT,
            properties={"key": "value"}
        )
        node2 = KnowledgeNode(
            id="test:node2",
            label="Test Node 2",
            type=NodeType.SKILL,
            properties={}
        )

        kg1.add_node(node1)
        kg1.add_node(node2)

        # Add edge
        edge = KnowledgeEdge(
            source="test:node1",
            target="test:node2",
            relation=EdgeType.RELATES_TO
        )
        kg1.add_edge(edge)

        # Save explicitly (though auto-save should have triggered)
        kg1.save_to_file(self.kg_path)

        # Create new KG instance and load
        kg2 = KnowledgeGraph(self.kg_path)

        # Verify nodes loaded correctly
        self.assertEqual(len(kg2.nodes), 2)
        self.assertIn("test:node1", kg2.nodes)
        self.assertIn("test:node2", kg2.nodes)

        loaded_node1 = kg2.nodes["test:node1"]
        self.assertEqual(loaded_node1.label, "Test Node 1")
        self.assertEqual(loaded_node1.type, NodeType.CONCEPT)
        self.assertEqual(loaded_node1.properties, {"key": "value"})

        # Verify edges loaded correctly
        self.assertEqual(len(kg2.edges), 1)
        self.assertEqual(kg2.edges[0].source, "test:node1")
        self.assertEqual(kg2.edges[0].target, "test:node2")
        self.assertEqual(kg2.edges[0].relation, EdgeType.RELATES_TO)

    def test_kg_auto_save(self):
        """Test that KG auto-saves after modifications."""
        kg = KnowledgeGraph(self.kg_path)

        # Add node (should trigger auto-save)
        node = KnowledgeNode(
            id="test:autosave",
            label="Auto Save Test",
            type=NodeType.CONCEPT
        )
        kg.add_node(node)

        # Verify file was written
        self.assertTrue(os.path.exists(self.kg_path))

        # Verify content is valid JSON
        with open(self.kg_path, 'r') as f:
            data = json.load(f)

        self.assertIn("nodes", data)
        self.assertIn("test:autosave", data["nodes"])

    def test_kg_auto_load(self):
        """Test that KG auto-loads from file at initialization."""
        # Create and save KG
        kg1 = KnowledgeGraph(self.kg_path)
        node = KnowledgeNode(
            id="test:autoload",
            label="Auto Load Test",
            type=NodeType.LESSON
        )
        kg1.add_node(node)
        kg1.save_to_file(self.kg_path)

        # Create new instance - should auto-load
        kg2 = KnowledgeGraph(self.kg_path)

        # Verify node was auto-loaded
        self.assertIn("test:autoload", kg2.nodes)
        self.assertEqual(kg2.nodes["test:autoload"].label, "Auto Load Test")


class TestConceptExtraction(unittest.TestCase):
    """Test concept extraction from lessons and text."""

    def test_extract_concepts_from_lesson(self):
        """Test that real concepts are extracted from lesson text."""
        kg = KnowledgeGraph()

        lesson_text = """
        Implemented CAMEL role-based decomposition using arXiv:2303.17760.
        The system now uses DSPy for prompt optimization and Voyager-style
        skill injection to improve performance. Knowledge graph integration
        helps with few-shot learning and reflection.
        """

        concepts = kg.extract_concepts_from_lesson(lesson_text)

        # Verify concepts were extracted
        self.assertIsInstance(concepts, list)
        self.assertGreater(len(concepts), 0, "Should extract at least one concept")

        # Verify specific concepts were found
        expected_concepts = ["CAMEL", "DSPy", "Voyager", "knowledge graph", "few-shot", "reflection"]
        found_concepts = [c for c in expected_concepts if c in concepts]
        self.assertGreater(len(found_concepts), 0, "Should find known concepts")

    def test_extract_arxiv_references(self):
        """Test that arXiv references are extracted as concepts."""
        kg = KnowledgeGraph()

        lesson_text = "Based on arXiv:2303.17760 and arXiv:2305.16291 papers"
        concepts = kg.extract_concepts_from_lesson(lesson_text)

        # Check for arXiv references
        arxiv_refs = [c for c in concepts if "arXiv" in c]
        self.assertGreater(len(arxiv_refs), 0, "Should extract arXiv references")

    def test_no_duplicate_concepts(self):
        """Test that duplicate concepts are removed."""
        kg = KnowledgeGraph()

        lesson_text = "DSPy optimization with DSPy prompts using DSPy framework"
        concepts = kg.extract_concepts_from_lesson(lesson_text)

        # Verify no duplicates
        self.assertEqual(len(concepts), len(set(concepts)), "Should not have duplicate concepts")

    def test_link_lesson_to_concepts(self):
        """Test that lessons can be linked to extracted concepts."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        temp_file.close()
        kg_path = temp_file.name

        try:
            kg = KnowledgeGraph(kg_path)

            # Add lesson node
            lesson_id = kg.add_lesson_node({
                "id": "lesson_test_1",
                "lesson": "Use DSPy for prompt optimization",
                "task_category": "optimization",
                "importance": 8
            })

            # Link to concepts
            concepts = ["DSPy", "prompt optimization"]
            kg.link_lesson_to_concepts(lesson_id, concepts)

            # Verify concept nodes were created
            self.assertIn("concept:dspy", kg.nodes)
            self.assertIn("concept:prompt_optimization", kg.nodes)

            # Verify edges exist
            edges_from_lesson = [e for e in kg.edges if e.source == lesson_id]
            self.assertEqual(len(edges_from_lesson), 2, "Should have 2 edges to concepts")

        finally:
            if os.path.exists(kg_path):
                os.remove(kg_path)


class TestContextBuilder(unittest.TestCase):
    """Test context builder combines multiple sources."""

    def setUp(self):
        """Set up test workspace."""
        self.workspace = Path(__file__).parent.parent
        self.temp_dir = tempfile.mkdtemp()

    def test_context_builder_initialization(self):
        """Test that context builder initializes correctly."""
        builder = ContextBuilder(self.workspace)

        self.assertIsNotNone(builder.kg)
        self.assertIsInstance(builder.context_parts, list)
        self.assertEqual(len(builder.context_parts), 0)

    def test_add_skills_to_context(self):
        """Test adding skills to context."""
        builder = ContextBuilder(self.workspace)

        # Add skills
        builder.add_skills("implement error handling", top_k=2)

        # Verify context was added
        if builder.context_parts:  # If skills were found
            context = builder.build()
            self.assertIn("VOYAGER SKILL INJECTION", context)
            self.assertIn("RELEVANT SKILL", context)

    def test_add_kg_context(self):
        """Test adding knowledge graph context."""
        # Create temp KG with test data
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        temp_file.close()
        kg_path = temp_file.name

        try:
            kg = KnowledgeGraph(kg_path)

            # Add test nodes
            kg.add_typed_node("context_builder", NodeType.FUNCTION, {"file": "context_builder.py"})
            kg.add_typed_node("knowledge_graph", NodeType.CONCEPT)

            builder = ContextBuilder(Path(kg_path).parent)
            builder.kg = kg  # Use test KG

            # Add KG context
            builder.add_kg_context("context builder implementation")

            # Build and verify
            context = builder.build()
            if context:  # If matches were found
                self.assertIn("KNOWLEDGE GRAPH CONTEXT", context)

        finally:
            if os.path.exists(kg_path):
                os.remove(kg_path)

    def test_context_builder_chaining(self):
        """Test that context builder methods can be chained."""
        builder = ContextBuilder(self.workspace)

        # Chain methods
        result = builder.add_skills("test query").add_kg_context("test query").reset()

        # Verify chaining returns self
        self.assertIsInstance(result, ContextBuilder)

        # Verify reset cleared context
        self.assertEqual(len(builder.context_parts), 0)

    def test_build_context_convenience_function(self):
        """Test the convenience function for building context."""
        context = build_context(
            "error handling implementation",
            workspace=self.workspace,
            include_skills=True,
            include_lessons=True,
            include_kg=True
        )

        # Verify context is a string (may be empty if no matches)
        self.assertIsInstance(context, str)


class TestQueryExpansion(unittest.TestCase):
    """Test query expansion improves retrieval."""

    def test_expand_query_basic(self):
        """Test basic query expansion."""
        query = "fix error in function"
        expanded = expand_query(query)

        # Verify expansion
        self.assertIsInstance(expanded, list)
        self.assertGreater(len(expanded), len(query.split()), "Should expand to more terms")

        # Should include original query words (as separate terms)
        self.assertIn("fix", expanded)
        self.assertIn("error", expanded)
        self.assertIn("function", expanded)

    def test_expand_query_with_synonyms(self):
        """Test that synonyms are added."""
        query = "optimize performance"
        expanded = expand_query(query)

        # Check for synonyms
        self.assertIn("optimize", [t for t in expanded if "optimize" in t] or expanded)

        # Should have related terms
        potential_synonyms = ["improve", "enhance", "speed", "efficiency"]
        has_synonym = any(syn in expanded for syn in potential_synonyms)
        self.assertTrue(has_synonym, "Should include at least one synonym")

    def test_expand_query_extracts_keywords(self):
        """Test that keywords are extracted (3+ chars)."""
        query = "implement a new test for the API endpoint"
        expanded = expand_query(query)

        # Should extract keywords
        expected_keywords = ["implement", "test", "api", "endpoint"]
        for keyword in expected_keywords:
            self.assertIn(keyword, expanded, f"Should extract keyword: {keyword}")

    def test_expand_query_no_short_words(self):
        """Test that short words (< 3 chars) are not extracted as keywords."""
        query = "fix a bug in my code"
        expanded = expand_query(query)

        # Should not include short words as separate keywords
        self.assertNotIn("a", expanded)
        self.assertNotIn("in", expanded)
        self.assertNotIn("my", expanded)

    def test_expansion_log_formatting(self):
        """Test expansion log message formatting."""
        original = "test query"
        expanded = expand_query(original)

        log_msg = get_expansion_log(original, expanded)

        # Verify log format
        self.assertIsInstance(log_msg, str)
        self.assertIn(original, log_msg)
        self.assertIn("QUERY EXPANSION", log_msg)
        self.assertIn("Expanded terms count", log_msg)

    def test_query_expansion_improves_retrieval(self):
        """Test that expanded queries improve retrieval coverage."""
        # Original narrow query
        narrow_query = "refactor"
        narrow_expanded = expand_query(narrow_query)

        # Broader query with context
        broad_query = "refactor code structure"
        broad_expanded = expand_query(broad_query)

        # Broader query should have more terms
        self.assertGreater(
            len(broad_expanded),
            len(narrow_expanded),
            "More specific queries should expand to more terms"
        )


if __name__ == "__main__":
    unittest.main()
