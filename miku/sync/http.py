from typing import Any, Dict
import requests
import time

from .paginator import Paginator
from .image import Image

from miku.errors import mapping, HTTPException, AniListServerError
from miku.fields import *
from miku.query import Query, QueryFields, QueryOperation
from miku.media import Media, Manga, Anime
from miku.user import User
from miku.character import Character

class SyncHTTPHandler:
    URL = 'https://graphql.anilist.co'

    def __init__(self, session: requests.Session=None) -> None:
        self.session = session or requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })

        self.token = None

    def close(self):
        self.session.close()

    def get_access_token_from_pin(self, pin: str, client_id: str, client_secret: str) -> str:
        json = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': pin,
        }

        response = self.session.post('https://anilist.co/api/v2/oauth/token', json=json)
        data = response.json()

        return data['access_token']

    def request(self, query: str, variables: Dict[str, Any]):
        if self.token is not None:
            self.session.headers['Authorization'] = 'Bearer ' + self.token

        payload = {
            'query': query,
            'variables': variables,
        }

        for retry in range(5):
            response = self.session.post(self.URL, json=payload)
            data = response.json()

            if response.status_code == 429:
                retry_after = int(response.headers['Retry-After'])
                time.sleep(retry_after)

                continue

            if data.get('errors'):
                cls = mapping.get(data['errors'][0]['status'], HTTPException)
                raise cls(data)

            return data

        raise AniListServerError('Could not fullfil the request because of some internal server error')

    def get_user(self, search: str):
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

        return self.request(query, variables)

    def get_media(self, search: str, type: str=None):
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

        return self.request(query, variables)

    def get_anime(self, search: str):
        return self.get_media(search, 'ANIME')

    def get_manga(self, search: str):
        return self.get_media(search, 'MANGA')

    def get_studio(self, search: str):
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

        return self.request(query, variables)

    def get_staff(self, search: str):
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

        return self.request(query, variables)

    def get_site_statisics(self):
        operation = QueryOperation(
            type='query',
            variables={}
        )

        fields = QueryFields('SiteStatistics')

        for field in SITE_STATISTICS_FIELDS:
            fields.add_field(field)

        query = Query(operation, fields)
        query = query.build()

        return self.request(query, {})

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

    def get_character(self, search: str):
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

        return self.request(query, variables)