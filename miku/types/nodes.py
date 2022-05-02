from typing import List, TypedDict

from .media import Media
from .character import Character
from .studio import Studio
from .staff import Staff

__all__ = (
    'MediaNodes',
    'AnimeNodes',
    'MangaNodes',
    'CharacterNodes',
    'StaffNodes',
    'StudioNodes',
)

class MediaNodes(TypedDict):
    nodes: List[Media]

class AnimeNodes(MediaNodes):
    pass

class MangaNodes(MediaNodes):
    pass

class CharacterNodes(TypedDict):
    nodes: List[Character]

class StudioNodes(TypedDict):
    nodes: List[Studio]

class StaffNodes(TypedDict):
    nodes: List[Staff]

