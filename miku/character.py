from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from .image import Image
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
        return f'<Character name={self.name["full"]!r}>'

    @property
    def apperances(self) -> Optional[List[Media]]:
        """
        This character's apperances on difference mangas and animes.

        Returns:
            A list of [Media](./media.md).
        """
        if not self._payload.get('media'):
            return None

        from .media import Media

        animes = self._payload['media']['nodes']
        return [Media(anime, self._http) for anime in animes]

    @property
    def name(self) -> types.Name:
        """
        Returns:
            A [CharacterName](./character.md) object
        """
        return self._payload['name']

    @property
    def image(self) -> Image:
        """
        Returns:
            An [Image](./image.md) object.
        """
        return Image(self._http.session, self._payload['image']) # type: ignore

    @property
    def birth(self) -> types.DateOfBirth:
        """
        Returns:
            A [CharacterBirthdate](./character.md) object.
        """
        return self._payload['dateOfBirth']
