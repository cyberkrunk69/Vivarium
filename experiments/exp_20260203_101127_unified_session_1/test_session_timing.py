
import sys
sys.path.append('D:\codingProjects\claude_parasite_brain_suck')
import time
from pathlib import Path

start = time.perf_counter()

# Test safety imports
try:
    from safety_sandbox import initialize_sandbox
    print(f"safety_sandbox: {time.perf_counter() - start:.3f}s")
except ImportError as e:
    print(f"safety_sandbox: MISSING - {e}")

safety_time = time.perf_counter()
try:
    from safety_gateway import SafetyGateway
    from safety_sanitize import sanitize_task
    from safety_killswitch import get_kill_switch
    from safety_network import scan_for_network_access
    print(f"safety modules: {time.perf_counter() - safety_time:.3f}s")
except ImportError as e:
    print(f"safety modules: MISSING - {e}")

kg_time = time.perf_counter()
try:
    from knowledge_graph import KnowledgeGraph
    kg = KnowledgeGraph()
    kg_file = Path('D:\codingProjects\claude_parasite_brain_suck') / 'knowledge_graph.json'
    if kg_file.exists():
        kg.load_json(str(kg_file))
    print(f"knowledge graph: {time.perf_counter() - kg_time:.3f}s")
except Exception as e:
    print(f"knowledge graph: FAILED - {e}")

total = time.perf_counter() - start
print(f"Total simulation: {total:.3f}s")
