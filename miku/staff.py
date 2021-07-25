from typing import List, Optional

from .character import CharacterName, CharacterBirthdate, Character
from .image import Image
from . import utils

class StaffName(CharacterName):
    pass

class StaffBirthdate(CharacterBirthdate):

    @utils.remove_docstring
    def __init__(self, birth) -> None:
        self.year: Optional[int] = birth['year']
        self.month: Optional[int] = birth['month']
        self.day: Optional[int] = birth['day']


class StaffDeathdate(StaffBirthdate):
    pass

class Staff:
    """
    Attributes:
        id: The id of the staff member.
        language: The primary language of the staff member. Current values: Japanese, English, Korean, Italian, Spanish, Portuguese, French, German, Hebrew, Hungarian, Chinese, Arabic, Filipino, Catalan.
        primary_occupations: The person's primary occupations.
        gender: The staff's gender. Usually Male, Female, or Non-binary but can be any string.
        age: The person's age in years.
        home_town: The persons birthplace or hometown.
        url: The url for the staff page on the AniList website.
    """
    def __init__(self, payload, session, cls) -> None:
        self._payload = payload
        self._cls = cls
        self._session = session

        self.id: int = self._payload['id']
        self.language: str = self._payload['languageV2']
        self.description: str = self._payload['description']
        self.primary_occupations: List[str] = self._payload['primaryOccupations']
        self.gender: str = self._payload['gender']
        self.age: int = self._payload['age']
        self.home_town: str = self._payload['homeTown']
        self.url: str = self._payload['siteUrl']

    @property
    def name(self) -> StaffName:
        """
        The names of the staff member.

        Returns:
            A subclass of [CharacterName](./character-name.md).
        """
        return StaffName(self._payload['name'])

    @property
    def image(self) -> Image:
        """
        The staff images.

        Returns:
            An [Image](image.md) object.
        """
        return self._cls(self._session, self._payload['image'])

    @property
    def birth(self) -> StaffBirthdate:
        """
        Returns:
            A subclass of [CharacterBirthdate](./character-birthdate.md).
        """
        return StaffBirthdate(self._payload['dateOfBirth'])

    @property
    def death(self) -> StaffDeathdate:
        """
        Returns:
            A subclass of [CharacterBirthdate](./character-birthdate.md).
        """
        return StaffDeathdate(self._payload['dateOfDeath'])

    @property
    def characters(self) -> utils.Data[Character]:
        """
        Characters voiced by the actor.

        Returns:
            A [Data](./data.md) object.
        """
        characters = self._payload['characters']['nodes']
        return utils.Data([Character(character, self._session, self._cls) for character in characters])