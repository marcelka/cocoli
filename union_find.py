def create_sets(iterables):
    sets = {}
    for iterable in iterables:
        first = iterable[0]
        sets[first] = None
        for item in iterable[1:]:
            sets[item] = first
    return sets

def find(sets, item):
    if sets[item] == None: return item
    result = find(sets, sets[item])
    sets[item] = result
    return result

def union(sets, item1, item2):
    sets[find(sets, item1)] = find(sets, item2)

import unittest

class TestUnionFind(unittest.TestCase):

  def test_union_find(self):
      sets = create_sets([(1, 2, 3), (4, 5, 6), (7,), (8, 9, 10, 11)])

      self.assertEqual(find(sets, 1), find(sets, 2))
      self.assertEqual(find(sets, 8), find(sets, 11))
      self.assertNotEqual(find(sets, 1), find(sets, 7))

      union(sets, 1, 7)

      self.assertEqual(find(sets, 1), find(sets, 7))
      self.assertNotEqual(find(sets, 1), find(sets, 11))

      union(sets, 1, 10)
      self.assertEqual(find(sets, 1), find(sets, 11))


if __name__ == '__main__':
    unittest.main()
