from itertools import product, combinations

def dimensions(data):
    item = data[0]
    result = [len(data)]
    if hasattr(item, '__iter__'):
        result.extend(dimensions(item))
    return result

def tree_dimension(dim):
    n = next(i for i in range(dim+1) if 2**i > dim)
    return 2**n

def zero_array(dimensions):
    d0 = dimensions[0]
    if len(dimensions) == 1:
        return [0 for i in range(d0)]
    else:
        return [zero_array(dimensions[1:]) for i in range(d0)]

def get(data, index):
    if len(index) == 0: return data
    return get(data[index[0]], index[1:])

def add1(data, index, value):
    if len(index) == 1:
        data[index[0]] += value
        return
    return add1(data[index[0]], index[1:], value)

def init(data):
    """Creates and returns Fenwick tree from provided iterable data."""
    dims = dimensions(data)
    tree = zero_array(list(tree_dimension(i) for i in dims))
    for index in product(*list(range(d) for d in dims)):
        add(tree, dims, index, get(data, index))
    return tree

def add(tree, dims, pos, value):
    """
    Adds value to Fenwick tree, such that this operation corresponds to
    data[x1][x2][..][xn] += value where (x1, x2, ..., xn) is equal to dims.

    Arguments:
    tree -- Fenwick tree created via init
    dims -- dimensions of data array
    pos -- tuple representing indexes in multidimensional data
    value -- number that is added to value at given position
    """
    def tree_indexes(index, dim):
        i = index + 1
        res = []
        while True:
            if i > dim: return res
            res.append(i-1)
            i += i & -i
    for index in product(*list(tree_indexes(pos[i], dims[i]) for i in
        range(len(dims)))):
        add1(tree, index, value)

def prefix_sum(tree, end):
    """
    Returns prefix sum of the muti-dimensional list that corresponds to the
    provided Fenwick tree. Prefix sum is the sum of all elements with indexes
    (x1, x2, ..., xn) such that x[i] < end[i] for each i.

    Arguments:
    tree -- Fenwick tree created via init
    end -- tuple representing indexes in multidimensional data
    """
    def tree_indexes(index):
        i = index 
        res = []
        while True:
            if i <= 0: return res
            res.append(i-1)
            i = i & (i-1)
    return sum(get(tree, index) for index in product(*list(tree_indexes(i) for i
        in end)))

def interval_sum(tree, start, end):
    """
    Returns sum of interval within the muti-dimensional list that corresponds to
    the provided Fenwick tree. Interval sum is the sum of all elements with
    indexes (x1, x2, ..., xn) such that start[i] <= x[i] < end[i] for each i.

    Arguments:
    tree -- Fenwick tree created via init
    start -- tuple representing indexes in multidimensional data
    end -- tuple representing indexes in multidimensional data; end[i] must be
           greater or equal to start[i] for each i
    """
    d = len(start)
    res = 0
    for i in range(d+1):
        for indexes in combinations(range(d), i):
            x = list(end)
            for index in indexes: x[index] = start[index]
            res += (-1)**i * prefix_sum(tree, x)
    return res

def simple_sum(data, start, end):
    dim = len(start)
    if dim == 1:
        return sum(data[start[0]:end[0]])
    res = 0
    for i in range(start[0], end[0]):
        res += simple_sum(data[i], start[1:], end[1:])
    return res


import unittest
import random

class TestFenwickTree(unittest.TestCase):

    def test_fenwick_tree(self):
        data = [1, 2, 3, 4, 5, 6]
        tree = init(data)
        self.assertEqual(prefix_sum(tree, [3]), 6)
        self.assertEqual(interval_sum(tree, [2], [6]), 18)
        add(tree, [6], [2], 10)
        self.assertEqual(prefix_sum(tree, [3]), 16)
        self.assertEqual(interval_sum(tree, [2], [6]), 28)

    def test_fenwick_tree_2d(self):
        data = [[1, 2, 3, 4], [5, 6, 7, 8]] 
        tree = init(data)
        self.assertEqual(prefix_sum(tree, [2, 3]), 24)
        self.assertEqual(interval_sum(tree, [0, 1], [2, 3]), 18)
        add(tree, [2, 4], [1, 2], 10)
        self.assertEqual(prefix_sum(tree, [2, 3]), 34)
        self.assertEqual(interval_sum(tree, [0, 1], [2, 3]), 28)

    def test_fenwick_tree_random(self):
        for d in range(1, 5):
            dims = tuple(random.randint(1, 10) for i in range(d))
            data = zero_array(dims)
            for _ in range(5**d):
                index = tuple(random.choice(range(d)) for d in dims)
                add1(data, index, random.randint(1, 1000))
            tree = init(data)
            for _ in range(500):
                index = tuple(random.randint(0, i-1) for i in dims)
                value = random.randint(1, 1000)
                add1(data, index, value)
                add(tree, dims, index, value)
                start = tuple(random.choice(range(d)) for d in dims)
                end = tuple(random.choice(range(start[i], dims[i])) for i in range(d))

                self.assertEqual(prefix_sum(tree, end),
                                 simple_sum(data, [0 for d in dims], end))

                self.assertEqual(interval_sum(tree, start, end),
                                 simple_sum(data, start, end))


if __name__ == '__main__':
    unittest.main()
