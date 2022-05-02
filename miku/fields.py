from typing import Tuple, Any

__all__ = (
    'USER_FIELDS',
    'STUDIO_FIELDS',
    'CHARACTER_FIELDS',
    'MEDIA_FIELDS',
    'MEDIA_TREND_FIELDS',
    'STAFF_FIELDS',
    'SITE_STATISTICS_FIELDS',
    'THREAD_FIELDS',
    'THREAD_COMMENT_FIELDS'
)

USER_FIELDS: Tuple[Any, ...] = (
    'id',
    'name',
    'about',
    'bannerImage',
    'bans',
    'siteUrl',
    'isFollower',
    'isFollowing',
    'isBlocked',
    {'avatar': ('large', 'medium')},
    {'options': ('titleLanguage', 'displayAdultContent', 'airingNotifications', 'profileColor', {'notificationOptions': ('type', 'enabled')})},
)

STUDIO_FIELDS: Tuple[str, ...] = (
    'id',
    'name',
    'siteUrl',
    'isAnimationStudio',
    'favourites'
)

CHARACTER_FIELDS: Tuple[Any, ...] = (
    'id',
    'description',
    'gender',
    'age',
    'siteUrl',
    'favourites',
    {'name': ('first', 'middle', 'last', 'full', 'native', 'alternative')},
    {'image': ('large', 'medium')},
    {'dateOfBirth': ('year', 'month', 'day')}
)

MEDIA_FIELDS: Tuple[Any, ...] = (
    'description',
    'averageScore',
    'meanScore',
    'popularity',
    'favourites',
    'status',
    'episodes',
    'siteUrl',
    'bannerImage',
    'id',
    'idMal',
    'type',
    'format',
    'season',
    'duration',
    'chapters',
    'volumes',
    'isLicensed',
    'source',
    'updatedAt',
    'genres',
    'trending',
    'isAdult',
    'synonyms',
    'hashtag',
    {'trailer': ('id', 'site', 'thumbnail')},
    {'title': ('romaji', 'english', 'native')},
    {'coverImage': ('large', 'medium')},
    {'tags': ('name', 'id', 'description', 'category', 'rank', 'isGeneralSpoiler', 'isMediaSpoiler', 'isAdult', 'userId')},
    {'nextAiringEpisode': ('id', 'episode', 'mediaId', 'airingAt', 'timeUntilAiring')},
    {'characters': {'nodes': CHARACTER_FIELDS}},
    {'studios': {'nodes': STUDIO_FIELDS}},
    {'streamingEpisodes': ('thumbnail', 'title', 'site', 'url')},
    {'rankings': ('id', 'rank', 'year', 'format', 'type', 'season', 'allTime', 'context')}
)

MEDIA_TREND_FIELDS = (
    'mediaId',
    'date',
    'trending',
    'popularity',
    'averageScore',
    'inProgress',
    'releasing',
    'episode',
)


STAFF_FIELDS: Tuple[Any, ...] = (
    'id',
    'languageV2',
    'description',
    'primaryOccupations',
    'gender',
    'homeTown',
    'siteUrl',
    'age',
    {'name': ('first', 'middle', 'last', 'full', 'native', 'alternative')},
    {'image': ('large', 'medium')},
    {'dateOfBirth': ('year', 'month', 'day')},
    {'dateOfDeath': ('year', 'month', 'day')}
)

SITE_STATISTICS_FIELDS: Tuple[Any, ...] = (
    {'users': {'nodes': ('date', 'change', 'count')}},
    {'anime': {'nodes': ('date', 'change', 'count')}},
    {'manga': {'nodes': ('date', 'change', 'count')}},
    {'users': {'nodes': ('date', 'change', 'count')}},
    {'characters': {'nodes': ('date', 'change', 'count')}},
    {'staff': {'nodes': ('date', 'change', 'count')}},
    {'studios': {'nodes': ('date', 'change', 'count')}},
    {'reviews': {'nodes': ('date', 'change', 'count')}}
)

THREAD_FIELDS: Tuple[Any, ...] = (
    'id',
    'title',
    'body',
    'userId',
    'replyUserId',
    'replyCommentId',
    'replyCount',
    'viewCount',
    'isLocked',
    'isSticky',
    'isSubscribed',
    'likeCount',
    'isLiked',
    'repliedAt',
    'createdAt',
    'updatedAt',
    'siteUrl',
    {'categories': ('id', 'name')},
    {'user': USER_FIELDS},
    {'replyUser': USER_FIELDS},
    {'likes': USER_FIELDS}
)

THREAD_COMMENT_FIELDS: Tuple[Any, ...] = (
    'id',
    'userId',
    'threadId',
    'comment',
    'likeCount',
    'isLiked',
    'createdAt',
    'updatedAt',
    'siteUrl',
    'childComments',
    {'user': USER_FIELDS},
    {'likes': USER_FIELDS},
    {'thread': THREAD_FIELDS}
)