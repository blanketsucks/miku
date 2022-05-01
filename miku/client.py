from typing import Optional, Union, cast
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
        """
        AnilistClient constructor.

        Args:
            loop: An optional argument defining the event loop used for the client's requests.
            session: An optional argument defining the session used to send requests with.
        """
        self.loop = _get_event_loop(loop)
        self.http = HTTPHandler(self.loop, session)

    async def close(self):
        """
        Closes the http session.
        """
        return await self.http.close()

    @classmethod
    def from_access_token(cls, access_token: str, **kwargs) -> 'AnilistClient':
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
    async def from_authorization_pin(cls, pin: str, client_id: str, client_secret: str, **kwargs) -> 'AnilistClient':
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

    async def __aexit__(self, *exc):
        await self.close()

    async def fetch_site_statistics(self) -> SiteStatistics:
        data = await self.http.get_site_statisics()
        return SiteStatistics(data['data']['SiteStatistics'])

    async def fetch_user(self, name: str) -> User:
        data = await self.http.get_user(name)
        return User(data['data']['User'], self.http,)

    async def fetch_media(self, name: str, *, type: Optional[MediaType] = None) -> Media:
        data = await self.http.get_media(name, type.value if type else None)
        return Media(data['data']['Media'], self.http)

    async def fetch_anime(self, name: str) -> Anime:
        data = await self.fetch_media(name, type=MediaType.ANIME)
        return cast(Anime, data)

    async def fetch_manga(self, name: str) -> Manga:
        data = await self.fetch_media(name, type=MediaType.MANGA)
        return cast(Manga, data)

    async def fetch_character(self, name: str) -> Character:
        data = await self.http.get_character(name)
        return Character(data['data']['Character'], self.http)

    async def fetch_studio(self, name: str) -> Studio:
        data = await self.http.get_studio(name)
        return Studio(data['data']['Studio'], self.http)

    async def fetch_staff(self, name: str) -> Staff:
        data = await self.http.get_staff(name)
        return Staff(data['data']['Staff'], self.http)

    async def fetch_thread(self, id: Union[int, str]):
        data = await self.http.get_thread(id)
        return Thread(data['data']['Thread'], self.http)

    def users(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[User]:
        return self.http.get_users(name, per_page=per_page, page=page)

    def medias(self, name: str, type: Optional[MediaType] = None, *, per_page: int = 3, page: int = 1) -> Paginator[Media]:
        return self.http.get_medias(name, type.value if type else None, per_page=per_page, page=page)

    def animes(self, name: str, *, per_page: int = 3, page: int = 1) -> Paginator[Anime]:
        return self.medias(name, type=MediaType.ANIME, per_page=per_page, page=page) # type: ignore

    def mangas(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Manga]:
        return self.medias(name, type=MediaType.MANGA, per_page=per_page, page=page) # type: ignore

    def characters(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Character]:
        return self.http.get_characters(name, per_page=per_page, page=page)
