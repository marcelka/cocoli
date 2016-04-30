def primes(N):
    """
    Returns primes from 1 to N (inclusive) using sieve of Eratosthenes. Works in
    asymptotic time complexity N*log(log(N)) (based on assumption that there are
    N/log(N) primes smaller than N).
    """
    result = set(range(2, N+1))
    for i in range(2, N+1):
        if i not in result: continue
        ki = 2*i
        while ki < N+1:
            if ki in result: result.remove(ki)
            ki += i
    return result


import random
import math

def is_prime(n, error):
    """
    Uses probabilistic Miller-Rabin primality test to determine whether n is
    prime or composite.

    Arguments:
    n -- number to be tested
    error -- maximum acceptable probability that the result will be wrong
    """
    if n <= 0: raise ValueError("Argument is not a positive integer")
    if n == 1: return False
    if n == 2: return True
    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    assert(2**s * d == n-1 and d % 2 == 1)
    def could_be_prime():
        a = random.randint(1, n-1)
        x = pow(a, d, n)
        if x == 1: return True
        for r in range(s):
            if x == n-1: return True
            x = x**2 % n
        return False
    # At least 3/4 of numbers are witnesses for compositeness of any n.
    for i in range(int(math.log(1/error, 4))+1):
        if not could_be_prime(): return False
    return True


import unittest

class TestPrimesLibrary(unittest.TestCase):

  def test_by_comparison(self):
      eratosthenes = tuple(primes(1000))
      miller_rabin = tuple(p for p in range(2, 1000) if is_prime(p, 10**-10))
      self.assertEqual(eratosthenes, miller_rabin)

if __name__ == '__main__':
    unittest.main()
