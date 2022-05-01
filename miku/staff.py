from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING

from .character import Name, DateOfBirth, Character
from .image import Image
from .utils import IDComparable

if TYPE_CHECKING:
    from .http import HTTPHandler

__all__ = (
    'DateOfDeath',
    'Staff'
)

class DateOfDeath(DateOfBirth):
    pass

class Staff(IDComparable):
    __slots__ = (
        '_payload',
        '_http'
        'id',
        'language',
        'description',
        'primary_occupations',
        'gender',
        'age',
        'home_town',
        'url'
    )

    def __init__(self, payload: Dict[str, Any], http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.id: int = self._payload['id']
        self.language: str = self._payload['languageV2']
        self.description: str = self._payload['description']
        self.primary_occupations: List[str] = self._payload['primaryOccupations']
        self.gender: str = self._payload['gender']
        self.age: int = self._payload['age']
        self.home_town: str = self._payload['homeTown']
        self.url: str = self._payload['siteUrl']

    @property
    def name(self) -> Name:
        """
        The names of the staff member.

        Returns:
            A subclass of [CharacterName](./character.md).
        """
        return self._payload['name']

    @property
    def image(self) -> Image:
        return Image(self._http.session, self._payload['image']) # type: ignore

    @property
    def birth(self) -> DateOfBirth:
        """
        Returns:
            A subclass of [CharacterBirthdate](./character.md).
        """
        return self._payload['dateOfBirth']

    @property
    def death(self) -> DateOfDeath:
        """
        Returns:
            A subclass of [CharacterBirthdate](./character.md).
        """
        return self._payload['dateOfDeath']

    @property
    def characters(self) -> List[Character]:
        """
        Characters voiced by the actor.

        Returns:
            A [Data](./data.md) object.
        """
        return [Character(character, self._http) for character in self._payload['characters']['nodes']]

