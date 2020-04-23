import networkx as nx
import matplotlib.pyplot as plt
import pylab

from GraphQDMR.NetworkX.GraphQDMR2NetworkXConverter import GraphQDMR2NetworkXConverter

class VisualizerQDMR:
    @staticmethod
    def visualize(graph_qdmr):
        nx_graph    = GraphQDMR2NetworkXConverter.convert(graph_qdmr)
        options     = {
            'node_color': 'yellow',
            'node_size': 50,
            'width': 3,
            'edge_color' : 'orange',
            'font_color' : 'green',
            'arrowstyle': '-|>',
            'arrowsize': 20,

            }
        if hasattr(graph_qdmr, 'raw_question'):
            raw_question = graph_qdmr.raw_question
            plt.title(raw_question)
        pos = nx.circular_layout(nx_graph)
        nx.draw_networkx(nx_graph, pos=pos, arrows=True, **options)
        x_values, y_values = zip(*pos.values())
        x_max = max(x_values)
        x_min = min(x_values)
        x_margin = (x_max - x_min) * 0.25
        plt.xlim(x_min - x_margin, x_max + x_margin)
        plt.get_current_fig_manager().window.state('zoomed')
        plt.show()
