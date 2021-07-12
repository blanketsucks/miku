from dataclasses import dataclass
from typing import Any, Dict
import aiohttp

from .image import Image


class Title:
    def __init__(self, payload) -> None:
        self.__payload = payload['title']

    @property
    def romaji(self) -> str:
        return self.__payload['romaji']

    @property
    def english(self) -> str:
        return self.__payload['english']

    @property
    def native(self) -> str:
        return self.__payload['native']

class Anime:
    def __init__(self, payload: Dict[str, Any], session: aiohttp.ClientSession) -> None:
        self._payload = payload
        self._session = session

    def __repr__(self) -> str:
        return '<Anime title={0.title.romaji!r}>'.format(self)

    @property
    def title(self):
        return Title(self._payload)

    @property
    def banner_image(self):
        return Image(self._session, self._payload['bannerImage'])

    @property
    def cover_image(self):
        return Image(self._session, self._payload['coverImage'])