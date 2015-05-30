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
    Returns shortest path values and next move along this path in a directed
    graph for each pair of vertices using Floyd-Warshall algorithm. For example,
    if the shortest path from vertex "v1" to vertex "v2" is ("v1"->"v3",
    "v3"->"v4", "v4"->"v1") and has length 7, result["v1"]["v2"] will be equal
    to (7, "v3"). If there are multiple next moves leading to same (minimum)
    distance, one of them (randomly chosen) will be returned.

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

    distance = [[None for v in vertices] for w in vertices]
    next_move = [[None for v in vertices] for w in vertices]

    for id1, id2 in product(ids, repeat=2):
        v1, v2 = id2v[id1], id2v[id2]
        if v1 in weights and v2 in weights[v1]:
            distance[id1][id2] = weights[v1][v2]
            next_move[id1][id2] = id2
        else:
            distance[id1][id2] = None
        distance[id1][id1] = 0

    for new in ids:
        for id1, id2 in product(ids, repeat=2):
            if distance[id1][new] != None and distance[new][id2] != None:
                via_new = distance[id1][new] + distance[new][id2]
                if distance[id1][id2] == None or via_new < distance[id1][id2]:
                    distance[id1][id2] = via_new
                    next_move[id1][id2] = next_move[id1][new]

    dist_res = dict((v, {}) for v in vertices)
    nm_res = dict((v, dict((v, None) for v in vertices)) for v in vertices)

    for id1, id2 in product(ids, repeat=2):
        v1, v2 = id2v[id1], id2v[id2]
        if next_move[id1][id2] != None:
            nm_res[v1][v2] = id2v[next_move[id1][id2]]
        dist_res[v1][v2] = distance[id1][id2]

    return dist_res, nm_res

def path(start, end, next_moves):
    path = [start]
    while True:
        if next_moves[path[-1]] == None: return None
        path.append(next_moves[path[-1]][end])
        if path[-1] == end: return path

def find_cycle(graph):
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
    dists, next_moves = shortest_distances(weights)
    for v in graph:
        if dists[v][v] < 0: return path(v, v, next_moves)


from itertools import combinations
import random
import unittest
import dijkstra

class TestFloydWarshall(unittest.TestCase):

    def test_floyd_warshall(self):
        weights = {1: {2: 100, 3: 10}, 3: {2: 20, 4: 1}, 4: {2: 2}}
        dist, next_move = shortest_distances(weights)
        self.assertEqual((dist[1][1], next_move[1][1]), (0, None))
        self.assertEqual((dist[1][2], next_move[1][2]), (13, 3))
        self.assertEqual((dist[1][3], next_move[1][3]), (10, 3))
        self.assertEqual((dist[1][4], next_move[1][4]), (11, 3))
        self.assertEqual((dist[2][3], next_move[2][3]), (None, None))

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
            self.assertEqual(fw_result[0][v1][v2], dijkstra_result)

    def test_cycle_detection(self):
        self.assertEqual(find_cycle({1: [2], 2: [3, 4], 3: [5]}), None)
        self.assertEqual(tuple(find_cycle({1: [2], 2: [3, 4], 4: [1], 3: [5]})),
                         (1, 2, 4, 1))


if __name__ == '__main__':
    unittest.main()
