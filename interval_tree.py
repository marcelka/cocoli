def build_tree(data, reducing_fn):
    n = len(data)
    i = next(2**j for j in range(n + 1) if 2**j >= n)
    tree = [0] * i * 2

    floor = data + [0] * (i - n)
    while True:
        if i == 0: return tree
        tree[i:2 * i] = floor
        i //= 2
        floor = [reducing_fn(floor[2 * j:2 * j + 2]) for j in range(i)]

def left_child(i, grandness=1):
    return i * 2**grandness

def right_child(i, grandness=1):
    return i * 2**grandness + 2**grandness - 1

def parent(i):
    return i // 2

# including a, including b
def resolve_query(tree, reducing_fn, a, b):
    values = []
    n = len(tree)

    def add_vals(i, k):
        start = left_child(i, k) - n // 2
        end = right_child(i, k) - n // 2

        if a <= start and b >= end:
            values.append(tree[i])
        elif (a >= start and a <= end) or (b >= start and b <= end):
            add_vals(2 * i, k - 1)
            add_vals(2 * i + 1, k - 1)

    N = next(i for i in range(n) if 2**i == n) - 1
    add_vals(1, N)
    return reducing_fn(values)

def update(tree, reducing_fn, pos, val):
    p = pos + len(tree) // 2
    v = val

    while True:
        tree[p] = v
        if p == 1: return
        p = parent(p)
        lc = left_child(p)
        v = reducing_fn(tree[lc:lc + 2])


import unittest

class TestIntervalTree(unittest.TestCase):

  def test_build_tree(self):
      self.assertEqual(build_tree([0, 1, 2, 3], sum), [0, 6, 1, 5, 0, 1, 2, 3])
      self.assertEqual(build_tree([0, 1, 2], sum), [0, 3, 1, 2, 0, 1, 2, 0])
      self.assertEqual(build_tree([0, 1, 2, 3], min), [0, 0, 0, 2, 0, 1, 2, 3])
      self.assertEqual(build_tree([1], sum), [0, 1])
      self.assertEqual(build_tree([], sum), [0, 0])

  def test_resolve_query(self):
      tree4 = build_tree([0, 1, 2, 3], sum)
      self.assertEqual(resolve_query(tree4, sum, 0, 3), 6)
      self.assertEqual(resolve_query(tree4, sum, 0, 0), 0)
      self.assertEqual(resolve_query(tree4, sum, 2, 2), 2)
      self.assertEqual(resolve_query(tree4, sum, 0, 1), 1)
      self.assertEqual(resolve_query(tree4, sum, 1, 2), 3)

      tree6 = build_tree([0, 1, 2, 3, 4, 5], sum)
      self.assertEqual(resolve_query(tree6, sum, 0, 5), 15)
      self.assertEqual(resolve_query(tree6, sum, 2, 4), 9)
      self.assertEqual(resolve_query(tree6, sum, 2, 1), 0)

  def test_update(self):
      tree6 = build_tree([0, 1, 2, 3, 4, 5], sum)
      update(tree6, sum, 3, 10)
      self.assertEqual(resolve_query(tree6, sum, 0, 5), 22)
      self.assertEqual(resolve_query(tree6, sum, 2, 4), 16)
      self.assertEqual(resolve_query(tree6, sum, 1, 2), 3)
      update(tree6, sum, 4, -1)
      self.assertEqual(resolve_query(tree6, sum, 0, 5), 17)


if __name__ == '__main__':
    unittest.main()
