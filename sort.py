def merge(list1, list2, key):
    """
    Merges sorted lists, producing a new sorted list. Returns merged list and
    inversion count.
    """
    result = []
    inversion_count = 0
    i1 = i2 = 0
    while True:
        if i1 == len(list1):
            result.extend(list2[i2:])
            return result, inversion_count
        elif i2 == len(list2):
            result.extend(list1[i1:])
            return result, inversion_count
        elif key(list1[i1]) <= key(list2[i2]):
            result.append(list1[i1])
            i1 += 1
        else:
            result.append(list2[i2])
            i2 += 1
            inversion_count += len(list1) - i1

def _sort_and_count(_list, key=lambda x:x):
    """
    Uses mergesort algorithm to sort the provided list and count the number of
    inversions. Returns new stable-sorted list and number of inversions. Does
    not modify the old list.
    """
    if len(_list) == 1:
        return _list, 0
    middle = len(_list) // 2
    l1, inv1 = _sort_and_count(_list[:middle], key)
    l2, inv2 = _sort_and_count(_list[middle:], key)
    merged_list, merged_inv = merge(l1, l2, key)
    return merged_list, merged_inv + inv1 + inv2

def mergesorted(_list, key=lambda x: x):
    """
    Uses mergesort algorithm to sort the provided list. Returns new
    stable-sorted list, does not modify the old list.
    """
    return _sort_and_count(_list, key)[0]

def inversions(_list, key=lambda x: x):
    """Returns number of inversions in _list."""
    return _sort_and_count(_list, key)[1]


import unittest
import random
from itertools import combinations

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

    def test_inversions(self):
        data = [1, 5, 2, 3, 4, 0]
        self.assertEqual(inversions(data), 8)
        sorted_data = list(range(100))
        self.assertEqual(inversions(sorted_data), 0)

    def test_inversions_random(self):
        for i in range(10):
            data = [random.randint(0, 100) for i in range(100)]
            result = 0
            for i, j in combinations(range(100), 2):
                if i < j and data[i] > data[j]:
                    result += 1
            self.assertEqual(inversions(data), result)

      
if __name__ == '__main__':
    unittest.main()
