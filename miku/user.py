
from .image import Image

class User:
    def __init__(self, payload, session) -> None:
        self._payload = payload
        self._session = session

    def __repr__(self) -> str:
        return '<User id={0.id} name={0.name!r}>'.format(self)

    @property
    def name(self) -> str:
        """
        Returns:
            The name of the user.
        """
        return self._payload['name']

    @property
    def id(self) -> int:
        """
        Returns:
            The id of the user.
        """
        return self._payload['id']

    @property
    def avatar(self) -> Image:
        """
        Returns:
            The avatar of the user as an [Image](./image.md) object.
        """
        return Image(self._session, self._payload['avatar'])

    @property
    def url(self) -> str:
        """
        Returns:
            The user profile's URL.
        """
        return self._payload['siteUrl']