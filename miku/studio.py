from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING

from .utils import IDComparable

if TYPE_CHECKING:
    from .http import HTTPHandler
    from .media import Media

__all__ = 'Studio',

class Studio(IDComparable):
    __slots__ = (
        '_payload',
        '_http',
        'id',
        'name',
        'is_animation_studio',
        'url',
        'favourites'
    )

    def __init__(self, payload: Dict[str, Any], http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.id: int = payload['id']
        self.name: str = payload['name']
        self.is_animation_studio: bool = payload['isAnimationStudio']
        self.url: str = payload['siteUrl']
        self.favourites: int = payload['favourites']

    @property
    def medias(self) -> List[Media]:
        """
        The media the studio has worked on.

        Returns:
            A [Data](data.md) object.
        """
        from .media import Media

        medias = self._payload['media']['nodes']
        return [Media(media, self._http) for media in medias]
