from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class Name:
    first: str
    middle: str
    last: str
    full: str
    native: str

class BirthDate:
    def __init__(self, character: 'Character') -> None:
        birth = character._payload['dateOfBirth']
        self.character = character

        self.year: Optional[int] = birth['year'] 
        self.month: Optional[int] = birth['month'] 
        self.day: Optional[int] = birth['day']

    def get_datetime(self):
        age = self.character.age
        if not age:
            return None

        if any(date is None for date in (self.month, self.day)):
            return None

        if len(age.split('-')) == 2:
            age = age.split('-')[0]

        dt = datetime.datetime(year=int(age), month=self.month, day=self.day)
        timedelta = datetime.datetime.utcnow() - dt

        years = timedelta.days // 365
        new = datetime.datetime(year=years, month=self.month, day=self.day)

        return new

class Character:
    def __init__(self, payload, session) -> None:
        self._payload = payload
        self._session = session

        self.description: str = payload['description']
        self.age: str = payload['age']
        self.birth = BirthDate(self)

    def __repr__(self) -> str:
        return '<Character name={0.name.full!r}>'.format(self)

    @property
    def name(self):
        name = self._payload['name']
        return Name(name['first'], name['middle'], name['last'], name['full'], name['native'])