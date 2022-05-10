from __future__ import annotations

from typing import (
    Any,
    AsyncIterator,
    Dict, 
    Callable, 
    Generic, 
    Generator,
    List,
    Literal, 
    Optional, 
    TYPE_CHECKING, 
    Type, 
    TypeVar,
    overload, 
)
from abc import ABC, abstractmethod

from .query import Query
from .utils import MaybeAwaitable, maybe_coroutine

if TYPE_CHECKING:
    from .http import HTTPHandler

T = TypeVar('T')
S = TypeVar('S')

__all__ = (
    'AbstractAsyncPaginator',
    'Page',
    'Paginator',
    'ChunkPaginator'
)

class _MappedPaginator(Generic[T, S]):
    def __init__(self, paginator: AbstractAsyncPaginator[T], f: Callable[[T], MaybeAwaitable[S]]) -> None:
        self._paginator = paginator
        self._func = f

    def __await__(self) -> Generator[Any, None, List[S]]:
        return self.collect().__await__()

    async def __aiter__(self) -> AsyncIterator[S]:
        async for page in self._paginator:
            for item in page:
                yield await maybe_coroutine(self._func, item)

    async def collect(self) -> List[S]:
        return [await maybe_coroutine(self._func, item) async for page in self._paginator for item in page]

class _FilteredPaginator(Generic[T]):
    def __init__(self, paginator: AbstractAsyncPaginator[T], f: Callable[[T], MaybeAwaitable[bool]]) -> None:
        self._paginator = paginator
        self._func = f

    def __await__(self) -> Generator[Any, None, List[T]]:
        return self.collect().__await__()

    async def __aiter__(self) -> AsyncIterator[T]:
        async for page in self._paginator:
            for item in page:
                if await maybe_coroutine(self._func, item):
                    yield item

    async def collect(self) -> List[T]:
        return [item async for page in self._paginator for item in page if await maybe_coroutine(self._func, item)]

class AbstractAsyncPaginator(ABC, Generic[T]):
    def __aiter__(self):
        return self

    async def __anext__(self) -> Page[T]:
        page = await self.next()
        if not page:
            raise StopAsyncIteration

        return page

    def __await__(self):
        return self.collect().__await__()

    @abstractmethod
    async def next(self) -> Optional[Page[T]]:
        raise NotImplementedError 
        
    @abstractmethod
    async def current(self) -> Optional[Page[T]]:
        raise NotImplementedError

    @abstractmethod
    async def previous(self) -> Optional[Page[T]]:
        raise NotImplementedError

    @overload
    async def collect(self, *, with_pages: Literal[True]) -> List[Page[T]]:
        ...
    @overload
    async def collect(self, *, with_pages: Literal[False]) -> List[T]:
        ...
    @overload
    async def collect(self) -> List[T]:
        ...
    async def collect(self, *, with_pages: bool = False) -> Any:
        if with_pages:
            return [page async for page in self]

        return [obj async for page in self for obj in page]

    def map(self, func: Callable[[T], MaybeAwaitable[S]]) -> _MappedPaginator[T, S]:
        return _MappedPaginator(self, func)

    def filter(self, predicate: Callable[[T], MaybeAwaitable[bool]]) -> _FilteredPaginator[T]:
        return _FilteredPaginator(self, predicate)

class Page(Generic[T]):
    def __init__(self, http: HTTPHandler, model: Type[T], payload: List[Any]) -> None:
        self.http = http
        self.model = model
        self.payload = payload
        self.index = 0

    def __repr__(self) -> str:
        return f'<Page entries={self.entries}>'

    def __iter__(self):
        return self

    def __next__(self) -> T:
        data = self.next()
        if not data:
            raise StopIteration

        return data

    def __getitem__(self, index: int) -> T:
        data = self.payload[index]
        return self.model(data, self.http)

    @property
    def entries(self) -> int:
        return len(self.payload)

    def next(self) -> Optional[T]:
        if self.index >= self.entries:
            return None

        data = self.payload[self.index]
        self.index += 1

        return self.model(data, self.http)

    def current(self) -> Optional[T]:
        if self.index >= self.entries:
            return None

        data = self.payload[self.index]
        return self.model(data, self.http)

    def previous(self) -> T:
        if self.index <= 0:
            self.index = 0
        else:
            self.index -= 1

        data = self.payload[self.index]
        return self.model(data, self.http)

class Paginator(AbstractAsyncPaginator[T]):
    def __init__(self, http: HTTPHandler, model: Type[T], rtype: str, query: Query, **variables: Any) -> None:
        self.http = http
        self.query = query
        self.rtype = rtype
        self.variables = variables
        self.model = model

        self.has_next_page = True
        self.current_page = 0
        self.next_page = 1

    async def fetch_page(self, page: int) -> Optional[Page[T]]:
        variables = self.variables.copy()
        variables['page'] = page

        data = await self.http.request(self.query, 'Page', **variables)
        if not data:
            return None

        return Page(self.http, self.model, data[self.rtype])

    async def next(self) -> Optional[Page[T]]:
        if not self.has_next_page:
            return None

        self.variables['page'] = self.next_page

        data = await self.http.request(self.query, 'Page', **self.variables)
        if not data:
            return None

        page = data['pageInfo']

        self.has_next_page = page['hasNextPage']
        self.next_page = page['currentPage'] + 1
        self.current_page = page['currentPage']

        return Page(self.http, self.model, data[self.rtype])

    async def current(self) -> Optional[Page[T]]:
        data = await self.http.request(self.query, 'Page', **self.variables)
        if not data:
            return None

        return Page(self.http, self.model, data[self.rtype])

    async def previous(self) -> Optional[Page[T]]:
        if not self.current_page:
            self.current_page = 0
            self.next_page = 1
        else:
            self.next_page = self.current_page
            self.current_page -= 1
        
        self.variables['page'] = self.current_page

        data = await self.http.request(self.query, 'Page', **self.variables)
        if not data:
            return None

        return Page(self.http, self.model, data[self.rtype])

class ChunkPaginator(AbstractAsyncPaginator[T]):
    def __init__(self, http: HTTPHandler, model: Type[T], rtype: str, query: Query, **variables: Any) -> None:
        self.http = http
        self.model = model
        self.variables = variables
        self.rtype = rtype
        self.query = query
        self.chunks: Dict[int, Any] = {}
        self.has_next_chunk = True

    async def fetch_chunk(self, chunk: int) -> Optional[Page[T]]:
        variables = self.variables.copy()
        variables['chunk'] = chunk

        data = await self.http.request(self.query, self.rtype, **variables)
        if not data:
            return None

        return Page(self.http, self.model, data['lists'])

    async def current(self) -> Optional[Page[T]]:
        data = await self.http.request(self.query, self.rtype, **self.variables)
        if not data:
            return None

        return Page(self.http, self.model, data['lists'])

    async def next(self) -> Optional[Page[T]]:
        if not self.has_next_chunk:
            return None

        data = await self.http.request(self.query, self.rtype, **self.variables)
        if not data:
            self.has_next_chunk = False
            return None

        self.has_next_chunk = data['hasNextChunk']
        self.variables['chunk'] += 1

        return Page(self.http, self.model, data['lists'])

    async def previous(self) -> Optional[Page[T]]:
        if not self.variables['chunk']:
            return None

        self.variables['chunk'] -= 1
        data = await self.http.request(self.query, self.rtype, **self.variables)
        if not data:
            return None

        self.has_next_chunk = data['hasNextChunk']
        return Page(self.http, self.model, data['lists'])

