from collections import namedtuple
from typing import Any, Dict, List, Optional, TYPE_CHECKING
import enum
import datetime
import aiohttp

from .image import Image

if TYPE_CHECKING:
    from .character import Character

__all__ = (
    'Tag',
    'MediaFormat',
    'MediaStatus',
    'MediaType',
    'MediaSource',
    'Title',
    'Media',
    'Manga',
    'Anime'
)

Tag = namedtuple('Tag', ['name'])

class MediaFormat(enum.Enum):
    TV = 'TV'
    TV_SHORT = 'TV_SHORT'
    MOVIE = 'MOVIE'
    OVA = 'OVA'
    ONA = 'ONA'
    MUSIC = 'MUSIC'
    MANGA = 'MANGA'
    NOVEL = 'NOVEL'
    ONE_SHOT = 'ONE_SHOT'

class MediaStatus(enum.Enum):
    FINISHED = 'FINISHED'
    RELEASING = 'RELEASING'
    NOT_YET_RELEASED = 'NOT_YET_RELEASED'
    CANCELLED = 'CANCELLED'
    HIATUS = 'HIATUS'

class MediaType(enum.Enum):
    ANIME = 'ANIME'
    MANGA = 'MANGA'

class MediaSource(enum.Enum):
    ORIGINAL = 'ORIGINAL'
    MANGA = 'MANGA'
    LIGHT_NOVEL = 'LIGHT_NOVEL'
    VISUAL_NOVEL = 'VISUAL_NOVEL'
    VIDEO_GAME = 'VIDEO_GAME'
    OTHER = 'OTHER'
    NOVEL = 'NOVEL'
    DOUJINSHI = 'DOUJINSHI'
    ANIME = 'ANIME'

class Title:
    def __init__(self, payload) -> None:
        self.__payload = payload['title']

    @property
    def romaji(self) -> str:
        return self.__payload['romaji']

    @property
    def english(self) -> str:
        return self.__payload['english']

    @property
    def native(self) -> str:
        return self.__payload['native']

class Media:
    """
    A class defining a media.
    Both the Manga and Anime classes inherit from this class.
    """
    def __init__(self, payload: Dict[str, Any], session: aiohttp.ClientSession) -> None:
        self._payload = payload
        self._session = session

    def __repr__(self) -> str:
        return '<{0.__class__.__name__} title={0.title.romaji!r}>'.format(self)

    @property
    def type(self) -> MediaType:
        """
        Returns:
            The type of the media.
        """
        return MediaType(self._payload['type'])

    @property
    def format(self) -> MediaFormat:
        """
        Returns:
            The format of this media.
        """
        return MediaFormat(self._payload['format'])

    @property
    def status(self) -> MediaStatus:
        """
        Returns:
            The status of this media.
        """
        return MediaStatus(self._payload['status'])

    @property
    def tags(self) -> List[Tag]:
        """
        Returns:
            A list of `Tag`s.
        """
        return [Tag(data['name']) for data in self._payload['tags']]

    @property
    def url(self) -> str:
        """
        Returns:
            Anilist URL for this media.
        """
        return self._payload['siteUrl']

    @property
    def score(self) -> int:
        """
        Returns:
            The average score of this media.
        """
        return self._payload['averageScore']

    @property
    def duration(self) -> Optional[int]:
        """
        Returns:
            The general length of each anime episode in minutes or None.
        """
        return self._payload['duration']

    @property
    def chapters(self) -> Optional[int]:
        """
        Returns:
            The amount of chapters the manga has when complete or None.
        """
        return self._payload['chapters']

    @property
    def volumes(self) -> Optional[int]:
        """
        Returns:
            The amount of volumes the manga has when complete or None.
        """
        return self._payload['volumes']

    @property
    def source(self) -> MediaSource:
        return self._payload['source']

    @property
    def is_licensed(self) -> bool:
        """
        Returns:
            If the media is officially licensed or a self-published doujin release.
        """
        return self._payload['isLicensed']

    @property
    def updated_at(self) -> datetime.datetime:
        """
        Returns:
            The last time this media was updated at.
        """
        return datetime.datetime.fromtimestamp(self._payload['updatedAt'])

    @property
    def genres(self) -> List[str]:
        """
        Returns:
            The genres of this media.
        """
        return self._payload['genres']

    @property
    def trending(self) -> int:
        """
        Returns:
            The amount of related activity in the past hour.
        """
        return self._payload['trending']

    @property
    def is_adult(self) -> bool:
        """
        Returns:
            A bool indecating if the media is intended only for 18+ adult audiences.
        """
        return self._payload['isAdult']

    @property
    def synonyms(self) -> List[str]:
        """
        Returns:
            Alternative titles of the media.
        """
        return self._payload['synonyms']

    @property
    def episodes(self) -> Optional[int]:
        """
        Returns:
            The number of the episodes this media has.
            If the type of the media is MANGA then this returns None.
        """
        return self._payload['episodes']

    @property
    def title(self) -> Title:
        """
        Returns:
            A `Title` object with the attribute: 'english', 'native' and 'romaji'.
        """
        return Title(self._payload)

    @property
    def description(self) -> str:
        """
        Returns:
            The description of this media.
        """
        return self._payload['description']

    @property
    def banner_image(self) -> Image:
        """
        Returns:
            an [Image](./media) object.
        """

        return Image(self._session, self._payload['bannerImage'])

    @property
    def cover_image(self) -> Image:
        """
        Returns:
            an [Image](./media) object.
        """
        return Image(self._session, self._payload['coverImage'])

    @property
    def characters(self) -> List[Character]:
        """
        Returns:
            A list of [Character](./character.md) that appear on this media.
        """
        from .character import Character

        characters = self._payload['characters']['nodes']
        return [Character(data, self._session) for data in characters]

class Anime(Media):
    pass

class Manga(Media):
    pass

def _get_media(payload):
    if payload['type'] == 'ANIME':
        return Anime

    return Manga