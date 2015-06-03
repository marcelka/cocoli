import heapq

def shortest_paths(neighs, start):
    """
    Returns a tuple of two dicts (dists, prevs). Dists contains lengths of
    shortest paths from start to all reachable vertices. Prevs contains previous
    vertex of the shortest path, which can be easily used to reconstruct the
    whole path.

    Arguments:
    neighs -- dict of dict such that neighs[v1][v2] = d iff there is an edge
              from v1 to v2 with length d
    start -- the starting vertex
    """
    visited = set()
    to_visit = [(0, start, None)]
    heapq.heapify(to_visit)
    prevs = {} # previous vertex of ideal path
    dists = {}
    while True:
        if not to_visit:
            return dists, prevs
        dist, vertex, prev = heapq.heappop(to_visit)
        if vertex in visited: continue
        for n in neighs[vertex]:
            if n in visited: continue
            heapq.heappush(to_visit, (neighs[vertex][n] + dist, n, vertex))
        prevs[vertex] = prev
        dists[vertex] = dist
        visited.add(vertex)

def shortest_path(neighs, start, stop):
    """
    Returs length of shortest path from start to stop and the shortest path (as
    a sequence of vertices, including start and stop).
    If start and stop are not connected, returns (None, None).

    Arguments:
    neighs -- dict of dict such that neighs[v1][v2] = d iff there is an edge
              from v1 to v2 with length d
    start -- the starting vertex
    stop -- the final vertex
    """
    dists, prevs = shortest_paths(neighs, start)
    if stop not in dists: return None, None
    def _path(v):
        if v == start: return [v]
        res = _path(prevs[v])
        res.append(v)
        return res
    return dists[stop], tuple(_path(stop))


import unittest

class TestDijkstra(unittest.TestCase):

    def test_dijkstra(self):
        graph = {'s': {'a': 2, 'b': 1},
                 'a': {'s': 3, 'b': 4, 'c': 8},
                 'b': {'s': 4, 'a': 2, 'd': 2},
                 'c': {'a': 2, 'd': 7, 't': 4},
                 'd': {'b': 1, 'c': 11, 't': 5},
                 't': {'c': 3, 'd': 5},}
        self.assertEqual(shortest_path(graph, 's', 't'), (8, ('s', 'b', 'd', 't')))

if __name__ == '__main__':
    unittest.main()
