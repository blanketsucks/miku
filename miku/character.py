from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict, TYPE_CHECKING

from .image import Image

if TYPE_CHECKING:
    from .http import HTTPHandler
    from .media import Media

__all__ = (
    'Name',
    'DateOfBirth',
    'Character'
)

class Name(TypedDict):
    first: str
    middle: str
    last: str
    full: str
    native: str
    alternatives: List[str]

class DateOfBirth(TypedDict):
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]

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

    def __init__(self, payload: Dict[str, Any], http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.description: str = self._payload['description']
        self.favourites: int = self._payload['favourites']
        self.url: str = self._payload['siteUrl']
        self.gender: str = self._payload['gender']
        self.age: str = self._payload['age']

    def __repr__(self) -> str:
        return '<Character name={0.name.full!r}>'.format(self)

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
    def name(self) -> Name:
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
    def birth(self) -> DateOfBirth:
        """
        Returns:
            A [CharacterBirthdate](./character.md) object.
        """
        return self._payload['dateOfBirth']
