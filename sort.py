def merge(list1, list2, key):
    """Merges sorted lists, producing a new sorted list."""
    result = []
    i1 = i2 = 0
    while True:
        if i1 == len(list1):
            result.extend(list2[i2:])
            return result
        elif i2 == len(list2):
            result.extend(list1[i1:])
            return result
        elif key(list1[i1]) <= key(list2[i2]):
            result.append(list1[i1])
            i1 += 1
        else:
            result.append(list2[i2])
            i2 += 1

def mergesorted(_list, key=lambda x: x):
    """Uses mergesort algorithm to sort the provided list."""
    """Returns new sorted list, does not modify the old list."""
    """Stable sort"""
    if len(_list) == 1:
        return _list
    middle = len(_list) // 2
    return merge(mergesorted(_list[:middle]), mergesorted(_list[middle:]), key)


import unittest
import random

class TestSortLibrary(unittest.TestCase):

  def test_mergesort_random(self):
      for i in range(10):
          data = list(range(100))
          random.shuffle(data)
          data_backup = list(data)
          sorted_data = mergesorted(data)
          self.assertEqual(tuple(sorted_data), tuple(range(100)))
          self.assertEqual(tuple(data), tuple(data_backup))

  def test_mergesort(self):
      data = [1, 7, 5, 6, 2, 3, 4, 8, 0, 9]
      sorted_data = mergesorted(data)
      self.assertEqual(tuple(sorted_data), tuple(range(10)))

  def test_mergesort_stability(self):
      data = [(2, 4), (5, 2), (5, 1), (1, 5)]
      sorted_data = mergesorted(data)
      result = [(1, 5), (2, 4), (5, 1), (5, 2)]
      sorted_data_key = mergesorted(data, key=lambda x: x[0])
      result_key = [(1, 5), (2, 4), (5, 2), (5, 1)]
      self.assertEqual(tuple(sorted_data), tuple(result))
      self.assertEqual(tuple(sorted_data_key), tuple(result_key))
      
if __name__ == '__main__':
    unittest.main()
