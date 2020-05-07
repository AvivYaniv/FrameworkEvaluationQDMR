
from GraphQDMR import *
from GraphQDMR.UnifyGraphQDMR.SemanticPreservativeStructureAction import *
from GraphQDMR.EvaluatorQDMR.GraphMatcherQDMR.NormalStringReprGraphMatcherQDMR import *
from VisualizerQDMR import *
from ParserQDMR import *
from ReaderQDMR.GoldReader import GoldReader

def example_graph_0_1():
    v1 = VertexQDMR(OperationQDMR.SELECT,       'return ball')
    v2 = VertexQDMR(OperationQDMR.PROJECT,      'return {} that is partially hidden by ball')
    v3 = VertexQDMR(OperationQDMR.PROJECT,      'return shape of {}')
    
    g = GraphQDMR()
    
    vid_v1 = g.add_vertex(v1)
    vid_v2 = g.add_vertex(v2)
    vid_v3 = g.add_vertex(v3)
    
    g.add_edge(vid_v1, vid_v2)
    g.add_edge(vid_v2, vid_v3)
    
    VisualizerQDMR.visualize(g)
    
    return g

def example_graph_0_2():
    v1 = VertexQDMR(OperationQDMR.SELECT,       'return object')
    v2 = VertexQDMR(OperationQDMR.PROJECT,      'return {} that is partially hidden by a ball')
    v3 = VertexQDMR(OperationQDMR.PROJECT,      'return shape of {}')
    
    g = GraphQDMR()
    
    vid_v1 = g.add_vertex(v1)
    vid_v2 = g.add_vertex(v2)
    vid_v3 = g.add_vertex(v3)
    
    g.add_edge(vid_v1, vid_v2)
    g.add_edge(vid_v2, vid_v3)
    
    VisualizerQDMR.visualize(g)
    
    return g

def example_graph_1_1():
    v1 = VertexQDMR(OperationQDMR.SELECT,       'return ball')
    v2 = VertexQDMR(OperationQDMR.SELECT,       'return object')
    v3 = VertexQDMR(OperationQDMR.PROJECT,      'return {} that is partially hidden by {}')
    v4 = VertexQDMR(OperationQDMR.PROJECT,      'return shape of {}')
    
    g = GraphQDMR()
    
    vid_v1 = g.add_vertex(v1)
    vid_v2 = g.add_vertex(v2)
    vid_v3 = g.add_vertex(v3)
    vid_v4 = g.add_vertex(v4)
    
    g.add_edge(vid_v2, vid_v3)
    g.add_edge(vid_v1, vid_v3)
    g.add_edge(vid_v3, vid_v4)
    
    print(g)
    print("Multiline Normal String Representation:")
    print(NormalStringReprBuilderQDMR(g, multiline=True).build())
    print()

    VisualizerQDMR.visualize(g)
    
    return g

def example_graph_1_2():
    v1 = VertexQDMR(OperationQDMR.SELECT,       'return object')
    v2 = VertexQDMR(OperationQDMR.SELECT,       'return ball')
    v3 = VertexQDMR(OperationQDMR.PROJECT,      'return {} that is partially hidden by {}')
    v4 = VertexQDMR(OperationQDMR.PROJECT,      'return shape of {}')
    
    g = GraphQDMR()
    
    vid_v1 = g.add_vertex(v1)
    vid_v2 = g.add_vertex(v2)
    vid_v3 = g.add_vertex(v3)
    vid_v4 = g.add_vertex(v4)
    
    g.add_edge(vid_v1, vid_v3)
    g.add_edge(vid_v2, vid_v3)
    g.add_edge(vid_v3, vid_v4)
    
    print(g)
    print("NOT Multiline Normal String Representation:")
    print(NormalStringReprBuilderQDMR(g, multiline=False).build())
    print()

    VisualizerQDMR.visualize(g)
    
    return g

def example_graph_1():
    v1 = VertexQDMR(OperationQDMR.SELECT,       'return papers')
    v2 = VertexQDMR(OperationQDMR.FILTER,       'return {} in ACL')
    v3 = VertexQDMR(OperationQDMR.PROJECT,      'return keywords of {}')
    v4 = VertexQDMR(OperationQDMR.GROUP,        'return number of {} for each {}')
    v5 = VertexQDMR(OperationQDMR.COMPARATIVE,  'return {} where {} is more than 100')
    
    g = GraphQDMR()
    
    vid_v1 = g.add_vertex(v1)
    vid_v2 = g.add_vertex(v2)
    vid_v3 = g.add_vertex(v3)
    vid_v4 = g.add_vertex(v4)
    vid_v5 = g.add_vertex(v5)
    
    g.add_edge(vid_v1, vid_v2)
    g.add_edge(vid_v2, vid_v3)
    g.add_edge(vid_v2, vid_v4)
    g.add_edge(vid_v3, vid_v4)
    g.add_edge(vid_v3, vid_v5)
    g.add_edge(vid_v4, vid_v5)
    
    print(g)
    print("Multiline Normal String Representation:")
    print(NormalStringReprBuilderQDMR(g, multiline=True).build())
    print()
    
    return g
    
def example_graph_2():
    v1 = VertexQDMR(OperationQDMR.SELECT,       'return phone number of  1031 Daugavpils Parkway')
    v2 = VertexQDMR(OperationQDMR.SELECT,       'return postal code of  1031 Daugavpils Parkway')
    v3 = VertexQDMR(OperationQDMR.UNION,        'return {} ,  {}')
    
    g = GraphQDMR()
    
    vid_v1 = g.add_vertex(v1)
    vid_v2 = g.add_vertex(v2)
    vid_v3 = g.add_vertex(v3)
    
    g.add_edge(vid_v1, vid_v3)
    g.add_edge(vid_v2, vid_v3)
    
    print(g)
    
def convert_graph_1():
    decomposition   = 'return bookstores ;return number of  #1 ;return if  #2 is equal to  two ;return light ;return #4 that is bright ;return windows of #1 ;return #1 where  #5 is visible through #6 ;return number of  #7 ;return if  #8 is at least one ;return if  both  #3 and #9 are true'
    operators_list  = ['select', 'aggregate', 'boolean', 'select', 'filter', 'project', 'comparative', 'aggregate', 'boolean', 'boolean']
    graph           = GoldParserQDMR.parse(decomposition, operators_list)
    print(graph)
    return graph

def check_percentage_of_structure_actions(graphs):
    total_graphs = 0
    filter_chain_n = 0
    project_chain_n = 0
    excpetions_graphs = 0

    for g in graphs:
        total_graphs += 1
        try:
            # print(NormalStringReprBuilderQDMR(g, multiline=False).build())
            if UnifyFilterChains.apply(g):
                filter_chain_n += 1
                # print("\n------------------------", NormalStringReprBuilderQDMR(g, multiline=False).build())
            if UnifyProjectChains.apply(g):
                project_chain_n += 1

        except Exception as e:
            if not str(e).startswith("Logical Error"):
                print("\n***********************************\n", "\t\t", e, "\n***********************************\n")
            excpetions_graphs += 1

    print("Total: ", total_graphs)
    print("Filter Chain: ", filter_chain_n)
    print("Filter Chain percentage: ", filter_chain_n / total_graphs)
    print("Project Chain: ", project_chain_n)
    print("Project Chain percentage: ", project_chain_n / total_graphs)
    print("Exeption graphs: ", excpetions_graphs)

if '__main__' == __name__:
    '''
    g1 = example_graph_1_1()
    g2 = example_graph_1_2()

    if NormalStringGraphMatcherQDMR.check(g1, g2):
        print("*** Graphs 1.1 and 1.2 match :) ***")
    else:
        raise Exception("Graphs 1.1 and 1.2 don't match")

    print()
    print()
    print()

    example_graph_1()
'''
    
    graphs = GoldReader.read_file_qdmr_graphs("train.csv")

    check_percentage_of_structure_actions(graphs)
    #graphs = GoldReader.read_file_qdmr_graphs(GoldReader.TRAIN_QUESTIONS_FILE_NAME)
    #for g in graphs:
    #    VisualizerQDMR.visualize(g)