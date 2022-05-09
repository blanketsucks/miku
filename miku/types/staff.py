from __future__ import annotations

from typing import TYPE_CHECKING, List, TypedDict, Optional

from .image import Image
from .common import Name, FuzzyDate

if TYPE_CHECKING:
    from .nodes import CharacterNodes

__all__ = (
    'Staff',
)

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
    dateOfBirth: FuzzyDate
    dateOfDeath: FuzzyDate
    characters: CharacterNodes