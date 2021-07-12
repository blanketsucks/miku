
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
)

_anime = ' '.join(ANIME_FIELDS)

CHARACTER_FIELDS = (
    'name { first middle last full native }',
    'id',
    'image { large medium }',
    'description',
    'gender',
    'dateOfBirth { year month day }',
    'age',
    'siteUrl',
    'favourites',
    'media () edges { node { {fields} }'
)