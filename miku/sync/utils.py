from typing import TypeVar, Iterator, Callable

from miku.utils import Data as _Data

T = TypeVar("T")

class Data(_Data[T]):

    def filter(self, check: Callable[[T], bool]) -> Iterator[T]:
        for elem in self:
            if check(elem):
                yield elem