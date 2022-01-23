import operator

from streams import Stream, foreach, filter, cons, first, rest, count, map, dropwhile, takewhile


def is_prime(n: int) -> bool:
    if n < 2:
        raise ValueError(f'Argument `n` must be at least 2. {n} received.')
    else:
        ps = primes
        while (p := first(ps)) ** 2 <= n and n % p != 0:
            ps = rest(ps)
        else:
            return p * p > n


def sieve(s: Stream[int]) -> Stream:
    return cons(first(s),
                lambda: sieve(filter(lambda x: x % first(s) != 0,
                                     rest(s))))


def add(s1: Stream[int], s2: Stream[int]):
    return map(operator.add, s1, s2)


ones = cons(1, lambda: ones)

integers = cons(1, lambda: add(ones, integers))

fibs = cons(0, lambda: cons(1, lambda: add(rest(fibs), fibs)))

primes = cons(2, lambda: filter(is_prime, count(3)))

if __name__ == '__main__':
    foreach(lambda p: print(f'{p:,d}'),
            takewhile(lambda n: n < 20,
                      dropwhile(lambda n: n < 10,
                                integers)))
