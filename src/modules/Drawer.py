import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.figure import Figure
import matplotlib.axes

def draw_graph(graph: nx.Graph, size: (int, int), subgraph: nx.Graph = None):
    fig = Figure(figsize=size)
    a = fig.add_subplot()
    a.plot()
    pos = nx.circular_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=1, ax=a)
    edge_labels = nx.get_edge_attributes(graph, "weight")
    if subgraph is not None:
        pos = nx.circular_layout(subgraph)
        nx.draw_networkx_edges(subgraph, pos, ax=a, width=2.75)

    nx.draw_networkx_edge_labels(graph, pos, edge_labels, ax=a)
    margins = {
        "left": 0.0001,
        "bottom": 0.0001,
        "right": 0.9999,
        "top": 0.9999
    }
    fig.subplots_adjust(**margins)
    return fig


def draw_graphic(y, size: (int, int), y_second=None, full_size=None):
    fig = Figure(figsize=size)
    a = fig.add_subplot()
    lowest_len = full_size if full_size is not None else len(y)
    tick_dist = lowest_len // 4
    # a.set_xticks([i * tick_dist for i in range(5)] + [lowest_len])
    a.set_xlim([-3, lowest_len])
    a.plot(y, marker='o', markersize=2, linewidth=2, label='лучш.')
    if y_second is not None:
        a.plot(y_second, marker='o', markersize=2, linewidth=2, label='сред.')

    a.legend()
    a.set_xlabel("Номер поколения")
    a.set_ylabel("Приспособленность в поколении")
    return fig

