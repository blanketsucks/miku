from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING
import enum
import datetime
import aiohttp

from .paginator import Data
from .image import Image

if TYPE_CHECKING:
    from .studio import Studio
    from .character import Character

__all__ = (
    'MediaFormat',
    'MediaStatus',
    'MediaType',
    'MediaSource',
    'MediaTitle',
    'Media',
    'Manga',
    'Anime'
)


class MediaFormat(enum.Enum):
    """
    An `enum.Enum` defining a media format.

    Attributes:
        TV: Anime broadcast on television.
        TV_SHORT: Anime which are under 15 minutes in length and broadcast on television.
        MOVIE: Anime movies with a theatrical release.
        SPECIAL: Special episodes that have been included in DVD/Blu-ray releases, picture dramas, pilots, etc.
        OVA: (Original Video Animation) Anime that have been released directly on DVD/Blu-ray without originally going through a theatrical release or television broadcast.
        ONA: (Original Net Animation) Anime that have been originally released online or are only available through streaming services.
        MUSIC: Short anime released as a music video.
        MANGA: Professionally published manga with more than one chapter.
        NOVEL: Written books released as a series of light novels.
        ONE_SHOT: Manga with just one chapter.
    """
    TV: str = 'TV'
    TV_SHORT: str = 'TV_SHORT'
    MOVIE: str = 'MOVIE'
    SPECIAL: str = 'SPECIAL'
    OVA: str = 'OVA'
    ONA: str = 'ONA'
    MUSIC: str = 'MUSIC'
    MANGA: str = 'MANGA'
    NOVEL: str = 'NOVEL'
    ONE_SHOT: str = 'ONE_SHOT'

class MediaStatus(enum.Enum):
    """
    An `enum.Enum` defining a media status.

    Attributes:
        FINISHED: Has completed and is no longer being released.
        RELEASING: Currently releasing.
        NOT_YET_RELEASED: To be released at a later date.
        CANCELLED: Ended before the work could be finished
        HIATUS: Is currently paused from releasing and will resume at a later date
    """
    FINISHED: str = 'FINISHED'
    RELEASING: str = 'RELEASING'
    NOT_YET_RELEASED: str = 'NOT_YET_RELEASED'
    CANCELLED: str = 'CANCELLED'
    HIATUS: str = 'HIATUS'

class MediaType(enum.Enum):
    """
    An `enum.Enum` defining a media type.

    Attributes:
        ANIME: Japanese Anime.
        MANGA: Asian comic
    """
    ANIME: str = 'ANIME'
    MANGA: str = 'MANGA'

class MediaSource(enum.Enum):
    """
    An `enum.Enum` defining a medias' source.

    Attributes:
        ORIGINAL: An original production not based of another work.
        MANGA: Asian comic book.
        LIGHT_NOVEL: Written work published in volumes.
        VISUAL_NOVEL: Video game driven primary by text and narrative.
        VIDEO_GAME: Video game.
        OTHER: Other.
        NOVEL: Written works not published in volumes.
        DOUJINSHI: Self-published works.
        ANIME: Japanese Anime.
    """
    ORIGINAL: str = 'ORIGINAL'
    MANGA: str = 'MANGA'
    LIGHT_NOVEL: str = 'LIGHT_NOVEL'
    VISUAL_NOVEL: str = 'VISUAL_NOVEL'
    VIDEO_GAME: str = 'VIDEO_GAME'
    OTHER: str = 'OTHER'
    NOVEL: str = 'NOVEL'
    DOUJINSHI: str = 'DOUJINSHI'
    ANIME: str = 'ANIME'

class MediaTitle:
    """
    A media title.

    Attributes:
        romaji: The title in Romaji.
        english: The title in English.
        native: The title in native language.
    """
    def __init__(self, payload) -> None:
        self.romaji: str = payload['title']['romaji']
        self.english: str = payload['title']['english']
        self.native: str = payload['title']['native']

    def __repr__(self) -> str:
        return '<Title romaji={0.romaji!r} english={0.english!r} native={0.native!r}>'.format(self)


class Media:
    """
    A class defining a media.
    Both the Manga and Anime classes inherit from this class.

    Attributes:
        url: Anilist URL for this media.
        average_score: The average score of this media.
        is_licensed: a bool indicating if the media is officially licensed or a self-published doujin release.
        genres: The genres of this media.
        trending: The amount of related activity in the past hour.
        is_adult: A bool indicating if the media is intended only for 18+ adult audiences.
        synonyms: Alternative titles of the media.
        description: The description of this media.
    """
    def __init__(self, payload: Dict[str, Any], session: aiohttp.ClientSession, cls) -> None:
        self._payload = payload
        self._cls = cls
        self._session = session

        self.url: str = self._payload['siteUrl']
        self.average_score: int = self._payload['averageScore']
        self.is_licensed: bool = self._payload['isLicensed']
        self.genres: List[str] = self._payload['genres']
        self.trending: int = self._payload['trending']
        self.is_adult: bool = self._payload['isAdult']
        self.synonyms: List[str] = self._payload['synonyms']
        self.description: str = self._payload['description']

    def __repr__(self) -> str:
        return '<{0.__class__.__name__} title={0.title.romaji!r}>'.format(self)

    @property
    def type(self) -> MediaType:
        """
        Returns:
            A [MediaType](./media-type.md) object.
        """
        return MediaType(self._payload['type'])

    @property
    def format(self) -> MediaFormat:
        """
        Returns:
            A [MediaFormat](./media-format.md) object.
        """
        return MediaFormat(self._payload['format'])

    @property
    def status(self) -> MediaStatus:
        """
        Returns:
            A [MediaStatus](./media-status.md) object.
        """
        return MediaStatus(self._payload['status'])

    @property
    def tags(self) -> List[str]:
        """
        Returns:
            A list of tag names.
        """
        return [tag['name'] for tag in self._payload['tags']]

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
        """
        Returns:
            A [MediaSource](./media-source.md) object.
        """
        return MediaSource(self._payload['source'])

    @property
    def updated_at(self) -> datetime.datetime:
        """
        Returns:
            The last time this media was updated at.
        """
        return datetime.datetime.fromtimestamp(self._payload['updatedAt'])

    @property
    def episodes(self) -> Optional[int]:
        """
        Returns:
            The number of the episodes this media has.
            If the type of the media is MANGA then this returns None.
        """
        return self._payload['episodes']

    @property
    def title(self) -> MediaTitle:
        """
        Returns:
            A [MediaTitle](./media-title.md) object.
        """
        return MediaTitle(self._payload)

    @property
    def banner_image(self) -> Image:
        """
        Returns:
            an [Image](./media) object.
        """

        return self._cls(self._session, self._payload['bannerImage'])

    @property
    def cover_image(self) -> Image:
        """
        Returns:
            an [Image](./media) object.
        """
        return self._cls(self._session, self._payload['coverImage'])

    @property
    def characters(self) -> Data[Character]:
        """
        Returns:
            A list of [Character](./character.md) that appear on this media.
        """
        from .character import Character

        characters = self._payload['characters']['nodes']
        return Data([Character(data, self._session, self._cls) for data in characters])

class Anime(Media):
    pass

class Manga(Media):
    pass

def _get_media(payload):
    if payload['type'] == 'ANIME':
        return Anime

    return Manga