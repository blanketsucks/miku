from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, List, Optional

from .image import Image

if TYPE_CHECKING:
    from .nodes import MediaNodes

__all__ = (
    'Name',
    'DateOfBirth',
    'Character',
)

class Name(TypedDict):
    first: str
    middle: str
    last: str
    full: str
    native: str
    alternatives: List[str]

class DateOfBirth(TypedDict):
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]

class Character(TypedDict):
    description: str
    favourites: int
    siteUrl: str
    gender: str
    age: str
    name: Name
    dateOfBirth: DateOfBirth
    media: MediaNodes
    image: Image