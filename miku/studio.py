from __future__ import annotations

from typing import List, TYPE_CHECKING

from .utils import IDComparable, cached_slot_property
from .media import Media
from . import types

if TYPE_CHECKING:
    from .http import HTTPHandler

__all__ = 'Studio',

class Studio(IDComparable):
    __slots__ = (
        '_payload',
        '_http',
        '_cs_media'
        'id',
        'name',
        'is_animation_studio',
        'url',
        'favourites'
    )

    def __init__(self, payload: types.Studio, http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.id: int = payload['id']
        self.name: str = payload['name']
        self.is_animation_studio: bool = payload['isAnimationStudio']
        self.url: str = payload['siteUrl']
        self.favourites: int = payload['favourites']

    def __repr__(self) -> str:
        return f'<Studio id={self.id} name={self.name!r}>'

    @cached_slot_property('_cs_media')
    def medias(self) -> List[Media]:
        medias = self._payload['media']['nodes']
        return [Media(media, self._http) for media in medias]

