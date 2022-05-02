from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING
import datetime

from .enums import MediaFormat, MediaRankType, MediaSource, MediaStatus, MediaType, MediaSeason
from .utils import IDComparable, cached_slot_property
from .image import Image
from . import types

if TYPE_CHECKING:
    from .http import HTTPHandler
    from .character import Character

__all__ = (
    'MediaTitle',
    'MediaTrailer',
    'MediaTag',
    'Media',
    'Manga',
    'Anime'
)

class MediaTrend:

    def __init__(self, payload: types.MediaTrend) -> None:
        self.media_id: int = payload['mediaId']
        self.episode: int = payload['episode']
        self.releasing: bool = payload['releasing']
        self.in_progress: int = payload['inProgress']


class MediaTitle:
    __slots__ = ('romaji', 'english', 'native')

    def __init__(self, payload: types.MediaTitle) -> None:
        self.romaji: str = payload['romaji']
        self.english: str = payload['english']
        self.native: str = payload['native']

    def __repr__(self) -> str:
        return '<Title romaji={0.romaji!r} english={0.english!r} native={0.native!r}>'.format(self)

class MediaTrailer(IDComparable):
    __slots__ = ('id', 'site', 'thumbnail')

    def __init__(self, payload: types.MediaTrailer) -> None:
        self.id: str = payload['id']
        self.site: str = payload['site']
        self.thumbnail: str = payload['thumbnail']
    
    def __repr__(self) -> str:
        return f'<MediaTrailer id={self.id!r} site={self.site!r}>'

class MediaTag(IDComparable):
    __slots__ = (
        'id', 
        'name', 
        'category', 
        'description', 
        'rank', 
        'is_general_spoiler', 
        'is_media_spoiler',
        'is_adult',
        'user_id'
    )

    def __init__(self, payload: types.MediaTag) -> None:
        self.id: int = payload['id']
        self.name: str = payload['name']
        self.category: str = payload['category']
        self.description: str = payload['description']
        self.rank: int = payload['rank']
        self.is_general_spoiler: bool = payload['isGeneralSpoiler']
        self.is_media_spoiler: bool = payload['isMediaSpoiler']
        self.is_adult: bool = payload['isAdult']
        self.user_id: int = payload['userId']

    def __repr__(self) -> str:
        return f'<MediaTag id={self.id} name={self.name!r}>'

class MediaAiringSchedule(IDComparable):
    __slots__ = ('_payload', 'id', 'episode', 'media_id')

    def __init__(self, payload: types.MediaAiringSchedule) -> None:
        self._payload = payload

        self.id: int = payload['id']
        self.episode: int = payload['episode']
        self.media_id: int = payload['mediaId']

    @property
    def airing_at(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._payload['airingAt'])

    @property
    def time_until_airing(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self._payload['timeUntilAiring'])

    def __repr__(self) -> str:
        return f'<MediaAiringSchedule id={self.id} episode={self.episode}>'

class MediaStreamingEpisode:
    __slots__ = ('title', 'thumbnail', 'url', 'site')

    def __init__(self, payload: types.MediaStreamingEpisode) -> None:
        self.title: str = payload['title']
        self.thumbnail: str = payload['thumbnail']
        self.url: str = payload['url']
        self.site: str = payload['site']

    def __repr__(self) -> str:
        return f'<MediaStreamingEpisode title={self.title!r} site={self.site!r}>'

class MediaRank(IDComparable):
    __slots__ = ('_payload', 'id', 'rank', 'year', 'all_time', 'context')

    def __init__(self, payload: types.MediaRank) -> None:
        self._payload = payload

        self.id: int = payload['id']
        self.rank: int = payload['rank']
        self.year: int = payload['year']
        self.all_time: bool = payload['allTime']
        self.context: str = payload['context']

    def __repr__(self) -> str:
        return f'<MediaRank id={self.id} rank={self.rank}>'

    @property
    def type(self) -> MediaRankType:
        return MediaRankType(self._payload['type'])

    @property
    def format(self) -> MediaFormat:
        return MediaFormat(self._payload['format'])

    @property
    def season(self) -> MediaSeason:
        return MediaSeason(self._payload['season'])
    

class Media(IDComparable):
    __slots__ = (
        '_payload',
        '_http',
        '_cs_characters',
        'id',
        'mal_id',
        'url',
        'average_score',
        'mean_score',
        'is_licensed',
        'genres',
        'trending',
        'is_adult',
        'synonyms',
        'description',
        'hashtag',
        'popularity',
        'favourites',
    )

    def __init__(self, payload: types.Media, http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.id: int = payload['id']
        self.mal_id: int = payload['idMal']
        self.url: str = self._payload['siteUrl']
        self.average_score: Optional[int] = self._payload['averageScore']
        self.mean_score: int = self._payload['meanScore']
        self.is_licensed: bool = self._payload['isLicensed']
        self.genres: List[str] = self._payload['genres']
        self.trending: int = self._payload['trending']
        self.is_adult: bool = self._payload['isAdult']
        self.synonyms: List[str] = self._payload['synonyms']
        self.description: str = self._payload['description']
        self.hashtag: str = self._payload['hashtag']
        self.popularity: int = self._payload['popularity']
        self.favourites: int = self._payload['favourites']

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f'<{name} id={self.id} title={self.title.romaji!r} average_score={self.average_score}>'

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
    def season(self) -> MediaSeason:
        return MediaSeason(self._payload['season'])

    @property
    def source(self) -> MediaSource:
        return MediaSource(self._payload['source'])

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
    def episodes(self) -> Optional[int]:
        return self._payload['episodes']

    @property
    def updated_at(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._payload['updatedAt'])

    @property
    def title(self) -> MediaTitle:
        return MediaTitle(self._payload['title'])

    @property
    def tags(self) -> List[MediaTag]:
        return [MediaTag(tag) for tag in self._payload['tags']]

    @property
    def trailer(self) -> Optional[MediaTrailer]:
        return MediaTrailer(self._payload['trailer']) if self._payload['trailer'] else None

    @property
    def next_airing_episode(self) -> Optional[MediaAiringSchedule]:
        data = self._payload['nextAiringEpisode']
        return MediaAiringSchedule(data) if data else None

    @property
    def streaming_episodes(self) -> Optional[List[MediaStreamingEpisode]]:
        data = self._payload['streamingEpisodes']
        return [MediaStreamingEpisode(episode) for episode in data] if data else None

    @property
    def rankings(self) -> List[MediaRank]:
        return [MediaRank(rank) for rank in self._payload['rankings']]

    @property
    def banner(self) -> Image:
        return Image(self._http.session, self._payload['bannerImage']) # type: ignore

    @property
    def cover(self) -> Image:
        return Image(self._http.session, self._payload['coverImage']) # type: ignore

    @cached_slot_property('_cs_characters')
    def characters(self) -> List[Character]:
        from .character import Character

        characters = self._payload['characters']['nodes']
        return [Character(data, self._http) for data in characters]

class Anime(Media):
    pass

class Manga(Media):
    pass
