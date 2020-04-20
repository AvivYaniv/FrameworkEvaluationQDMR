
class SemanticPreservativeVertexAction:
    @staticmethod
    def check_to_apply(vertex_qdmr):
        pass
    
    @staticmethod
    def apply_on_vertex(vertex_qdmr):
        pass
    
    @staticmethod
    def apply(graph_qdmr):
        for vertex_qdmr in graph_qdmr.vertices_gen():
            if SemanticPreservativeVertexAction.check_to_apply(vertex_qdmr):
                SemanticPreservativeVertexAction.apply_on_vertex(vertex_qdmr)
