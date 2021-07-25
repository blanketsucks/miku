import requests
from typing import Optional

from .http import SyncHTTPHandler
from .image import Image
from .paginator import Paginator

from miku.media import Anime, Media, Manga
from miku.character import Character
from miku.user import User
from miku.studio import Studio
from miku.staff import Staff
from miku.statistics import SiteStatistics

__all__ = (
    'AnilistClient',
)

class SyncAnilistClient:
    def __init__(self, session: requests.Session=None) -> None:
        """
        AnilistClient constructor.

        Args:
            loop: An optional argument defining the event loop used for the client's requests.
            session: An optional argument defining the session used to send requests with.
        """
        self.http = SyncHTTPHandler(session)

    @classmethod
    def from_access_token(cls, access_token: str, **kwargs) -> 'SyncAnilistClient':
        """
        Creates a client from an access token.
        """
        self = cls(**kwargs)
        self.http.token = access_token

        return self

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.http.close()

    def fetch_site_statistics(self) -> SiteStatistics:
        """
        Fetches site statistics.

        Returns:
            A [SiteStatistics][./site-statistics.md] object.
        """
        data = self.http.get_site_statisics()
        return SiteStatistics(data['data']['SiteStatistics'])

    def fetch_user(self, name: str) -> User:
        """
        Fetches a user.

        Returns:
            A [User](./user.md) object.
        """
        data = self.http.get_user(name)
        return User(data['data']['User'], self.http.session, Image)

    def fetch_media(self, name: str, *, type: Optional[str]=None) -> Media:
        """
        Fetches a media.

        Returns:
            A [Media](./media.md) object.
        """
        data = self.http.get_media(name, type)
        return Media(data['data']['Media'], self.http.session, Image)

    def fetch_anime(self, name: str) -> Anime:
        """
        Fetches an anime.

        Returns:
            A [Media](./media.md) object.
        """
        data = self.http.get_anime(name)
        return Anime(data['data']['Media'], self.http.session, Image)

    def fetch_manga(self, name: str) -> Manga:
        """
        Fetches a manga.

        Returns:
            A [Media](./media.md) object.
        """
        data = self.http.get_manga(name)
        return Manga(data['data']['Media'], self.http.session, Image)

    def fetch_character(self, name: str) -> Character:
        """
        Fetches a character.

        Returns:
            A [Character](./character.md) object.
        """
        data = self.http.get_character(name)
        return Character(data['data']['Character'], self.http.session, Image)

    async def fetch_studio(self, name: str) -> Studio:
        """
        Fetches a studio.
        
        Returns:
            A [Studio](./studio.md) object.
        """
        data = self.http.get_studio(name)
        return Studio(data['data']['Studio'], self.http.session, Image)

    def fetch_staff(self, name: str) -> Staff:
        """
        Fetches a staff

        Returns:
            A [Staff](./staff.md) object.
        """
        data = self.http.get_staff(name)
        return Staff(data['data']['Staff'], self.http.session)

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
