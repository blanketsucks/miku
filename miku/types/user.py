from __future__ import annotations

from typing import TypedDict, List, TYPE_CHECKING

from .image import Image

if TYPE_CHECKING:
    from .nodes import CharacterNodes, AnimeNodes, MangaNodes, StaffNodes, StudioNodes

__all__ = (
    'UserNotificationOption',
    'UserOptions',
    'UserFavourites',
    'User',
)

class UserNotificationOption(TypedDict):
    enabled: bool
    type: str

class UserOptions(TypedDict):
    titleLanguage: str
    displayAdultContent: bool
    airingNotifications: bool
    profileColor: str
    notificationOptions: List[UserNotificationOption]

class UserFavourites(TypedDict):
    anime: AnimeNodes
    manga: MangaNodes
    characters: CharacterNodes
    staff: StaffNodes
    studios: StudioNodes

class User(TypedDict):
    id: int
    name: str
    siteUrl: str
    options: UserOptions
    bannerImage: Image
    avatar: Image