import networkx as nx

class GraphQDMR2NetworkXConverter:
    @staticmethod
    def convert_vertex(vertex_qdmr):
        return str(vertex_qdmr)
    
    @staticmethod
    def convert(graph_qdmr):
        G = nx.DiGraph(directed=True)
        for v in graph_qdmr.vertices.values():
            current_vertex_converted = GraphQDMR2NetworkXConverter.convert_vertex(v)
            G.add_node(current_vertex_converted)
            for in_v in v.incoming:
                incoming_vertex_converted = GraphQDMR2NetworkXConverter.convert_vertex(in_v)
                G.add_edge(incoming_vertex_converted, current_vertex_converted)
        return G
    