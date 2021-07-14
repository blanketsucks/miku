from __future__ import annotations

import datetime
from typing import List, Optional, Tuple, Union, TYPE_CHECKING

from .image import Image

if TYPE_CHECKING:
    from .media import Manga, Anime

class Name:
    def __init__(self, payload) -> None:
        self._payload = payload

    @property
    def first(self) -> str:
        return self._payload['first']

    @property
    def middle(self) -> str:
        return self._payload['middle']

    @property
    def last(self) -> str:
        return self._payload['last']

    @property
    def full(self) -> str:
        return self._payload['full']

    @property
    def native(self) -> str:
        return self._payload['first']

class BirthDate:
    def __init__(self, character: 'Character') -> None:
        self._birth = character._payload['dateOfBirth']
        self.character = character

    @property
    def year(self) -> Optional[int]:
        return self._birth['year']

    @property
    def month(self) -> Optional[int]:
        return self._birth['month']

    @property
    def day(self) -> Optional[int]:
        return self._birth['day']

    def get_datetime(self, age: str=None) -> Optional[Tuple[datetime.datetime]]:
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
    """
    def __init__(self, payload, session) -> None:
        self._payload = payload
        self._session = session

        self.description: str = self._payload['description']
        self.favourites: int = self._payload['favourites']
        self.url: str = self._payload['siteUrl']
        self.gender: str = self._payload['gender']

    def __repr__(self) -> str:
        return '<Character name={0.name.full!r}>'.format(self)

    @property
    def apperances(self) -> List[Union[Anime, Manga]]:
        """
        This character's apperances on difference mangas and animes.

        Returns:
            A list of [Media](./media.md).
        """
        from .media import _get_media

        animes = self._payload['media']['nodes']
        return [_get_media(anime)(anime, self._session) for anime in animes]

    @property
    def name(self) -> Name:
        """
        Returns:
            A `Name` object containing the following attributes: 
            `first`, `middle`, `last`, `full` and `native`.
        """
        return Name(self._payload['name'])

    @property
    def image(self) -> Image:
        """
        Returns:
            An [Image](./image.md) object.
        """
        return Image(self._session, self._payload['image'])

    @property
    def birth(self) -> BirthDate:
        """
        Returns:
            A `BirthDate` object which contains the: `year`, `month` and `day` properties,
            and the `get_datetime` method which returns `Optional[Tuple[datetime.datetime]]`.
        """
        return BirthDate(self._payload['dateOfBirth'])
