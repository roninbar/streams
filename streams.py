import operator
from typing import Callable, TypeAlias, TypeVar, Any

T = TypeVar('T')

Promise: TypeAlias = Callable[[], T]

Stream: TypeAlias = tuple | tuple[T, Promise[Any]]  # Actually, tuple[T, Promise[Stream[T]]]

the_empty_stream = ()


def force(p: Promise[T]) -> T:
    return p()


def is_null(s: Stream[T]) -> bool:
    return s == the_empty_stream


# noinspection PyShadowingNames
def cons(first: T, rest: Promise[Stream[T]]) -> Stream[T]:
    return first, rest


def first(s: Stream[T]) -> T:
    return s[0]


def rest(s: Stream[T]) -> Stream[T]:
    return force(s[1])


# noinspection PyShadowingBuiltins
def range(start: int, finish: int, step: int = 1) -> Stream[int]:
    if start < finish if step > 0 else finish < start:
        return cons(start, lambda: range(start + step, finish, step))
    else:
        return the_empty_stream


def foreach(proc: Callable[[T], None], s: Stream[T]) -> None:
    if not is_null(s):
        proc(first(s))
        foreach(proc, rest(s))


# noinspection PyShadowingBuiltins
def filter(test: Callable[[T], bool], s: Stream[T]) -> Stream[T]:
    if is_null(s):
        return the_empty_stream
    elif test(first(s)):
        return cons(first(s),
                    filter(test, rest(s)))
    else:
        return filter(test, rest(s))


# noinspection PyShadowingBuiltins
def map(proc: Callable[[tuple], T], *ss: tuple[Stream[T]]) -> Stream[T]:
    if is_null(ss[0]):
        return the_empty_stream
    else:
        return cons(proc(*[first(s) for s in ss]),
                    lambda: map(proc, *[rest(s) for s in ss]))


if __name__ == '__main__':
    foreach(print, map(operator.add,
                       range(10, 20),
                       range(30, 40)))
