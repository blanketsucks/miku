import asyncio
from typing import Any, Dict
import aiohttp

from .query import Query, QueryFields, QueryOperation
from .fields import *
from .media import Anime, Manga, Media
from .character import Character
from .paginator import Paginator
from .user import User
from .image import Image
from .errors import AniListServerError, HTTPException, mapping

__all__ = (
    'HTTPHandler',
)

class HTTPHandler:
    URL = 'https://graphql.anilist.co'

    def __init__(self, loop: asyncio.AbstractEventLoop, session: aiohttp.ClientSession=None) -> None:
        if session:
            ret = 'Expected an aiohttp.ClientSession instance but got {0.__class__.__name__!r} instead'
            raise TypeError(ret.format(session))       

        self.session = session
        self.loop = loop
        self.token = None

    async def create_session(self):
        self.session = session = aiohttp.ClientSession(loop=self.loop)
        return session

    async def request(self, query: str, variables: Dict[str, Any]):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token

        url = self.URL

        session = self.session
        if not session:
            session = await self.create_session()

        payload = {
            'query': query,
            'variables': variables
        }

        for retry in range(5):
            async with session.post(url, json=payload, headers=headers) as response:
                try:
                    data = await response.json()
                except aiohttp.ContentTypeError:
                    continue

                if response.status == 429:
                    retry_after = response.headers['Retry-After']
                    await asyncio.sleep(int(retry_after))

                    continue
                
                if data.get('errors'):
                    cls = mapping.get(data['errors'][0]['status'], HTTPException)
                    raise cls(data)

                return data

        raise AniListServerError('Could not fullfil the request because of some internal server error')

    async def close(self):
        if not self.session:
            return None

        return await self.session.close()

    async def get_user(self, search: str):
        operation = QueryOperation(
            type="query", 
            variables={"$search": "String"}
        )

        fields = QueryFields("User", search='$search')

        for field in USER_FIELDS:
            fields.add_field(field)

        media = ' '.join(ANIME_FIELDS)
        characters = ' '.join(CHARACTER_FIELDS) 
        studios = ' '.join(STUDIO_FIELDS)
        staff = ' '.join(STAFF_FIELDS)

        anime = 'anime { nodes {' + media + ' }}'
        manga = 'manga { nodes {' + media + ' }}'
        character = 'characters { nodes {' + characters + ' }}'
        studio = 'studios { nodes {' + studios + ' }}'
        staff = 'staff { nodes {' + staff + ' }}'

        fields.add_field('favourites', ' '.join((anime, manga, character, studio, staff)))

        query = Query(operation, fields)
        query = query.build()

        variables = {
            'search': search,
        }

        return await self.request(query, variables)

    async def get_media(self, search: str, type: str=None):
        operation = QueryOperation(
            type="query", 
            variables={"$search": "String"}
        )

        fields = QueryFields("Media", search='$search')
        if type:
            fields.arguments['type'] = type

        for field in ANIME_FIELDS:
            fields.add_field(field)

        fields.add_field('characters', 'nodes {' + ' '.join(CHARACTER_FIELDS) + ' }')
        fields.add_field('studios', 'nodes {' + ' '.join(STUDIO_FIELDS) + ' }')

        query = Query(operation, fields)
        query = query.build()

        variables = {
            'search': search,
        }

        return await self.request(query, variables)

    async def get_anime(self, search: str):
        return await self.get_media(search, 'ANIME')

    async def get_manga(self, search: str):
        return await self.get_media(search, 'MANGA')

    async def get_studio(self, search: str):
        operation = QueryOperation(
            type="query", 
            variables={"$search": "String"}
        )

        fields = QueryFields("Studio", search='$search')

        for field in STUDIO_FIELDS:
            fields.add_field(field)

        fields.add_field('media', 'nodes {' + ' '.join(ANIME_FIELDS) + ' }')

        query = Query(operation, fields)
        query = query.build()

        variables = {
            'search': search,
        }

        return await self.request(query, variables)

    async def get_staff(self, search: str):
        operation = QueryOperation(
            type="query", 
            variables={"$search": "String"}
        )

        fields = QueryFields("Staff", search='$search')

        for field in STAFF_FIELDS:
            fields.add_field(field)

        fields.add_field('characters', 'nodes {' + ' '.join(CHARACTER_FIELDS) + ' }')

        query = Query(operation, fields)
        query = query.build()

        variables = {
            'search': search,
        }

        return await self.request(query, variables)

    async def get_site_statisics(self):
        operation = QueryOperation(
            type='query',
            variables={}
        )

        fields = QueryFields('SiteStatistics')

        for field in SITE_STATISTICS_FIELDS:
            fields.add_field(field)

        query = Query(operation, fields)
        query = query.build()

        return await self.request(query, {})

    def get_users(self, search: str, *, per_page: int=5, page: int=0):
        operation = QueryOperation(
            type="query", 
            variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
        )

        fields = QueryFields("Page", page="$page", perPage="$perPage")

        fields.add_field("pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage")
        field = fields.add_field('users', *USER_FIELDS, search='$search')
        
        media = ' '.join(ANIME_FIELDS)
        characters = ' '.join(CHARACTER_FIELDS) 
        studios = ' '.join(STUDIO_FIELDS)
        staff = ' '.join(STAFF_FIELDS)

        anime = 'anime { nodes {' + media + ' }}'
        manga = 'manga { nodes {' + media + ' }}'
        character = 'characters { nodes {' + characters + ' }}'
        studio = 'studios { nodes {' + studios + ' }}'
        staff = 'staff { nodes {' + staff + ' }}'

        field.add_field('favourites', ' '.join((anime, manga, character, studio, staff)))

        query = Query(operation, fields)
        query = query.build()

        variables = {
            'search': search,
            'page': page,
            'perPage': per_page
        }

        return Paginator(self, 'users', query, variables, User, Image)

    def get_medias(self, search: str, type: str=None, *, per_page: int=5, page: int=0):
        operation = QueryOperation(
            type="query", 
            variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
        )

        fields = QueryFields("Page", page="$page", perPage="$perPage")
        fields.add_field("pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage")

        field = fields.add_field("media", *ANIME_FIELDS, search='$search')

        if type:
            field.arguments['type'] = type

        field.add_field('characters', 'nodes {' + ' '.join(CHARACTER_FIELDS) + ' }')

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'search': search,
            'page': page,
            'perPage': per_page
        }

        cls = Media

        if type == 'ANIME':
            cls = Anime
        else:
            cls = Manga

        return Paginator(self, 'media', query, variables, cls, Image)  

    def get_animes(self, search: str, *, per_page: int=5, page: int=0):
        return self.get_medias(search, 'ANIME', per_page=per_page, page=page)

    def get_mangas(self, search: str, *, per_page: int=5, page: int=0):
        return self.get_medias(search, 'MANGA', per_page=per_page, page=page)

    def get_characters(self, search: str, *, per_page: int=5, page: int=0):
        operation = QueryOperation(
            type="query", 
            variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
        )

        fields = QueryFields("Page", page="$page", perPage="$perPage")

        fields.add_field("pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage")
        field = fields.add_field("characters", *CHARACTER_FIELDS, search='$search')

        field.add_field('media', 'nodes {' + ' '.join(ANIME_FIELDS) + ' }')

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'search': search,
            'page': page,
            'perPage': per_page
        }

        return Paginator(self, 'characters', query, variables, Character, Image)

    async def get_character(self, search: str):
        operation = QueryOperation(
            type="query", 
            variables={"$search": "String"}
        )

        fields = QueryFields("Character", search='$search')

        for field in CHARACTER_FIELDS:
            fields.add_field(field)

        fields.add_field('media', 'nodes {' + ' '.join(ANIME_FIELDS) + ' }')

        query = Query(operation, fields)
        query = query.build()

        variables = {
            'search': search,
        }

        return await self.request(query, variables)