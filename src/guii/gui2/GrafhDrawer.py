import networkx as nx
from matplotlib.figure import Figure

class GrafhDrawer:

    def draw(self, graph: nx.Graph):
        fig = Figure(figsize=(7, 7))
        a = fig.add_subplot(111)
        a.plot()
        pos = nx.circular_layout(graph)
        nx.draw(graph, pos, with_labels=1, ax=a)
        edge_labels = nx.get_edge_attributes(graph, "weight")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels, ax=a)
        margins = {
            "left": 0.01,
            "bottom": 0.01,
            "right": 0.990,
            "top": 0.990
        }
        fig.subplots_adjust(**margins)
        return fig