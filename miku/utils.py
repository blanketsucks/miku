from typing import Any

__all__ = 'IDComparable',

class IDComparable:
    id: int

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

