from GraphQDMR import GraphQDMR, VertexQDMR, OperationQDMR
from VisualizerQDMR import VisualizerQDMR
import networkx as nx


class GraphNetworkX2QDMRConverter:
    @staticmethod
    def convert_vertex(vertex_networkx):
        # TODO fix this function
        return VertexQDMR(OperationQDMR.SELECT, str(vertex_networkx))

    @staticmethod
    def get_vids(edge):

    @staticmethod
    def convert(graph_networkx):
        G = GraphQDMR()
        vid_to_vertex_dict = dict()
        for v in graph_networkx.nodes():
            current_vertex_converted = GraphNetworkX2QDMRConverter.convert_vertex(v)
            vid = G.add_vertex(current_vertex_converted)
            vid_to_vertex_dict[vid] = current_vertex_converted

        for edge in graph_networkx.out_edges():
            incoming_vertex_converted, current_vertex_converted = GraphNetworkX2QDMRConverter.get_vids(edge)
            G.add_edge(incoming_vertex_converted, current_vertex_converted)
        return G



def create_temp_qdmr_graph():
    # TODO remove
    v1 = VertexQDMR(OperationQDMR.SELECT, 'return papers')
    v2 = VertexQDMR(OperationQDMR.FILTER, 'return {} in ACL')
    v3 = VertexQDMR(OperationQDMR.PROJECT, 'return keywords of {}')
    v4 = VertexQDMR(OperationQDMR.GROUP, 'return numbeddr of {} for each {}')
    v5 = VertexQDMR(OperationQDMR.COMPARATIVE, 'return {} where {} is more than 100')

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
    return g

def create_simple_qdmr_graph():
    # TODO remove
    v1 = VertexQDMR(OperationQDMR.SELECT, 'return papers')
    v2 = VertexQDMR(OperationQDMR.FILTER, 'return {} in ACL')

    g = GraphQDMR()

    vid_v1 = g.add_vertex(v1)
    vid_v2 = g.add_vertex(v2)

    g.add_edge(vid_v1, vid_v2)

    return g

if '__main__' == __name__:
    # TODO remove
    print("banana")
    g_qdmr_input = create_simple_qdmr_graph()
    g_nx = VisualizerQDMR.visualize(g_qdmr_input)
    g_qdmr_output = GraphNetworkX2QDMRConverter.convert(g_nx)