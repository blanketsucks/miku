from miku.paginator import Paginator
from typing import Any, Dict
import aiohttp

from .query import Query, QueryFields, QueryOperation
from .fields import ANIME_FIELDS, CHARACTER_FIELDS
from .anime import Anime
from .character import Character

class HTTPException(Exception):
    def __init__(self, message: str, status: int) -> None:
        self.status = status
        super().__init__(f'{status}: {message}')

class HTTPHandler:
    URL = 'https://graphql.anilist.co'

    def __init__(self) -> None:
        self.session = None

    async def create_session(self):
        self.session = session = aiohttp.ClientSession()
        return session

    async def request(self, query: str, variables: Dict[str, Any]):
        url = self.URL

        session = self.session
        if not session:
            session = await self.create_session()

        payload = {
            'query': query,
            'variables': variables
        }

        async with session.post(url, json=payload) as response:
            data = await response.json()
            
            if data.get('errors'):
                errors = data.get('errors')
                error = errors[0]

                raise HTTPException(error['message'], error['status'])

            return data

    async def close(self):
        if not self.session:
            return None

        return await self.session.close()

    def get_anime(self, search: str, *, per_page: int=5, page: int=0):
        operation = QueryOperation(
            type="query", 
            variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
        )

        fields = QueryFields("Page", page="$page", perPage="$perPage")
        fields.add_field("pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage")

        fields.add_field("media (search: $search, type: ANIME)", ' '.join(ANIME_FIELDS))

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'search': search,
            'page': page,
            'perPage': per_page
        }

        return Paginator(self, 'media', query, variables, Anime)

    def get_character(self, search: str, *, per_page: int=5, page: int=0):
        operation = QueryOperation(
            type="query", 
            variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
        )

        fields = QueryFields("Page", page="$page", perPage="$perPage")

        fields.add_field("pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage")
        fields.add_field("characters (search: $search)", ' '.join(CHARACTER_FIELDS))

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'search': search,
            'page': page,
            'perPage': per_page
        }

        return Paginator(self, 'characters', query, variables, Character)