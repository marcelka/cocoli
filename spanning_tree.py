import union_find

def min_spanning_tree(graph):
    vertices, edges = set(), []
    for v1 in graph:
        for v2 in graph[v1]:
            edges.append((graph[v1][v2], v1, v2))
            vertices.update((v1, v2))
    edges = sorted(edges, reverse=True)
    sets = dict((v, None) for v in vertices)
    result = dict((v, {}) for v in vertices)
    result_weight = 0
    while True:
        if not edges:
            return result, result_weight
        weight, v1, v2 = edges.pop()
        if union_find.find(sets, v1) != union_find.find(sets, v2):
            result[v1][v2] = weight
            result[v2][v1] = weight
            result_weight += weight
            union_find.union(sets, v1, v2)


import unittest

class TestSpanningTree(unittest.TestCase):

    def test_min_spanning_tree(self):
        graph = {0: {1: 5, 2: 8, 3: 10},
                 1: {0: 5, 2: 9, 3: 9},
                 2: {0: 8, 1: 9, 3: 3},
                 3: {0: 10, 1: 9, 2: 3}}
        result = {0: {1: 5, 2: 8},
                  1: {0: 5},
                  2: {0: 8, 3: 3},
                  3: {2: 3}}
        mst = min_spanning_tree(graph)
        self.assertEqual(mst[0], result)
        self.assertEqual(mst[1], 16)


if __name__ == '__main__':
    unittest.main()
