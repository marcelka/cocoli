def primes(N):
    """Returns primes from 1 to N using sieve of Eratosthenes."""
    """Asymptotic time complexity: N*log(log(N))"""
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
    """Miller-Rabin primality test."""
    if n <= 0: raise ValueError("Argument is not a positive integer")
    if n == 1: return False
    if n == 2: return True
    s = next(x for x in range(n) if (n-1) % (2**x) != 0) - 1
    d = (n - 1) // (2**s)
    def could_be_prime():
        a = random.randint(1, n-1)
        if (a**d) % n == 1: return True
        for r in range(s):
            if a**(d*2**r) % n == n-1: return True
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
