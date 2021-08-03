from __future__ import annotations
from typing import List, TYPE_CHECKING, Union

from .utils import Data

if TYPE_CHECKING:
    from .media import Anime, Manga

class Studio:
    """
    Attributes:
        id: The id of the studio.
        name: The name of the studio.
        is_animation_studio: If the studio is an animation studio or a different kind of company.
        url: The url for the studio page on the AniList website.
        favourites: The amount of users who have favourited the studio
    """
    def __init__(self, payload, session) -> None:
        self._payload = payload
        self._session = session

        self.id: int = payload['id']
        self.name: str = payload['name']
        self.is_animation_studio: bool = payload['isAnimationStudio']
        self.url: str = payload['siteUrl']
        self.favourites: int = payload['favourites']

    def __eq__(self, other):
        return self.id == other.id

    @property
    def medias(self) -> List[Union[Anime, Manga]]:
        """
        The media the studio has worked on.

        Returns:
            A [Data](data.md) object.
        """
        from .media import _get_media

        medias = self._payload['media']['nodes']
        return Data([_get_media(media)(media, self._session) for media in medias])

    def to_dict(self):
        return self._payload.copy()
