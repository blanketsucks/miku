import aiohttp
import asyncio
from typing import Optional, Union

from .http import HTTPHandler
from .media import Anime, Media, Manga
from .paginator import Paginator
from .character import Character
from .user import User
from .studio import Studio
from .staff import Staff
from .statistics import SiteStatistics
from .image import Image
from .threads import Thread

def _get_event_loop(loop=None) -> asyncio.AbstractEventLoop:
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
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop]=None, session: aiohttp.ClientSession=None) -> None:
        """
        AnilistClient constructor.

        Args:
            loop: An optional argument defining the event loop used for the client's requests.
            session: An optional argument defining the session used to send requests with.
        """
        self.loop = _get_event_loop(loop)
        self.http = HTTPHandler(loop, session)

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
        """
        Creates a client from a code pin.

        Args:
            pin: The code pin to use.
            client_id: The client id to use.
            client_secret: The client secret to use.

        Returns:
            A [AnilistClient](./client.md) object.
        """
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
        """
        Fetches site statistics.

        Returns:
            A [SiteStatistics][./site-statistics.md] object.
        """
        data = await self.http.get_site_statisics()
        return SiteStatistics(data['data']['SiteStatistics'])

    async def fetch_user(self, name: str) -> User:
        """
        Fetches a user.

        Returns:
            A [User](./user.md) object.
        """
        data = await self.http.get_user(name)
        return User(data['data']['User'], self.http, Image)

    async def fetch_media(self, name: str, *, type: Optional[str]=None) -> Media:
        """
        Fetches a media.

        Returns:
            A [Media](./media.md) object.
        """
        data = await self.http.get_media(name, type)
        return Media(data['data']['Media'], self.http, Image)

    async def fetch_anime(self, name: str) -> Anime:
        """
        Fetches an anime.

        Returns:
            A [Media](./media.md) object.
        """
        data = await self.http.get_anime(name)
        return Anime(data['data']['Media'], self.http, Image)

    async def fetch_manga(self, name: str) -> Manga:
        """
        Fetches a manga.

        Returns:
            A [Media](./media.md) object.
        """
        data = await self.http.get_manga(name)
        return Manga(data['data']['Media'], self.http, Image)

    async def fetch_character(self, name: str) -> Character:
        """
        Fetches a character.

        Returns:
            A [Character](./character.md) object.
        """
        data = await self.http.get_character(name)
        return Character(data['data']['Character'], self.http, Image)

    async def fetch_studio(self, name: str) -> Studio:
        """
        Fetches a studio.
        
        Returns:
            A [Studio](./studio.md) object.
        """
        data = await self.http.get_studio(name)
        return Studio(data['data']['Studio'], self.http, Image)

    async def fetch_staff(self, name: str) -> Staff:
        """
        Fetches a staff

        Returns:
            A [Staff](./staff.md) object.
        """
        data = await self.http.get_staff(name)
        return Staff(data['data']['Staff'], self.http, Image)

    async def fetch_thread(self, id: Union[int, str]):
        data = await self.http.get_thread(id)
        return Thread(data['data']['Thread'], self.http, Image)

    def users(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[User]:
        """
        The same as [AnilistClient.media](./client.md#miku.client.AnilistClient.media) but 
        the [Page](./page.md) retreived through the [Paginator](./paginator.md) returns a [User](./user.md) object.

        Args:
            name: The name of the users being searched.
            page: The page to show for the search.
            per_page: Amount of results shown per page.

        Returns:
            A [Paginator](./paginator.md) object.
        """
        return self.http.get_users(name, per_page=per_page, page=page)

    def medias(self, name: str, type: Optional[str]=None, *, per_page: int=3, page: int=1) -> Paginator[Media]:
        """
        Retruns a [Paginator](./paginator.md) object which can be iterated through to get an object of 
        [Page](./page.md) which the same thing can be done for to retrieve the [Media](./media.md) object.

        Args:
            name: The name of the media being searched.
            type: Type of media searched. Can be None for a global search.
            page: The page to show for the search.
            per_page: Amount of results shown per page.

        Returns:
            A [Paginator](./paginator.md) object.
        """
        return self.http.get_medias(name, type, per_page=per_page, page=page)

    def animes(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Anime]:
        """
        The same as [AnilistClient.media](./client.md#miku.client.AnilistClient.media) 
        but the [Page](./page.md) retreived through the [Paginator](./paginator.md) returns an [Anime](./media.md) object.

        Args:
            name: The name of the anime being searched.
            page: The page to show for the search.
            per_page: Amount of results shown per page.

        Returns:
            A [Paginator](./paginator.md) object.
        """
        return self.http.get_animes(name, per_page=per_page, page=page)

    def mangas(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Manga]:
        """
        The same as [AnilistClient.media](./client.md#miku.client.AnilistClient.media) 
        but the [Page](./page.md) retreived through the [Paginator](./paginator.md) returns a [Manga](./media.md) object.

        Args:
            name: The name of the manga being searched.
            page: The page to show for the search.
            per_page: Amount of results shown per page.

        Returns:
            A [Paginator](./paginator.md) object.
        """
        return self.http.get_mangas(name, per_page=per_page, page=page)

    def characters(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Character]:
        """
        The same as [AnilistClient.media](./client.md#miku.client.AnilistClient.media) but
        the [Page](./page.md) retreived through the [Paginator](./paginator.md) returns a [Character](./character.md) object.

        Args:
            name: The name of the character being searched.
            page: The page to show for the search.
            per_page: Amount of results shown per page.
        Returns:
            A [Paginator](./paginator.md) object.
        """
        return self.http.get_characters(name, per_page=per_page, page=page)
