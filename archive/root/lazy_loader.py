import knowledge_graph
import demo_injection

class LazyLoader:
    def __init__(self):
        self.knowledge_graph = None
        self.demo_injection = None

    def load_knowledge_graph(self):
        if self.knowledge_graph is None:
            self.knowledge_graph = knowledge_graph.load()
        return self.knowledge_graph

    def inject_demo(self):
        if self.demo_injection is None:
            self.demo_injection = demo_injection.inject()
        return self.demo_injection