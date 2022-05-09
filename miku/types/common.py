from typing import TypedDict, List, Optional

__all__ = (
    'Name',
    'FuzzyDate'
)

class Name(TypedDict):
    first: str
    middle: str
    last: str
    full: str
    native: str
    alternatives: List[str]

class FuzzyDate(TypedDict):
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
