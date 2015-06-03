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
      sets = {1: None, 2: 1, 3: 1, 4: None, 5: 4, 6: 4,
              7: None, 8: None, 9: 8, 10: 8, 11: 8}

      self.assertEqual(find(sets, 1), 1)
      self.assertEqual(find(sets, 2), 1)
      self.assertEqual(find(sets, 8), 8)
      self.assertEqual(find(sets, 11), 8)
      self.assertEqual(find(sets, 7), 7)

      union(sets, 1, 7)

      self.assertEqual(find(sets, 1), find(sets, 7))
      self.assertNotEqual(find(sets, 1), find(sets, 11))

      union(sets, 1, 10)
      self.assertEqual(find(sets, 1), find(sets, 11))


if __name__ == '__main__':
    unittest.main()
