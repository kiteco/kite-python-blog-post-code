# mr.py
from functools import reduce
from typing import Callable, Iterable, TypeVar, Union, Optional

T = TypeVar('T')
S = TypeVar('S')
Number = Union[int, float]


print()
def map_reduce(
    it: Iterable[T],
    mapper: Callable[[T], S],
    reducer: Callable[[S, S], S],
    filterer: Optional[Callable[[S], bool]]
) -> S:
    mapped = map(mapper, it)
    filtered = filter(filterer, mapped)
    reduced = reduce(reducer, filtered)
    return reduced


def mapper(x: Number) -> Number:
    return x ** 2


def filterer(x: Number) -> bool:
    return x % 2 == 0


def reducer(x: Number, y: Number) -> Number:
    return x + y


results = map_reduce(
    range(10),
    mapper=mapper,
    reducer=reducer,
    filterer=filterer
)
print(results)