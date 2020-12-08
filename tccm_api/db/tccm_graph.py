from py2neo import Relationship, Node, NodeMatcher, Cursor, Subgraph, Graph


class TccmGraph:
    def __init__(self, graph: Graph):
        self.graph = graph

    def get_concept(self, uri):
        return NodeMatcher(self.graph).match('Concept').where(f"_.uri='{uri}'").first()
