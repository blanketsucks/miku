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
    'AsyncAnilistClient',
)

class SyncAnilistClient:
    def __init__(self, session: requests.Session=None) -> None:
        """
        SyncAnilistClient constructor.

        Args:
            session: An optional argument defining the session used to send requests with.
        """
        self.http = SyncHTTPHandler(session)

    def close(self):
        return self.http.close()

    @classmethod
    def from_access_token(cls, access_token: str, **kwargs) -> 'SyncAnilistClient':
        self = cls(**kwargs)
        self.http.token = access_token

        return self

    @classmethod
    def from_authorization_pin(cls, pin: str, client_id: str, client_secret: str, **kwargs) -> 'SyncAnilistClient':
        self = cls(**kwargs)
        access_token = self.http.get_access_token_from_pin(
            code=pin,
            client_id=client_id,
            client_secret=client_secret,       
        )

        self.http.token = access_token
        return self

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def fetch_site_statistics(self) -> SiteStatistics:
        data = self.http.get_site_statisics()
        return SiteStatistics(data['data']['SiteStatistics'])

    def fetch_user(self, name: str) -> User:
        data = self.http.get_user(name)
        return User(data['data']['User'], self.http.session, Image)

    def fetch_media(self, name: str, *, type: Optional[str]=None) -> Media:
        data = self.http.get_media(name, type)
        return Media(data['data']['Media'], self.http.session, Image)

    def fetch_anime(self, name: str) -> Anime:
        data = self.http.get_anime(name)
        return Anime(data['data']['Media'], self.http.session, Image)

    def fetch_manga(self, name: str) -> Manga:
        data = self.http.get_manga(name)
        return Manga(data['data']['Media'], self.http.session, Image)

    def fetch_character(self, name: str) -> Character:
        data = self.http.get_character(name)
        return Character(data['data']['Character'], self.http.session, Image)

    def fetch_studio(self, name: str) -> Studio:
        data = self.http.get_studio(name)
        return Studio(data['data']['Studio'], self.http.session, Image)

    def fetch_staff(self, name: str) -> Staff:
        data = self.http.get_staff(name)
        return Staff(data['data']['Staff'], self.http.session)

    def users(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[User]:
        return self.http.get_users(name, per_page=per_page, page=page)

    def medias(self, name: str, type: Optional[str]=None, *, per_page: int=3, page: int=1) -> Paginator[Media]:
        return self.http.get_medias(name, type, per_page=per_page, page=page)

    def animes(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Anime]:
        return self.http.get_animes(name, per_page=per_page, page=page)

    def mangas(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Manga]:
        return self.http.get_mangas(name, per_page=per_page, page=page)

    def characters(self, name: str, *, per_page: int=3, page: int=1) -> Paginator[Character]:
        return self.http.get_characters(name, per_page=per_page, page=page)
