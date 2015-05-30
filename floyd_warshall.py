from itertools import product

def directed(undirected_weights):
    result = dict((v, {}) for v in undirected_weights)
    for v1 in undirected_weights:
        for v2 in undirected_weights[v1]:
            result[v2][v1] = undirected_weights[v1][v2]
            result[v1][v2] = undirected_weights[v1][v2]
    return result

def shortest_distances(weights):
    """
    Returns shortest path values in a directed graph for each pair of vertices
    using Floyd-Warshall algorithm.
    Arguments:
    weights -- dict of dicts such that weights[v1][v2] = w iff there is an edge
               from v1 to v2 with weight w
    Complexity: len(weights)**3
    """
    vertices = set(weights.keys())
    for v in weights:
        vertices.update(weights[v].keys())
    id2v = dict(enumerate(vertices))
    ids = id2v.keys()

    result = [[None for v in vertices] for w in vertices]

    for id1, id2 in product(ids, repeat=2):
        v1, v2 = id2v[id1], id2v[id2]
        if v1 in weights and v2 in weights[v1]:
            result[id1][id2] = weights[v1][v2]
        else:
            result[id1][id2] = None
        result[id1][id1] = 0

    for new in ids:
        for id1, id2 in product(ids, repeat=2):
            if result[id1][new] != None and result[new][id2] != None:
                via_new = result[id1][new] + result[new][id2]
                if result[id1][id2] == None:
                    result[id1][id2] = via_new
                else:
                    result[id1][id2] = min(result[id1][id2], via_new)

    vertex_result = dict((v, {}) for v in vertices)
    for id1, id2 in product(ids, repeat=2):
        v1, v2 = id2v[id1], id2v[id2]
        vertex_result[v1][v2] = result[id1][id2]

    return vertex_result

def has_cycle(graph):
    """Returns True iff the given directed graph has a cycle.

    Arguments:
    graph -- dict such that graph[vertex] = dict/iterable of neighbors; if the
             value is a dict, all its keys are considered neighbors of vertex
    Complexity: len(graph)**3
    """
    weights = dict((v, {}) for v in graph)
    for v1 in graph:
        for v2 in graph[v1]:
            weights[v1][v2] = -1
    distances = shortest_distances(weights)
    return any(distances[v][v] < 0 for v in graph)


from itertools import combinations
import random
import unittest
import dijkstra

class TestFloydWarshall(unittest.TestCase):

    def test_floyd_warshall(self):
        weights = {1: {2: 100, 3: 10}, 3: {2: 20, 4: 1}, 4: {2: 2}}
        result = shortest_distances(weights)
        self.assertEqual(result[1][1], 0)
        self.assertEqual(result[1][2], 13)
        self.assertEqual(result[1][3], 10)
        self.assertEqual(result[1][4], 11)
        self.assertEqual(result[2][3], None)

    def test_by_comparison(self):
        VERTEX_COUNT = 20
        EDGE_COUNT = 100
        MAX_DIST = 1000
        vertices = list(range(VERTEX_COUNT))
        edges = random.sample(list(combinations(vertices, 2)), EDGE_COUNT)
        weights = dict((v, {}) for v in vertices)
        for edge in edges:
            weights[edge[0]][edge[1]] = random.randint(1, MAX_DIST)
        neighs = dijkstra.compute_neighs(weights)
        fw_result = shortest_distances(weights)
        for v1, v2 in product(vertices, repeat=2):
            dijkstra_result = dijkstra.shortest_path(neighs, v1, v2)[0]
            self.assertEqual(fw_result[v1][v2], dijkstra_result)

    def test_cycle_detection(self):
        self.assertFalse(has_cycle({1: [2], 2: [3, 4], 3: [5]}))
        self.assertTrue(has_cycle({1: [2], 2: [3, 4], 4: [1], 3: [5]}))


if __name__ == '__main__':
    unittest.main()
