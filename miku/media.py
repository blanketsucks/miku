from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING
import datetime

from .enums import MediaFormat, MediaSource, MediaStatus, MediaType
from .image import Image

if TYPE_CHECKING:
    from .http import HTTPHandler
    from .character import Character

__all__ = (
    'MediaTitle',
    'Media',
    'Manga',
    'Anime'
)

class MediaTitle:
    __slots__ = ('romaji', 'english', 'native')

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.romaji: str = payload['title']['romaji']
        self.english: str = payload['title']['english']
        self.native: str = payload['title']['native']

    def __repr__(self) -> str:
        return '<Title romaji={0.romaji!r} english={0.english!r} native={0.native!r}>'.format(self)

class Media:
    __slots__ = (
        '_payload',
        '_http',
        'url',
        'average_score',
        'is_licensed',
        'genres',
        'trending',
        'is_adult',
        'synonyms',
        'description'
    )

    def __init__(self, payload: Dict[str, Any], http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.url: str = self._payload['siteUrl']
        self.average_score: int = self._payload['averageScore']
        self.is_licensed: bool = self._payload['isLicensed']
        self.genres: List[str] = self._payload['genres']
        self.trending: int = self._payload['trending']
        self.is_adult: bool = self._payload['isAdult']
        self.synonyms: List[str] = self._payload['synonyms']
        self.description = self._payload['description']

    def __repr__(self) -> str:
        return '<{0.__class__.__name__} title={0.title.romaji!r}>'.format(self)

    @property
    def type(self) -> MediaType:
        return MediaType(self._payload['type'])

    @property
    def format(self) -> MediaFormat:
        return MediaFormat(self._payload['format'])

    @property
    def status(self) -> MediaStatus:
        return MediaStatus(self._payload['status'])

    @property
    def tags(self) -> List[str]:
        return [tag['name'] for tag in self._payload['tags']]

    @property
    def duration(self) -> Optional[int]:
        return self._payload['duration']

    @property
    def chapters(self) -> Optional[int]:
        return self._payload['chapters']

    @property
    def volumes(self) -> Optional[int]:
        return self._payload['volumes']

    @property
    def source(self) -> MediaSource:
        return MediaSource(self._payload['source'])

    @property
    def updated_at(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._payload['updatedAt'])

    @property
    def episodes(self) -> Optional[int]:
        return self._payload['episodes']

    @property
    def title(self) -> MediaTitle:
        return MediaTitle(self._payload)

    @property
    def banner(self) -> Image:
        return Image(self._http.session, self._payload['bannerImage']) # type: ignore

    @property
    def cover(self) -> Image:
        return Image(self._http.session, self._payload['coverImage']) # type: ignore

    @property
    def characters(self) -> List[Character]:
        from .character import Character

        characters = self._payload['characters']['nodes']
        return [Character(data, self._http) for data in characters]

class Anime(Media):
    pass

class Manga(Media):
    pass
