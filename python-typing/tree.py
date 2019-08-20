# tree.py (final)
from typing import Tuple, Iterable, Dict, List, DefaultDict, TypeVar
from collections import defaultdict

T = TypeVar('T')

Relation = Tuple[T, T]


def create_tree(tuples: Iterable[Relation]) -> DefaultDict[T, List[T]]:
    """
    Return a tree given tuples of (child, father)

    The tree structure is as follows:

        tree = {node_1: [node_2, node_3],
                node_2: [node_4, node_5, node_6],
                node_6: [node_7, node_8]}
    """
    # convert to dict
    tree: DefaultDict[T, List[T]] = defaultdict(list)
    for pair in tuples:
        child, father = pair
        if father:
            tree[father].append(child)

    return tree


print(create_tree([(2.0, 1.0), (3.0, 1.0), (4.0, 3.0), (1.0, 6.0)]))

"""
Generic Classes
"""


def return_values() -> Iterable[float]:
    yield 4.0
    yield 5.0
    yield 6.0


def chain(*args: Iterable[T]) -> Iterable[T]:
    for arg in args:
        yield from arg


print(list(chain([1, 2, 3], return_values(), 'string')))

