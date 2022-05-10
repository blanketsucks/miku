from typing import Tuple, Any

__all__ = (
    'USER_FIELDS',
    'USER_FAVOURITES_FIELDS',
    'STUDIO_FIELDS',
    'CHARACTER_FIELDS',
    'MEDIA_FIELDS',
    'MEDIA_TAG_FIELDS',
    'MEDIA_TREND_FIELDS',
    'STAFF_FIELDS',
    'SITE_STATISTICS_FIELDS',
    'THREAD_FIELDS',
    'THREAD_COMMENT_FIELDS',
    'MEDIA_LIST_FIELDS',
    'MEDIA_LIST_GROUP_FIELDS',
    'MEDIA_LIST_COLLECTION_FIELDS'
)

MEDIA_LIST_TYPE_OPTION_FIELDS = (
    'sectionOrder',
    'splitCompletedSectionByFormat',
    'customLists',
    'advancedScoring',
    'advancedScoringEnabled'
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
    'unreadNotificationCount',
    'donatorTier',
    'donatorBadge',
    'moderatorRoles',
    {'avatar': ('large', 'medium')},
    {'options': ('titleLanguage', 'displayAdultContent', 'airingNotifications', 'profileColor', {'notificationOptions': ('type', 'enabled')})},
    {'mediaListOptions': ('scoreFormat', 'rowOrder', {'animeList': MEDIA_LIST_TYPE_OPTION_FIELDS}, {'mangaList': MEDIA_LIST_TYPE_OPTION_FIELDS})},
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

MEDIA_TAG_FIELDS: Tuple[Any, ...] = (
    'name', 'id', 'description', 'category', 'rank', 'isGeneralSpoiler', 'isMediaSpoiler', 'isAdult', 'userId'
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
    {'tags': MEDIA_TAG_FIELDS},
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

USER_FAVOURITES_FIELDS: Tuple[Any, ...] = (
    # Apparently the anime and manga fields just completely break the API so they are not included
    # for now until I figure out how to get them working.
    {'characters': {'nodes': CHARACTER_FIELDS}},
    {'staff': {'nodes': STAFF_FIELDS}},
    {'studios': {'nodes': STUDIO_FIELDS}},
)

MEDIA_LIST_FIELDS: Tuple[Any, ...] = (
    'id',
    'userId',
    'mediaId',
    'status',
    'score',
    'progress',
    'progressVolumes',
    'repeat',
    'notes',
    'private',
    'priority',
    'notes',
    'hiddenFromStatusLists',
    'customLists',
    'advancedScores',
    'updatedAt',
    'createdAt',
    {'startedAt': ('year', 'month', 'day')},
    {'completedAt': ('year', 'month', 'day')},
    {'media': MEDIA_FIELDS},
)

MEDIA_LIST_GROUP_FIELDS: Tuple[Any, ...] = (
    'name',
    'isCustomList',
    'isSplitCompletedList',
    'status',
    {'entries': MEDIA_LIST_FIELDS},
)

MEDIA_LIST_COLLECTION_FIELDS: Tuple[Any, ...] = (
    'hasNextChunk',
    {'lists': MEDIA_LIST_GROUP_FIELDS},
)

