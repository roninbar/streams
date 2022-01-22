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


def stream_enumerate_interval(low: int, high: int) -> Stream[int]:
    if low < high:
        return cons_stream(low, lambda: stream_enumerate_interval(low + 1, high))
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


if __name__ == '__main__':
    stream_for_each(print, stream_enumerate_interval(10, 20))

