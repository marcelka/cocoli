# Return all divisors of integer n
def divisors(n):
    # get factors and their counts
    factors = {}
    nn = n
    i = 2
    while i*i <= nn:
        while nn % i == 0:
            if not i in factors:
                factors[i] = 0
            factors[i] += 1
            nn //= i
        i += 1
    if nn > 1:
        factors[nn] = 1

    primes = list(factors.keys())

    # generates factors from primes[k:] subset
    def generate(k):
        if k == len(primes):
            yield 1
        else:
            rest = generate(k+1)
            prime = primes[k]
            for factor in rest:
                prime_to_i = 1
                # prime_to_i iterates prime**i values, i being all possible exponents
                for _ in range(factors[prime] + 1):
                    yield factor * prime_to_i
                    prime_to_i *= prime

    # in python3, `yield from generate(0)` would also work
    for factor in generate(0):
        yield factor


import unittest

class TestMaxFlow(unittest.TestCase):

  def test_divisors(self):
      self.assertEqual(sorted(list(divisors(1))), [1])
      self.assertEqual(sorted(list(divisors(5))), [1, 5])
      self.assertEqual(sorted(list(divisors(20))), [1, 2, 4, 5, 10, 20])

if __name__ == '__main__':
    unittest.main()
