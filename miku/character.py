from __future__ import annotations

import datetime
from typing import List, Optional, Tuple, Union, TYPE_CHECKING

from .image import Image

if TYPE_CHECKING:
    from .media import Manga, Anime

__all__ = (
    'CharacterName',
    'CharacterBirthdate',
    'Character'
)

class CharacterName:
    """
    Attributes:
        first: The character's given name.
        middle: The character's middle name.
        last: The character's surname.
        full: The character's first and last name.
        native: The character's full name in their native language.
        alternatives: Other names the character might be referred to as.
    """
    def __init__(self, payload) -> None:
        self.first: str = payload['first']
        self.middle: str = payload['middle']
        self.last: str = payload['last']
        self.full: str = payload['full']
        self.native: str = payload['native']
        self.alternatives: List[str] = payload['alternative']

class CharacterBirthdate:
    """
    Attributes:
        year: Numeric Year.
        month: Numeric month.
        day: Numeric day.
    """
    def __init__(self, character: 'Character') -> None:
        """
        Args:
            character: A [Character](./character.md) object
        """
        birth = character._payload['dateOfBirth']
        self.character = character

        self.year: Optional[int] = birth['year']
        self.month: Optional[int] = birth['month']
        self.day: Optional[int] = birth['day']


    def get_datetime(self, age: Optional[str]=None) -> Optional[Tuple[datetime.datetime]]:
        """
        A function that computes the character's aproximate birth in relation with today's time.

        Args:
            age: If this is None, it will use the character's age.

        Returns:
            An aproximate datetime.
        """
        age = age or self.character.age
        if not age:
            return None

        if any(date is None for date in (self.month, self.day)):
            return None

        if len(age.split('-')) == 2:
            young, old = age.split('-')

            youngest = self.get_datetime(young)
            oldest = self.get_datetime(old)

            return youngest, oldest

        dt = datetime.datetime(year=int(age), month=self.month, day=self.day)
        timedelta = datetime.datetime.utcnow() - dt

        years = timedelta.days // 365
        new = datetime.datetime(year=years, month=self.month, day=self.day)

        return new, None

class Character:
    """
    Attributes:
        description: The description of this character.
        gender: The gender of this character.
        url: This character's Anilist URL.
        favourites: The number of favourites on this character.
        age: The age of this character.
    """
    def __init__(self, payload, session) -> None:
        self._payload = payload
        self._session = session

        self.description: str = self._payload['description']
        self.favourites: int = self._payload['favourites']
        self.url: str = self._payload['siteUrl']
        self.gender: str = self._payload['gender']
        self.age: str = self._payload['age']

    def __repr__(self) -> str:
        return '<Character name={0.name.full!r}>'.format(self)

    @property
    def apperances(self) -> Optional[List[Union[Anime, Manga]]]:
        """
        This character's apperances on difference mangas and animes.

        Returns:
            A list of [Media](./media.md).
        """
        if not self._payload.get('media'):
            return None

        from .media import _get_media

        animes = self._payload['media']['nodes']
        return [_get_media(anime)(anime, self._session) for anime in animes]

    @property
    def name(self) -> CharacterName:
        """
        Returns:
            A [CharacterName](./character.md) object
        """
        return CharacterName(self._payload['name'])

    @property
    def image(self) -> Image:
        """
        Returns:
            An [Image](./image.md) object.
        """
        return self._cls(self._session, self._payload['image'])

    @property
    def birth(self) -> CharacterBirthdate:
        """
        Returns:
            A [CharacterBirthdate](./character.md) object.
        """
        return CharacterBirthdate(self._payload['dateOfBirth'])

    def to_dict(self):
        return self._payload.copy()
