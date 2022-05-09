from typing import Any, Dict, Optional, Union, Tuple, List
import asyncio
import aiohttp

from .query import Query, QueryField, QueryFields, QueryOperation
from .fields import *
from .media import Media
from .character import Character
from .paginator import Paginator, ChunkPaginator
from .user import User, MediaListGroup
from .errors import HTTPException, ERROR_MAPPING
from . import types

__all__ = (
    'HTTPHandler',
)

class HTTPHandler:
    URL = 'https://graphql.anilist.co'

    def __init__(
        self, 
        loop: asyncio.AbstractEventLoop, 
        token: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        self.session: aiohttp.ClientSession = session # type: ignore
        self.loop = loop
        self.token = token
        self.lock = asyncio.Lock()

    async def create_session(self) -> aiohttp.ClientSession:
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

    async def request(self, query: Query, rtype: Optional[str] = None, **variables: Any):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token

        session = self.session
        if not session:
            session = await self.create_session()

        payload: Dict[str, Any] = {'query': query.build()}
        if variables:
            payload['variables'] = variables

        async with self.lock:
            async with session.post(self.URL, json=payload, headers=headers) as response:
                data = await response.json()
                if response.status == 200:
                    return data['data'] if type is None else data['data'][rtype]

                if response.status == 429:
                    retry_after = float(response.headers['Retry-After'])
                    await asyncio.sleep(retry_after)

                    return await self.request(query, rtype, **variables)

                error = ERROR_MAPPING.get(response.status, HTTPException)
                raise error(response.status, data)

        raise RuntimeError('Unreachable code')

    async def close(self):
        if not self.session:
            return None

        return await self.session.close()

    def parse_args(self, search: Union[int, str]):
        operation_variables: Dict[str, Any] = {}
        variables: Dict[str, Any] = {}
        arguments: Dict[str, Any] = {}

        if isinstance(search, str):
            operation_variables['$search'] = 'String'
            arguments['search'] = '$search'
            variables['search'] = search
        else:
            operation_variables['$id'] = 'Int'
            arguments['id'] = '$id'
            variables['id'] = search

        return operation_variables, variables, arguments

    def build_query(self, fields: Union[Dict[str, Any], Tuple[Any, ...]], obj: Union[QueryFields, QueryField]) -> None:
        def _build_dict(f: Dict[str, Any]) -> None:
            name = next(iter(f))
            return self.build_query(f[name], obj.add_field(name))

        if isinstance(fields, dict):
            return _build_dict(fields)

        for field in fields:
            if isinstance(field, dict):
                _build_dict(field)
            else:
                obj.add_field(field)

    async def get_all_tags(self) -> List[types.MediaTag]:
        operation = QueryOperation(type='query')

        fields = QueryFields('MediaTagCollection')
        self.build_query(MEDIA_TAG_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'MediaTagCollection')

    async def get_all_genres(self) -> List[str]:
        operation = QueryOperation(type='query')
        fields = QueryFields('GenreCollection')

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'GenreCollection')

    async def get_thread_from_user_id(self, user_id: int) -> types.Thread:
        operation = QueryOperation(type='query', variables={'$userId': 'Int'})

        fields = QueryFields('Thread', userId='$userId')
        self.build_query(THREAD_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'Thread', userId=user_id)

    async def get_thread(self, search: Union[str, int]) -> types.Thread:
        operation_variables, variables, arguments = self.parse_args(search)
        operation = QueryOperation(type='query', variables=operation_variables)
        
        fields = QueryFields('Thread', **arguments)
        self.build_query(THREAD_FIELDS, fields)
        
        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'Thread', **variables)

    async def get_thread_comments(self, id: int) -> List[types.ThreadComment]:
        operation_variables, variables, arguments = self.parse_args(id)
        operation = QueryOperation(type='query', variables=operation_variables)

        fields = QueryFields('ThreadComment', **arguments)
        self.build_query(THREAD_COMMENT_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'ThreadComment', **variables)

    async def get_user(self, search: Union[str, int]) -> types.User:
        operation_variables, variables, arguments = self.parse_args(search)
        operation = QueryOperation(type='query', variables=operation_variables)

        fields = QueryFields('User', **arguments)
        self.build_query(USER_FIELDS, fields)

        favourites = fields.add_field('favourites')
        self.build_query(USER_FAVOURITES_FIELDS, favourites)

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'User', **variables)

    async def get_current_user(self) -> types.User:
        operation = QueryOperation(type='query')

        fields = QueryFields('Viewer')
        self.build_query(USER_FIELDS, fields)

        favourites = fields.add_field('favourites')
        self.build_query(USER_FAVOURITES_FIELDS, favourites)

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'Viewer')

    async def get_media(self, search: Union[str, int], type: Optional[str] = None) -> types.Media:
        operation_variables, variables, arguments = self.parse_args(search)
        operation = QueryOperation(type='query', variables=operation_variables)

        fields = QueryFields('Media', **arguments)
        if type is not None:
            fields.arguments['type'] = type

        self.build_query(MEDIA_FIELDS, fields)
        query = Query(operation=operation, fields=fields)

        return await self.request(query, 'Media', **variables)

    async def get_media_trend(self, media_id: int) -> types.MediaTrend:
        operation = QueryOperation(type='query', variables={'$mediaId': 'Int'})

        fields = QueryFields('MediaTrend', mediaId='$mediaId')
        self.build_query(MEDIA_TREND_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'MediaTrend', mediaId=media_id)

    async def get_studio(self, search: Union[str, int]) -> types.Studio:
        operation_variables, variables, arguments = self.parse_args(search)
        operation = QueryOperation(type='query', variables=operation_variables)

        fields = QueryFields('Studio', **arguments)
        self.build_query(STUDIO_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'Studio', **variables)

    async def get_staff(self, search: Union[str, int]) -> types.Staff:
        operation_variables, variables, arguments = self.parse_args(search)
        operation = QueryOperation(
            type='query', 
            variables=operation_variables
        )

        fields = QueryFields('Staff', **arguments)
        self.build_query(STAFF_FIELDS, fields)

        characters = fields.add_field('characters')
        nodes = characters.add_field('nodes')
        self.build_query(CHARACTER_FIELDS, nodes)

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'Staff', **variables)

    async def get_site_statisics(self) -> types.SiteStatistics:
        operation = QueryOperation(type='query')

        fields = QueryFields('SiteStatistics')
        self.build_query(SITE_STATISTICS_FIELDS, fields)

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'SiteStatistics')

    async def get_character(self, search: Union[str, int]) -> types.Character:
        operation_variables, variables, arguments = self.parse_args(search)
        operation = QueryOperation(type='query', variables=operation_variables)

        fields = QueryFields('Character', **arguments)
        self.build_query(CHARACTER_FIELDS, fields)

        media = fields.add_field('media')
        nodes = media.add_field('nodes')
        self.build_query(MEDIA_FIELDS, nodes)

        query = Query(operation=operation, fields=fields)
        return await self.request(query, 'Character', **variables)

    def get_users(self, search: str, *, per_page: int = 5, page: int = 0):
        operation = QueryOperation(
            type='query', 
            variables={'$page': 'Int', '$perPage': 'Int', '$search': 'String'}
        )

        fields = QueryFields('Page', page='$page', perPage='$perPage')
        fields.add_field('pageInfo', 'total', 'currentPage', 'lastPage', 'hasNextPage', 'perPage')

        field = fields.add_field('users', search='$search')
        self.build_query(USER_FIELDS, field)

        query = Query(operation=operation, fields=fields)
        return Paginator(self, User, 'users', query, search=search, page=page, perPage=per_page)

    def get_medias(self, search: str, type: Optional[str] = None, *, per_page: int = 5, page: int = 0):
        operation = QueryOperation(
            type='query', 
            variables={'$page': 'Int', '$perPage': 'Int', '$search': 'String'}
        )

        fields = QueryFields('Page', page='$page', perPage='$perPage')
        fields.add_field('pageInfo', 'total', 'currentPage', 'lastPage', 'hasNextPage', 'perPage')

        field = fields.add_field('media', search='$search')
        self.build_query(MEDIA_FIELDS, field)

        if type:
            field.arguments['type'] = type

        characters = field.add_field('characters')
        nodes = characters.add_field('nodes')
        self.build_query(CHARACTER_FIELDS, nodes)

        query = Query(operation=operation, fields=fields)
        return Paginator(self, Media, 'media', query, search=search, page=page, perPage=per_page)

    def get_characters(self, search: str, *, per_page: int = 5, page: int = 0):
        operation = QueryOperation(
            type='query', 
            variables={'$page': 'Int', '$perPage': 'Int', '$search': 'String'}
        )

        fields = QueryFields('Page', page='$page', perPage='$perPage')
        fields.add_field('pageInfo', 'total', 'currentPage', 'lastPage', 'hasNextPage', 'perPage')

        field = fields.add_field('characters', search='$search')
        self.build_query(CHARACTER_FIELDS, field)

        media = field.add_field('media')
        nodes = media.add_field('nodes')
        self.build_query(MEDIA_FIELDS, nodes)

        query = Query(operation=operation, fields=fields)
        return Paginator(self, Character, 'characters', query, search=search, page=page, perPage=per_page)

    def get_media_list_collection(
        self, user_id: int, type: str, per_chunk: int = 50, chunk: int = 0
    ) -> ChunkPaginator[MediaListGroup]:
        operation = QueryOperation(
            type='query', 
            variables={'$userId': 'Int', '$type': 'MediaType', '$chunk': 'Int', '$perChunk': 'Int'}
        )

        fields = QueryFields(
            name='MediaListCollection', 
            userId='$userId', 
            type='$type', 
            chunk='$chunk', 
            perChunk='$perChunk'
        )

        self.build_query(MEDIA_LIST_COLLECTION_FIELDS, fields)
        query = Query(operation=operation, fields=fields)

        variables = {
            'userId': user_id,
            'type': type,
            'chunk': chunk,
            'perChunk': per_chunk
        }

        return ChunkPaginator(self, MediaListGroup, 'MediaListCollection', query, **variables)