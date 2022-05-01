import asyncio
from typing import Any, Dict, Optional, Union, Tuple
import aiohttp

from .query import Query, QueryField, QueryFields, QueryOperation
from .fields import *
from .media import Media
from .character import Character
from .paginator import Paginator
from .user import User
from .errors import HTTPException, ERROR_MAPPING

__all__ = (
    'HTTPHandler',
)

class HTTPHandler:
    URL = 'https://graphql.anilist.co'

    def __init__(self, loop: asyncio.AbstractEventLoop, session: Optional[aiohttp.ClientSession] = None) -> None:
        if session:
            ret = 'Expected an aiohttp.ClientSession instance but got {0.__class__.__name__!r} instead'
            raise TypeError(ret.format(session))       

        self.session = session
        self.loop = loop
        self.token: Optional[str] = None
        self.lock = asyncio.Lock()

    async def create_session(self):
        self.session = session = aiohttp.ClientSession(loop=self.loop)
        return session

    async def get_access_token_from_pin(self, pin: str, client_id: str, client_secret: str) -> str:
        json = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': pin,
        }

        if not self.session:
            self.session = await self.create_session()

        async with self.session.post('https://anilist.co/api/v2/oauth/token', json=json) as response:
            data = await response.json()
            return data['access_token']

    async def request(self, query: str, variables: Dict[str, Any]):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token

        session = self.session
        if not session:
            session = await self.create_session()

        payload = {'query': query, 'variables': variables}

        async with self.lock:
            async with session.post(self.URL, json=payload, headers=headers) as response:
                data = await response.json()
                if response.status == 200:
                    return data

                if response.status == 429:
                    retry_after = float(response.headers['Retry-After'])
                    await asyncio.sleep(retry_after)

                    return await self.request(query, variables)

                error = ERROR_MAPPING.get(response.status, HTTPException)
                raise error(response.status, data)

        raise RuntimeError('Unreachable code')

    async def close(self):
        if not self.session:
            return None

        return await self.session.close()

    def parse_args(self, id: Union[int, str]):
        operation_variables = {}
        variables = {}
        arguments = {}

        if isinstance(id, str):
            operation_variables['$search'] = 'String'
            arguments['search'] = '$search'
            variables['search'] = id
        else:
            operation_variables['$id'] = 'Int'
            arguments['id'] = '$id'
            variables['id'] = id

        return operation_variables, variables, arguments

    def build_query(self, fields: Union[Dict[str, Any], Tuple[Any, ...]], obj: Union[QueryFields, QueryField]) -> None:
        if isinstance(fields, dict):
            name = list(fields.keys())[0]
            return self.build_query(fields[name], obj.add_field(name))

        for field in fields:
            if isinstance(field, dict):
                name = list(field.keys())[0]
                self.build_query(field[name], obj.add_field(name))
            else:
                obj.add_field(field)

    async def get_thread_from_user_id(self, user_id: int):
        operation = QueryOperation(
            type="query", 
            variables={"$userId": "Int"}
        )

        fields = QueryFields("Thread", userId='$userId')
        self.build_query(THREAD_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'userId': user_id,
        }

        return await self.request(query, variables)

    async def get_thread(self, id: Union[str, int]):
        operation_variables, variables, arguments = self.parse_args(id)

        operation = QueryOperation(
            type="query",
            variables=operation_variables
        )
        
        fields = QueryFields("Thread", **arguments)
        self.build_query(THREAD_FIELDS, fields)
        
        query = Query(operation=operation, fields=fields)
        query = query.build()

        return await self.request(query, variables)

    async def get_thread_comments(self, id: int):
        operation_variables, variables, arguments = self.parse_args(id)

        operation = QueryOperation(
            type="query",
            variables=operation_variables
        )

        fields = QueryFields("ThreadComment", **arguments)
        self.build_query(THREAD_COMMENT_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        query = query.build()

        return await self.request(query, variables)

    async def get_user(self, search: str):
        operation = QueryOperation(
            type="query", 
            variables={"$search": "String"}
        )

        fields = QueryFields("User", search='$search')
        self.build_query(USER_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'search': search,
        }

        return await self.request(query, variables)

    async def get_media(self, search: str, type: Optional[str] = None):
        operation = QueryOperation(
            type="query", 
            variables={"$search": "String"}
        )

        fields = QueryFields("Media", search='$search')
        if type is not None:
            fields.arguments['type'] = type

        self.build_query(MEDIA_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'search': search,
        }

        return await self.request(query, variables)

    async def get_studio(self, search: str):
        operation = QueryOperation(
            type="query", 
            variables={"$search": "String"}
        )

        fields = QueryFields("Studio", search='$search')
        self.build_query(STUDIO_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
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
        self.build_query(STAFF_FIELDS, fields)

        characters = fields.add_field('characters')
        nodes = characters.add_field('nodes')
        self.build_query(CHARACTER_FIELDS, nodes)

        query = Query(operation=operation, fields=fields)
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
        self.build_query(SITE_STATISTICS_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        query = query.build()

        return await self.request(query, {})

    async def get_character(self, search: str):
        operation = QueryOperation(
            type="query", 
            variables={"$search": "String"}
        )

        fields = QueryFields("Character", search='$search')
        self.build_query(CHARACTER_FIELDS, fields)

        media = fields.add_field('media')
        nodes = media.add_field('nodes')
        self.build_query(MEDIA_FIELDS, nodes)

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'search': search,
        }

        return await self.request(query, variables)

    def get_users(self, search: str, *, per_page: int=5, page: int=0):
        operation = QueryOperation(
            type="query", 
            variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
        )

        fields = QueryFields("Page", page="$page", perPage="$perPage")
        fields.add_field("pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage")

        field = fields.add_field('users', search='$search')
        self.build_query(USER_FIELDS, field)

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'search': search,
            'page': page,
            'perPage': per_page
        }

        return Paginator(self, 'users', query, variables, User)

    def get_medias(self, search: str, type: Optional[str] = None, *, per_page: int = 5, page: int = 0):
        operation = QueryOperation(
            type="query", 
            variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
        )

        fields = QueryFields("Page", page="$page", perPage="$perPage")
        fields.add_field("pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage")

        field = fields.add_field("media", search='$search')
        self.build_query(MEDIA_FIELDS, field)

        if type:
            field.arguments['type'] = type

        characters = field.add_field('characters')
        nodes = characters.add_field('nodes')
        self.build_query(CHARACTER_FIELDS, nodes)

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'search': search,
            'page': page,
            'perPage': per_page
        }

        return Paginator(self, 'media', query, variables, Media)  

    def get_characters(self, search: str, *, per_page: int = 5, page: int = 0):
        operation = QueryOperation(
            type="query", 
            variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
        )

        fields = QueryFields("Page", page="$page", perPage="$perPage")
        fields.add_field("pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage")

        field = fields.add_field("characters", search='$search')
        self.build_query(CHARACTER_FIELDS, field)

        media = field.add_field('media')
        nodes = media.add_field('nodes')
        self.build_query(MEDIA_FIELDS, nodes)

        query = Query(operation=operation, fields=fields)
        query = query.build()

        variables = {
            'search': search,
            'page': page,
            'perPage': per_page
        }

        return Paginator(self, 'characters', query, variables, Character)