from enum import Enum
from typing import List

from .image import Image

__all__ = (
    'UserTitleLanguage',
    'UserNotificationOptionType',
    'UserNotificationOption',
    'UserOptions',
    'User'
)

class UserTitleLanguage(Enum):
    """
    An `enum.Enum` defining a user title language option.

    Attributes:
        ROMAJI: The romanization of the native language title.
        ENGLISH: The official english title.
        NATIVE: Official title in it's native language.
        ROMAJI_STYLISED: The romanization of the native language title, stylised by media creator.
        ENGLISH_STYLISED: The official english title, stylised by media creator.
        NATIVE_STYLISED: Official title in it's native language, stylised by media creator.
    """
    ROMAJI: str = 'ROMAJI'
    ENGLISH: str = 'ENGLISH'
    NATIVE: str = 'NATIVE'
    ROMAJI_STYLISED: str = 'ROMAJI_STYLISED'
    ENGLISH_STYLISED: str = 'ENGLISH_STYLISED'
    NATIVE_STYLISED: str = 'NATIVE_STYLISED'

class UserNotificationOptionType(Enum):
    """
    Attributes:
        ACTIVITY_MESSAGE: A user has sent you message
        ACTIVITY_REPLY: A user has replied to your activity
        FOLLOWING: A user has followed you
        ACTIVITY_MENTION: A user has mentioned you in their activity
        THREAD_COMMENT_MENTION: A user has mentioned you in a forum comment
        THREAD_SUBSCRIBED: A user has commented in one of your subscribed forum threads
        THREAD_COMMENT_REPLY: A user has replied to your forum comment
        AIRING: An anime you are currently watching has aired
        ACTIVITY_LIKE: A user has liked your activity
        ACTIVITY_REPLY_LIKE: A user has liked your activity reply
        THREAD_LIKE: A user has liked your forum thread
        THREAD_COMMENT_LIKE: A user has liked your forum comment
        ACTIVITY_REPLY_SUBSCRIBED: A user has replied to activity you have also replied to
        RELATED_MEDIA_ADDITION: A new anime or manga has been added to the site where its related media is on the user's list
    """
    ACTIVITY_MESSAGE: str = 'ACTIVITY_MESSAGE'
    ACTIVITY_REPLY: str = 'ACTIVITY_REPLY'
    FOLLOWING: str = 'FOLLOWING'
    ACTIVITY_MENTION: str = 'ACTIVITY_MENTION'
    THREAD_COMMENT_MENTION: str = 'THREAD_COMMENT_MENTION'
    THREAD_SUBSCRIBED: str = 'THREAD_SUBSCRIBED'
    THREAD_COMMENT_REPLY: str = 'THREAD_COMMENT_REPLY'
    AIRING: str = 'AIRING'
    ACTIVITY_LIKE: str = 'ACTIVITY_LIKE'
    ACTIVITY_REPLY_LIKE: str = 'ACTIVITY_REPLY_LIKE'
    THREAD_LIKE: str = 'THREAD_LIKE'
    THREAD_COMMENT_LIKE: str = 'THREAD_COMMENT_LIKE'
    ACTIVITY_REPLY_SUBSCRIBED: str = 'ACTIVITY_REPLY_SUBSCRIBED'
    RELATED_MEDIA_ADDITION: str = 'RELATED_MEDIA_ADDITION'

class UserNotificationOption:
    """
    Attributes:
        enabled: Whether this type of notification is enabled.
        type: A [UserNotificationOptionType](./user-notification-type.md) object.

    """
    def __init__(self, payload) -> None:
        self.enabled: bool = payload['enabled']
        self.type: UserNotificationOptionType = UserNotificationOptionType(payload['type'])

    def __repr__(self) -> str:
        return '<UserNotificationOption enabled={0.enabled} type={0.type!r}>'.format(self)

class UserOptions:
    """
    Attributes:
        title_language: The language the user wants to see media titles in. A [UserTitleLanguage](./user-title-language.md) object.
        display_adult_content: Whether the user has enabled viewing of 18+ content.
        airing_notifications: Whether the user receives notifications when a show they are watching aires.
        profile_color: Profile highlight color (blue, purple, pink, orange, red, green, gray).
        notification_options: A list of [UserNotificationOption](./user-notification.md) objects.
    """
    def __init__(self, payload) -> None:
        self.title_language: UserTitleLanguage = UserTitleLanguage(payload['titleLanguage'])
        self.display_adult_content: bool = payload['displayAdultContent']
        self.airing_notifications: bool = payload['airingNotifications']
        self.profile_color: str = payload['profileColor']
        self.notification_options: List[UserNotificationOption] = [] if payload.get('notificationOptions') is None else [
            UserNotificationOption(data) for data in payload['notificationOptions']
        ]

class User:
    """
    Attributes:
        name: The name of the user.
        id: The id of the user.
        url: The user profile's URL. 
    """
    def __init__(self, payload, session) -> None:
        self._payload = payload
        self._session = session

        self.name: str = self._payload['name']
        self.id: int = self._payload['id']
        self.url: str = self._payload['siteUrl']

    def __repr__(self) -> str:
        return '<User id={0.id} name={0.name!r}>'.format(self)

    @property
    def avatar(self) -> Image:
        """
        Returns:
            The avatar of the user as an [Image](./image.md) object.
        """
        return Image(self._session, self._payload['avatar'])

    @property
    def options(self) -> UserOptions:
        """
        Returns:
            A [UserOptions](./user-options.md) object.
        """
        return UserOptions(self._payload['options'])
