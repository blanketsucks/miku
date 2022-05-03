from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Generic

T = TypeVar('T')

if TYPE_CHECKING:
    from .http import HTTPHandler

__all__ = (
    'Chunk',
    'ChunkPaginator'
)

class Chunk(Generic[T]):
    def __init__(self, model: Type[T], http: HTTPHandler, data: List[Dict[str, Any]]) -> None:
        self.model = model
        self.http = http
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> T:
        data = self.next()
        if not data:
            raise StopIteration

        return data

    @property
    def entries(self) -> int:
        return len(self.data)

    def next(self) -> Optional[T]:
        if self.index >= self.entries:
            return None
        
        data = self.data[self.index]
        self.index += 1

        return self.model(data, self.http)
    
    def current(self) -> Optional[T]:
        if self.index >= self.entries:
            return None
        
        data = self.data[self.index]
        return self.model(data, self.http)

    def previous(self) -> Optional[T]:
        if self.index <= 0:
            self.index = 0
        else:
            self.index -= 1

        data = self.data[self.index]
        return self.model(data, self.http)

class ChunkPaginator(Generic[T]):
    def __init__(self, http: HTTPHandler, model: Type[T], type: str, variables: Dict[str, Any], query: str) -> None:
        self.http = http
        self.model = model
        self.variables = variables
        self.type = type
        self.query = query
        self.chunks: Dict[int, Any] = {}
        self.has_next_chunk = True

    def __await__(self):
        return self.collect().__await__()

    def __aiter__(self):
        return self

    async def __anext__(self):
        data = await self.next()
        if not data:
            raise StopAsyncIteration

        return data

    async def current(self) -> Optional[Chunk[T]]:
        data = await self.http.request(self.query, self.type, self.variables)
        if not data:
            return None

        return Chunk(self.model, self.http, data['lists'])

    async def next(self) -> Optional[Chunk[T]]:
        if not self.has_next_chunk:
            return None

        data = await self.http.request(self.query, self.type, self.variables)
        if not data:
            self.has_next_chunk = False
            return None

        self.has_next_chunk = data['hasNextChunk']
        self.variables['chunk'] += 1

        return Chunk(self.model, self.http, data['lists'])

    async def previous(self) -> Optional[Chunk[T]]:
        if not self.variables['chunk']:
            return None

        self.variables['chunk'] -= 1
        data = await self.http.request(self.query, self.type, self.variables)
        if not data:
            return None

        self.has_next_chunk = data['hasNextChunk']
        return Chunk(self.model, self.http, data['lists'])
    
    async def collect(self) -> List[T]:
        return [obj async for chunk in self for obj in chunk]