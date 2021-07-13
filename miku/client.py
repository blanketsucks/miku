import aiohttp
from typing import Optional

from .http import HTTPHandler
from .media import Anime, Media, Manga
from .paginator import Paginator
from .character import Character

class AnilistClient:
    def __init__(self) -> None:
        self.http = HTTPHandler()

    @classmethod
    def from_session(cls, session: aiohttp.ClientSession) -> 'AnilistClient':
        """
        Create a Client object from a user defined `aiohttp.ClientSession`.

        Args:
            session: An object of `aiohttp.ClientSession`

        Returns:
            A [AnilistClient](./client.md) object.
        """
        if not isinstance(session, aiohttp.ClientSession):
            ret = 'Expected an aiohttp.ClientSession instance but got {0.__class__.__name__!r} instead'
            raise TypeError(ret.format(session))

        self = cls()

        self.http.session = session
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.http.close()

    def media(self, name: str, type: Optional[str]=None, *, per_page: int=3, page: int=1) -> Paginator[Media]:
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
        return self.http.get_media(name, type, per_page=per_page, page=page)

    def anime(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Anime]:
        """
        The same as [AnilistClient.media](./client.md#miku.client.AnilistClient.media) but the [Page](./page.md) retreived through the
        [Paginator](./paginator.md) returns an [Anime](./media.md) object.

        Args:
            name: The name of the anime being searched.
            page: The page to show for the search.
            per_page: Amount of results shown per page.

        Returns:
            A [Paginator](./paginator.md) object.
        """
        return self.http.get_anime(name, per_page=per_page, page=page)

    def manga(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Manga]:
        """
        The same as [AnilistClient.media](./client.md#miku.client.AnilistClient.media) but the [Page](./page.md) retreived through the
        [Paginator](./paginator.md) returns a [Manga](./media.md) object.

        Args:
            name: The name of the manga being searched.
            page: The page to show for the search.
            per_page: Amount of results shown per page.

        Returns:
            A [Paginator](./paginator.md) object.
        """
        return self.http.get_manga(name, per_page=per_page, page=page)

    def character(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Character]:
        """
        The same as [AnilistClient.media](./client.md#miku.client.AnilistClient.media) but the [Page](./page.md) retreived through the
        [Paginator](./paginator.md) returns a [Character](./character.md) object.

        Args:
            name: The name of the character being searched.
            page: The page to show for the search.
            per_page: Amount of results shown per page.
            
        Returns:
            A [Paginator](./paginator.md) object.
        """
        return self.http.get_character(name, per_page=per_page, page=page)