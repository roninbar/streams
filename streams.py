from typing import Callable, TypeAlias, TypeVar, Any

T = TypeVar('T')

Promise: TypeAlias = Callable[[], T]

Stream: TypeAlias = tuple | tuple[T, Promise[Any]]  # Actually, tuple[T, Promise[Stream[T]]]

the_empty_stream = ()


def is_null(s: Stream[T]) -> bool:
    return s == the_empty_stream


def force(p: Promise[T]) -> T:
    return p()


def memoize(proc: Callable[[], T]) -> Callable[[], T]:
    already_run: bool = False
    result: T = None

    def memoized() -> T:
        nonlocal result, already_run
        if not already_run:
            result = proc()
            already_run = True
        return result

    return memoized


# noinspection PyShadowingNames
def pair(head: T, tail: Promise[Stream[T]]) -> Stream[T]:
    return head, memoize(tail)


def head(s: Stream[T]) -> T:
    return s[0]


def tail(s: Stream[T]) -> Stream[T]:
    return force(s[1])


# noinspection PyShadowingBuiltins
def range(start: int, finish: int, step: int = 1) -> Stream[int]:
    if start < finish if step > 0 else finish < start:
        return pair(start, lambda: range(start + step, finish, step))
    else:
        return the_empty_stream


def count(start: int, step: int = 1) -> Stream[int]:
    return pair(start,
                lambda: count(start + step))


def ref(n: int, s: Stream[T]) -> T:
    while n > 0:
        n, s = n - 1, tail(s)
    else:
        return head(s)


def foreach(proc: Callable[[T], None], s: Stream[T]) -> None:
    while not is_null(s):
        proc(head(s))
        s = tail(s)


# noinspection PyShadowingBuiltins
def filter(test: Callable[[T], bool], s: Stream[T]) -> Stream[T]:
    while not is_null(s) and not test(head(s)):
        s = tail(s)
    else:
        return the_empty_stream if is_null(s) else pair(head(s), lambda: filter(test, tail(s)))


# noinspection PyShadowingBuiltins
def map(proc: Callable[[tuple], T], *ss: tuple[Stream[T]]) -> Stream[T]:
    if is_null(ss[0]):
        return the_empty_stream
    else:
        return pair(proc(*[head(s) for s in ss]),
                    lambda: map(proc, *[tail(s) for s in ss]))


def takewhile(test: Callable[[T], bool], s: Stream[T]) -> Stream[T]:
    if is_null(s) or not test(head(s)):
        return the_empty_stream
    else:
        return pair(head(s), lambda: takewhile(test, tail(s)))


def dropwhile(test: Callable[[T], bool], s: Stream[T]) -> Stream[T]:
    while not is_null(s) and test(head(s)):
        s = tail(s)
    else:  # is_null(s) or not test(head(s))
        return s
