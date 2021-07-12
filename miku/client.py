import aiohttp

from .http import HTTPHandler
from .anime import Anime
from .paginator import Paginator
from .character import Character

class AnilistClient:
    def __init__(self) -> None:
        self.http = HTTPHandler()

    @classmethod
    def from_session(cls, session: aiohttp.ClientSession) -> 'AnilistClient':
        """
        Create a Client instance from a user defined `aiohttp.ClientSession`.

        Args:
            session: An instance of `aiohttp.ClientSession`

        Returns:
            A [AnilistClient](./client.md) instance.
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

    def anime(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Anime]:
        """
        Retruns a [Paginator](./paginator.md) instance which can be iterated through to get an instance of 
        [Page](./page.md) which the same thing can be done for to retrieve the [Anime](./anime.md) instance

        Args:
            name: The name of the anime being searched.
            page: The page to show for the search.
            per_page: Amount of results shown per page.

        Returns:
            A [Paginator](./paginator.md) instance
        """
        return self.http.get_anime(name, per_page=per_page, page=page)

    def character(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Character]:
        return self.http.get_character(name, per_page=per_page, page=page)