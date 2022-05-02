from __future__ import annotations

from typing import Any, Literal, Optional, Union, overload
import aiohttp
import asyncio

from .http import HTTPHandler
from .media import Anime, Media, Manga
from .paginator import Paginator
from .character import Character
from .user import User
from .studio import Studio
from .staff import Staff
from .statistics import SiteStatistics
from .threads import Thread
from .enums import MediaType

def _get_event_loop(loop: Optional[asyncio.AbstractEventLoop] = None) -> asyncio.AbstractEventLoop:
    if loop:
        if not isinstance(loop, asyncio.BaseEventLoop):
            raise TypeError('Invalid type for loop argument')

        return loop

    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.get_event_loop()

__all__ = (
    'AnilistClient',
)

class AnilistClient:
    def __init__(
        self,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None, 
        session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        self.loop = _get_event_loop(loop)
        self.http = HTTPHandler(self.loop, session)

    @classmethod
    def from_access_token(cls, access_token: str, **kwargs: Any) -> AnilistClient:
        """
        Creates a client from an access token.

        Args:
            access_token: The access token to use.

        Returns:
            A [AnilistClient](./client.md) object.
        """
        self = cls(**kwargs)
        self.http.token = access_token

        return self

    @classmethod
    async def from_authorization_pin(cls, pin: str, client_id: str, client_secret: str, **kwargs: Any) -> AnilistClient:
        self = cls(**kwargs)
        access_token = await self.http.get_access_token_from_pin(
            pin=pin,
            client_id=client_id,
            client_secret=client_secret,       
        )

        self.http.token = access_token
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args: Any):
        await self.close()

    async def close(self):
        return await self.http.close()

    async def fetch_site_statistics(self) -> SiteStatistics:
        data = await self.http.get_site_statisics()
        return SiteStatistics(data)

    async def fetch_user(self, search: Union[int, str]) -> User:
        data = await self.http.get_user(search)
        return User(data, self.http)

    @overload
    async def fetch_media(self, search: Union[int, str], *, type: Literal[MediaType.ANIME]) -> Anime:
        ...
    @overload
    async def fetch_media(self, search: Union[int, str], *, type: Literal[MediaType.MANGA]) -> Manga:
        ...
    @overload
    async def fetch_media(self, search: Union[int, str], *, type: Literal[None] = None) -> Media:
        ...
    async def fetch_media(self, search: Union[int, str], *, type: Optional[MediaType] = None) -> Media:
        data = await self.http.get_media(search, type.value if type else None)
        return Media(data, self.http)

    async def fetch_anime(self, search: Union[int, str]) -> Anime:
        return await self.fetch_media(search, type=MediaType.ANIME)

    async def fetch_manga(self, search: Union[int, str]) -> Manga:
        return await self.fetch_media(search, type=MediaType.MANGA)
        
    async def fetch_character(self, search: Union[int, str]) -> Character:
        data = await self.http.get_character(search)
        return Character(data, self.http)

    async def fetch_studio(self, search: Union[int, str]) -> Studio:
        data = await self.http.get_studio(search)
        return Studio(data, self.http)

    async def fetch_staff(self, search: Union[int, str]) -> Staff:
        data = await self.http.get_staff(search)
        return Staff(data, self.http)

    async def fetch_thread(self, search: Union[int, str]):
        data = await self.http.get_thread(search)
        return Thread(data, self.http)

    def users(self, name: str, *, per_page: int= 5, page: int = 0) -> Paginator[User]:
        return self.http.get_users(name, per_page=per_page, page=page)

    @overload
    def medias(self, name: str, type: Literal[MediaType.ANIME], *, per_page: int = 5, page: int = 0) -> Paginator[Anime]:
        ...
    @overload
    def medias(self, name: str, type: Literal[MediaType.MANGA], *, per_page: int = 5, page: int = 0) -> Paginator[Manga]:
        ...
    @overload
    def medias(self, name: str, type: Literal[None] = None, *, per_page: int = 5, page: int = 0) -> Paginator[Media]:
        ...
    def medias(self, name: str, type: Optional[MediaType] = None, *, per_page: int = 5, page: int = 0) -> Paginator[Media]: # type: ignore
        return self.http.get_medias(name, type.value if type else None, per_page=per_page, page=page)

    def characters(self, name: str, *, per_page: int = 5, page: int = 0) -> Paginator[Character]:
        return self.http.get_characters(name, per_page=per_page, page=page)
