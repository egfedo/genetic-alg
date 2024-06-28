import copy
import time

import networkx as nx
import random

class Solver:

    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.nodes = list(graph.nodes)
        self.edges = list(graph.edges)
        self.edge_no = dict(zip(self.edges, [i for i in range(len(self.edges))]))

    def compare_edges(self, e1: tuple, e2: tuple):
        return (e1[0] == e2[0] and e1[1] == e2[1]) or (e1[0] == e2[1] and e1[1] == e2[0])

    # def rand_walk(self, allowed_edges: set = None):
    #     visited = [False * len(self.nodes)]
    #     tree = set()
    #     curr = 0
    #     adj = self.graph.adja
    #     while len(tree) < len(self.nodes) - 1:

    def random_prim(self, subgraph_set: set = None):
        subgraph = self.graph.edge_subgraph(subgraph_set) if subgraph_set is not None else self.graph
        adj = dict(subgraph.adjacency())
        tree_set = set()
        curr = random.choice(self.nodes)
        connected = {curr}
        curr_edges = [tuple([curr, dest]) for dest in list(adj[curr].keys())]
        while len(connected) != len(self.nodes):
            edge = random.choice(curr_edges)
            curr_edges.remove(edge)
            if edge[1] in connected:
                continue
            curr = edge[1]
            connected.add(curr)
            tree_set.add(edge)
            for dest in list(adj[curr].keys()):
                curr_edges.append(tuple([curr, dest]))
        return tree_set

    def mutate(self, tree_set: set):
        tree = self.graph.edge_subgraph(tree_set).copy()
        output = set(tree.edges)
        rand_edge = random.choice(tuple(tree.edges))
        output.remove(rand_edge)
        tree.remove_edge(*rand_edge)
        comp_a, comp_b = tuple(nx.components.connected_components(tree))
        edges = self.edges
        random.shuffle(edges)
        for edge in edges:
            if edge == rand_edge:
                continue
            if (edge[0] in comp_a and edge[1] in comp_b) or (edge[1] in comp_a and edge[0] in comp_b):
                output.add(edge)
                return output

    def crossover(self, tree_a: set, tree_b: set):
        subgraph = tree_a.union(tree_b)
        return self.random_prim(subgraph)

    def algorithm(self):
        generation = [self.random_prim() for _ in range(100)]

        global answer

        for i in range(600):
            generation.sort(key=self.tree_weight)
            if self.tree_weight(generation[0]) == answer:
                print(f"Converged at iteration #{i}")
                break
            # print(fitness)
            # mod_fitness = tuple(
            #     map(
            #         lambda x: ((x - worst) / (best - worst)) * 100 + ((x - best) / (worst - best)) * 40,
            #         fitness
            #     )
            # )
            mod_fitness = [100-i for i in range(100)]
            # print(mod_fitness)
            parents = random.choices(generation, weights=mod_fitness, k=50)
            # print(parents)
            # print(sorted(tuple(map(self.tree_weight, parents))))
            generation = []
            while len(generation) != 100:
                couple = random.choices(parents, k=2)
                if random.random() > 0.9:
                    continue
                child = self.crossover(*couple)
                if random.random() <= 0.1:
                    child = self.mutate(child)
                generation.append(child)

        generation.sort(key=self.tree_weight)
        fitness = tuple(map(self.tree_weight, generation))
        print(generation)
        print(fitness)
        pass

    def tree_weight(self, tree: set):
        return sum((self.graph.edges[edge]['weight'] for edge in tree))


g = nx.Graph()
n = 10
nodes = tuple(i+1 for i in range(n))
print(nodes)
answer = 9
print(answer)
weights = [
    [0, 1, 100, 100, 100, 100, 100, 100, 100, 100],
    [1, 0, 1, 100, 100, 100, 100, 100, 100, 100],
    [100, 1, 0, 1, 100, 100, 100, 100, 100, 100],
    [100, 100, 1, 0, 1, 100, 100, 100, 100, 100],
    [100, 100, 100, 1, 0, 1, 100, 100, 100, 100],
    [100, 100, 100, 100, 1, 0, 1, 100, 100, 100],
    [100, 100, 100, 100, 100, 1, 0, 1, 100, 100],
    [100, 100, 100, 100, 100, 100, 1, 0, 1, 100],
    [100, 100, 100, 100, 100, 100, 100, 1, 0, 1],
    [100, 100, 100, 100, 100, 100, 100, 100, 1, 0]
]
print([(x, y, weights[x-1][y-1]) for x in nodes for y in nodes])
g.add_weighted_edges_from([(x, y, weights[x-1][y-1]) for x in nodes for y in nodes])
solver = Solver(g)
start = time.time_ns()
solver.algorithm()
print(f"Elapsed time: {time.time_ns() - start} ns")