
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
    'synonyms',
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
    'options { titleLanguage displayAdultContent airingNotifications profileColor notificationOptions { type enabled } }'
)

STUDIO_FIELDS = (
    'id',
    'name',
    'siteUrl',
    'isAnimationStudio',
    'favourites'
)

STAFF_FIELDS = (
    'id',
    'name { first middle last full native alternative }',
    'languageV2',
    'image { medium large }',
    'description',
    'primaryOccupations',
    'gender',
    'dateOfBirth { year month day }',
    'dateOfDeath { year month day }',
    'homeTown',
    'siteUrl',
    'age',
)

SITE_STATISTICS_FIELDS = (
    'users { nodes { date change count }}',
    'anime { nodes { date change count }}',
    'manga { nodes { date change count }}',
    'characters { nodes { date change count }}',
    'staff { nodes { date change count }}',
    'studios { nodes { date change count }}',
    'reviews { nodes { date change count }}'
)
