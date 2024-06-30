import copy
import time

import networkx as nx
import random

class Solver:
    solutionz=[]

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

    def algorithm(self, gen,count_steps,p_c,p_m):
        generation = [self.random_prim() for _ in range(gen)]

        global answer
        best_solutions = []

        for i in range(count_steps):
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
            best_solutions.append(generation[:3])
            mod_fitness = [gen-i for i in range(gen)]
            # print(mod_fitness)
            parents = random.choices(generation, weights=mod_fitness, k=gen//2)
            # print(parents)
            # print(sorted(tuple(map(self.tree_weight, parents))))
            generation = []
            while len(generation) != gen:
                couple = random.choices(parents, k=2)
                if random.random() > p_c:
                    continue
                child = self.crossover(*couple)
                if random.random() <= p_m:
                    child = self.mutate(child)
                generation.append(child)

        generation.sort(key=self.tree_weight)
        fitness = tuple(map(self.tree_weight, generation))

        with open('best_solutions.txt', 'w') as f:
            for step, solutions in enumerate(best_solutions):
                for sol in solutions:
                    f.write(f'{sol}\n')

        for step, solutions in enumerate(best_solutions):
            for sol in solutions:
                self.solutionz.append(sol, self.tree_weight(sol))

        print(generation)
        print(fitness)
        pass

    def tree_weight(self, tree: set):
        return sum((self.graph.edges[edge]['weight'] for edge in tree))

answer=0