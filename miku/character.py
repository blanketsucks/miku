from __future__ import annotations

from typing import List, TYPE_CHECKING

from .image import Image
from .common import Name, FuzzyDate
from . import types

if TYPE_CHECKING:
    from .http import HTTPHandler
    from .media import Media

__all__ = (
    'Character',
)

class Character:
    __slots__ = (
        '_payload',
        '_http',
        'description',
        'favourites',
        'url',
        'gender',
        'age'
    )

    def __init__(self, payload: types.Character, http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.description: str = self._payload['description']
        self.favourites: int = self._payload['favourites']
        self.url: str = self._payload['siteUrl']
        self.gender: str = self._payload['gender']
        self.age: str = self._payload['age']

    def __repr__(self) -> str:
        return f'<Character name={self.name.full!r}>'

    @property
    def apperances(self) -> List[Media]:
        from .media import Media

        animes = self._payload['media']['nodes']
        return [Media(anime, self._http) for anime in animes]

    @property
    def name(self) -> Name:
        return Name(self._payload['name'])

    @property
    def image(self) -> Image:
        return Image(self._http.session, self._payload['image'])

    @property
    def birth(self) -> FuzzyDate:
        return FuzzyDate(self._payload['dateOfBirth'])

