import operator

from streams import Stream, foreach, filter, pair, head, tail, count, map, takewhile, dropwhile


def is_prime(n: int) -> bool:
    if n < 2:
        raise ValueError(f'Argument `n` must be at least 2. {n} received.')
    else:
        ps = primes
        while (p := head(ps)) ** 2 <= n and n % p != 0:
            print(f'{n:,d} % {p} == {n % p}')
            ps = tail(ps)
        else:
            return p * p > n


def sieve(s: Stream[int]) -> Stream:
    return pair(head(s),
                lambda: sieve(filter(lambda x: x % head(s) != 0,
                                     tail(s))))


def add(s1: Stream[int], s2: Stream[int]):
    return map(operator.add, s1, s2)


ones = pair(1, lambda: ones)

integers = pair(1, lambda: add(ones, integers))

fibs = pair(0, lambda: pair(1, lambda: add(tail(fibs), fibs)))

primes = pair(2, lambda: filter(is_prime, count(3)))

if __name__ == '__main__':
    foreach(lambda p: print(f'{p:,d}'),
            takewhile(lambda n: n < 20,
                      dropwhile(lambda n: n < 10,
                                integers)))
