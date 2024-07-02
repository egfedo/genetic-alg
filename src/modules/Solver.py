import networkx as nx
import random


class Solver:

    def __init__(self, graph: nx.Graph, size_gener, count_gener, p_c, p_m):
        self.size_gener = size_gener
        self.count_gener = count_gener
        self.p_c = p_c
        self.p_m = p_m

        self.graph = graph
        self.nodes = list(graph.nodes)
        self.edges = list(graph.edges)

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
        generation = [self.random_prim() for _ in range(self.size_gener)]

        global answer
        best_solutions = []
        best_weights = []
        average_weights = []

        break_counter = 0

        for i in range(self.count_gener):
            generation.sort(key=self.tree_weight)

            best_solutions.append(generation[:3])
            best_weights.append(tuple(map(self.tree_weight, best_solutions[i])))
            average_weights.append(sum(map(self.tree_weight, generation)) / self.size_gener)

            if i > 1 and best_weights[i-1][0] == best_weights[i][0]:
                break_counter += 1
                if break_counter >= 25:
                    break
            else:
                break_counter = 0
            mod_fitness = [self.size_gener - i for i in range(self.size_gener)]
            parents = random.choices(generation, weights=mod_fitness, k=self.size_gener // 2)
            generation = []
            while len(generation) != self.size_gener:
                couple = random.choices(parents, k=2)
                if random.random() > self.p_c:
                    continue
                child = self.crossover(*couple)
                if random.random() <= self.p_m:
                    child = self.mutate(child)
                generation.append(child)

        return best_solutions, best_weights, average_weights

    def tree_weight(self, tree: set):
        return sum((self.graph.edges[edge]['weight'] for edge in tree))
