import random
from itertools import combinations

def graph(edges, values=True):
    vertices = set()
    for e in edges: vertices.update(e)
    if values:
        result = dict((v, {}) for v in vertices)
        for v1, v2 in edges:
            result[v1][v2] = edges[(v1, v2)]
    else:
        result = dict((v, set()) for v in vertices)
        for v1, v2 in edges:
            result[v1].add(v2)
    return result

def edges(graph, values=True):
    result = {} if values else set()
    for v1 in graph:
        for v2 in graph[v1]:
            edge = (v1, v2)
            if values: result[edge] = graph[v1][v2]
            else: result.add(edge)
    return result

def directed(undirected_graph):
    result = dict((v, {}) for v in undirected_graph)
    for v1 in undirected_graph:
        for v2 in undirected_graph[v1]:
            result[v2][v1] = undirected_graph[v1][v2]
            result[v1][v2] = undirected_graph[v1][v2]
    return result

def random_graph(value_generator, vertex_count, edge_count=None,
        edge_prob=None):
    vertices = list(range(vertex_count))
    if len([_ for _ in [edge_count, edge_prob] if _ == None]) != 1:
        raise ValueError("One of edge_count and edge_prob has to be specified.")
    if edge_count != None:
        edges = random.sample(list(combinations(vertices, 2)), edge_count)
    elif edge_prob != None:
        edges = []
        for edge in list(combinations(vertices, 2)):
            if random.random() < edge_prob: edges.append(edge)

    graph = dict((v, {}) for v in vertices)
    for edge in edges:
        graph[edge[0]][edge[1]] = value_generator()
    return graph
