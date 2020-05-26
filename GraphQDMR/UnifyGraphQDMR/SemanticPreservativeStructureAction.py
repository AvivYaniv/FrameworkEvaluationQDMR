from GraphQDMR import *
from VisualizerQDMR import VisualizerQDMR


class SemanticPreservativeStructureAction:
   
    @staticmethod
    def apply(graph_qdmr : GraphQDMR):
       pass


class UnifyFilterChains(SemanticPreservativeStructureAction):

    @staticmethod
    def dfsUtil(graph_qdmr : GraphQDMR, visited_dict : dict, vertex_qdmr : VertexQDMR) -> bool:
        found = False
        if vertex_qdmr in visited_dict:
            return False
        else:
            visited_dict[vertex_qdmr] = True
            if vertex_qdmr.operation == OperationQDMR.FILTER and vertex_qdmr.outgoing.__len__() == 1 and vertex_qdmr.incoming.__len__() == 1: #sanity check
                child_vertex = vertex_qdmr.outgoing[0]
                if child_vertex.operation == OperationQDMR.FILTER and child_vertex.incoming.__len__() == 1: # found chain
                    child_vertex.set_incoming(vertex_qdmr.incoming)
                    child_vertex.merge_step_desc(vertex_qdmr.step_desc)
                    graph_qdmr.remove_vertex(vertex_qdmr)
                    UnifyFilterChains.dfsUtil(graph_qdmr, visited_dict, child_vertex)
                    return True

            for adjacent_vertex in vertex_qdmr.outgoing_gen():
                found |= UnifyFilterChains.dfsUtil(graph_qdmr, visited_dict, adjacent_vertex)
            return found

    @staticmethod
    def apply(graph_qdmr : GraphQDMR):
        found = False
        visited_dict = {}
        for vertex_qdmr in graph_qdmr.vertices_gen():
            found |= UnifyFilterChains.dfsUtil(graph_qdmr, visited_dict, vertex_qdmr)
        return found




from ParserQDMR.GoldParserQDMR import GoldParserQDMR #GoldParserQDMR

def test(decomposition, operators):
    g = GoldParserQDMR.parse(decomposition, operators)
    print(g)
    #VisualizerQDMR.visualize(g)

    print(UnifyFilterChains.apply(g))

    print(g)
    #VisualizerQDMR.visualize(g)


if __name__ == '__main__':
    decomposition = "return cubes ;return #1 that  are purple ;return #1 that  #2 is  to the right of ;return if  #3 is  shiny ;return if  #3 is  matte ;return #4 , #5"
    operators = "['select', 'filter', 'filter', 'boolean', 'boolean', 'union']"
    test(decomposition, operators)

'''
    decomposition = "return flights ;return #1 that  are one way ;return #2 from atlanta ;return #3 to  pittsburgh ;return fares of #4 ;return #5 that  are the  lowest"
    operators = "['select', 'filter', 'filter', 'filter', 'project', 'filter']"
    test(decomposition, operators)

    decomposition = "return papers ;return #1 from  VLDB conference ;return #2 before 1995 ;return #2 after 2002 ;return #3 ,  #4 ;return authors of  #5"
    operators = "['select', 'filter', 'filter', 'filter', 'union', 'project']"
    test(decomposition, operators)

    decomposition = "return papers ;return #1 by H. V. Jagadish ;return #2 on  PVLDB ;return #3 after 2000"
    operators = "['select', 'filter', 'filter', 'filter']"
    test(decomposition, operators)

    decomposition = "return papers ;return #1 by H. V. Jagadish ;return #2 on  PVLDB ;return #3 after 2000 ;return number of  #4"
    operators = "['select', 'filter', 'filter', 'filter', 'aggregate']"
    test(decomposition, operators)
'''

