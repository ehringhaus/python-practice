from itertools import groupby
from functools import reduce
from typing import Iterator
from dataclasses import dataclass
from operator import attrgetter


@dataclass
class OrderedLetterCount:
    index: int
    letter: str
    count: int


def abc_sort(s: str) -> str:
    return ''.join(sorted(iter(s)))


def abc_group(s: str) -> Iterator[str]:
    return groupby(s)


def abc_label(g: Iterator[str]) -> OrderedLetterCount:
    for i, (char, group) in enumerate(g):
        yield OrderedLetterCount(i, char, len(list(group)))


def sort_results(data: OrderedLetterCount) -> OrderedLetterCount:
    return sorted(list(data), key=attrgetter('count'), reverse=True)[:3]


def display_results(sorted_data: OrderedLetterCount) -> str:
    for ele in sorted_data:
        print(ele.letter, '->', ele.count)


def compose(*funcs):
    def _compose(f, g):
        def _c(x):
            return f(g(x))
        return _c
    return reduce(_compose, funcs)


test_strings = ['aabbbccde',
                'google',
                'hihowareyoudoingtoday']

fx = compose(display_results,
             sort_results,
             abc_label,
             abc_group,
             abc_sort)

for string in test_strings:
    print(string)
    fx(string)
    print('-' * 10)
