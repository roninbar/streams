import streams


def is_prime(n: int) -> bool:
    if n < 2:
        raise ValueError(f'Argument `n` must be at least 2. {n} received.')
    else:
        p = 2
        while p * p <= n:
            if n % p == 0:
                break
            p += 1
        else:
            return True
        return False


if __name__ == '__main__':
    streams.foreach(lambda p: print(f'{p:,d}'),
                    streams.filter(is_prime,
                                   streams.range(10_000, 100_000)))
