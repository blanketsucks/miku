from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional
import functools

from .enums import UserNotificationOptionType, UserTitleLanguage
from .image import Image
from .media import Manga, Anime
from .character import Character
from .staff import Staff
from .studio import Studio
from .utils import IDComparable

if TYPE_CHECKING:
    from .http import HTTPHandler

__all__ = (
    'UserNotificationOption',
    'UserOptions',
    'User'
)
class UserNotificationOption:
    __slots__ = ('enabled', 'type')

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.enabled: bool = payload['enabled']
        self.type = UserNotificationOptionType(payload['type'])

    def __repr__(self) -> str:
        return '<UserNotificationOption enabled={0.enabled} type={0.type!r}>'.format(self)

class UserOptions:
    __slots__ = (
        'title_language',
        'display_adult_content',
        'airing_notifications',
        'profile_color',
        'notification_options'
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.title_language: UserTitleLanguage = UserTitleLanguage(payload['titleLanguage'])
        self.display_adult_content: bool = payload['displayAdultContent']
        self.airing_notifications: bool = payload['airingNotifications']
        self.profile_color: str = payload['profileColor']
        self.notification_options: List[UserNotificationOption] = [
            UserNotificationOption(data) for data in payload['notificationOptions']
        ]

class UserFavourites:
    __slots__ = ('_payload', '_http')

    def __init__(self, payload: Dict[str, Any], http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

    @functools.cached_property
    def anime(self) -> List[Anime]:
        return [Anime(anime, self._http) for anime in self._payload['anime']['nodes']]

    @functools.cached_property
    def manga(self) -> List[Manga]:
        return [Manga(manga, self._http) for manga in self._payload['manga']['nodes']]

    @functools.cached_property
    def characters(self) -> List[Character]:
        return [Character(character, self._http) for character in self._payload['characters']['nodes']]

    @functools.cached_property
    def studios(self) -> List[Studio]:
        return [Studio(studio, self._http) for studio in self._payload['studios']['nodes']]

    @functools.cached_property
    def staff(self) -> List[Staff]:
        return [Staff(staff, self._http) for staff in self._payload['staff']['nodes']]

class User(IDComparable):
    __slots__ = (
        '_payload',
        '_http',
        'name',
        'id',
        'url'
    )

    def __init__(self, payload: Dict[str, Any], http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.name: str = self._payload['name']
        self.id: int = self._payload['id']
        self.url: str = self._payload['siteUrl']

    def __repr__(self) -> str:
        return '<User id={0.id} name={0.name!r}>'.format(self)

    async def fetch_thread(self):
        from .threads import Thread

        data = await self._http.get_thread_from_user_id(self.id)
        return Thread(data['data']['Thread'], self._http)

    @property
    def avatar(self) -> Image:
        """
        Returns:
            The avatar of the user as an [Image](./image.md) object.
        """
        return Image(self._http.session, self._payload['avatar']) # type: ignore

    @property
    def banner(self) -> Optional[Image]:
        """
        Returns:
            The banner of the user as an [Image](./image.md) object.
        """
        if not self._payload['bannerImage']:
            return None

        return Image(self._http.session, self._payload['bannerImage']) # type: ignore
 
    @property
    def options(self) -> UserOptions:
        """
        Returns:
            A [UserOptions](./user.md) object.
        """
        return UserOptions(self._payload['options'])
