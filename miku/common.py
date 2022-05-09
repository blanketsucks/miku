from typing import List, Optional

from . import types

__all__ = (
    'Name',
    'FuzzyDate',
)

class Name:
    __slots__ = (
        'first',
        'middle',
        'last',
        'full',
        'native',
        'alternatives',
    )

    def __init__(self, payload: types.Name) -> None:
        self.first: str = payload['first']
        self.middle: str = payload['middle']
        self.last: str = payload['last']
        self.full: str = payload['full']
        self.native: str = payload['native']
        self.alternatives: List[str] = payload['alternatives']

class FuzzyDate:
    __slots__ = ('year', 'month', 'day')

    def __init__(self, payload: types.FuzzyDate) -> None:
        self.year: Optional[int] = payload['year']
        self.month: Optional[int] = payload['month']
        self.day: Optional[int] = payload['day']