from __future__ import annotations

from typing import TYPE_CHECKING, List, TypedDict, Optional

from .image import Image
from .character import DateOfBirth, Name

if TYPE_CHECKING:
    from .nodes import CharacterNodes

__all__ = (
    'DateOfDeath',
    'Staff'
)

class DateOfDeath(TypedDict):
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]

class Staff(TypedDict):
    id: int
    description: str
    languageV2: str
    siteUrl: str
    primaryOccupations: List[str]
    gender: str
    age: int
    homeTown: str
    image: Image
    name: Name
    dateOfBirth: DateOfBirth
    dateOfDeath: DateOfDeath
    characters: CharacterNodes