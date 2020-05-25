from abc import abstractmethod
from GraphQDMR.UnifyGraphQDMR.utils import *
from GraphQDMR import *

class SemanticPreservativeVertexAction:
    """
    Semantic preservative action for SINGLE vertex
    """

    @abstractmethod
    def check_to_apply(vertex_qdmr):
        pass

    @abstractmethod
    def apply_on_vertex(vertex_qdmr):
        pass
    
    def apply(self, graph_qdmr):
        """
        Iterate over QDMR graph vertices one by one, 
        and apply action on vertices if needed
        """
        for vertex_qdmr in graph_qdmr.vertices_gen():
            if self.check_to_apply(vertex_qdmr):
                self.apply_on_vertex(vertex_qdmr)


class SortVertexAttributes(SemanticPreservativeVertexAction):
    @staticmethod
    def check_to_apply(vertex_qdmr):
        return vertex_qdmr.operation in [ OperationQDMR.UNION, OperationQDMR.INTERSECTION, OperationQDMR.BOOLEAN]

    @staticmethod
    def apply_on_vertex(vertex_qdmr):
        vertex_qdmr.incoming.sort( key = cmp_to_key(VertexQDMR.compare))












'''
from ParserQDMR.GoldParserQDMR import GoldParserQDMR #GoldParserQDMR

def test(decomposition, operators):
    g = GoldParserQDMR.parse(decomposition, operators)
    print(g)
    SortVertexAttributes().apply(g)
    print(g)

if __name__ == '__main__':

    decomposition = "return authors ;return #1 that  have cooperated with  H. V. Jagadish ;return #1 that  have cooperated with  Divesh Srivastava ;return #2 ,  #3"
    operators = "['select', 'filter', 'filter', 'union']"
    test(decomposition, operators)

    print('Done')
'''