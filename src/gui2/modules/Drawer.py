import networkx as nx
from matplotlib.figure import Figure


class Drawer:

    def draw_graph(self, graph: nx.Graph, size: (int, int)):
        fig = Figure(figsize=size)
        a = fig.add_subplot()
        a.plot()
        pos = nx.circular_layout(graph)
        nx.draw(graph, pos, with_labels=1, ax=a)
        edge_labels = nx.get_edge_attributes(graph, "weight")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels, ax=a)
        margins = {
            "left": 0.001,
            "bottom": 0.001,
            "right": 0.999,
            "top": 0.999
        }
        fig.subplots_adjust(**margins)
        return fig

    def draw_graphic(self, y, size: (int, int)):
        fig = Figure(figsize=size)
        a = fig.add_subplot()
        a.plot(y)
        a.set_xlabel("Номер поколения")
        a.set_ylabel("Лучшая приспособленность в поколении")
        return fig

