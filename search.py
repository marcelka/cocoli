def _bin_search(condition, minv, maxv, fn):
    if minv + 1 >= maxv:
        return fn([x for x in (minv, maxv) if condition(x)])
    avg = (minv + maxv) // 2

    if condition(avg):
        boundaries = sorted([avg, fn(minv, maxv)])
    else:
        boundaries = sorted([avg, -fn(-minv, -maxv)])
    return _bin_search(condition, boundaries[0], boundaries[1], fn)

def bin_search(condition, minv, maxv, fn, check=False):
    """
    Returns min/max value that passes condition. Expects the value to be between
    minv and maxv.

    Arguments:
    condition -- unary function that returns True/False
    minv, maxv -- integers defining the range where to search for the result
    fn -- either min or max, defines whether to look for minimum or maximum
    """
    if not condition(minv) and not condition(maxv):
        raise ValueError(
            "Neither minv (%s) nor maxv (%s) passes the condition." %
            (minv, maxv))
    return _bin_search(condition, minv, maxv, fn)


import unittest

class TestSearch(unittest.TestCase):

  def test_bin_search(self):
      self.assertEqual(bin_search(lambda x: x < 10, 0, 100, max, True), 9)
      self.assertEqual(bin_search(lambda x: x > 10, 0, 100, min, True), 11)
      with self.assertRaises(ValueError):
          bin_search(lambda x: x > 10, 0, 5, min, True)

if __name__ == '__main__':
    unittest.main()
