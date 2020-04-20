import networkx as nx
import matplotlib.pyplot as plt
import pylab

from GraphQDMR.NetworkX.GraphQDMR2NetworkXConverter import GraphQDMR2NetworkXConverter

class VisualizerQDMR:
    @staticmethod
    def visualize(graph_qdmr):
        nx_graph    = GraphQDMR2NetworkXConverter.convert(graph_qdmr)
        options     = {
            'node_color': 'blue',
            'node_size': 50,
            'width': 3,
            'edge_color' : 'green',
            'font_color' : 'red',
            'arrowstyle': '-|>',
            'arrowsize': 20,
            }
        nx.draw_networkx(nx_graph, arrows=True, **options)
        pylab.show()
