from GraphQDMR import *

class SemanticPreservativeVertexAction:
    """
    Semantic preservative action for SINGLE vertex
    """
    
    @staticmethod
    def check_to_apply(vertex_qdmr):
        pass
    
    @staticmethod
    def apply_on_vertex(vertex_qdmr):
        pass
    
    @staticmethod
    def apply(graph_qdmr):
        """
        Iterate over QDMR graph vertices one by one, 
        and apply action on vertices if needed
        """
        for vertex_qdmr in graph_qdmr.vertices_gen():
            if SemanticPreservativeVertexAction.check_to_apply(vertex_qdmr):
                SemanticPreservativeVertexAction.apply_on_vertex(vertex_qdmr)


class SortVertexAttributes(SemanticPreservativeVertexAction):
    @staticmethod
    def check_to_apply(vertex_qdmr):
        return True

    @staticmethod
    def apply_on_vertex(vertex_qdmr):
        vertex_qdmr.step_desc.sort()
        vertex_qdmr.incoming.sort(key = VertexQDMR.get_key_for_lexicographic_comparator)
