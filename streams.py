import operator
from typing import Callable, TypeAlias, TypeVar, Any

T = TypeVar('T')

Promise: TypeAlias = Callable[[], T]

Stream: TypeAlias = tuple[T, Promise[Any]]  # Actually, tuple[T, Promise[Stream[T]]]

the_empty_stream = ()


def force(p: Promise[T]) -> T:
    return p()


def stream_null(s: Stream[T]) -> bool:
    return s == the_empty_stream


def cons_stream(first, rest: Promise[Stream[T]]) -> Stream[T]:
    return first, rest


def stream_first(s: Stream[T]) -> T:
    return s[0]


def stream_rest(s: Stream[T]) -> Stream[T]:
    return force(s[1])


def stream_enumerate_interval(start: int, finish: int, step: int = 1) -> Stream[int]:
    if start < finish if step > 0 else finish < start:
        return cons_stream(start, lambda: stream_enumerate_interval(start + step, finish, step))
    else:
        return the_empty_stream


def stream_for_each(proc: Callable[[T], None], s: Stream[T]) -> None:
    if not stream_null(s):
        proc(stream_first(s))
        stream_for_each(proc, stream_rest(s))


def stream_filter(pred: Callable[[T], bool], s: Stream[T]) -> Stream[T]:
    if stream_null(s):
        return the_empty_stream
    elif pred(stream_first(s)):
        return cons_stream(stream_first(s),
                           stream_filter(pred, stream_rest(s)))
    else:
        return stream_filter(pred, stream_rest(s))


def stream_map(proc: Callable[[], T], *ss: list[Stream]) -> Stream[T]:
    if stream_null(ss[0]):
        return the_empty_stream
    else:
        return cons_stream(proc(*[stream_first(s) for s in ss]),
                           lambda: stream_map(proc, *[stream_rest(s) for s in ss]))


if __name__ == '__main__':
    stream_for_each(print, stream_map(operator.add,
                                      stream_enumerate_interval(10, 20),
                                      stream_enumerate_interval(30, 40)))
