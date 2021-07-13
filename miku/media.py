from collections import namedtuple
from typing import Any, Dict, List, Optional, TYPE_CHECKING
import enum
import aiohttp

from .image import Image

if TYPE_CHECKING:
    from .character import Character

Tag = namedtuple('Tag', ['name'])

class MediaFormat(enum.Enum):
    """
    An `enum.Enum` defining a media format.
    """
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
    """
    An `enum.Enum` defining a media status.
    """
    FINISHED = 'FINISHED'
    RELEASING = 'RELEASING'
    NOT_YET_RELEASED = 'NOT_YET_RELEASED'
    CANCELLED = 'CANCELLED'
    HIATUS = 'HIATUS'

class MediaType(enum.Enum):
    """
    An `enum.Enum` defining a media type.
    """
    ANIME = 'ANIME'
    MANGA = 'MANGA'

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