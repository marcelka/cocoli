import heapq

def compute_neighs(vertices, weights):
    result = {}
    for v in vertices: result[v] = []
    for edge, weight in weights.items():
        result[edge[0]].append((edge[1], weight))
    return result

def shortest_paths(neighs, start):
    """ Returs shortest paths from start to all reachable vertices."""
    """ Input:
            neighs: dict from vertex to iterable of 2-tuples (vertex, distance)
            start:  the starting vertex
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
        for n,dist_nv in neighs[vertex]:
            if n in visited: continue
            heapq.heappush(to_visit, (dist_nv+dist, n, vertex))
        prevs[vertex] = prev
        dists[vertex] = dist
        visited.add(vertex)

def shortest_path(neighs, start, stop):
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
        graph = {'s': (('a', 2), ('b', 1)),
                 'a': (('s', 3), ('b', 4), ('c', 8)),
                 'b': (('s', 4), ('a', 2), ('d', 2)),
                 'c': (('a', 2), ('d', 7), ('t', 4)),
                 'd': (('b', 1), ('c', 11), ('t', 5)),
                 't': (('c', 3), ('d', 5)),}
        self.assertEqual(shortest_path(graph, 's', 't'), (8, ('s', 'b', 'd', 't')))

if __name__ == '__main__':
    unittest.main()
