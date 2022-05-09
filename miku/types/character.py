from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, List, Optional

from .image import Image
from .common import Name, FuzzyDate

if TYPE_CHECKING:
    from .nodes import MediaNodes

__all__ = (
    'Character',
)

class Character(TypedDict):
    description: str
    favourites: int
    siteUrl: str
    gender: str
    age: str
    name: Name
    dateOfBirth: FuzzyDate
    media: MediaNodes
    image: Image