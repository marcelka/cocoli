from collections import namedtuple, defaultdict
from structures import SimpleQueue

Edge = namedtuple('Edge', ['start', 'end'])

def augmenting_path(neighs, source, drain):
    visited = set()
    to_visit = SimpleQueue([source])
    prevs = {}
    while True:
        if drain in visited: return path(source, drain, prevs)
        if not to_visit: return None
        v = to_visit.pop()
        for n in neighs(v):
            if n not in visited and n not in to_visit:
                to_visit.push(n)
                prevs[n] = v
        visited.add(v)

def path(start, end, prevs):
    path = [Edge(prevs[end], end)]
    while True:
        last = path[-1][0]
        if last == start: return list(reversed(path))
        path.append(Edge(prevs[last], last))

def residual_graph_neighs(capacity, flow):
    neighs = defaultdict(set)
    rgcapacity = {}
    for e in capacity:
        flowing = flow[e] if e in flow else 0
        if capacity[e] > flowing:
            neighs[e.start].add(e.end)
            rgcapacity[e] = capacity[e] - flowing
        if flowing > 0:
            neighs[e.end].add(e.start)
            rgcapacity[Edge(e.end, e.start)] = flowing
    return neighs, rgcapacity

def max_flow(capacity, source, drain):
    """Capacity: dict from Edge to max flow capacity for that edge."""
    """Returns max flow and its value."""
    flow = {}
    for e in capacity: flow[e] = 0
    while True:
        rgneighs, rgcapacity = residual_graph_neighs(capacity, flow)
        aug_path = augmenting_path(lambda v: rgneighs[v], source, drain)
        if aug_path == None:
            return flow, sum(flow[e] for e in flow if e[0] == source)
        amount = min(rgcapacity[e] for e in aug_path)
        for e in aug_path:
            if e in flow: flow[e] += amount
            else: flow[Edge(e.end, e.start)] -= amount


import unittest

class TestMaxFlow(unittest.TestCase):

  def test_max_flow(self):
      capacity = {Edge("s", 1): 10, Edge(1, "d"): 6}
      self.assertEqual(max_flow(capacity, "s", "d")[1], 6)

      capacity = {Edge("s", 1): 10, Edge(2, "d"): 6}
      self.assertEqual(max_flow(capacity, "s", "d")[1], 0)

      capacity = {
          Edge("s", 1): 10,
          Edge("s", 3): 4,
          Edge(1, 2): 13,
          Edge(1, 4): 4,
          Edge(2, "d"): 10,
          Edge(3, 2): 4,
          Edge(4, "d"): 4,
      }
      self.assertEqual(max_flow(capacity, "s", "d")[1], 14)

if __name__ == '__main__':
    unittest.main()
