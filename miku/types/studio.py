from __future__ import annotations

from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from .nodes import MediaNodes

__all__ = 'Studio',

class Studio(TypedDict):
    id: int
    name: str
    favourites: int
    isAnimationStudio: bool
    siteUrl: str
    media: MediaNodes