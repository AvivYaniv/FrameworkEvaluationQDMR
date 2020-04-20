
from GraphQDMR import *
from VisualizerQDMR import *
from ParserQDMR import *
from ReaderQDMR.GoldReader import GoldReader

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
    
if '__main__' == __name__:
    graphs = GoldReader.read_file_qdmr_graphs(GoldReader.TRAIN_QUESTIONS_FILE_NAME)
    for g in graphs:
        VisualizerQDMR.visualize(g)
    