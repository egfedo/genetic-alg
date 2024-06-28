import networkx as nx
from matplotlib.figure import Figure
import matplotlib

class GraphDrawer:

    def draw(self, matr: [[int]]):
        g = nx.Graph()
        for i in range(len(matr)):
            g.add_node(str(i+1))
        for i in range(len(matr)):
            for j in range(i):
                el = matr[i][j]
                if el:
                    g.add_edge(str(i+1), str(j+1), weight=matr[i][j])

        fig = Figure(figsize=(3, 3), facecolor='black', frameon=False)
        a = fig.add_subplot(111)
        a.plot()
        pos = nx.circular_layout(g)
        nx.draw(g, pos, with_labels=1, ax=a)
        edge_labels = nx.get_edge_attributes(g, "weight")
        nx.draw_networkx_edge_labels(g, pos, edge_labels, ax=a)
        margins = {
            "left": 0.01,
            "bottom": 0.01,
            "right": 0.990,
            "top": 0.990
        }
        fig.subplots_adjust(**margins)
        return fig


g = GraphDrawer()
g.draw([[1, 1], [1, 1]])