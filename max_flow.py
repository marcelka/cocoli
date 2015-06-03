from collections import namedtuple, defaultdict
try:
    from queue import Queue
except ImportError:
    from Queue import Queue

def augmenting_path(neighs, source, drain):
    visited = set()
    to_visit = Queue()
    to_visit.put(source)
    prevs = {}
    while True:
        if drain in visited: return path(source, drain, prevs)
        if to_visit.empty(): return None, 0
        v = to_visit.get()
        if v in visited: continue
        for n, cap in neighs(v):
            if n not in visited:
                to_visit.put(n)
                prevs[n] = (v, cap)
        visited.add(v)

def path(start, end, prevs):
    path = [end]
    capacity = prevs[end][1]
    while True:
        last = path[-1]
        if last == start: return list(reversed(path)), capacity
        capacity = min(capacity, prevs[last][1])
        path.append(prevs[last][0])

def max_flow(capacity, source, drain):
    """
    Returns max flow and its value. Flow is described by dict of dicts such that
    flow[v1][v2] = f iff there is a flow from v1 to v2 of value f.

    Arguments:
    capacity -- dict of dicts such that capacity[v1][v2] is the flow capacity of
                edge from v1 to v2
    source -- the source vertex
    drain -- the drain vertex
    """
    vertices = set(capacity.keys())
    for v in capacity:
        vertices.update(capacity[v].keys())

    _neighs = defaultdict(set)
    for v in capacity:
        for w in capacity[v]:
            _neighs[v].add(w)
            _neighs[w].add(v)

    flow = dict((v1, dict((v2, 0) for v2 in vertices)) for v1 in vertices)

    while True:
        def residual_graph_neighs(v):
            for w in _neighs[v]:
                c = (capacity[v][w] if v in capacity and w in capacity[v] else 0) - flow[v][w]
                if c>0: yield (w, c)

        aug_path, amount = augmenting_path(residual_graph_neighs, source, drain)
        if aug_path == None:
            return flow, sum(flow[source].values())

        for i in range(len(aug_path) - 1):
            v1, v2 = aug_path[i], aug_path[i+1]
            flow[v1][v2] += amount
            flow[v2][v1] -= amount


import unittest

class TestMaxFlow(unittest.TestCase):

  def test_max_flow(self):
      capacity = {"s": {1: 10}, 1: {"d": 6}}
      self.assertEqual(max_flow(capacity, "s", "d")[1], 6)

      capacity = {"s": {1: 10}, 2: {"d": 6}}
      self.assertEqual(max_flow(capacity, "s", "d")[1], 0)

      capacity = {
          "s": {1: 10, 3: 4},
          1: {2: 13, 4: 4},
          2: {"d": 10},
          3: {2: 4},
          4: {"d": 4},
      }
      self.assertEqual(max_flow(capacity, "s", "d")[1], 14)

if __name__ == '__main__':
    unittest.main()
