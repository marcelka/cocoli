def left_child(i, grandness=1):
    return i * 2**grandness

def right_child(i, grandness=1):
    return i * 2**grandness + 2**grandness - 1

def parent(i):
    return i // 2

def _reduce(v1, v2, reducing_fn, neutral):
    if v1 == neutral: return v2
    if v2 == neutral: return v1
    return reducing_fn(v1, v2)

# including a, including b
def resolve_query(tree, reducing_fn, a, b, neutral=None):
    values = []
    n = len(tree)
    result = neutral

    def update(i, k):
        nonlocal result
        start = left_child(i, k) - n // 2
        end = right_child(i, k) - n // 2

        if a <= start and b >= end:
            result = _reduce(tree[i], result, reducing_fn, neutral)
        elif (a >= start and a <= end) or (b >= start and b <= end):
            update(2 * i, k - 1)
            update(2 * i + 1, k - 1)

    N = next(i for i in range(n) if 2**i == n) - 1
    update(1, N)
    return result

def update(tree, reducing_fn, pos, val, neutral=None):
    p = pos + len(tree) // 2
    v = val

    while True:
        tree[p] = v
        if p == 1: return
        p = p // 2
        lc = 2 * p
        rc = lc + 1
        v = _reduce(tree[lc], tree[rc], reducing_fn, neutral)

def build_tree(data, reducing_fn, neutral=None):
    n = len(data)
    i = next(2**j for j in range(n + 1) if 2**j >= n)
    tree = [neutral] * i * 2

    for i in range(n):
        update(tree, reducing_fn, i, data[i], neutral)

    return tree


import unittest

def sum_two(a, b):
    return sum([a, b])

class TestIntervalTree(unittest.TestCase):

  def test_build_tree(self):
      self.assertEqual(build_tree([0, 1, 2, 3], sum_two), [None, 6, 1, 5, 0, 1, 2, 3])
      self.assertEqual(build_tree([0, 1, 2], sum_two), [None, 3, 1, 2, 0, 1, 2, None])
      self.assertEqual(build_tree([0, 1, 2, 3], min), [None, 0, 0, 2, 0, 1, 2, 3])
      self.assertEqual(build_tree([1], sum_two), [None, 1])
      self.assertEqual(build_tree([], sum_two), [None, None])

  def test_resolve_query(self):
      tree4 = build_tree([0, 1, 2, 3], sum_two)
      self.assertEqual(resolve_query(tree4, sum_two, 0, 3), 6)
      self.assertEqual(resolve_query(tree4, sum_two, 0, 0), 0)
      self.assertEqual(resolve_query(tree4, sum_two, 2, 2), 2)
      self.assertEqual(resolve_query(tree4, sum_two, 0, 1), 1)
      self.assertEqual(resolve_query(tree4, sum_two, 1, 2), 3)

      tree6 = build_tree([0, 1, 2, 3, 4, 5], sum_two)
      self.assertEqual(resolve_query(tree6, sum_two, 0, 5), 15)
      self.assertEqual(resolve_query(tree6, sum_two, 2, 4), 9)
      self.assertEqual(resolve_query(tree6, sum_two, 2, 1, 0), 0)

  def test_update(self):
      tree6 = build_tree([0, 1, 2, 3, 4, 5], sum_two)
      update(tree6, sum_two, 3, 10)
      self.assertEqual(resolve_query(tree6, sum_two, 0, 5), 22)
      self.assertEqual(resolve_query(tree6, sum_two, 2, 4), 16)
      self.assertEqual(resolve_query(tree6, sum_two, 1, 2), 3)
      update(tree6, sum_two, 4, -1)
      self.assertEqual(resolve_query(tree6, sum_two, 0, 5), 17)


if __name__ == '__main__':
    unittest.main()
