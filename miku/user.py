from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from .enums import MediaType, UserNotificationOptionType, UserTitleLanguage, ScoreFormat, ModeratorRole, MediaListStatus
from .image import Image
from .media import Manga, Anime, Media
from .character import Character
from .staff import Staff
from .studio import Studio
from .utils import IDComparable, cached_slot_property
from .paginator import ChunkPaginator
from . import types

if TYPE_CHECKING:
    from .http import HTTPHandler

__all__ = (
    'MediaListTypeOptions',
    'MediaListOptions',
    'MediaList',
    'MediaListGroup',
    'UserNotificationOption',
    'UserOptions',
    'UserFavourites',
    'User'
)

class MediaListTypeOptions:
    __slots__ = (
        'section_order',
        'split_completed_section_by_format',
        'custom_lists',
        'advanced_scoring',
        'advanced_scoring_enabled',
    )

    def __init__(self, payload: types.MediaListTypeOptions) -> None:
        self.section_order: List[str] = payload['sectionOrder']
        self.split_completed_section_by_format: bool = payload['splitCompletedSectionByFormat']
        self.custom_lists: List[str] = payload['customLists']
        self.advanced_scoring: List[str] = payload['advancedScoring']
        self.advanced_scoring_enabled: bool = payload['advancedScoringEnabled']

class MediaListOptions:
    __slots__ = (
        '_payload',
        'score_format',
        'row_order',
    )

    def __init__(self, payload: types.MediaListOptions) -> None:
        self._payload = payload

        self.score_format = ScoreFormat(payload['scoreFormat'])
        self.row_order: str = payload['rowOrder']

    @property
    def anime_list(self) -> MediaListTypeOptions:
        return MediaListTypeOptions(self._payload['animeList'])

    @property
    def manga_list(self) -> MediaListTypeOptions:
        return MediaListTypeOptions(self._payload['mangaList'])

class MediaList(IDComparable):
    __slots__ = (
        '_payload',
        '_http',
        'id',
        'media_id',
        'score',
        'progress',
        'repeat',
        'notes',
        'private',
        'priority',
    )

    def __init__(self, payload: types.MediaList, http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http
        
        self.id: int = payload['id']
        self.media_id: int = payload['mediaId']
        self.score: int = payload['score']
        self.progress: int = payload['progress']
        self.repeat: int = payload['repeat']
        self.notes: str = payload['notes']
        self.private: bool = payload['private']
        self.priority: int = payload['priority']

    def __repr__(self) -> str:
        return f'<MediaList id={self.id} status={self.status}>'

    @property
    def status(self) -> MediaListStatus:
        return MediaListStatus(self._payload['status'])

    @property
    def media(self) -> Media:
        return Media(self._payload['media'], self._http)


class MediaListGroup:
    __slots__ = (
        '_payload',
        '_http',
        '_cs_entries',
        'name',
        'is_custom_list',
        'is_split_custom_list',
    )

    def __init__(self, payload: types.MediaListGroup, http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.name: str = payload['name']
        self.is_custom_list: bool = payload['isCustomList']
        self.is_split_custom_list: bool = payload['isSplitCompletedList']

    def __repr__(self) -> str:
        return f'<MediaListGroup name={self.name!r} entries={len(self.entries)}>'

    @property
    def status(self) -> MediaListStatus:
        return MediaListStatus(self._payload['status'])

    @cached_slot_property('_cs_entries')
    def entries(self) -> List[MediaList]:
        return [MediaList(entry, self._http) for entry in self._payload['entries']]

class UserNotificationOption:
    __slots__ = ('enabled', 'type')

    def __init__(self, payload: types.UserNotificationOption) -> None:
        self.enabled: bool = payload['enabled']
        self.type = UserNotificationOptionType(payload['type'])

    def __repr__(self) -> str:
        return f'<UserNotificationOption enabled={self.enabled} type={self.type}>'

class UserOptions:
    __slots__ = (
        'title_language',
        'display_adult_content',
        'airing_notifications',
        'profile_color',
        'notification_options'
    )

    def __init__(self, payload: types.UserOptions) -> None:
        self.title_language: UserTitleLanguage = UserTitleLanguage(payload['titleLanguage'])
        self.display_adult_content: bool = payload['displayAdultContent']
        self.airing_notifications: bool = payload['airingNotifications']
        self.profile_color: str = payload['profileColor']
        self.notification_options: List[UserNotificationOption] = [
            UserNotificationOption(data) for data in payload['notificationOptions']
        ]

class UserFavourites:
    __slots__ = ('_payload', '_http', '_cs_anime', '_cs_manga', '_cs_characters', '_cs_staff', '_cs_studios')

    def __init__(self, payload: types.UserFavourites, http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

    def _get_nodes(self, type: str) -> Any:
        return self._payload.get(type, {}).get('nodes', [])

    @cached_slot_property('_cs_anime')
    def anime(self) -> List[Anime]:
        return [Anime(anime, self._http) for anime in self._get_nodes('anime')]

    @cached_slot_property('_cs_manga')
    def manga(self) -> List[Manga]:
        return [Manga(manga, self._http) for manga in self._get_nodes('manga')]

    @cached_slot_property('_cs_characters')
    def characters(self) -> List[Character]:
        return [Character(character, self._http) for character in self._get_nodes('characters')]

    @cached_slot_property('_cs_studios')
    def studios(self) -> List[Studio]:
        return [Studio(studio, self._http) for studio in self._get_nodes('studios')]

    @cached_slot_property('_cs_staff')
    def staff(self) -> List[Staff]:
        return [Staff(staff, self._http) for staff in self._get_nodes('staff')]

class User(IDComparable):
    __slots__ = (
        '_payload',
        '_http',
        'name',
        'id',
        'url',
        'about',
        'bans',
        'donator_tier',
        'donator_badge',
    )

    def __init__(self, payload: types.User, http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.name: str = payload['name']
        self.id: int = payload['id']
        self.url: str = payload['siteUrl']
        self.about: str = payload['about']
        self.bans: List[Any] = payload['bans']
        self.donator_tier: int = payload['donatorTier']
        self.donator_badge: str = payload['donatorBadge']

    def __repr__(self) -> str:
        return '<User id={0.id} name={0.name!r}>'.format(self)

    @property
    def avatar(self) -> Image:
        return Image(self._http.session, self._payload['avatar'])

    @property
    def banner(self) -> Optional[Image]:
        image = self._payload['bannerImage']
        return Image.from_url(self._http.session, image) if image else None
 
    @property
    def options(self) -> UserOptions:
        return UserOptions(self._payload['options'])

    @property
    def roles(self) -> List[ModeratorRole]:
        data = self._payload['moderatorRoles'] or []
        return [ModeratorRole(role) for role in data]

    @property
    def favourites(self) -> UserFavourites:
        return UserFavourites(self._payload['favourites'], self._http)

    @property
    def media_list_options(self) -> MediaListOptions:
        return MediaListOptions(self._payload['mediaListOptions'])

    async def fetch_thread(self):
        from .threads import Thread

        data = await self._http.get_thread_from_user_id(self.id)
        return Thread(data, self._http)

    def fetch_media_list(
        self, *, type: MediaType, per_chunk: int = 50, chunk: int = 0
    ) -> ChunkPaginator[MediaListGroup]:
        return self._http.get_media_list_collection(self.id, type.value, per_chunk, chunk)