from enum import Enum

__all__ = (
    'MediaFormat',
    'MediaStatus',
    'MediaType',
    'MediaSource',
    'UserTitleLanguage',
    'UserNotificationOptionType',
)

class MediaFormat(Enum):
    TV = 'TV'
    TV_SHORT = 'TV_SHORT'
    MOVIE = 'MOVIE'
    SPECIAL = 'SPECIAL'
    OVA = 'OVA'
    ONA = 'ONA'
    MUSIC = 'MUSIC'
    MANGA = 'MANGA'
    NOVEL = 'NOVEL'
    ONE_SHOT = 'ONE_SHOT'

class MediaStatus(Enum):
    FINISHED = 'FINISHED'
    RELEASING = 'RELEASING'
    NOT_YET_RELEASED = 'NOT_YET_RELEASED'
    CANCELLED = 'CANCELLED'
    HIATUS = 'HIATUS'

class MediaType(Enum):
    ANIME = 'ANIME'
    MANGA = 'MANGA'

class MediaSource(Enum):
    ORIGINAL = 'ORIGINAL'
    MANGA = 'MANGA'
    LIGHT_NOVEL = 'LIGHT_NOVEL'
    VISUAL_NOVEL = 'VISUAL_NOVEL'
    VIDEO_GAME = 'VIDEO_GAME'
    OTHER = 'OTHER'
    NOVEL = 'NOVEL'
    DOUJINSHI = 'DOUJINSHI'
    ANIME = 'ANIME'

class MediaSeason(Enum):
    WINTER = 'WINTER'
    SPRING = 'SPRING'
    SUMMER = 'SUMMER'
    FALL = 'FALL'

class MediaRankType(Enum):
    RATED = 'RATED'
    POPULAR = 'POPULAR'

class UserTitleLanguage(Enum):
    ROMAJI = 'ROMAJI'
    ENGLISH = 'ENGLISH'
    NATIVE = 'NATIVE'
    ROMAJI_STYLISED = 'ROMAJI_STYLISED'
    ENGLISH_STYLISED = 'ENGLISH_STYLISED'
    NATIVE_STYLISED = 'NATIVE_STYLISED'

class UserNotificationOptionType(Enum):
    ACTIVITY_MESSAGE = 'ACTIVITY_MESSAGE'
    ACTIVITY_REPLY = 'ACTIVITY_REPLY'
    FOLLOWING = 'FOLLOWING'
    ACTIVITY_MENTION = 'ACTIVITY_MENTION'
    THREAD_COMMENT_MENTION = 'THREAD_COMMENT_MENTION'
    THREAD_SUBSCRIBED = 'THREAD_SUBSCRIBED'
    THREAD_COMMENT_REPLY = 'THREAD_COMMENT_REPLY'
    AIRING = 'AIRING'
    ACTIVITY_LIKE = 'ACTIVITY_LIKE'
    ACTIVITY_REPLY_LIKE = 'ACTIVITY_REPLY_LIKE'
    THREAD_LIKE = 'THREAD_LIKE'
    THREAD_COMMENT_LIKE = 'THREAD_COMMENT_LIKE'
    ACTIVITY_REPLY_SUBSCRIBED = 'ACTIVITY_REPLY_SUBSCRIBED'
    RELATED_MEDIA_ADDITION = 'RELATED_MEDIA_ADDITION'