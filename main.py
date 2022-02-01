import operator
from functools import reduce

from streams import Stream, foreach, filter, pair, head, tail, count, map, takewhile, dropwhile


def is_prime(n: int) -> bool:
    if n >= 2:
        ps = primes
        while (p := head(ps)) ** 2 <= n and n % p != 0:
            print(f'{n:,d} % {p} == {n % p}')
            ps = tail(ps)
        else:
            return p * p > n
    else:
        raise ValueError(f'Argument `n` must be at least 2. {n} received.')


def sieve(s: Stream[int]) -> Stream:
    return pair(head(s),
                lambda: sieve(filter(lambda x: x % head(s) != 0,
                                     tail(s))))


def add(s1: Stream[int], s2: Stream[int]):
    return map(operator.add, s1, s2)


def scale(a: int, s: Stream[int]) -> Stream[int]:
    return map(lambda n: a * n, s)


def merge(*ss: tuple[Stream[int]]) -> Stream[int]:
    def merge2(s1: Stream[int], s2: Stream[int]) -> Stream[int]:
        if not s1:
            return s2
        elif not s2:
            return s1
        else:
            if head(s2) < head(s1):
                s1, s2 = s2, s1
            return pair(head(s1), lambda: merge2(tail(s1), s2 if head(s1) != head(s2) else tail(s2)))

    return reduce(merge2, ss, ())


ones = pair(1, lambda: ones)

integers = pair(1, lambda: add(ones, integers))

fibs = pair(0, lambda: pair(1, lambda: add(tail(fibs), fibs)))

primes = pair(2, lambda: filter(is_prime, count(3)))

s235 = pair(1, lambda: merge(scale(2, s235), scale(3, s235), scale(5, s235)))

if __name__ == '__main__':
    k = 0


    def writeln(p):
        global k
        print(f'[{k}] {p:,d}')
        k += 1


    foreach(writeln, takewhile(lambda p: p < 1_000_000, s235))