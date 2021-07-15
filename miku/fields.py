
__all__ = (
    'ANIME_FIELDS',
    'CHARACTER_FIELDS',
    'USER_FIELDS'
)

ANIME_FIELDS = (
    'title { romaji english native }',
    'description',
    'averageScore',
    'status',
    'episodes',
    'siteUrl',
    'coverImage { large medium }',
    'bannerImage',
    'tags { name }'
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
    'synonyms'
)

CHARACTER_FIELDS = (
    'name { first middle last full native alternative }',
    'id',
    'image { large medium }',
    'description',
    'gender',
    'dateOfBirth { year month day }',
    'age',
    'siteUrl',
    'favourites',
)

USER_FIELDS = (
    'id',
    'name',
    'about',
    'avatar { medium large }',
    'bannerImage',
    'bans',
    'siteUrl',
    'isFollower',
    'isFollowing',
    'isBlocked',
    'options { titleLanguage displayAdultContent airingNotifications profileColor notificationsOptions { type enabled } }'
)