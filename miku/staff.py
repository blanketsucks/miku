from __future__ import annotations

from typing import List, TYPE_CHECKING

from .character import Character
from .image import Image
from .utils import IDComparable, cached_slot_property
from .common import Name, FuzzyDate
from . import types

if TYPE_CHECKING:
    from .http import HTTPHandler

__all__ = (
    'Staff',
)


class Staff(IDComparable):
    __slots__ = (
        '_payload',
        '_http',
        '_cs_characters',
        'id',
        'language',
        'description',
        'primary_occupations',
        'gender',
        'age',
        'home_town',
        'url'
    )

    def __init__(self, payload: types.Staff, http: HTTPHandler) -> None:
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

    def __repr__(self) -> str:
        return f'<Staff id={self.id} name={self.name.full!r}>'

    @property
    def name(self) -> Name:
        return Name(self._payload['name'])

    @property
    def image(self) -> Image:
        return Image(self._http.session, self._payload['image']) # type: ignore

    @property
    def birth(self) -> FuzzyDate:
        return FuzzyDate(self._payload['dateOfBirth'])

    @property
    def death(self) -> FuzzyDate:
        return FuzzyDate(self._payload['dateOfDeath'])

    @cached_slot_property('_cs_characters')
    def characters(self) -> List[Character]:
        return [Character(character, self._http) for character in self._payload['characters']['nodes']]

